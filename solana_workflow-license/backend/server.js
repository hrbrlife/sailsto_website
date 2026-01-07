const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const { PublicKey } = require('@solana/web3.js');

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

// Путь к проекту
const PROJECT_ROOT = path.join(__dirname, '..');
const TEMPLATE_PROGRAM_PATH = path.join(PROJECT_ROOT, 'programs', 'license-registry');
const PROGRAMS_DIR = path.join(PROJECT_ROOT, 'programs');
const ANCHOR_TOML_PATH = path.join(PROJECT_ROOT, 'Anchor.toml');

// Функция для выполнения команд
function runCommand(command, cwd = PROJECT_ROOT) {
  return new Promise((resolve, reject) => {
    console.log(`[CMD] Running: ${command} in ${cwd}`);
    exec(command, { cwd, maxBuffer: 10 * 1024 * 1024 }, (error, stdout, stderr) => {
      if (error) {
        console.error(`[ERROR] ${stderr}`);
        reject({ error: error.message, stderr });
        return;
      }
      console.log(`[SUCCESS] ${stdout}`);
      resolve(stdout);
    });
  });
}

// Функция для копирования директории рекурсивно
function copyDirectory(src, dest) {
  console.log(`[COPY] ${src} → ${dest}`);
  
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }
  
  const entries = fs.readdirSync(src, { withFileTypes: true });
  
  for (let entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    
    if (entry.isDirectory()) {
      copyDirectory(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// Функция для генерации уникального имени программы
function generateProgramName(masterNftMint) {
  // Используем первые 8 символов mint адреса для уникальности
  const shortMint = masterNftMint.substring(0, 8).toLowerCase();
  return `license_registry_${shortMint}`;
}

// Функция для обновления MASTER_NFT_MINT в lib.rs
function updateMasterNftMint(libRsPath, masterNftMint) {
  console.log(`[UPDATE] Updating MASTER_NFT_MINT to: ${masterNftMint}`);
  
  let content = fs.readFileSync(libRsPath, 'utf8');
  
  // Заменяем MASTER_NFT_MINT
  const regex = /pub const MASTER_NFT_MINT: Pubkey = pubkey!\("([^"]+)"\);/;
  content = content.replace(regex, `pub const MASTER_NFT_MINT: Pubkey = pubkey!("${masterNftMint}");`);
  
  fs.writeFileSync(libRsPath, content, 'utf8');
  console.log('[UPDATE] MASTER_NFT_MINT updated successfully');
}

// Функция для обновления declare_id! в lib.rs
function updateDeclareId(libRsPath, programId) {
  console.log(`[UPDATE] Updating declare_id! to: ${programId}`);
  
  let content = fs.readFileSync(libRsPath, 'utf8');
  
  // Заменяем declare_id!
  const regex = /declare_id!\("([^"]+)"\);/;
  content = content.replace(regex, `declare_id!("${programId}");`);
  
  fs.writeFileSync(libRsPath, content, 'utf8');
  console.log('[UPDATE] declare_id! updated successfully');
}

// Функция для обновления Cargo.toml с новым именем пакета
function updateCargoToml(cargoTomlPath, newPackageName) {
  console.log(`[UPDATE] Updating Cargo.toml package name to: ${newPackageName}`);
  
  let content = fs.readFileSync(cargoTomlPath, 'utf8');
  
  // Заменяем имя пакета
  const regex = /name = "license-registry"/;
  content = content.replace(regex, `name = "${newPackageName}"`);
  
  fs.writeFileSync(cargoTomlPath, content, 'utf8');
  console.log('[UPDATE] Cargo.toml updated successfully');
}

// Функция для добавления нового member в Anchor.toml
function addMemberToAnchorToml(programName) {
  console.log(`[UPDATE] Adding ${programName} to Anchor.toml members...`);
  
  let content = fs.readFileSync(ANCHOR_TOML_PATH, 'utf8');
  
  // Проверяем, есть ли уже этот member
  if (content.includes(`programs/${programName}`)) {
    console.log('[INFO] Member already exists in Anchor.toml');
    return;
  }
  
  // Добавляем в [programs.devnet] если ещё нет
  if (!content.includes(`[programs.devnet]`)) {
    content += `\n[programs.devnet]\n`;
  }
  
  // Находим секцию [programs.devnet] и добавляем программу
  // Пока просто добавим в конец файла для простоты
  content += `\n# Auto-generated program for Master NFT\n`;
  content += `# ${programName} = "deploy"\n`;
  
  fs.writeFileSync(ANCHOR_TOML_PATH, content, 'utf8');
  console.log('[UPDATE] Anchor.toml updated successfully');
}

// Функция для получения публичного ключа из keypair файла
function getPublicKeyFromKeypair(keypairPath) {
  const keypairData = JSON.parse(fs.readFileSync(keypairPath, 'utf8'));
  const secretKey = Uint8Array.from(keypairData);
  const { Keypair } = require('@solana/web3.js');
  const keypair = Keypair.fromSecretKey(secretKey);
  return keypair.publicKey.toBase58();
}

// Главный endpoint для деплоя
app.post('/api/deploy', async (req, res) => {
  const { masterNftMint } = req.body;
  
  console.log('\n========================================');
  console.log('🚀 STARTING AUTOMATIC DEPLOYMENT');
  console.log('========================================\n');
  
  if (!masterNftMint) {
    return res.status(400).json({ error: 'Master NFT mint address is required' });
  }
  
  // Валидация адреса
  try {
    new PublicKey(masterNftMint);
  } catch (err) {
    return res.status(400).json({ error: 'Invalid Master NFT mint address' });
  }
  
  const programName = generateProgramName(masterNftMint);
  const programDir = path.join(PROGRAMS_DIR, programName);
  const libRsPath = path.join(programDir, 'src', 'lib.rs');
  const cargoTomlPath = path.join(programDir, 'Cargo.toml');
  const keypairPath = path.join(PROJECT_ROOT, 'target', 'deploy', `${programName}-keypair.json`);
  
  try {
    // Шаг 1: Создать новую программу (копировать template)
    console.log('\n[STEP 1/9] Creating new program from template...');
    console.log(`[INFO] Program name: ${programName}`);
    console.log(`[INFO] Program directory: ${programDir}`);
    
    if (fs.existsSync(programDir)) {
      console.log('[WARN] Program directory already exists, removing...');
      fs.rmSync(programDir, { recursive: true, force: true });
    }
    
    copyDirectory(TEMPLATE_PROGRAM_PATH, programDir);
    console.log('[SUCCESS] Program created from template');
    
    // Шаг 2: Обновить MASTER_NFT_MINT в lib.rs
    console.log('\n[STEP 2/9] Updating MASTER_NFT_MINT in lib.rs...');
    updateMasterNftMint(libRsPath, masterNftMint);
    
    // Шаг 3: Обновить Cargo.toml с новым именем пакета
    console.log('\n[STEP 3/9] Updating Cargo.toml...');
    updateCargoToml(cargoTomlPath, programName);
    
    // Шаг 4: Создать новый keypair для программы
    console.log('\n[STEP 4/9] Creating new program keypair...');
    
    const deployDir = path.dirname(keypairPath);
    if (!fs.existsSync(deployDir)) {
      fs.mkdirSync(deployDir, { recursive: true });
    }
    
    await runCommand(`solana-keygen new -o "${keypairPath}" --no-bip39-passphrase --force --silent`);
    
    // Шаг 5: Получить новый Program ID
    console.log('\n[STEP 5/9] Getting new Program ID...');
    const newProgramId = getPublicKeyFromKeypair(keypairPath);
    console.log(`[INFO] New Program ID: ${newProgramId}`);
    
    // Шаг 6: Обновить declare_id! с новым Program ID
    console.log('\n[STEP 6/9] Updating declare_id! in lib.rs...');
    updateDeclareId(libRsPath, newProgramId);
    
    // Шаг 7: Добавить в Anchor.toml
    console.log('\n[STEP 7/9] Updating Anchor.toml...');
    addMemberToAnchorToml(programName);
    
    // Шаг 8: Собрать программу (anchor build для конкретной программы)
    console.log('\n[STEP 8/9] Building program with Anchor...');
    console.log(`[CMD] anchor build --program-name ${programName}`);
    await runCommand(`anchor build --program-name ${programName}`);
    
    // Шаг 9: Задеплоить программу
    console.log('\n[STEP 9/9] Deploying program to Solana devnet...');
    const deployOutput = await runCommand(`anchor deploy --program-name ${programName} --program-keypair "${keypairPath}"`);
    
    console.log('\n========================================');
    console.log('✅ DEPLOYMENT SUCCESSFUL!');
    console.log('========================================\n');
    console.log(`📦 Program Name: ${programName}`);
    console.log(`🆔 Program ID: ${newProgramId}`);
    console.log(`🎯 Master NFT: ${masterNftMint}`);
    console.log(`📂 Location: programs/${programName}/`);
    
    res.json({
      success: true,
      programId: newProgramId,
      programName: programName,
      masterNftMint: masterNftMint,
      programPath: `programs/${programName}/`,
      message: 'Contract deployed successfully!',
      deployOutput: deployOutput
    });
    
  } catch (error) {
    console.error('\n========================================');
    console.error('❌ DEPLOYMENT FAILED!');
    console.error('========================================\n');
    console.error(error);
    
    res.status(500).json({
      success: false,
      error: error.error || error.message,
      stderr: error.stderr
    });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'Deployment server is running' });
});

// Endpoint для получения списка задеплоенных программ
app.get('/api/programs', (req, res) => {
  try {
    const programs = [];
    const programsDir = fs.readdirSync(PROGRAMS_DIR, { withFileTypes: true });
    
    for (let entry of programsDir) {
      if (entry.isDirectory() && entry.name.startsWith('license_registry_')) {
        const programPath = path.join(PROGRAMS_DIR, entry.name);
        const libRsPath = path.join(programPath, 'src', 'lib.rs');
        
        if (fs.existsSync(libRsPath)) {
          const content = fs.readFileSync(libRsPath, 'utf8');
          
          // Извлекаем MASTER_NFT_MINT
          const masterMatch = content.match(/pub const MASTER_NFT_MINT: Pubkey = pubkey!\("([^"]+)"\);/);
          const declareMatch = content.match(/declare_id!\("([^"]+)"\);/);
          
          programs.push({
            name: entry.name,
            path: `programs/${entry.name}/`,
            masterNftMint: masterMatch ? masterMatch[1] : 'unknown',
            programId: declareMatch ? declareMatch[1] : 'unknown'
          });
        }
      }
    }
    
    res.json({ programs });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Проверка наличия необходимых инструментов при старте
async function checkRequirements() {
  console.log('\n🔍 Checking requirements...\n');
  
  try {
    const solanaVersion = await runCommand('solana --version');
    console.log(`✅ Solana CLI: ${solanaVersion.trim()}`);
  } catch (err) {
    console.error('❌ Solana CLI not found! Install: https://docs.solana.com/cli/install-solana-cli-tools');
  }
  
  try {
    const anchorVersion = await runCommand('anchor --version');
    console.log(`✅ Anchor CLI: ${anchorVersion.trim()}`);
  } catch (err) {
    console.error('❌ Anchor CLI not found! Install: cargo install --git https://github.com/coral-xyz/anchor avm');
  }
  
  try {
    const balance = await runCommand('solana balance');
    console.log(`✅ Wallet balance: ${balance.trim()}`);
    
    const balanceValue = parseFloat(balance);
    if (balanceValue < 2) {
      console.warn('⚠️  Low balance! You need at least 2 SOL for deployment. Run: solana airdrop 2');
    }
  } catch (err) {
    console.error('❌ Cannot check wallet balance');
  }
  
  console.log('');
}

app.listen(PORT, () => {
  console.log(`\n🚀 Deployment Server running on http://localhost:${PORT}`);
  console.log(`📡 API Endpoint: http://localhost:${PORT}/api/deploy\n`);
  checkRequirements();
});

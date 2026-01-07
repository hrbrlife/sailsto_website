# 🚀 Автоматический деплой контракта

Этот проект автоматически деплоит отдельный контракт для каждого Master NFT при клике на кнопку "Initialize Registry".

## 📋 Предварительные требования

### 1. Установите Solana CLI
```powershell
# Windows: используйте WSL или скачайте installer
# https://docs.solana.com/cli/install-solana-cli-tools
```

### 2. Установите Anchor CLI
```powershell
cargo install --git https://github.com/coral-xyz/anchor avm --locked --force
avm install latest
avm use latest
```

### 3. Настройте Solana кошелёк
```powershell
# Переключитесь на devnet
solana config set --url https://api.devnet.solana.com

# Создайте кошелёк (если ещё нет)
solana-keygen new

# Пополните баланс (нужно минимум 2 SOL для деплоя)
solana airdrop 2
solana balance
```

## 🚀 Быстрый старт

### Шаг 1: Установите зависимости

#### Backend:
```powershell
cd backend
npm install
```

#### Frontend:
```powershell
cd frontend-vite
npm install  # или yarn install
```

### Шаг 2: Запустите серверы

#### Терминал 1 - Backend API:
```powershell
cd backend
npm start
```

**Должны увидеть:**
```
🚀 Deployment Server running on http://localhost:3001
📡 API Endpoint: http://localhost:3001/api/deploy

🔍 Checking requirements...

✅ Solana CLI: solana-cli 1.x.x
✅ Anchor CLI: anchor-cli 0.30.x
✅ Wallet balance: 2.5 SOL
```

#### Терминал 2 - Frontend:
```powershell
cd frontend-vite
npm run dev  # или yarn dev
```

**Должны увидеть:**
```
VITE v7.3.0  ready in X ms

➜  Local:   http://localhost:5174/
```

### Шаг 3: Используйте интерфейс

1. Откройте http://localhost:5174
2. Подключите кошелёк (Phantom/Solflare)
3. Нажмите **"Create Master NFT"**
   - Дождитесь создания NFT
   - Адрес mint будет показан в консоли
4. Нажмите **"Initialize Registry"**
   - 🚀 Backend автоматически:
     - Обновит `MASTER_NFT_MINT` в контракте
     - Создаст новый Program keypair
     - Обновит `declare_id!`
     - Соберёт программу (`anchor build`)
     - Задеплоит на devnet (`anchor deploy`)
     - Вернёт новый Program ID
   - ✅ Frontend инициализирует реестр с новым Program ID
5. **Готово!** Контракт задеплоен и работает только с вашим Master NFT

### Шаг 4: Создайте и активируйте лицензии

1. Нажмите **"Create License NFT"** - создаст Print Edition
2. Нажмите **"Activate License"** - активирует лицензию
3. Нажмите **"Check Status"** - проверит статус
4. Нажмите **"Revoke License"** - отзовёт лицензию

## 🏗️ Архитектура

```
User clicks "Initialize Registry"
         ↓
Frontend sends Master NFT mint to Backend API
         ↓
Backend:
  1. Creates NEW program directory: programs/license_registry_<mint_prefix>/
  2. Copies template from programs/license-registry/
  3. Updates MASTER_NFT_MINT in new lib.rs
  4. Updates Cargo.toml with new package name
  5. Creates new program keypair
  6. Gets new Program ID
  7. Updates declare_id! in new lib.rs
  8. Updates Anchor.toml
  9. Runs: anchor build --program-name license_registry_<mint_prefix>
  10. Runs: anchor deploy --program-name license_registry_<mint_prefix>
  11. Returns new Program ID
         ↓
Frontend:
  1. Receives new Program ID
  2. Initializes registry with new Program ID
  3. Ready to create licenses!
```

**Ключевая особенность**: 
- ✅ Каждый Master NFT → НОВАЯ ПРОГРАММА (папка programs/license_registry_xxxxxxxx/)
- ✅ Каждая программа → УНИКАЛЬНЫЙ Program ID
- ✅ Полная изоляция между разными Master NFT
- ✅ Template остаётся нетронутым (programs/license-registry/)

### Структура после нескольких деплоев:

```
programs/
├── license-registry/              ← TEMPLATE (не трогается)
│   ├── src/lib.rs
│   └── Cargo.toml
├── license_registry_ckfatspm/     ← Auto-created для Master NFT #1
│   ├── src/lib.rs                 ← MASTER_NFT_MINT = CKfatsPMUf8...
│   └── Cargo.toml
├── license_registry_8hk9pqr2/     ← Auto-created для Master NFT #2
│   ├── src/lib.rs                 ← MASTER_NFT_MINT = 8hK9PqR2xW3...
│   └── Cargo.toml
└── license_registry_5nm7tjw4/     ← Auto-created для Master NFT #3
    ├── src/lib.rs                 ← MASTER_NFT_MINT = 5Nm7TjW4yU1...
    └── Cargo.toml
```

## 📁 Структура проекта

```
sol_project/
├── backend/
│   ├── server.js          ← Express API для автоматического деплоя
│   └── package.json
├── frontend-vite/
│   └── src/
│       └── Master.jsx     ← Обновлённый с вызовом API
├── programs/
│   ├── license-registry/              ← TEMPLATE (не изменяется)
│   │   ├── src/lib.rs                 ← Базовый шаблон
│   │   └── Cargo.toml
│   ├── license_registry_ckfatspm/     ← Auto-generated для Master NFT #1
│   ├── license_registry_8hk9pqr2/     ← Auto-generated для Master NFT #2
│   └── ...                            ← Будет создаваться для каждого Master NFT
└── target/
    └── deploy/
        ├── license_registry_ckfatspm-keypair.json  ← Уникальный keypair
        ├── license_registry_8hk9pqr2-keypair.json
        └── ...
```

## 🔍 Логи и отладка

### Backend логи (Terminal 1):
```
========================================
🚀 STARTING AUTOMATIC DEPLOYMENT
========================================

[STEP 1/9] Creating new program from template...
[INFO] Program name: license_registry_ckfatspm
[INFO] Program directory: D:\sol_project\programs\license_registry_ckfatspm
[COPY] Copying template...
[SUCCESS] Program created from template

[STEP 2/9] Updating MASTER_NFT_MINT in lib.rs...
[UPDATE] MASTER_NFT_MINT updated successfully

[STEP 3/9] Updating Cargo.toml...
[UPDATE] Cargo.toml updated successfully

[STEP 4/9] Creating new program keypair...
[CMD] Running: solana-keygen new -o ...

[STEP 5/9] Getting new Program ID...
[INFO] New Program ID: 8szGkwr3kAQL1fVHCUPXp7jJQvNjMw3h4NZRqKqjqvTQ

[STEP 6/9] Updating declare_id! in lib.rs...
[UPDATE] declare_id! updated successfully

[STEP 7/9] Updating Anchor.toml...
[UPDATE] Anchor.toml updated successfully

[STEP 8/9] Building program with Anchor...
[CMD] Running: anchor build --program-name license_registry_ckfatspm

[STEP 9/9] Deploying program to Solana devnet...
[CMD] Running: anchor deploy --program-name license_registry_ckfatspm

========================================
✅ DEPLOYMENT SUCCESSFUL!
========================================

📦 Program Name: license_registry_ckfatspm
🆔 Program ID: 8szGkwr3kAQL1fVHCUPXp7jJQvNjMw3h4NZRqKqjqvTQ
🎯 Master NFT: CKfatsPMUf8SkiURsDXs7eK6GWb4Jsd6UDbs7twMCWxo
📂 Location: programs/license_registry_ckfatspm/
```

### Frontend логи (Browser Console):
```
🚀 Calling deployment API...
✅ Deployment successful! {programId: "8szGkw...", ...}
🔧 Initializing Registry with new Program ID...
📋 Registry PDA: BxK9h2...
✅ Registry initialized with auto-deployed contract
```

## 🐛 Troubleshooting

### ❌ "Anchor CLI not found"
```powershell
cargo install --git https://github.com/coral-xyz/anchor avm --locked --force
avm install latest
avm use latest
```

### ❌ "Insufficient funds"
```powershell
solana airdrop 2
solana balance
```

### ❌ "Failed to fetch" в браузере
Проверьте, что backend запущен:
```powershell
curl http://localhost:3001/api/health
```

Должен вернуть: `{"status":"ok","message":"Deployment server is running"}`

### ❌ Backend падает при `anchor build`
Проверьте, что Anchor установлен:
```powershell
anchor --version
```

### ❌ "Low balance! You need at least 2 SOL"
```powershell
solana airdrop 2
# Если не работает (devnet иногда нестабилен):
solana airdrop 1
solana airdrop 1
```

## 📊 Проверка деплоя

### 1. Проверьте Program ID в Solana Explorer:
```
https://explorer.solana.com/address/<Program_ID>?cluster=devnet
```

### 2. Проверьте программу через CLI:
```powershell
solana program show <Program_ID> --url devnet
```

### 3. Проверьте логи транзакции:
```powershell
solana confirm <signature> -v --url devnet
```

## 🎯 Для production (mainnet)

1. Обновите `Anchor.toml`:
```toml
[provider]
cluster = "Mainnet"
```

2. Переключите Solana CLI:
```powershell
solana config set --url https://api.mainnet-beta.solana.com
```

3. **ВАЖНО**: Убедитесь, что кошелёк пополнен (деплой на mainnet стоит ~3-5 SOL)

4. Обновите frontend RPC:
```javascript
const connection = new Connection(clusterApiUrl('mainnet-beta'), 'confirmed')
```

## 🔐 Безопасность

1. **Храните keypair-ы в безопасности**: `target/deploy/license_registry-keypair.json`
2. **Не коммитьте в git**: Уже добавлено в `.gitignore`
3. **Для production**: Используйте environment variables для sensitive данных
4. **Rate limiting**: В production добавьте rate limiting на backend API

## 💡 Дополнительные возможности

### Просмотр всех задеплоенных программ
```powershell
curl http://localhost:3001/api/programs
```

**Вернёт:**
```json
{
  "programs": [
    {
      "name": "license_registry_ckfatspm",
      "path": "programs/license_registry_ckfatspm/",
      "masterNftMint": "CKfatsPMUf8SkiURsDXs7eK6GWb4Jsd6UDbs7twMCWxo",
      "programId": "8szGkwr3kAQL1fVHCUPXp7jJQvNjMw3h4NZRqKqjqvTQ"
    },
    {
      "name": "license_registry_8hk9pqr2",
      "path": "programs/license_registry_8hk9pqr2/",
      "masterNftMint": "8hK9PqR2xW3yU1vD5Ks7MqTfNjC4RzHgBwA6EpYxLdVn",
      "programId": "5Nm7TjW4yU1vF2xC8Lp3HqKrMsN9BgDwEcY5TzXqRaUj"
    }
  ]
}
```

### Деплой нескольких контрактов
Просто создайте несколько Master NFT и для каждого нажмите "Initialize Registry":
- Master NFT #1 → программа `license_registry_ckfatspm/` → Program ID: `8szGk...`
- Master NFT #2 → программа `license_registry_8hk9pqr2/` → Program ID: `5Nm7T...`
- Master NFT #3 → программа `license_registry_5nm7tjw4/` → Program ID: `3Kp9R...`

### Удаление неиспользуемых программ
```powershell
# Удалить программу
rm -r programs/license_registry_xxxxxxxx/

# Закрыть on-chain программу (вернёт SOL):
solana program close <Program_ID>
```

### Апгрейд существующего контракта
```powershell
anchor upgrade target/deploy/license_registry.so --program-id <Program_ID>
```

### Закрытие программы (возврат SOL)
```powershell
solana program close <Program_ID>
```

## 📝 API Documentation

### POST `/api/deploy`

**Request:**
```json
{
  "masterNftMint": "CKfatsPMUf8SkiURsDXs7eK6GWb4Jsd6UDbs7twMCWxo"
}
```

**Response (Success):**
```json
{
  "success": true,
  "programId": "8szGkwr3kAQL1fVHCUPXp7jJQvNjMw3h4NZRqKqjqvTQ",
  "programName": "license_registry_ckfatspm",
  "masterNftMint": "CKfatsPMUf8SkiURsDXs7eK6GWb4Jsd6UDbs7twMCWxo",
  "programPath": "programs/license_registry_ckfatspm/",
  "message": "Contract deployed successfully!",
  "deployOutput": "..."
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Error message",
  "stderr": "Detailed error output"
}
```

### GET `/api/programs`

**Response:**
```json
{
  "programs": [
    {
      "name": "license_registry_ckfatspm",
      "path": "programs/license_registry_ckfatspm/",
      "masterNftMint": "CKfatsPMUf8SkiURsDXs7eK6GWb4Jsd6UDbs7twMCWxo",
      "programId": "8szGkwr3kAQL1fVHCUPXp7jJQvNjMw3h4NZRqKqjqvTQ"
    }
  ]
}
```

## 🤝 Contributing

Pull requests are welcome! Для крупных изменений сначала откройте issue.

## 📄 License

MIT

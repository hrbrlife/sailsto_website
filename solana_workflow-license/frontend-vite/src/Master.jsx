import { useState } from 'react'
import { useWallet, useConnection } from '@solana/wallet-adapter-react'
import { walletAdapterIdentity } from '@metaplex-foundation/umi-signer-wallet-adapters'
import { createUmi } from '@metaplex-foundation/umi-bundle-defaults'
import {
  createV1,
  TokenStandard,
  mintV1,
  mplTokenMetadata,
  fetchDigitalAsset,
} from '@metaplex-foundation/mpl-token-metadata'
import {
  generateSigner,
  percentAmount,
} from '@metaplex-foundation/umi'
import { PublicKey, SystemProgram } from '@solana/web3.js'
import { 
  TOKEN_PROGRAM_ID,
  getAssociatedTokenAddressSync,
} from '@solana/spl-token'
import { fromWeb3JsPublicKey } from '@metaplex-foundation/umi-web3js-adapters'
import * as anchor from '@coral-xyz/anchor'

// ============================================================================
// Program IDs - License Registry Contract
// ============================================================================
// Временный Program ID - замените после деплоя программы!
const LICENSE_REGISTRY_PROGRAM_ID = new PublicKey('11111111111111111111111111111111')
const METADATA_PROGRAM_ID = new PublicKey('metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s')


export default function Master({ onBack }) {
  const { connection } = useConnection()
  const wallet = useWallet()
  
  const [masterMint, setMasterMint] = useState('')
  const [licenseMint, setLicenseMint] = useState('')
  const [status, setStatus] = useState('')
  const [registryInitialized, setRegistryInitialized] = useState(false)

  // ============================================================================
  // 1️⃣ Создание Master NFT
  // ============================================================================
  const createMasterNFT = async () => {
    if (!wallet.publicKey) {
      setStatus('❌ Подключите кошелёк!')
      return
    }

    try {
      setStatus('⏳ Создаём Master NFT...')
      console.log('🔧 Starting Master NFT creation...')

      const umi = createUmi(connection.rpcEndpoint)
        .use(mplTokenMetadata())
        .use(walletAdapterIdentity(wallet))

      const masterMintSigner = generateSigner(umi)
      console.log('🔑 Master Mint:', masterMintSigner.publicKey)

      const tx = await createV1(umi, {
        mint: masterMintSigner,
        authority: umi.identity,
        name: 'Master License Authority',
        uri: 'https://arweave.net/master.json',
        sellerFeeBasisPoints: percentAmount(5),
        tokenStandard: TokenStandard.NonFungible,
      }).sendAndConfirm(umi, {
        send: { skipPreflight: false },
        confirm: { commitment: 'confirmed' }
      })

      const masterMintPubkey = masterMintSigner.publicKey.toString()
      setMasterMint(masterMintPubkey)
      
      setStatus(`✅ Master NFT создан!\n\nMint: ${masterMintPubkey}\nSignature: ${tx.signature}\n\n⚠️ Теперь нажмите "Initialize Registry"!`)
      console.log('✅ Master NFT created:', masterMintPubkey)

    } catch (error) {
      console.error('❌ Error:', error)
      let errorMsg = error.message || 'Unknown error'
      
      // Детальная информация об ошибке
      if (error.logs) {
        console.error('📜 Transaction logs:', error.logs)
        errorMsg += `\n\nLogs: ${error.logs.join('\n')}`
      }
      
      if (errorMsg.includes('Blockhash not found')) {
        errorMsg = 'RPC Error: Blockhash not found. Попробуйте снова через несколько секунд.'
      }
      
      setStatus(`❌ Ошибка: ${errorMsg}`)
    }
  }

  // ============================================================================
  // 2️⃣ Инициализация реестра (с автоматическим деплоем контракта!)
  // ============================================================================
  const initRegistry = async () => {
    if (!wallet.publicKey || !masterMint) {
      setStatus('❌ Сначала создайте Master NFT!')
      return
    }

    try {
      // ШАГ 1: Автоматический деплой контракта через backend API
      setStatus('🚀 Шаг 1/2: Деплоим контракт для этого Master NFT...\n(это займёт ~30-60 секунд)')
      console.log('🚀 Calling deployment API...')

      const deployResponse = await fetch('http://localhost:3001/api/deploy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ masterNftMint: masterMint })
      })

      if (!deployResponse.ok) {
        const errorData = await deployResponse.json()
        throw new Error(`Deployment failed: ${errorData.error || 'Unknown error'}`)
      }

      const deployData = await deployResponse.json()
      console.log('✅ Deployment successful!', deployData)

      const newProgramId = new PublicKey(deployData.programId)
      
      setStatus(`✅ Контракт задеплоен!\nProgram ID: ${deployData.programId}\n\n⏳ Шаг 2/2: Инициализируем реестр...`)

      // ШАГ 2: Инициализация реестра с НОВЫМ Program ID
      console.log('🔧 Initializing Registry with new Program ID...')

      const masterMintPubkey = new PublicKey(masterMint)

      const [registryPda] = PublicKey.findProgramAddressSync(
        [Buffer.from('registry'), masterMintPubkey.toBuffer()],
        newProgramId
      )

      const masterAta = getAssociatedTokenAddressSync(
        masterMintPubkey,
        wallet.publicKey,
        false,
        TOKEN_PROGRAM_ID
      )

      const [masterMetadataPda] = PublicKey.findProgramAddressSync(
        [
          Buffer.from('metadata'),
          METADATA_PROGRAM_ID.toBuffer(),
          masterMintPubkey.toBuffer(),
        ],
        METADATA_PROGRAM_ID
      )

      console.log('📋 Registry PDA:', registryPda.toBase58())

      const provider = new anchor.AnchorProvider(
        connection, 
        wallet, 
        { commitment: 'confirmed' }
      )
      
      const idl = await anchor.Program.fetchIdl(newProgramId, provider)
      if (!idl) {
        throw new Error('❌ Cannot fetch IDL from deployed program')
      }

      const program = new anchor.Program(idl, provider)

      const tx = await program.methods
        .initRegistry()
        .accounts({
          registry: registryPda,
          authority: wallet.publicKey,
          masterNftMint: masterMintPubkey,
          masterNftAta: masterAta,
          masterMetadata: masterMetadataPda,
          systemProgram: SystemProgram.programId,
          tokenProgram: TOKEN_PROGRAM_ID,
        })
        .rpc()

      setRegistryInitialized(true)
      setStatus(`✅✅ ГОТОВО!\n\n🎉 Контракт задеплоен!\nProgram ID: ${deployData.programId}\n\n✅ Реестр инициализирован!\nRegistry PDA: ${registryPda.toBase58()}\n\nTransaction: ${tx}`)
      console.log('✅ Registry initialized with auto-deployed contract')

    } catch (error) {
      console.error('❌ Error:', error)
      if (error.logs) console.error('📜 Logs:', error.logs)
      
      if (error.message.includes('ConstraintTokenOwner')) {
        setStatus('❌ У вас нет Master NFT в кошельке!')
      } else {
        setStatus(`❌ Ошибка: ${error.message}`)
      }
    }
  }

  // ============================================================================
  // 3️⃣ Создание License NFT
  // ============================================================================
  const createLicenseNFT = async () => {
    if (!wallet.publicKey || !masterMint) {
      setStatus('❌ Сначала создайте Master NFT!')
      return
    }

    if (!registryInitialized) {
      setStatus('⚠️ Сначала инициализируйте реестр!')
      return
    }

    try {
      setStatus('⏳ Создаём License NFT...')
      console.log('🖨️ Minting Print Edition...')

      const umi = createUmi(connection.rpcEndpoint)
        .use(mplTokenMetadata())
        .use(walletAdapterIdentity(wallet))

      const licenseMintSigner = generateSigner(umi)
      const masterMintPubkey = new PublicKey(masterMint)

      const tx = await mintV1(umi, {
        mint: licenseMintSigner,
        authority: umi.identity,
        name: `License #${Date.now()}`,
        uri: 'https://arweave.net/license.json',
        sellerFeeBasisPoints: percentAmount(5),
        tokenStandard: TokenStandard.NonFungible,
      }).sendAndConfirm(umi, {
        send: { skipPreflight: false },
        confirm: { commitment: 'confirmed' }
      })

      const licenseMintPubkey = licenseMintSigner.publicKey.toString()
      setLicenseMint(licenseMintPubkey)

      console.log('🔍 Verifying Print Edition...')
      const umiMint = fromWeb3JsPublicKey(new PublicKey(licenseMintPubkey))
      const asset = await fetchDigitalAsset(umi, umiMint)
      
      if (asset.edition && !asset.edition.isOriginal) {
        console.log('✅ Print Edition verified!')
        setStatus(`✅ License NFT создан!\n\nMint: ${licenseMintPubkey}\nEdition #: ${asset.edition.number}\nSignature: ${tx.signature}\n\n✅ Нажмите "Activate License"!`)
      }

    } catch (error) {
      console.error('❌ Error:', error)
      setStatus(`❌ Ошибка: ${error.message}`)
    }
  }

  // ============================================================================
  // 4️⃣ Активация лицензии
  // ============================================================================
  const activateLicense = async () => {
    if (!wallet.publicKey || !masterMint || !licenseMint) {
      setStatus('❌ Создайте Master и License NFT!')
      return
    }

    try {
      setStatus('⏳ Активируем лицензию...')
      console.log('🔧 Activating license...')

      const masterMintPubkey = new PublicKey(masterMint)
      const licenseMintPubkey = new PublicKey(licenseMint)

      const [registryPda] = PublicKey.findProgramAddressSync(
        [Buffer.from('registry'), masterMintPubkey.toBuffer()],
        LICENSE_REGISTRY_PROGRAM_ID
      )

      const [licenseEntryPda] = PublicKey.findProgramAddressSync(
        [Buffer.from('license'), licenseMintPubkey.toBuffer()],
        LICENSE_REGISTRY_PROGRAM_ID
      )

      const masterAta = getAssociatedTokenAddressSync(
        masterMintPubkey,
        wallet.publicKey,
        false,
        TOKEN_PROGRAM_ID
      )

      const [licenseMetadataPda] = PublicKey.findProgramAddressSync(
        [
          Buffer.from('metadata'),
          METADATA_PROGRAM_ID.toBuffer(),
          licenseMintPubkey.toBuffer(),
        ],
        METADATA_PROGRAM_ID
      )

      const [licenseEditionPda] = PublicKey.findProgramAddressSync(
        [
          Buffer.from('metadata'),
          METADATA_PROGRAM_ID.toBuffer(),
          licenseMintPubkey.toBuffer(),
          Buffer.from('edition'),
        ],
        METADATA_PROGRAM_ID
      )

      console.log('📋 License Entry PDA:', licenseEntryPda.toBase58())

      const provider = new anchor.AnchorProvider(connection, wallet, { commitment: 'confirmed' })
      const idl = await anchor.Program.fetchIdl(LICENSE_REGISTRY_PROGRAM_ID, provider)
      const program = new anchor.Program(idl, provider)

      const tx = await program.methods
        .activateLicense()
        .accounts({
          registry: registryPda,
          licenseEntry: licenseEntryPda,
          authority: wallet.publicKey,
          masterNftMint: masterMintPubkey,
          masterNftAta: masterAta,
          licenseNftMint: licenseMintPubkey,
          licenseMetadata: licenseMetadataPda,
          licenseEdition: licenseEditionPda,
          systemProgram: SystemProgram.programId,
          tokenProgram: TOKEN_PROGRAM_ID,
        })
        .rpc()

      setStatus(`✅ Лицензия активирована!\n\nEntry: ${licenseEntryPda.toBase58()}\nSignature: ${tx}`)
      console.log('✅ Activated, tx:', tx)

    } catch (error) {
      console.error('❌ Error:', error)
      if (error.logs) console.error('📜 Logs:', error.logs)
      
      if (error.message.includes('InvalidParent')) {
        setStatus('❌ License NFT не является Print Edition!')
      } else if (error.message.includes('AlreadyActive')) {
        setStatus('⚠️ Лицензия уже активна!')
      } else {
        setStatus(`❌ Ошибка: ${error.message}`)
      }
    }
  }

  // ============================================================================
  // 5️⃣ Отзыв лицензии
  // ============================================================================
  const revokeLicense = async () => {
    if (!wallet.publicKey || !masterMint || !licenseMint) {
      setStatus('❌ Укажите адреса NFT!')
      return
    }

    try {
      setStatus('⏳ Отзываем лицензию...')

      const masterMintPubkey = new PublicKey(masterMint)
      const licenseMintPubkey = new PublicKey(licenseMint)

      const [registryPda] = PublicKey.findProgramAddressSync(
        [Buffer.from('registry'), masterMintPubkey.toBuffer()],
        LICENSE_REGISTRY_PROGRAM_ID
      )

      const [licenseEntryPda] = PublicKey.findProgramAddressSync(
        [Buffer.from('license'), licenseMintPubkey.toBuffer()],
        LICENSE_REGISTRY_PROGRAM_ID
      )

      const masterAta = getAssociatedTokenAddressSync(
        masterMintPubkey,
        wallet.publicKey,
        false,
        TOKEN_PROGRAM_ID
      )

      const provider = new anchor.AnchorProvider(connection, wallet, { commitment: 'confirmed' })
      const idl = await anchor.Program.fetchIdl(LICENSE_REGISTRY_PROGRAM_ID, provider)
      const program = new anchor.Program(idl, provider)

      const tx = await program.methods
        .revokeLicense()
        .accounts({
          registry: registryPda,
          licenseEntry: licenseEntryPda,
          authority: wallet.publicKey,
          masterNftMint: masterMintPubkey,
          masterNftAta: masterAta,
          tokenProgram: TOKEN_PROGRAM_ID,
        })
        .rpc()

      setStatus(`✅ Лицензия отозвана!\n\nSignature: ${tx}`)

    } catch (error) {
      console.error('❌ Error:', error)
      if (error.message.includes('AlreadyInactive')) {
        setStatus('⚠️ Лицензия уже неактивна!')
      } else {
        setStatus(`❌ Ошибка: ${error.message}`)
      }
    }
  }

  // ============================================================================
  // 6️⃣ Проверка статуса
  // ============================================================================
  const checkStatus = async () => {
    if (!licenseMint) {
      setStatus('❌ Укажите License Mint!')
      return
    }

    try {
      setStatus('⏳ Загружаем данные...')

      const licenseMintPubkey = new PublicKey(licenseMint)
      const [licenseEntryPda] = PublicKey.findProgramAddressSync(
        [Buffer.from('license'), licenseMintPubkey.toBuffer()],
        LICENSE_REGISTRY_PROGRAM_ID
      )

      const provider = new anchor.AnchorProvider(connection, wallet, { commitment: 'confirmed' })
      const idl = await anchor.Program.fetchIdl(LICENSE_REGISTRY_PROGRAM_ID, provider)
      const program = new anchor.Program(idl, provider)

      const entry = await program.account.licenseEntry.fetch(licenseEntryPda)

      const statusEmoji = entry.status.active ? '✅ Active' : '❌ Inactive'
      const activatedDate = new Date(entry.activatedTimestamp.toNumber() * 1000).toLocaleString()

      setStatus(`
📊 Статус лицензии

License Mint: ${entry.licenseNftMint.toBase58()}
Edition #: ${entry.editionNumber.toString()}
Status: ${statusEmoji}
History: ${entry.historyCount} активаций

Activated: ${activatedDate}
Block: ${entry.activatedAt.toString()}

PDA: ${licenseEntryPda.toBase58()}
      `)

    } catch (error) {
      console.error('❌ Error:', error)
      if (error.message.includes('Account does not exist')) {
        setStatus('❌ Лицензия не найдена! Сначала активируйте.')
      } else {
        setStatus(`❌ Ошибка: ${error.message}`)
      }
    }
  }

  // ============================================================================
  // Styles
  // ============================================================================
  const sectionStyle = {
    marginBottom: '25px',
    padding: '20px',
    border: '2px solid',
    borderRadius: '8px',
    backgroundColor: '#fff',
  }

  const buttonStyle = {
    padding: '12px 24px',
    margin: '8px 5px',
    fontSize: '15px',
    cursor: 'pointer',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontWeight: 'bold',
    transition: 'all 0.3s',
  }

  const inputStyle = {
    width: '100%',
    padding: '12px',
    margin: '10px 0',
    fontSize: '13px',
    borderRadius: '6px',
    border: '1px solid #ddd',
    fontFamily: 'monospace',
    backgroundColor: '#fafafa',
    color: '#333'
  }

  // ============================================================================
  // UI
  // ============================================================================
  return (
    <div style={{ padding: '20px', maxWidth: '900px', margin: '0 auto', fontFamily: 'monospace' }}>
      <button onClick={onBack} style={{ marginBottom: '20px', padding: '10px 20px' }}>
        ← Назад
      </button>

      <h1 style={{ textAlign: 'center', color: '#4CAF50' }}>🎫 License Registry Manager</h1>
      <p style={{ textAlign: 'center', color: '#666', marginBottom: '30px' }}>
        Управление иерархической системой лицензирования
      </p>

      {/* Инструкция */}
      <div style={{ ...sectionStyle, backgroundColor: '#e3f2fd' }}>
        <h3>📖 Порядок действий:</h3>
        <ol style={{ lineHeight: '1.8' }}>
          <li><strong>Create Master NFT</strong> → создаёт корневой NFT авторизации</li>
          <li><strong>Initialize Registry</strong> → инициализирует реестр лицензий on-chain</li>
          <li><strong>Create License NFT</strong> → создаёт Print Edition (дочерний NFT)</li>
          <li><strong>Activate License</strong> → регистрирует лицензию в смарт-контракте</li>
          <li><strong>Check Status</strong> → проверяет текущее состояние</li>
          <li><strong>Revoke License</strong> (опционально) → отзывает лицензию</li>
        </ol>
      </div>

      {/* Master NFT Section */}
      <div style={{ ...sectionStyle, borderColor: '#4CAF50' }}>
        <h2>1️⃣ Master NFT (Root Authority)</h2>
        <button onClick={createMasterNFT} style={buttonStyle} disabled={!wallet.connected}>
          🎨 Create Master NFT
        </button>
        <input
          type="text"
          placeholder="Master Mint Address (автозаполнится)"
          value={masterMint}
          onChange={(e) => setMasterMint(e.target.value)}
          style={inputStyle}
        />
        <button 
          onClick={initRegistry} 
          style={{ ...buttonStyle, backgroundColor: registryInitialized ? '#9E9E9E' : '#4CAF50' }} 
          disabled={!masterMint || registryInitialized}
        >
          {registryInitialized ? '✅ Registry Initialized' : '🏗️ Initialize Registry'}
        </button>
      </div>

      {/* License NFT Section */}
      <div style={{ ...sectionStyle, borderColor: '#2196F3' }}>
        <h2>2️⃣ License NFT (Print Edition)</h2>
        <button 
          onClick={createLicenseNFT} 
          style={buttonStyle} 
          disabled={!registryInitialized}
        >
          📝 Create License NFT
        </button>
        <input
          type="text"
          placeholder="License Mint Address (автозаполнится)"
          value={licenseMint}
          onChange={(e) => setLicenseMint(e.target.value)}
          style={inputStyle}
        />
      </div>

      {/* License Management Section */}
      <div style={{ ...sectionStyle, borderColor: '#FF9800' }}>
        <h2>3️⃣ License Management</h2>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <button 
            onClick={activateLicense} 
            style={buttonStyle} 
            disabled={!licenseMint}
          >
            ✅ Activate License
          </button>
          <button 
            onClick={revokeLicense} 
            style={{...buttonStyle, backgroundColor: '#f44336'}}
            disabled={!licenseMint}
          >
            ❌ Revoke License
          </button>
          <button 
            onClick={checkStatus} 
            style={{...buttonStyle, backgroundColor: '#9C27B0'}}
            disabled={!licenseMint}
          >
            📊 Check Status
          </button>
        </div>
      </div>

      {/* Status Display */}
      <div style={{ ...sectionStyle, backgroundColor: '#f5f5f5', borderColor: '#9E9E9E' }}>
        <h3>📋 Status Log:</h3>
        <pre style={{ 
          whiteSpace: 'pre-wrap', 
          wordBreak: 'break-all',
          fontSize: '13px',
          lineHeight: '1.6',
          maxHeight: '400px',
          overflow: 'auto',
          color: '#333'
        }}>
          {status || 'Waiting for action...'}
        </pre>
      </div>
    </div>
  )
}

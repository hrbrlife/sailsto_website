import { useState, useEffect } from 'react'
import { useWallet, useConnection } from '@solana/wallet-adapter-react'
import { WalletMultiButton } from '@solana/wallet-adapter-react-ui'
import Master from './Master.jsx'
import Childs from './Childs.jsx'
import './App.css'

function App() {
  console.log('🔵 App rendering...')
  
  const { connected, publicKey } = useWallet()
  const { connection } = useConnection()
  const [page, setPage] = useState('home')
  const [balance, setBalance] = useState(0)

  console.log('🟢 App state:', { connected, page })

  useEffect(() => {
    console.log('🟡 useEffect running')
    if (connected && publicKey) {
      connection.getBalance(publicKey).then(bal => {
        console.log('💰 Balance loaded:', bal)
        setBalance(bal / 1e9)
      }).catch(err => {
        console.error('❌ Balance error:', err)
      })
    }
  }, [connected, publicKey, connection])

  const renderPage = () => {
    console.log('📄 Rendering page:', page)
    
    switch (page) {
      case 'master':
        console.log('📄 Rendering Master component')
        return <Master onBack={() => setPage('home')} />
      case 'childs':
        console.log('📄 Rendering Childs component')
        return <Childs onBack={() => setPage('home')} />
      default:
        console.log('📄 Rendering home page')
        return (
          <div style={{ padding: '20px' }}>
            <h1>Unified Licensing & KYC</h1>
            <WalletMultiButton />
            {connected && (
              <div style={{ marginTop: '20px' }}>
                <p>Wallet Balance: {balance.toFixed(4)} SOL</p>
                <button onClick={() => setPage('master')}>Master Page</button>
                <button style={{ marginLeft: '10px' }} onClick={() => setPage('childs')}>Childs Page</button>
              </div>
            )}
          </div>
        )
    }
  }

  console.log('🎨 About to render App JSX')

  return (
    <div className="App">
      {renderPage()}
    </div>
  )
}

export default App

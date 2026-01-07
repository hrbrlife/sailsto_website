import { Buffer } from 'buffer';
if (typeof window !== 'undefined') {
    window.Buffer = Buffer;
    window.global = window;
    window.process = { env: {} };
}
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { ConnectionProvider, WalletProvider } from '@solana/wallet-adapter-react'
import { WalletModalProvider, WalletMultiButton } from '@solana/wallet-adapter-react-ui'
import { PhantomWalletAdapter } from '@solana/wallet-adapter-wallets'
import { clusterApiUrl } from '@solana/web3.js'
import { useMemo } from 'react'
import './index.css'
import App from './App.jsx'
import '@solana/wallet-adapter-react-ui/styles.css'

console.log('🔴 main.jsx loaded!')
console.log('Root element:', document.getElementById('root'))

function WalletContextProvider({ children }) {
  const network = 'devnet'
  // Используем более надёжный RPC endpoint
  const endpoint = useMemo(() => {
    // Можно использовать свой RPC или платный сервис для лучшей производительности
    // return 'https://api.devnet.solana.com' // Официальный devnet
    return clusterApiUrl(network) // Стандартный endpoint
  }, [network])
  
  const wallets = useMemo(() => [new PhantomWalletAdapter()], [])

  console.log('🌐 RPC Endpoint:', endpoint)

  return (
    <ConnectionProvider endpoint={endpoint}>
      <WalletProvider wallets={wallets} autoConnect>
        <WalletModalProvider>
          {children}
        </WalletModalProvider>
      </WalletProvider>
    </ConnectionProvider>
  )
}

console.log('🟡 Creating React root...')

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <WalletContextProvider>
      <App />
    </WalletContextProvider>
  </StrictMode>,
)

console.log('🟢 React root created!')

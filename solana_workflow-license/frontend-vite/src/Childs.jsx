import { useWallet } from '@solana/wallet-adapter-react'

export default function Childs({ onBack }) {
  const { connected } = useWallet()

  return (
    <div style={{ padding: '20px' }}>
      <button onClick={onBack}>Back to Home</button>
      <h1>Childs Page</h1>
      <p>Manage child licenses.</p>
      {connected ? (
        <div>
          <p>Connected wallet: displaying child licenses...</p>
          <ul>
            <li>License 1</li>
            <li>License 2</li>
          </ul>
        </div>
      ) : (
        <p>Please connect your wallet to view child licenses.</p>
      )}
    </div>
  )
}
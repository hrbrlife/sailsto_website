# Copilot Instructions for Unified Licensing & KYC

## Architecture Overview

This is a **Solana blockchain project** implementing a hierarchical NFT-based licensing system with KYC verification:

1. **Master NFTs** → Platform authorization root (created via Metaplex)
2. **License NFTs** → Printable editions derived from master (minted via `MintNewEditionFromMasterEditionViaToken`)
3. **KYC Verification** → Admin-controlled state for license holders
4. **SPL-2022 Token** → Compliance-enabled token mint restricted to KYC-verified users

**Key Insight**: The system enforces compliance by restricting token transfer to verified users via on-chain state checks. License ownership determines KYC eligibility.

## Tech Stack

| Layer | Technologies |
|-------|---------------|
| Smart Contract | Rust + Anchor 0.30.x, SPL Token-2022 |
| Frontend | React 19 + Vite 7 + Metaplex UMI SDK |
| Blockchain | Solana devnet/localnet |
| NFT Standard | Metaplex Token Metadata (printable editions) |

## Build & Deployment Workflows

### Solana Program
```bash
anchor build          # Compiles Rust → IDL + program.so
anchor deploy         # Deploys to configured cluster (Anchor.toml)
```
**Config Location**: [Anchor.toml](Anchor.toml) defines cluster, wallet, and test command.

### Frontend Development
```bash
cd frontend-vite
yarn dev              # Starts Vite dev server on localhost:5173
yarn build            # Builds for production
yarn lint             # Runs ESLint
```
**Critical Setup**: [vite.config.js](frontend-vite/vite.config.js) includes Metaplex polyfills (`buffer`, `stream`) required for browser compatibility with Metaplex UMI SDK.

## Core Patterns & Conventions

### Account Derivation (Anchor PDAs)
All program state uses PDA seeds matching the Solana standard:
- **Master**: `seeds=[b"master", master_nft_mint]`
- **Token Config**: `seeds=[b"token", spl_token_mint]`
- **License State**: `seeds=[b"license", license_mint]`
- **KYC State**: `seeds=[b"kyc", user_pubkey]`

When deriving PDAs in frontend, use exact seed ordering from [lib.rs](programs/unified-licensing-kyc/src/lib.rs) account structs.

### Metaplex Metadata Interaction
The program uses `MintNewEditionFromMasterEditionViaToken` for license issuance:
- Requires **master edition** PDA (not mint)
- Requires **master metadata** PDA for parent reference
- License becomes a **print edition** (has parent relationship)
- Frontend derivation: `findMasterEditionPda()`, `findMetadataPda()`, `findEditionMarkerPda()`

### Frontend Wallet Integration
[App.jsx](frontend-vite/src/App.jsx) establishes standard Solana wallet adapters:
- `WalletMultiButton` for provider selection
- `useWallet()` for signer context
- `useConnection()` for RPC endpoint

**Pattern**: All transaction building requires `wallet.publicKey` check first.

### UMI-Based Transaction Building
[Master.jsx](frontend-vite/src/Master.jsx) demonstrates Metaplex UMI workflow:
```javascript
const umi = createUmi(connection.rpcEndpoint)
  .use(mplTokenMetadata())
  .use(walletAdapterIdentity(wallet));
// Use UMI for Metaplex operations (NFT creation, edition minting)
```
UMI handles Metaplex-specific instructions and metadata interactions. For non-Metaplex operations (KYC checks, token minting), use Anchor client.

## Common Development Tasks

### Adding a New Program Instruction
1. Define `#[derive(Accounts)]` struct with PDA seeds in comments
2. Implement function in `#[program]` module
3. Use `require!()` macro for validation (converts to error codes)
4. Ensure account bumps are handled: `ctx.bumps.account_name`

### Deriving Frontend Client
Use Anchor IDL to auto-generate TypeScript types:
```bash
anchor build  # Generates target/idl/unified_licensing_kyc.json
```
Import IDL for type-safe anchor-client interactions.

### KYC Verification Flow
- Admin calls `set_kyc_status(user, is_verified)` → writes to KYC PDA
- User calls `execute()` → program checks `kyc_state.is_verified`
- If `token_config.required_kyc = true`, transfers fail for unverified users

## Project Structure

```
programs/unified-licensing-kyc/
├── src/lib.rs              # Single file: all instructions + account structs
└── Cargo.toml              # Anchor program config
frontend-vite/
├── src/
│   ├── App.jsx            # Router + wallet context
│   ├── Master.jsx         # Master NFT creation (Metaplex UMI)
│   ├── Childs.jsx         # License/KYC operations
│   └── main.jsx           # Entry point
└── vite.config.js         # Critical: Metaplex polyfills
```

**No separate modules**: All Rust code is in `lib.rs` for clarity given the program's scope.

## Debugging & Testing

### Failed Transactions
- Check `ErrorCode::*` enum in lib.rs (custom errors)
- Verify PDA derivation matches program (seed ordering, program ID)
- Ensure signer authority matches account owner

### Token Metadata Issues
- Verify metadata accounts exist before deriving edition PDAs
- Master edition must be initialized before minting editions
- Printable editions require `maxSupply` on master edition

### Frontend Compatibility
- If Metaplex operations fail: check `vite.config.js` polyfills are loaded
- Browser console errors often indicate missing globals (`Buffer`, `process`)
- Solana devtools extension useful for transaction inspection

## Error Codes
Defined in lib.rs and returned as `Err()` from instructions:
- `Unauthorized` - Signer mismatch or ownership validation failed
- `InvalidAmount` - NFT amount != 1 or insufficient tokens
- `NoKyc` - User not verified when `required_kyc = true`

## External Dependencies to Know

| Package | Purpose | Quirk |
|---------|---------|-------|
| `@metaplex-foundation/mpl-token-metadata` | Metadata & edition creation | Requires UMI SDK integration |
| `@solana/wallet-adapter-react` | Wallet context | Must initialize with `ConnectionProvider` |
| `anchor-lang` | Rust macros for accounts/validation | Seeds must exactly match frontend derivation |
| `spl-token-2022` | Token transfers with hooks | Uses different program ID than legacy SPL |

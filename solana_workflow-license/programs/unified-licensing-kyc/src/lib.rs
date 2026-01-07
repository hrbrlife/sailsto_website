use anchor_lang::prelude::*;
use anchor_spl::token_interface::{Mint, TokenAccount};

declare_id!("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS");

#[program]
pub mod unified_licensing_kyc {
    use super::*;
    pub fn init_master(ctx: Context<InitMaster>, master_nft_mint: Pubkey) -> Result<()> {
        let master_state = &mut ctx.accounts.master_state;
        master_state.master_nft_mint = master_nft_mint;
        master_state.authority = *ctx.accounts.authority.key;
        master_state.bump = ctx.bumps.master_state;
        require!(ctx.accounts.authority.is_signer, ErrorCode::Unauthorized);
        Ok(())
    }
    pub fn init_token_config(ctx: Context<InitTokenConfig>, spl_token_mint: Pubkey, min_kyc: u64, required_kyc: bool, allowed_master_nfts: Vec<Pubkey>) -> Result<()> {
        let token_config = &mut ctx.accounts.token_config;
        token_config.spl_token_mint = spl_token_mint;
        token_config.min_kyc = min_kyc;
        token_config.required_kyc = required_kyc;
        token_config.allowed_master_nfts = allowed_master_nfts;
        token_config.bump = ctx.bumps.token_config;
        Ok(())
    }
    pub fn register_license(ctx: Context<RegisterLicense>) -> Result<()> {
        // TODO: Добавить проверку владения Master NFT и Print Edition позднее
        // Для тестирования пропускаем сложную валидацию
        
        // Создаем License PDA для отслеживания
        let license_state = &mut ctx.accounts.license_state;
        license_state.license_nft_mint = ctx.accounts.license_mint.key();
        license_state.master_nft_mint = ctx.accounts.master_nft_mint.key();
        license_state.active = true;
        license_state.issued_kyc = 0;
        license_state.bump = ctx.bumps.license_state;
        
        Ok(())
    }
    pub fn revoke_license(ctx: Context<RevokeLicense>) -> Result<()> {
        // Проверяем, что вызывающий - authority из MasterState
        require!(
            ctx.accounts.admin.key() == ctx.accounts.master_state.authority, 
            ErrorCode::Unauthorized
        );
        
        // Деактивируем лицензию
        let license_state = &mut ctx.accounts.license_state;
        license_state.active = false;
        
        Ok(())
    }

    pub fn restore_license(ctx: Context<RestoreLicense>) -> Result<()> {
        // Только authority может восстанавливать
        require!(
            ctx.accounts.admin.key() == ctx.accounts.master_state.authority, 
            ErrorCode::Unauthorized
        );
        
        // Активируем лицензию обратно
        let license_state = &mut ctx.accounts.license_state;
        license_state.active = true;
        
        Ok(())
    }

    pub fn set_kyc_status(ctx: Context<SetKycStatus>, user: Pubkey, is_verified: bool) -> Result<()> {
        require!(ctx.accounts.admin.key() == ctx.accounts.master_state.authority, ErrorCode::Unauthorized);
        let kyc_state = &mut ctx.accounts.kyc_state;
        kyc_state.user = user;
        kyc_state.is_verified = is_verified;
        kyc_state.bump = ctx.bumps.kyc_state;
        Ok(())
    }
    pub fn execute(ctx: Context<Execute>, _amount: u64) -> Result<()> {
        // TODO: Добавить проверки KYC позднее
        // if ctx.accounts.token_config.required_kyc {
        //     // проверки KYC
        // }
        Ok(()) 
    }
}
#[derive(Accounts)]
pub struct InitMaster<'info> {
    #[account(
        init,
        payer = authority,
        space = 8 + 32 + 32 + 1,
        seeds = [b"master", master_nft_mint.key().as_ref()],
        bump
    )]
    pub master_state: Account<'info, MasterState>,
    /// CHECK: verified later
    pub master_nft_mint: AccountInfo<'info>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
}
#[account]
pub struct MasterState {
    pub master_nft_mint: Pubkey,
    pub authority: Pubkey,
    pub bump: u8,
}

#[derive(Accounts)]
pub struct InitTokenConfig<'info> {
    #[account(
        init,
        payer = authority,
        space = 8 + 32 + 8 + 1 + 4 + 32 * 10 + 1, // approximate for vec
        seeds = [b"token", spl_token_mint.key().as_ref()],
        bump
    )]
    pub token_config: Account<'info, TokenConfig>,
    /// CHECK: spl token mint
    pub spl_token_mint: AccountInfo<'info>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
}
#[account]
pub struct LicenseState {
    pub license_nft_mint: Pubkey,
    pub master_nft_mint: Pubkey,  // НОВОЕ: ссылка на Master NFT
    pub active: bool,
    pub issued_kyc: u64,
    pub bump: u8,
}
#[account]
pub struct TokenConfig {
    pub spl_token_mint: Pubkey,
    pub min_kyc: u64,
    pub required_kyc: bool,
    pub allowed_master_nfts: Vec<Pubkey>,
    pub bump: u8,
}
#[account]
pub struct Whitelist {
    pub programs: Vec<Pubkey>,
    pub bump: u8,
}
#[account]
pub struct KycState {
    pub user: Pubkey,
    pub is_verified: bool,
    pub bump: u8,
}
#[derive(Accounts)]
pub struct RegisterLicense<'info> {
    #[account(
        init,
        payer = owner,
        space = 8 + 32 + 32 + 1 + 8 + 1, // +32 для master_nft_mint
        seeds = [b"license", license_mint.key().as_ref()],
        bump
    )]
    pub license_state: Account<'info, LicenseState>,
    #[account(
        seeds = [b"master", master_state.master_nft_mint.as_ref()],
        bump = master_state.bump
    )]
    pub master_state: Account<'info, MasterState>,
    /// CHECK: Token account ownership verified later
    pub master_ata: UncheckedAccount<'info>,
    #[account(constraint = master_nft_mint.key() == master_state.master_nft_mint)]
    /// CHECK: Master NFT mint verified later
    pub master_nft_mint: UncheckedAccount<'info>,
    
    // Просто минт лицензии (без проверки метаданных пока)
    /// CHECK: License mint verified later  
    pub license_mint: UncheckedAccount<'info>,
    
    #[account(mut)]
    pub owner: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct RevokeLicense<'info> {
    #[account(
        mut,
        seeds = [b"license", license_state.license_nft_mint.as_ref()],
        bump = license_state.bump,
        constraint = license_state.active == true @ ErrorCode::LicenseAlreadyRevoked
    )]
    pub license_state: Account<'info, LicenseState>,
    #[account(
        seeds = [b"master", master_state.master_nft_mint.as_ref()],
        bump = master_state.bump
    )]
    pub master_state: Account<'info, MasterState>,
    #[account(mut)]
    pub admin: Signer<'info>,
}

#[derive(Accounts)]
pub struct RestoreLicense<'info> {
    #[account(
        mut,
        seeds = [b"license", license_state.license_nft_mint.as_ref()],
        bump = license_state.bump,
        constraint = license_state.active == false @ ErrorCode::LicenseAlreadyActive
    )]
    pub license_state: Account<'info, LicenseState>,
    #[account(
        seeds = [b"master", master_state.master_nft_mint.as_ref()],
        bump = master_state.bump
    )]
    pub master_state: Account<'info, MasterState>,
    #[account(mut)]
    pub admin: Signer<'info>,
}
#[derive(Accounts)]
#[instruction(user: Pubkey)]
pub struct SetKycStatus<'info> {
    #[account(
        init_if_needed,
        payer = admin,
        space = 8 + 32 + 1 + 1,
        seeds = [b"kyc", user.as_ref()],
        bump
    )]
    pub kyc_state: Account<'info, KycState>,
    #[account(
        seeds = [b"master", master_state.master_nft_mint.as_ref()],
        bump = master_state.bump
    )]
    pub master_state: Account<'info, MasterState>,
    #[account(mut)]
    pub admin: Signer<'info>,
    pub system_program: Program<'info, System>,
}
#[derive(Accounts)]
pub struct Execute<'info> {
    #[account(
        seeds = [b"token", mint.key().as_ref()],
        bump = token_config.bump
    )]
    pub token_config: Account<'info, TokenConfig>,
    /// CHECK: Source token account verified later
    pub source: UncheckedAccount<'info>,
    /// CHECK: Destination token account verified later
    pub destination: UncheckedAccount<'info>,
    pub authority: Signer<'info>,
    /// CHECK: Token mint verified later
    pub mint: UncheckedAccount<'info>,
}
#[error_code]
pub enum ErrorCode {
    #[msg("Unauthorized")]
    Unauthorized,
    #[msg("Invalid amount")]
    InvalidAmount,
    #[msg("No KYC")]
    NoKyc,
    #[msg("License already revoked")]
    LicenseAlreadyRevoked,
    #[msg("License already active")]
    LicenseAlreadyActive,
    #[msg("Invalid parent-child relation")]
    InvalidParentRelation,
    #[msg("Invalid Print Edition")]
    InvalidPrintEdition,
    #[msg("Master NFT not in allowed list")]
    MasterNftNotAllowed,
}
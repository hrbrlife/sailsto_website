use anchor_lang::prelude::*;
use anchor_spl::token_interface::{Mint, TokenAccount, TokenInterface};
use mpl_token_metadata::accounts::{Metadata, Edition};

declare_id!("11111111111111111111111111111111");

// ============================================================================
// ВАЖНО: Адрес Master NFT для этого контракта
// ============================================================================
// ⚠️ ЗАМЕНИТЕ на реальный адрес вашего Master NFT после его создания!
// ⚠️ КАЖДЫЙ Master NFT = НОВЫЙ деплой с НОВЫМ Program ID!
//
// ПОЛНАЯ ИНСТРУКЦИЯ ПО ДЕПЛОЮ (для каждого Master NFT):
// 
// 1. Создайте Master NFT через фронтенд (кнопка "Create Master NFT")
// 2. Скопируйте его mint адрес из консоли браузера
// 3. Вставьте mint адрес сюда вместо "11111111111111111111111111111111"
// 
// 4. СОЗДАЙТЕ НОВЫЙ Program Keypair:
//    solana-keygen new -o target/deploy/license_registry-keypair.json --force
//    (--force перезаписывает старый, создавая НОВЫЙ Program ID)
// 
// 5. Запустите: anchor build
//    (это сгенерирует новый Program ID в target/idl/license_registry.json)
// 
// 6. ОБНОВИТЕ declare_id! выше на новый Program ID из:
//    target/deploy/license_registry-keypair.json (публичный ключ)
//    или из вывода: solana address -k target/deploy/license_registry-keypair.json
// 
// 7. Пересоберите с новым ID: anchor build
// 
// 8. Задеплойте программу: anchor deploy
//    (создастся НОВЫЙ контракт с НОВЫМ Program ID)
// 
// 9. Обновите в frontend-vite/src/Master.jsx:
//    - Строка 28: LICENSE_REGISTRY_PROGRAM_ID = новый Program ID
// 
// 10. Готово! Этот контракт работает ТОЛЬКО с этим Master NFT!
//
// ИТОГО: Каждый Master NFT → Новый keypair → Новый Program ID → Новый деплой
pub const MASTER_NFT_MINT: Pubkey = pubkey!("11111111111111111111111111111111");

#[program]
pub mod license_registry {
    use super::*;

    /// Инициализация реестра лицензий для Master NFT
    pub fn init_registry(ctx: Context<InitRegistry>) -> Result<()> {
        let registry = &mut ctx.accounts.registry;
        
        // КРИТИЧЕСКАЯ ПРОВЕРКА: Master NFT должен совпадать с хардкоженным
        require!(
            ctx.accounts.master_nft_mint.key() == MASTER_NFT_MINT,
            ErrorCode::WrongMasterNFT
        );
        
        // Проверка владения Master NFT
        require!(
            ctx.accounts.master_nft_ata.amount >= 1,
            ErrorCode::NotMasterOwner
        );

        registry.authority = ctx.accounts.authority.key();
        registry.master_nft_mint = ctx.accounts.master_nft_mint.key();
        registry.total_licenses = 0;
        registry.active_licenses = 0;
        registry.bump = ctx.bumps.registry;

        msg!("Registry initialized for Master NFT: {}", registry.master_nft_mint);
        Ok(())
    }

    /// Активация лицензии (регистрация Print Edition NFT)
    pub fn activate_license(ctx: Context<ActivateLicense>) -> Result<()> {
        let registry = &mut ctx.accounts.registry;
        let license_entry = &mut ctx.accounts.license_entry;

        // КРИТИЧЕСКАЯ ПРОВЕРКА: Master NFT должен совпадать с хардкоженным
        require!(
            ctx.accounts.master_nft_mint.key() == MASTER_NFT_MINT,
            ErrorCode::WrongMasterNFT
        );

        // 1. Проверка владения Master NFT
        require!(
            ctx.accounts.master_nft_ata.amount >= 1,
            ErrorCode::NotMasterOwner
        );

        // 2. Проверка что License NFT является Print Edition
        let edition_data = ctx.accounts.license_edition.to_account_info().try_borrow_data()?;
        let edition: Edition = Edition::deserialize(&mut &edition_data[..])?;
        
        require!(
            edition.parent == ctx.accounts.master_nft_mint.key(),
            ErrorCode::InvalidParent
        );

        // 3. Проверка метаданных лицензии
        let license_metadata_data = ctx.accounts.license_metadata.to_account_info().try_borrow_data()?;
        let license_metadata: Metadata = Metadata::deserialize(&mut &license_metadata_data[..])?;
        
        require!(
            license_metadata.mint == ctx.accounts.license_nft_mint.key(),
            ErrorCode::InvalidMetadata
        );

        // 4. Проверка что лицензия еще не активна
        if license_entry.license_nft_mint != Pubkey::default() {
            require!(
                license_entry.status == LicenseStatus::Inactive,
                ErrorCode::AlreadyActive
            );
        }

        // 5. Запись активации
        let clock = Clock::get()?;
        license_entry.license_nft_mint = ctx.accounts.license_nft_mint.key();
        license_entry.master_nft_mint = ctx.accounts.master_nft_mint.key();
        license_entry.edition_number = edition.edition;
        license_entry.status = LicenseStatus::Active;
        license_entry.activated_at = clock.slot;
        license_entry.activated_timestamp = clock.unix_timestamp;
        license_entry.deactivated_at = None;
        license_entry.deactivated_timestamp = None;
        license_entry.history_count = if license_entry.history_count == 0 { 1 } else { license_entry.history_count + 1 };
        license_entry.bump = ctx.bumps.license_entry;

        // 6. Обновление счетчиков реестра
        if license_entry.history_count == 1 {
            registry.total_licenses = registry.total_licenses.checked_add(1).unwrap();
        }
        registry.active_licenses = registry.active_licenses.checked_add(1).unwrap();

        msg!(
            "License activated: {} (Edition #{}), Block: {}, Time: {}",
            license_entry.license_nft_mint,
            edition.edition,
            clock.slot,
            clock.unix_timestamp
        );

        Ok(())
    }

    /// Деактивация лицензии (отзыв)
    pub fn revoke_license(ctx: Context<RevokeLicense>) -> Result<()> {
        let registry = &mut ctx.accounts.registry;
        let license_entry = &mut ctx.accounts.license_entry;

        // КРИТИЧЕСКАЯ ПРОВЕРКА: Master NFT должен совпадать с хардкоженным
        require!(
            ctx.accounts.master_nft_mint.key() == MASTER_NFT_MINT,
            ErrorCode::WrongMasterNFT
        );

        // 1. Проверка владения Master NFT
        require!(
            ctx.accounts.master_nft_ata.amount >= 1,
            ErrorCode::NotMasterOwner
        );

        // 2. Проверка что лицензия существует и активна
        require!(
            license_entry.license_nft_mint != Pubkey::default(),
            ErrorCode::LicenseNotFound
        );
        require!(
            license_entry.status == LicenseStatus::Active,
            ErrorCode::AlreadyInactive
        );

        // 3. Проверка связи с Master NFT
        require!(
            license_entry.master_nft_mint == ctx.accounts.master_nft_mint.key(),
            ErrorCode::InvalidMaster
        );

        // 4. Запись деактивации
        let clock = Clock::get()?;
        license_entry.status = LicenseStatus::Inactive;
        license_entry.deactivated_at = Some(clock.slot);
        license_entry.deactivated_timestamp = Some(clock.unix_timestamp);

        // 5. Обновление счетчиков реестра
        registry.active_licenses = registry.active_licenses.checked_sub(1).unwrap();

        msg!(
            "License revoked: {} (Edition #{}), Block: {}, Time: {}",
            license_entry.license_nft_mint,
            license_entry.edition_number,
            clock.slot,
            clock.unix_timestamp
        );

        Ok(())
    }

    /// Получение информации о лицензии (view function)
    pub fn get_license_info(ctx: Context<GetLicenseInfo>) -> Result<()> {
        let license_entry = &ctx.accounts.license_entry;
        
        msg!("License NFT: {}", license_entry.license_nft_mint);
        msg!("Master NFT: {}", license_entry.master_nft_mint);
        msg!("Edition #: {}", license_entry.edition_number);
        msg!("Status: {:?}", license_entry.status);
        msg!("Activated at block: {}", license_entry.activated_at);
        msg!("Activated timestamp: {}", license_entry.activated_timestamp);
        
        if let Some(deactivated_at) = license_entry.deactivated_at {
            msg!("Deactivated at block: {}", deactivated_at);
        }
        if let Some(deactivated_timestamp) = license_entry.deactivated_timestamp {
            msg!("Deactivated timestamp: {}", deactivated_timestamp);
        }
        
        msg!("History count: {}", license_entry.history_count);
        
        Ok(())
    }
}

// ============================================================================
// Account Structs
// ============================================================================

/// Реестр лицензий для конкретного Master NFT
/// PDA seeds: ["registry", master_nft_mint]
#[account]
pub struct LicenseRegistry {
    pub authority: Pubkey,           // Владелец Master NFT
    pub master_nft_mint: Pubkey,     // Mint адрес Master NFT
    pub total_licenses: u64,         // Всего зарегистрировано лицензий
    pub active_licenses: u64,        // Активных лицензий сейчас
    pub bump: u8,
}

impl LicenseRegistry {
    pub const LEN: usize = 8 + // discriminator
        32 + // authority
        32 + // master_nft_mint
        8 + // total_licenses
        8 + // active_licenses
        1; // bump
}

/// Запись о конкретной лицензии (Print Edition NFT)
/// PDA seeds: ["license", license_nft_mint]
#[account]
pub struct LicenseEntry {
    pub license_nft_mint: Pubkey,        // Mint адрес License NFT
    pub master_nft_mint: Pubkey,         // Mint адрес родительского Master NFT
    pub edition_number: u64,             // Номер Print Edition
    pub status: LicenseStatus,           // Текущий статус (Active/Inactive)
    pub activated_at: u64,               // Блок активации
    pub activated_timestamp: i64,        // Unix timestamp активации
    pub deactivated_at: Option<u64>,     // Блок деактивации (если была)
    pub deactivated_timestamp: Option<i64>, // Unix timestamp деактивации
    pub history_count: u32,              // Количество активаций/деактиваций
    pub bump: u8,
}

impl LicenseEntry {
    pub const LEN: usize = 8 + // discriminator
        32 + // license_nft_mint
        32 + // master_nft_mint
        8 + // edition_number
        1 + // status enum
        8 + // activated_at
        8 + // activated_timestamp
        1 + 8 + // deactivated_at Option<u64>
        1 + 8 + // deactivated_timestamp Option<i64>
        4 + // history_count
        1; // bump
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, Copy, PartialEq, Eq, Debug)]
pub enum LicenseStatus {
    Active,
    Inactive,
}

// ============================================================================
// Instruction Contexts
// ============================================================================

#[derive(Accounts)]
pub struct InitRegistry<'info> {
    #[account(
        init,
        payer = authority,
        space = LicenseRegistry::LEN,
        seeds = [b"registry", master_nft_mint.key().as_ref()],
        bump
    )]
    pub registry: Account<'info, LicenseRegistry>,

    #[account(mut)]
    pub authority: Signer<'info>,

    /// Master NFT mint account
    pub master_nft_mint: InterfaceAccount<'info, Mint>,

    /// Master NFT token account (проверка владения)
    #[account(
        constraint = master_nft_ata.mint == master_nft_mint.key(),
        constraint = master_nft_ata.owner == authority.key(),
        constraint = master_nft_ata.amount >= 1
    )]
    pub master_nft_ata: InterfaceAccount<'info, TokenAccount>,

    /// Master NFT metadata (для валидации)
    /// CHECK: Validated via Metaplex deserialization
    pub master_metadata: UncheckedAccount<'info>,

    pub system_program: Program<'info, System>,
    pub token_program: Interface<'info, TokenInterface>,
}

#[derive(Accounts)]
pub struct ActivateLicense<'info> {
    #[account(
        mut,
        seeds = [b"registry", master_nft_mint.key().as_ref()],
        bump = registry.bump,
        has_one = master_nft_mint @ ErrorCode::InvalidMaster
    )]
    pub registry: Account<'info, LicenseRegistry>,

    #[account(
        init_if_needed,
        payer = authority,
        space = LicenseEntry::LEN,
        seeds = [b"license", license_nft_mint.key().as_ref()],
        bump
    )]
    pub license_entry: Account<'info, LicenseEntry>,

    #[account(mut)]
    pub authority: Signer<'info>,

    /// Master NFT mint
    pub master_nft_mint: InterfaceAccount<'info, Mint>,

    /// Master NFT ATA (proof of ownership)
    #[account(
        constraint = master_nft_ata.mint == master_nft_mint.key(),
        constraint = master_nft_ata.owner == authority.key(),
        constraint = master_nft_ata.amount >= 1
    )]
    pub master_nft_ata: InterfaceAccount<'info, TokenAccount>,

    /// License NFT mint (Print Edition)
    pub license_nft_mint: InterfaceAccount<'info, Mint>,

    /// License NFT metadata
    /// CHECK: Validated via Metaplex deserialization
    pub license_metadata: UncheckedAccount<'info>,

    /// License NFT edition account (contains parent relationship)
    /// CHECK: Validated via Edition deserialization
    pub license_edition: UncheckedAccount<'info>,

    pub system_program: Program<'info, System>,
    pub token_program: Interface<'info, TokenInterface>,
}

#[derive(Accounts)]
pub struct RevokeLicense<'info> {
    #[account(
        mut,
        seeds = [b"registry", master_nft_mint.key().as_ref()],
        bump = registry.bump,
        has_one = master_nft_mint @ ErrorCode::InvalidMaster
    )]
    pub registry: Account<'info, LicenseRegistry>,

    #[account(
        mut,
        seeds = [b"license", license_entry.license_nft_mint.as_ref()],
        bump = license_entry.bump
    )]
    pub license_entry: Account<'info, LicenseEntry>,

    #[account(mut)]
    pub authority: Signer<'info>,

    /// Master NFT mint
    pub master_nft_mint: InterfaceAccount<'info, Mint>,

    /// Master NFT ATA (proof of ownership)
    #[account(
        constraint = master_nft_ata.mint == master_nft_mint.key(),
        constraint = master_nft_ata.owner == authority.key(),
        constraint = master_nft_ata.amount >= 1
    )]
    pub master_nft_ata: InterfaceAccount<'info, TokenAccount>,

    pub token_program: Interface<'info, TokenInterface>,
}

#[derive(Accounts)]
pub struct GetLicenseInfo<'info> {
    #[account(
        seeds = [b"license", license_entry.license_nft_mint.as_ref()],
        bump = license_entry.bump
    )]
    pub license_entry: Account<'info, LicenseEntry>,
}

// ============================================================================
// Error Codes
// ============================================================================

#[error_code]
pub enum ErrorCode {
    #[msg("Not the owner of Master NFT")]
    NotMasterOwner,
    
    #[msg("License NFT parent does not match Master NFT")]
    InvalidParent,
    
    #[msg("Invalid metadata account")]
    InvalidMetadata,
    
    #[msg("License already active")]
    AlreadyActive,
    
    #[msg("License not found")]
    LicenseNotFound,
    
    #[msg("License already inactive")]
    AlreadyInactive,
    
    #[msg("Invalid Master NFT")]
    InvalidMaster,
    
    #[msg("Wrong Master NFT - this contract is tied to a specific Master NFT")]
    WrongMasterNFT,
}

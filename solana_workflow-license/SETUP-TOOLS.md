# ⚡ Быстрая установка инструментов

## 1️⃣ Установка Solana CLI (Windows)

### Вариант A: Через WSL (рекомендуется)
```powershell
# 1. Установите WSL2 если ещё нет:
wsl --install

# 2. Откройте WSL terminal и установите Solana:
sh -c "$(curl -sSfL https://release.solana.com/stable/install)"

# 3. Добавьте в PATH:
echo 'export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 4. Проверка:
solana --version
```

### Вариант B: Нативный Windows installer
```powershell
# Скачайте installer с:
# https://github.com/solana-labs/solana/releases

# Или используйте Chocolatey:
choco install solana
```

## 2️⃣ Установка Rust (если ещё нет)

```powershell
# Скачайте rustup-init.exe с:
# https://www.rust-lang.org/tools/install

# Или используйте команду:
winget install Rustlang.Rustup
```

После установки перезапустите PowerShell и проверьте:
```powershell
rustc --version
cargo --version
```

## 3️⃣ Установка Anchor CLI

```powershell
# Установите Anchor Version Manager (AVM):
cargo install --git https://github.com/coral-xyz/anchor avm --locked --force

# Установите latest версию Anchor:
avm install latest
avm use latest

# Проверка:
anchor --version
```

**Примечание**: Установка может занять 10-20 минут, так как компилируется из исходников.

## 4️⃣ Настройка Solana кошелька

```powershell
# Переключитесь на devnet:
solana config set --url https://api.devnet.solana.com

# Создайте новый кошелёк:
solana-keygen new

# ВАЖНО: Сохраните seed phrase в безопасном месте!

# Проверьте адрес:
solana address

# Пополните баланс (нужно минимум 2 SOL для деплоя):
solana airdrop 2

# Проверьте баланс:
solana balance
```

## 5️⃣ Проверка готовности

Запустите все команды - все должны работать:
```powershell
solana --version      # → solana-cli 1.x.x
anchor --version      # → anchor-cli 0.30.x
rustc --version       # → rustc 1.x.x
cargo --version       # → cargo 1.x.x
solana balance        # → 2 SOL (или больше)
```

## ✅ Теперь можно запускать проект!

```powershell
# Терминал 1 - Backend:
cd D:\sol_project\backend
npm start

# Терминал 2 - Frontend:
cd D:\sol_project\frontend-vite
npm run dev
```

## 🐛 Troubleshooting

### "command not found" после установки
Перезапустите PowerShell или добавьте в PATH:
```powershell
$env:Path += ";C:\Users\<username>\.cargo\bin"
```

### Airdrop не работает
Devnet иногда нестабилен. Попробуйте:
```powershell
solana airdrop 1
# Подождите 10 секунд
solana airdrop 1
```

Или используйте альтернативный RPC:
```powershell
solana airdrop 2 --url https://api.devnet.solana.com
```

### Anchor установка падает с ошибкой
Убедитесь что установлен Visual Studio Build Tools:
```powershell
# Скачайте с:
# https://visualstudio.microsoft.com/downloads/
# Выберите "Build Tools for Visual Studio"
# Установите "Desktop development with C++"
```

### Нет интернета или медленная установка
Anchor можно установить из готового binary:
```powershell
# Скачайте с GitHub releases:
# https://github.com/coral-xyz/anchor/releases
```

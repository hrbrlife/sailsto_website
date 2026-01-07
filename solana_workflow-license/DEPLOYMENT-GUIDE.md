# Инструкция по деплою license-registry контракта

## Архитектура
**КРИТИЧЕСКИ ВАЖНО**: Каждый Master NFT = отдельный деплой контракта с уникальным Program ID!

Это означает:
- Нельзя использовать один контракт для нескольких Master NFT
- Каждый раз нужно создавать НОВЫЙ Program keypair
- Каждый Master NFT имеет свой собственный Program ID

## Предварительные требования

1. **Установите Solana CLI**:
```powershell
# Скачайте и установите с https://docs.solana.com/cli/install-solana-cli-tools
# Для Windows: используйте WSL или официальный installer
```

2. **Установите Anchor CLI**:
```powershell
cargo install --git https://github.com/coral-xyz/anchor avm --locked --force
avm install latest
avm use latest
```

3. **Настройте Solana на devnet**:
```powershell
solana config set --url https://api.devnet.solana.com
solana config set -k C:\Users\<ваш_пользователь>\.config\solana\id.json
```

4. **Пополните баланс (нужно ~2 SOL для деплоя)**:
```powershell
solana airdrop 2
```

---

## Процесс деплоя для НОВОГО Master NFT

### Шаг 1: Создайте Master NFT
```
1. Откройте http://localhost:5174
2. Подключите кошелёк (Phantom/Solflare)
3. Нажмите "Create Master NFT"
4. Дождитесь успешного создания
5. СКОПИРУЙТЕ mint адрес из консоли браузера (F12 → Console)
   Пример: CKfatsPMUf8SkiURsDXs7eK6GWb4Jsd6UDbs7twMCWxo
```

### Шаг 2: Вставьте Master NFT адрес в контракт
```
1. Откройте: programs/license-registry/src/lib.rs
2. Найдите строку 20 (примерно):
   pub const MASTER_NFT_MINT: Pubkey = pubkey!("11111111111111111111111111111111");
3. Замените "11111..." на ваш РЕАЛЬНЫЙ mint адрес:
   pub const MASTER_NFT_MINT: Pubkey = pubkey!("CKfatsPMUf8SkiURsDXs7eK6GWb4Jsd6UDbs7twMCWxo");
4. Сохраните файл (Ctrl+S)
```

### Шаг 3: СОЗДАЙТЕ новый Program Keypair
```powershell
cd D:\sol_project

# ОБЯЗАТЕЛЬНО: Создайте НОВЫЙ keypair с --force
solana-keygen new -o target/deploy/license_registry-keypair.json --force

# Это создаст НОВЫЙ уникальный Program ID для этого Master NFT!
```

### Шаг 4: Получите новый Program ID
```powershell
# Узнайте публичный ключ нового Program ID:
solana address -k target/deploy/license_registry-keypair.json

# Скопируйте вывод, например:
# 8szGkwr3kAQL1fVHCUPXp7jJQvNjMw3h4NZRqKqjqvTQ
```

### Шаг 5: Обновите declare_id! в контракте
```
1. Откройте: programs/license-registry/src/lib.rs
2. Найдите строку 5:
   declare_id!("11111111111111111111111111111111");
3. Замените на НОВЫЙ Program ID из предыдущего шага:
   declare_id!("8szGkwr3kAQL1fVHCUPXp7jJQvNjMw3h4NZRqKqjqvTQ");
4. Сохраните файл (Ctrl+S)
```

### Шаг 6: Соберите программу
```powershell
anchor build
```

**Ожидаемый вывод:**
```
Compiling license-registry v0.1.0
Finished release [optimized] target(s) in X.XXs
```

### Шаг 7: Задеплойте программу на devnet
```powershell
anchor deploy
```

**Ожидаемый вывод:**
```
Deploying cluster: https://api.devnet.solana.com
Upgrade authority: <ваш кошелёк>
Deploying program "license-registry"...
Program Id: 8szGkwr3kAQL1fVHCUPXp7jJQvNjMw3h4NZRqKqjqvTQ

Deploy success
```

### Шаг 8: Обновите frontend с новым Program ID
```
1. Откройте: frontend-vite/src/Master.jsx
2. Найдите строку 28:
   const LICENSE_REGISTRY_PROGRAM_ID = new PublicKey('11111111111111111111111111111111');
3. Замените на НОВЫЙ Program ID:
   const LICENSE_REGISTRY_PROGRAM_ID = new PublicKey('8szGkwr3kAQL1fVHCUPXp7jJQvNjMw3h4NZRqKqjqvTQ');
4. Сохраните файл (Ctrl+S)
```

### Шаг 9: Перезапустите frontend
```powershell
cd frontend-vite
yarn dev
```

### Шаг 10: Протестируйте полный цикл
```
1. Откройте http://localhost:5174
2. Нажмите "Initialize Registry" → должен создаться реестр
3. Нажмите "Create License NFT" → должна создаться лицензия
4. Нажмите "Activate License" → лицензия активируется
5. Нажмите "Check Status" → увидите is_active: true
6. Нажмите "Revoke License" → лицензия деактивируется
7. Нажмите "Check Status" → увидите is_active: false
```

---

## Для следующего Master NFT

**ПОВТОРИТЕ ВСЕ ШАГИ ЗАНОВО**:
1. Создайте новый Master NFT
2. Замените `MASTER_NFT_MINT` в lib.rs
3. **ОБЯЗАТЕЛЬНО** создайте НОВЫЙ keypair: `solana-keygen new -o ... --force`
4. Обновите `declare_id!` с новым Program ID
5. `anchor build`
6. `anchor deploy` → получите НОВЫЙ Program ID
7. Обновите `LICENSE_REGISTRY_PROGRAM_ID` в Master.jsx

**Результат**: Каждый Master NFT имеет свой собственный контракт!

---

## Проверка успешного деплоя

### 1. Проверьте программу на devnet:
```powershell
solana program show <Program ID>
```

**Вывод должен содержать:**
```
Program Id: 8szGkwr3kAQL1fVHCUPXp7jJQvNjMw3h4NZRqKqjqvTQ
Owner: BPFLoaderUpgradeab1e11111111111111111111111
ProgramData Address: <адрес>
Authority: <ваш кошелёк>
Last Deployed In Slot: <номер слота>
Data Length: <размер>
```

### 2. Проверьте IDL:
```powershell
cat target/idl/license_registry.json
```

Должен содержать правильный Program ID в поле `address`.

### 3. Проверьте консоль браузера:
После инициализации реестра должны увидеть:
```
Registry initialized: <PDA адрес>
Transaction confirmed
```

---

## Troubleshooting

### Ошибка: "Program not deployed"
**Причина**: Контракт не задеплоен или Program ID неправильный в frontend.
**Решение**: Проверьте, что Program ID в Master.jsx совпадает с выводом `anchor deploy`.

### Ошибка: "Wrong Master NFT"
**Причина**: Master NFT mint адрес в контракте не совпадает с используемым NFT.
**Решение**: Убедитесь, что `MASTER_NFT_MINT` в lib.rs = реальный mint адрес вашего Master NFT.

### Ошибка: "Insufficient funds"
**Причина**: Не хватает SOL для деплоя.
**Решение**: 
```powershell
solana airdrop 2
solana balance
```

### Ошибка: "Invalid keypair"
**Причина**: Keypair не существует или поврежден.
**Решение**:
```powershell
solana-keygen new -o target/deploy/license_registry-keypair.json --force
```

---

## Структура файлов после деплоя

```
sol_project/
├── programs/
│   └── license-registry/
│       └── src/
│           └── lib.rs  ← MASTER_NFT_MINT + declare_id! обновлены
├── target/
│   ├── deploy/
│   │   ├── license_registry-keypair.json  ← НОВЫЙ для каждого Master NFT
│   │   └── license_registry.so  ← Скомпилированная программа
│   └── idl/
│       └── license_registry.json  ← Правильный Program ID
└── frontend-vite/
    └── src/
        └── Master.jsx  ← LICENSE_REGISTRY_PROGRAM_ID обновлен
```

---

## Важные заметки

1. **Каждый Master NFT = новый Program ID** - это гарантирует изоляцию и безопасность
2. **Храните keypair-ы** - они нужны для апгрейда контракта
3. **Devnet vs Mainnet** - меняйте в `Anchor.toml`: cluster = "Mainnet"
4. **Стоимость деплоя на mainnet** - ~3-5 SOL (зависит от размера программы)

---

## Дополнительные команды

### Апгрейд существующего контракта:
```powershell
# Если нужно обновить логику БЕЗ смены Program ID:
anchor upgrade target/deploy/license_registry.so --program-id <Program ID>
```

### Закрытие программы (возврат SOL):
```powershell
solana program close <Program ID>
```

### Проверка логов транзакции:
```powershell
solana confirm <signature> -v
```

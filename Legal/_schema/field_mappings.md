# Document Field Mappings

> **Purpose**: Maps document placeholders to person/role data fields.
> Used by the populate tool to fill documents from the registry.

---

## Placeholder Syntax

Documents use this marker syntax:

```markdown
Current (manual):     [________________]
New (auto-populate):  [PERSON:P001.display_name]
                      [ROLE:company.ceo.display_name]
                      [ROLE:company.ceo.address.full]
```

---

## Field Reference

### Person Fields

| Field Path | Description | Example |
|------------|-------------|---------|
| `display_name` | Full display name | "Robert J. Doyle" |
| `legal_name.first` | First name | "Robert" |
| `legal_name.last` | Last name | "Doyle" |
| `address.street1` | Street address line 1 | "123 Main St" |
| `address.street2` | Street address line 2 | "Suite 400" |
| `address.city` | City | "Helena" |
| `address.state` | State | "MT" |
| `address.zip` | ZIP code | "59601" |
| `address.full` | Full formatted address | "123 Main St, Helena, MT 59601" |
| `phone` | Phone number | "+1-406-555-1234" |
| `email` | Email address | "robert@example.com" |
| `signature_block.name_line` | Signature name | "Robert J. Doyle" |

### Role-Based Fields

| Field Path | Description | Example |
|------------|-------------|---------|
| `{entity}.{role}.display_name` | Role holder's name | "Robert J. Doyle" |
| `{entity}.{role}.address.full` | Role holder's address | "123 Main St..." |
| `{entity}.{role}.title` | Role title | "Chief Executive Officer" |
| `{entity}.{role}.abbreviation` | Role abbreviation | "CEO" |

---

## Document Mappings

### A1 - Articles of Organization

```yaml
document: A1
path: "Company/Formation/A1_Articles_of_Organization.md"

fields:
  - location: "Section 1 - Organizer signature"
    current: "[________________]"
    mapping: "[ROLE:company.organizer.display_name]"
    context: "Printed Name:"
    
  - location: "Section 2 - Registered Agent name"
    current: "[________________]"
    mapping: "[ROLE:company.registered_agent.display_name]"
    context: "The name of the registered agent"
    
  - location: "Section 2 - Registered Agent address"
    current: "[________________]"
    mapping: "[ROLE:company.registered_agent.address.full]"
    context: "The street address of the registered agent"
```

---

### B1 - Master Operating Agreement

```yaml
document: B1
path: "Company/Governance/B1_Master_Operating_Agreement.md"

fields:
  - location: "§5.2"
    current: "5.2. The initial Manager is [________________]."
    mapping: "[ROLE:company.manager.display_name]"
    
  - location: "§6.2 - CEO"
    current: "The Chief Executive Officer is [________________]."
    mapping: "[ROLE:company.ceo.display_name]"
    
  - location: "§6.2 - CTO"
    current: "The Chief Technology Officer is [________________]."
    mapping: "[ROLE:company.cto.display_name]"
    
  - location: "§6.2 - CMO"
    current: "The Chief Marketing Officer is [________________]."
    mapping: "[ROLE:company.cmo.display_name]"
    
  - location: "§6.2 - CFO"
    current: "The Chief Financial Officer is [________________]."
    mapping: "[ROLE:company.cfo.display_name]"
    
  - location: "§6.2 - CCO"
    current: "The Chief Compliance Officer is [________________]."
    mapping: "[ROLE:company.cco.display_name]"
    
  - location: "§8.1 - Member name"
    current: "are [________________], holding"
    mapping: "[ROLE:company.member.display_name]"
    
  - location: "§8.1 - Member percentage"
    current: "holding [___] percent"
    mapping: "[ROLE:company.member.ownership_percentage]"
    
  - location: "§8.1 - Member address"
    current: "at [________________]."
    mapping: "[ROLE:company.member.address.full]"
    
  - location: "Signature - Manager"
    current: "Printed Name: [________________]"
    mapping: "[ROLE:company.manager.display_name]"
    context: "MANAGER SIGNATURE"
    
  - location: "Signature - Member"
    current: "Printed Name: [________________]"
    mapping: "[ROLE:company.member.display_name]"
    context: "MEMBER SIGNATURE"
```

---

### B2 - Officer Appointment Resolution

```yaml
document: B2
path: "Company/Governance/B2_Officer_Appointment_Resolution.md"

fields:
  - location: "§2.2 - CEO name"
    current: "The [TERM:CEO] Chief Executive Officer is [________________]"
    mapping: "[ROLE:company.ceo.display_name]"
    
  - location: "§2.2 - CEO address"
    current: "with an address at [________________]."
    mapping: "[ROLE:company.ceo.address.full]"
    
  - location: "§2.3 - CTO name"
    current: "The [TERM:CTO] Chief Technology Officer is [________________]"
    mapping: "[ROLE:company.cto.display_name]"
    
  - location: "§2.3 - CTO address"
    current: "with an address at [________________]."
    mapping: "[ROLE:company.cto.address.full]"
    
  - location: "§2.4 - CMO name"
    current: "The [TERM:CMO] Chief Marketing Officer is [________________]"
    mapping: "[ROLE:company.cmo.display_name]"
    
  - location: "§2.4 - CMO address"
    current: "with an address at [________________]."
    mapping: "[ROLE:company.cmo.address.full]"
    
  - location: "§2.5 - CFO name"
    current: "The [TERM:CFO] Chief Financial Officer is [________________]"
    mapping: "[ROLE:company.cfo.display_name]"
    
  - location: "§2.5 - CFO address"
    current: "with an address at [________________]."
    mapping: "[ROLE:company.cfo.address.full]"
    
  - location: "§2.6 - CCO name"
    current: "Officer, who also serves as the BSA/AML Officer, is [________________]"
    mapping: "[ROLE:company.cco.display_name]"
    
  - location: "§2.6 - CCO address"
    current: "with an address at [________________]."
    mapping: "[ROLE:company.cco.address.full]"
    
  - location: "§4.2.1 - Contract threshold"
    current: "exceeding [________________] dollars"
    mapping: "[CONFIG:thresholds.contract_approval]"
    type: config
    
  - location: "§4.2.2 - Hiring threshold"
    current: "exceeding [________________] dollars"
    mapping: "[CONFIG:thresholds.hiring_approval]"
    type: config
    
  - location: "§4.2.3 - CapEx threshold"
    current: "exceeding [________________] dollars"
    mapping: "[CONFIG:thresholds.capex_approval]"
    type: config
    
  - location: "§5.1.1 - CEO salary"
    current: "salary of [________________] dollars"
    mapping: "[CONFIG:compensation.ceo_salary]"
    type: config
    
  - location: "§5.1.2 - CTO salary"
    current: "salary of [________________] dollars"
    mapping: "[CONFIG:compensation.cto_salary]"
    type: config
    
  - location: "§5.1.3 - CMO salary"
    current: "salary of [________________] dollars"
    mapping: "[CONFIG:compensation.cmo_salary]"
    type: config
    
  - location: "§5.1.4 - CFO salary"
    current: "salary of [________________] dollars"
    mapping: "[CONFIG:compensation.cfo_salary]"
    type: config
    
  - location: "§5.1.5 - CCO salary"
    current: "salary of [________________] dollars"
    mapping: "[CONFIG:compensation.cco_salary]"
    type: config
    
  - location: "Signature - Manager"
    current: "Printed Name: [________________]"
    mapping: "[ROLE:company.manager.display_name]"
    
  - location: "Signature - CEO"
    current: "Printed Name: [________________]"
    mapping: "[ROLE:company.ceo.display_name]"
    
  - location: "Signature - CCO"
    current: "Printed Name: [________________]"
    mapping: "[ROLE:company.cco.display_name]"
```

---

### B3 - Officer Rotation Succession Policy

```yaml
document: B3
path: "Company/Governance/B3_Officer_Rotation_Succession_Policy.md"

fields:
  - location: "Signature"
    current: "Printed Name: [________________]"
    mapping: "[ROLE:company.manager.display_name]"
```

---

### B7 - Acceptable Client Use Policy

```yaml
document: B7
path: "Company/Compliance/B7_Acceptable_Client_Use_Policy.md"

fields:
  - location: "Signature"
    current: "Printed Name: [________________]"
    mapping: "[ROLE:company.cco.display_name]"
```

---

### B10 - Insurance and Capital Policy

```yaml
document: B10
path: "Company/Governance/B10_Insurance_and_Capital_Policy.md"

fields:
  - location: "Signature"
    current: "Printed Name: [________________]"
    mapping: "[ROLE:company.manager.display_name]"
```

---

### A2 - Exhibit A Series List

```yaml
document: A2
path: "Client_Series/Formation/A2_Exhibit_A_Series_List.md"

fields:
  - location: "§2.2.3 - P-1 member"
    current: "initial member of this series is [________________]"
    mapping: "[ROLE:P-1.manager.display_name]"
    
  - location: "§2.3.3 - T-1 member"
    current: "initial member of this series is [________________]"
    mapping: "[ROLE:T-1.manager.display_name]"
    
  - location: "§2.4.3 - T-2 member"
    current: "initial member of this series is [________________]"
    mapping: "[ROLE:T-2.manager.display_name]"
    
  # ... continues for each series
```

---

### C1 - ABN Registration CCASH

```yaml
document: C1
path: "Internal/Registration/C1_ABN_Registration_CCASH.md"

fields:
  - location: "§3.4 - Business address"
    current: "[________________], [City], [State] [ZIP]"
    mapping: "[CONFIG:company.business_address]"
    type: config
    
  - location: "Signature - Name"
    current: "Printed Name: [________________]"
    mapping: "[ROLE:company.ceo.display_name]"
    
  - location: "Signature - Title"
    current: "Title: [TERM:Officer] [________________]"
    mapping: "[ROLE:company.ceo.title]"
    
  - location: "§5.1 - Phone"
    current: "telephone number is [________________]"
    mapping: "[CONFIG:company.phone]"
    type: config
    
  - location: "§5.2 - Email"
    current: "email address is [________________]"
    mapping: "[CONFIG:company.email]"
    type: config
```

---

### D1 - Articles of Amendment

```yaml
document: D1
path: "Client_Series/Formation/D1_Articles_of_Amendment_Add_Series.md"

fields:
  - location: "§1.2 - Entity ID"
    current: "entity ID number from the Montana Secretary of State is [________________]"
    mapping: "[CONFIG:company.mt_entity_id]"
    type: config
    
  - location: "Signature - Name"
    current: "Printed Name: [________________]"
    mapping: "[ROLE:company.manager.display_name]"
    
  - location: "Signature - Title"
    current: "Title: [________________]"
    mapping: "[ROLE:company.manager.title]"
    default: "Manager"
    
  - location: "§6.1 - Phone"
    current: "telephone number is [________________]"
    mapping: "[CONFIG:company.phone]"
    type: config
    
  - location: "§6.2 - Email"
    current: "email address is [________________]"
    mapping: "[CONFIG:company.email]"
    type: config
```

---

### F1 - Client Services Agreement

```yaml
document: F1
path: "Client_Series/Client/F1_Client_Services_Agreement.md"

fields:
  - location: "Signature - Company representative"
    current: "Printed Name: [________________]"
    mapping: "[ROLE:company.ceo.display_name]"
    
  # Client fields filled per-client from client intake
```

---

### N1 - Partner MSB Agreement

```yaml
document: N1
path: "Client_Series/Schedule/N1_Partner_MSB_Agreement.md"

fields:
  - location: "Agreement Date"
    current: "**Agreement Date:** [________________], 20___"
    mapping: "[TRANSACTION:agreement_date]"
    type: transaction
    
  - location: "Effective Date"
    current: "**Effective Date:** [________________], 20___"
    mapping: "[TRANSACTION:effective_date]"
    type: transaction
    
  # Fee schedule fields are per-partner configuration
```

---

## Configuration Fields

Non-person data that also needs centralization:

```yaml
config:
  company:
    business_address: "[________________]"
    phone: "[________________]"
    email: "[________________]"
    mt_entity_id: "[________________]"
    
  thresholds:
    contract_approval: "[________________]"    # Dollars
    hiring_approval: "[________________]"      # Dollars  
    capex_approval: "[________________]"       # Dollars
    
  compensation:
    ceo_salary: "[________________]"
    cto_salary: "[________________]"
    cmo_salary: "[________________]"
    cfo_salary: "[________________]"
    cco_salary: "[________________]"
```

---

## Populate Command Usage

```bash
# Preview what would be populated (dry run)
ccash-validate populate --dry-run

# Populate all documents
ccash-validate populate --all

# Populate specific document
ccash-validate populate B1

# Populate only person fields (skip config)
ccash-validate populate --all --only persons

# Show mapping for a document
ccash-validate mappings B2
```

---

## Validation Rules

```yaml
rules:
  - id: FIELD-001
    description: "All [ROLE:*] markers must resolve to assigned person"
    severity: ERROR
    
  - id: FIELD-002
    description: "All [PERSON:*] markers must exist in registry"
    severity: ERROR
    
  - id: FIELD-003
    description: "All [CONFIG:*] markers must have value in config"
    severity: ERROR
    
  - id: FIELD-004
    description: "Unfilled [________________] should be replaced with markers"
    severity: WARNING
```

---

## Change History

| Date | Change | Author |
|------|--------|--------|
| 2025-12-15 | Initial field mappings created | Schema System |

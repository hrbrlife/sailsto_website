# Person Registry

> **Purpose**: Central registry of all persons who hold roles in CCASH entities.
> Update person data HERE, then populate documents automatically.

---

## Registry Summary

| Person ID | Name | Primary Role | Status |
|-----------|------|--------------|--------|
| P001 | Marcus Chen | Manager/CEO | Active |
| P002 | Sarah Okonkwo | CCO/BSA Officer | Active |
| P003 | David Park | CTO | Active |
| P004 | Elena Rodriguez | CFO | Active |
| RA001 | Northwest Registered Agent LLC | Registered Agent | Active |

---

## Person Records

### P001 - Marcus Chen

```yaml
person_id: P001
type: individual
status: active
effective_date: "2025-01-01"

legal_name:
  first: "Marcus"
  middle: "Wei"
  last: "Chen"
  suffix: null
display_name: "Marcus W. Chen"

address:
  street1: "742 Startup Avenue"
  street2: "Unit 12B"
  city: "Bozeman"
  state: "MT"
  zip: "59715"
  country: "USA"
address_formatted: "742 Startup Avenue, Unit 12B, Bozeman, MT 59715"

phone: "+1-406-555-0101"
email: "marcus.chen@ccash.io"

signature_block:
  name_line: "Marcus W. Chen"

compliance:
  date_of_birth: "1985-06-15"
  citizenship: "US"
  background_check_date: "2024-11-15"
  fit_proper_cleared: true

notes: "Founder. Serves as Manager, sole Member, and CEO."
```

---

### P002 - Sarah Okonkwo

```yaml
person_id: P002
type: individual
status: active
effective_date: "2025-01-01"

legal_name:
  first: "Sarah"
  middle: "Adaeze"
  last: "Okonkwo"
  suffix: null
display_name: "Sarah A. Okonkwo"

address:
  street1: "1890 Compliance Way"
  street2: null
  city: "Helena"
  state: "MT"
  zip: "59601"
  country: "USA"
address_formatted: "1890 Compliance Way, Helena, MT 59601"

phone: "+1-406-555-0102"
email: "sarah.okonkwo@ccash.io"

signature_block:
  name_line: "Sarah A. Okonkwo"

compliance:
  date_of_birth: "1982-03-22"
  citizenship: "US"
  background_check_date: "2024-11-20"
  fit_proper_cleared: true
  certifications:
    - "CAMS (Certified Anti-Money Laundering Specialist)"
    - "CFE (Certified Fraud Examiner)"

notes: "CCO and BSA/AML Officer. 12 years compliance experience in financial services. Independent from revenue functions."
```

---

### P003 - David Park

```yaml
person_id: P003
type: individual
status: active
effective_date: "2025-01-01"

legal_name:
  first: "David"
  middle: "Joon"
  last: "Park"
  suffix: null
display_name: "David J. Park"

address:
  street1: "456 Tech Center Drive"
  street2: "Suite 300"
  city: "Missoula"
  state: "MT"
  zip: "59801"
  country: "USA"
address_formatted: "456 Tech Center Drive, Suite 300, Missoula, MT 59801"

phone: "+1-406-555-0103"
email: "david.park@ccash.io"

signature_block:
  name_line: "David J. Park"

compliance:
  date_of_birth: "1988-11-08"
  citizenship: "US"
  background_check_date: "2024-11-18"
  fit_proper_cleared: true

notes: "CTO. Co-founder. 10 years experience in fintech infrastructure and payments."
```

---

### P004 - Elena Rodriguez

```yaml
person_id: P004
type: individual
status: active
effective_date: "2025-01-01"

legal_name:
  first: "Elena"
  middle: "Maria"
  last: "Rodriguez"
  suffix: "CPA"
display_name: "Elena M. Rodriguez, CPA"

address:
  street1: "2100 Financial Plaza"
  street2: "Floor 4"
  city: "Billings"
  state: "MT"
  zip: "59101"
  country: "USA"
address_formatted: "2100 Financial Plaza, Floor 4, Billings, MT 59101"

phone: "+1-406-555-0104"
email: "elena.rodriguez@ccash.io"

signature_block:
  name_line: "Elena M. Rodriguez, CPA"

compliance:
  date_of_birth: "1979-09-30"
  citizenship: "US"
  background_check_date: "2024-11-22"
  fit_proper_cleared: true
  certifications:
    - "CPA (Montana License #12345)"

notes: "CFO. 15 years experience in financial management, previously at regional bank."
```

---

### RA001 - Northwest Registered Agent LLC

```yaml
person_id: RA001
type: entity
status: active
effective_date: "2025-01-01"

entity_name: "Northwest Registered Agent LLC"
display_name: "Northwest Registered Agent LLC"

address:
  street1: "1900 Prospect Avenue"
  street2: null
  city: "Helena"
  state: "MT"
  zip: "59601"
  country: "USA"
address_formatted: "1900 Prospect Avenue, Helena, MT 59601"

phone: "+1-406-442-9000"
email: "montana@northwestregisteredagent.com"

registered_agent_type: commercial
service_account: "CCASH-2025-001"

notes: "Commercial registered agent. Serves as RA for Company and all Series."
```

---

## Data Fields Reference

### Computed Fields

| Field | Computation |
|-------|-------------|
| `address_formatted` | `street1, street2, city, state zip` |
| `signature_with_title` | `name_line` + role title |

### Required Fields by Context

| Context | Required Fields |
|---------|----------------|
| Any signature | `display_name` |
| Formation docs | `display_name`, `address_formatted` |
| Officer appointment | `display_name`, `address_formatted` |
| BSA/FinCEN filing | `legal_name.*`, `address.*`, `date_of_birth` |
| Contact section | `phone`, `email` |
| Registered Agent | `entity_name` OR `display_name`, `address` (Montana) |

---

## Validation Status

| Person | Required Fields | Compliance | Status |
|--------|-----------------|------------|--------|
| P001 | ✓ Complete | ✓ Cleared | Ready |
| P002 | ✓ Complete | ✓ Cleared | Ready |
| P003 | ✓ Complete | ✓ Cleared | Ready |
| P004 | ✓ Complete | ✓ Cleared | Ready |
| RA001 | ✓ Complete | N/A | Ready |

---

## Change History

| Date | Change | Author |
|------|--------|--------|
| 2025-12-15 | Initial person registry with mock data | Schema System |

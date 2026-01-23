# Entity Role Configuration

> **Purpose**: Flexible configuration system for entity roles.
> Defines minimums for compliance, but allows any structure beyond that.

---

## Design Philosophy

1. **Compliance Minimums** - Only enforce what's legally required
2. **Business Flexibility** - Everything else is optional configuration
3. **Inheritance Optional** - Series MAY inherit, not MUST inherit
4. **Custom Roles** - Allow roles not in the standard list

---

## Compliance Minimums (Hard Rules)

These are the ONLY hard requirements - everything else is flexible:

```yaml
compliance_minimums:
  # Montana LLC statutory requirements
  montana_llc:
    - role: registered_agent
      requirement: "Montana Code Ann. § 35-8-205"
      applies_to: [company, all_series]
      
    - role: organizer
      requirement: "Montana Code Ann. § 35-8-201"
      applies_to: [company]
      lifecycle: formation_only
      
  # FinCEN MSB requirements  
  fincen_msb:
    - role: bsa_officer
      requirement: "31 CFR § 1022.210"
      applies_to: [any_entity_with_fincen_registration]
      notes: "Each MSB must designate a compliance officer"
      
  # Independence requirements
  bsa_independence:
    - rule: "BSA Officer cannot also be CEO or CFO"
      check: "bsa_officer != ceo AND bsa_officer != cfo"
      severity: ERROR
      notes: "BSA officer must have independence from revenue functions"
```

---

## Entity Type Definitions

### company

```yaml
entity_type: company
description: "The parent Series LLC"

# Statutory minimum
statutory_roles:
  - registered_agent      # Required by Montana law
  - organizer            # Required for formation (then done)

# Governance minimum  
governance_roles:
  - manager              # At least one required for LLC
  - member               # At least one required for LLC

# Everything else is YOUR CHOICE
# The system tracks what you configure, not what you must have
```

### series

```yaml
entity_type: series
subtypes:
  - protected_series     # P-x, T-x series
  - client_series        # C-xxx series

# Statutory minimum
statutory_roles:
  - registered_agent     # Can share with company or have own

# Series-specific
# A series is a "series" of the LLC - it can have:
# - Its own managers (or inherit from company)
# - Its own officers (or none, relying on company)
# - Its own members (or company is sole member)

# CLIENT SERIES SPECIAL RULE:
# If a client series has its own FinCEN MSB registration,
# it MUST have its own BSA Officer (cannot use company's)
```

---

## Role Configuration Schema

Instead of templates, use a **configuration file** per entity:

```yaml
# Example: _config/entities/company.yaml
entity_id: company
entity_name: "CCASH MONEY SERVICES (US) SERIES LLC"
entity_type: company

# Configure the roles YOU want - not a template
roles:
  manager:
    enabled: true
    persons: [P001]
    
  member:
    enabled: true
    persons: [P001]
    ownership:
      P001: 100%
      
  registered_agent:
    enabled: true
    persons: [RA001]
    
  # Officer roles - configure what you need
  officers:
    ceo:
      enabled: true
      persons: [P001]
      
    cco:
      enabled: true
      persons: [P002]
      also_serves_as: [bsa_officer]
      
    cto:
      enabled: true
      persons: [P003]
      
    cfo:
      enabled: true
      persons: [P004]
      
    cmo:
      enabled: false        # Not using this role yet
      persons: []
      
    # Add ANY custom role
    head_of_partnerships:
      enabled: true
      persons: [P005]
      custom: true          # Not a standard role
```

---

## Series Configuration Examples

### Minimal Protected Series (Inherits Everything)

```yaml
# _config/entities/P-1.yaml
entity_id: P-1
entity_name: "Series P-1"
entity_type: protected_series

inheritance:
  from: company
  inherit_all: true        # Just inherit everything
  
# No additional configuration needed
# P-1 uses all company officers
```

### Protected Series with Own Officers

```yaml
# _config/entities/T-4.yaml
entity_id: T-4
entity_name: "Series T-4 (Technology)"
entity_type: protected_series

inheritance:
  from: company
  inherit: [manager, registered_agent]  # Only inherit these
  
roles:
  # Series has its own CTO
  cto:
    enabled: true
    persons: [P006]        # Different from company CTO
    
  # Custom role for this series
  platform_architect:
    enabled: true
    persons: [P007]
    custom: true
```

### Client Series (Independent MSB)

```yaml
# _config/entities/C-001.yaml
entity_id: C-001
entity_name: "Series C-001"
entity_type: client_series
client_name: "Acme Payments Inc."

# Client series are INDEPENDENT - no automatic inheritance
inheritance:
  from: null               # No inheritance by default
  
# Can optionally share registered agent
shared_roles:
  registered_agent:
    shared_with: company
    person: RA001
    
# Client must provide their own
roles:
  manager:
    enabled: true
    persons: [CLIENT-001-MGR]
    source: client
    
  bsa_officer:
    enabled: true
    persons: [CLIENT-001-BSA]
    source: client
    fincen_designated: true
    
  # Client can add any roles they want
  cfo:
    enabled: true
    persons: [CLIENT-001-CFO]
    source: client
```

### Single-Person LLC (Everything One Person)

```yaml
# Example: Single founder does everything
entity_id: company
entity_name: "Solo MSB LLC"
entity_type: company

roles:
  manager:
    enabled: true
    persons: [P001]
    
  member:
    enabled: true
    persons: [P001]
    
  registered_agent:
    enabled: true
    persons: [RA001]       # Must be separate (can't serve self)
    
  officers:
    # One person wears all hats EXCEPT compliance
    ceo:
      enabled: true
      persons: [P001]
      
    cto:
      enabled: true
      persons: [P001]      # Same person
      
    cfo:
      enabled: true
      persons: [P001]      # Same person
      
    # CCO/BSA MUST be different for independence
    cco:
      enabled: true
      persons: [P002]      # Different person required
      also_serves_as: [bsa_officer]
```

---

## Validation Rules

The system validates against compliance minimums, not templates:

```yaml
validation:
  # ERRORS - Must fix
  errors:
    - id: ENTITY-ERR-001
      rule: "Entity must have registered agent"
      check: entity.has_role(registered_agent)
      
    - id: ENTITY-ERR-002
      rule: "Entity with FinCEN registration must have BSA Officer"
      check: IF entity.has_fincen THEN entity.has_role(bsa_officer)
      
    - id: ENTITY-ERR-003
      rule: "BSA Officer must be independent"
      check: entity.bsa_officer NOT IN [entity.ceo, entity.cfo]
      
    - id: ENTITY-ERR-004
      rule: "LLC must have at least one manager"
      check: entity.has_role(manager)
      
    - id: ENTITY-ERR-005
      rule: "LLC must have at least one member"
      check: entity.has_role(member)
      
  # WARNINGS - Should review
  warnings:
    - id: ENTITY-WARN-001
      rule: "Consider having separate CCO for compliance independence"
      check: entity.cco != entity.ceo
      severity: WARNING
      
    - id: ENTITY-WARN-002
      rule: "Client series should have documented roles"
      check: client_series.roles.count > 2
      severity: INFO
```

---

## Role Combination Matrix

What's ALLOWED (not what's required):

```yaml
combinations:
  # One person CAN hold multiple roles (except where prohibited)
  allowed:
    - [manager, member]           # Very common
    - [manager, ceo]              # Common in small LLC
    - [ceo, cto]                  # Founder wears both hats
    - [ceo, cmo]                  # Founder wears both hats
    - [cfo, treasurer]            # Natural combination
    - [cco, privacy_officer]      # Natural combination
    - [cco, bsa_officer]          # Very common
    - [secretary, any_officer]    # Often combined
    
  # Prohibited combinations (compliance/independence)
  prohibited:
    - [cco, ceo]                  # Independence
    - [cco, cfo]                  # Independence
    - [bsa_officer, ceo]          # BSA independence
    - [bsa_officer, cfo]          # BSA independence
    - [registered_agent, self]    # Can't be own RA (if individual)
```

---

## Custom Roles

You can define any custom role:

```yaml
custom_roles:
  # Just add to your entity config
  head_of_partnerships:
    title: "Head of Partnerships"
    category: officer
    reports_to: ceo
    signature_authority: true
    
  compliance_analyst:
    title: "Compliance Analyst"
    category: staff
    reports_to: cco
    signature_authority: false
    
  series_coordinator:
    title: "Series Coordinator"
    category: operations
    reports_to: manager
    signature_authority: false
```

---

## Migration from Templates

Old approach (rigid):
```yaml
# "Company MUST have CEO, CTO, CFO, CCO"
required: [ceo, cto, cfo, cco]
```

New approach (flexible):
```yaml
# "Company must have manager + member + RA (statutory)"
# "Company with FinCEN must have BSA Officer (compliance)"
# "Everything else: configure what YOU need"
statutory: [manager, member, registered_agent]
compliance: [bsa_officer]  # If FinCEN registered
business: [configure_your_own]
```

---

## Summary

| Aspect | Old (Templates) | New (Configuration) |
|--------|-----------------|---------------------|
| Structure | Predefined | User-defined |
| Required roles | Many | Statutory minimum only |
| Optional roles | Listed | Unlimited |
| Custom roles | Not supported | Fully supported |
| Inheritance | Forced | Optional |
| Validation | Template match | Compliance check |

---

## Change History

| Date | Change | Author |
|------|--------|--------|
| 2025-12-15 | Initial template system | Schema System |
| 2025-12-15 | Redesigned as flexible configuration | Schema System |

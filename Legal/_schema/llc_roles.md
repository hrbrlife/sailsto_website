# LLC Role Types Registry

> **Purpose**: Defines all possible roles in the LLC and Series structure.
> These are the positions that can be assigned to persons.

---

## Statistics

| Category | Count |
|----------|-------|
| Governance Roles | 3 |
| Officer Roles | 7 |
| Compliance Roles | 3 |
| External Roles | 2 |
| **Total** | **15** |

---

## Role Categories

### Governance Roles

Roles with fundamental control over the entity.

#### manager
```yaml
role_id: manager
title: "Manager"
abbreviation: null
category: governance
description: "Primary governing authority of the LLC or Series"
authority:
  - "Full management authority"
  - "Appoint and remove officers"
  - "Approve material contracts"
  - "Admit and remove members"
statutory_basis: "Montana Code Ann. § 35-8-401"
bsa_related: false
signature_authority: true
required_for:
  - company
  - protected_series
  - client_series
```

#### member
```yaml
role_id: member
title: "Member"
abbreviation: null
category: governance
description: "Equity owner of the LLC or Series"
authority:
  - "Voting rights per operating agreement"
  - "Distributions per operating agreement"
  - "Approve fundamental changes"
statutory_basis: "Montana Code Ann. § 35-8-301"
bsa_related: false
signature_authority: false
required_for:
  - company
  - protected_series
optional_for:
  - client_series
```

#### organizer
```yaml
role_id: organizer
title: "Organizer"
abbreviation: null
category: governance
description: "Person who files formation documents"
authority:
  - "Sign and file articles of organization"
  - "Execute initial organizational actions"
statutory_basis: "Montana Code Ann. § 35-8-201"
bsa_related: false
signature_authority: true
lifecycle: formation_only
required_for:
  - company
notes: "Role terminates after formation complete"
```

---

### Officer Roles

Executive positions appointed by the Manager.

#### ceo
```yaml
role_id: ceo
title: "Chief Executive Officer"
abbreviation: "CEO"
category: officer
description: "Principal executive officer responsible for overall operations"
authority:
  - "Day-to-day management"
  - "Execute contracts within limits"
  - "Supervise other officers"
  - "Represent company externally"
reports_to: manager
bsa_related: false
signature_authority: true
required_for:
  - company
optional_for:
  - protected_series
```

#### cto
```yaml
role_id: cto
title: "Chief Technology Officer"
abbreviation: "CTO"
category: officer
description: "Principal technology officer responsible for technology strategy and operations"
authority:
  - "Technology strategy and architecture"
  - "IT vendor selection within limits"
  - "Security oversight"
  - "Development team management"
reports_to: ceo
bsa_related: false
signature_authority: true
required_for:
  - company
optional_for:
  - protected_series
```

#### cmo
```yaml
role_id: cmo
title: "Chief Marketing Officer"
abbreviation: "CMO"
category: officer
description: "Principal marketing officer responsible for marketing and growth"
authority:
  - "Marketing strategy"
  - "Brand management"
  - "Customer acquisition"
  - "Marketing vendor selection within limits"
reports_to: ceo
bsa_related: false
signature_authority: true
optional_for:
  - company
  - protected_series
```

#### cfo
```yaml
role_id: cfo
title: "Chief Financial Officer"
abbreviation: "CFO"
category: officer
description: "Principal financial officer responsible for financial management"
authority:
  - "Financial reporting"
  - "Treasury management"
  - "Budgeting and forecasting"
  - "Banking relationships"
reports_to: ceo
bsa_related: true
signature_authority: true
required_for:
  - company
optional_for:
  - protected_series
```

#### cco
```yaml
role_id: cco
title: "Chief Compliance Officer"
abbreviation: "CCO"
category: officer
description: "Principal compliance officer and BSA/AML Officer"
authority:
  - "Compliance program design and enforcement"
  - "SAR filing decisions"
  - "Relationship terminations for compliance"
  - "Regulatory engagement"
  - "Independent escalation to Manager"
reports_to: manager  # Direct report for independence
bsa_related: true
bsa_role: "BSA/AML Officer"
signature_authority: true
required_for:
  - company
cannot_combine_with:
  - ceo
  - cfo
notes: "Must be independent; cannot be combined with revenue-generating roles"
```

#### secretary
```yaml
role_id: secretary
title: "Secretary"
abbreviation: null
category: officer
description: "Corporate secretary responsible for records and governance"
authority:
  - "Maintain corporate records"
  - "Certify documents"
  - "Meeting minutes"
  - "Registered agent liaison"
reports_to: ceo
bsa_related: false
signature_authority: true
optional_for:
  - company
  - protected_series
```

#### treasurer
```yaml
role_id: treasurer
title: "Treasurer"
abbreviation: null
category: officer
description: "Treasury officer responsible for funds management"
authority:
  - "Cash management"
  - "Payment processing oversight"
  - "Banking operations"
reports_to: cfo
bsa_related: true
signature_authority: true
optional_for:
  - company
  - protected_series
```

---

### Compliance Roles

Specialized compliance positions.

#### bsa_officer
```yaml
role_id: bsa_officer
title: "BSA/AML Officer"
abbreviation: null
category: compliance
description: "Designated BSA/AML compliance officer for FinCEN"
authority:
  - "BSA/AML program design and enforcement"
  - "SAR filing authority"
  - "FinCEN registration and renewal"
  - "Independent escalation"
reports_to: manager
bsa_related: true
fincen_designated: true
signature_authority: true
required_for:
  - company
  - client_series
notes: "Often combined with CCO role at company level; Client Series must designate own BSA Officer"
```

#### ofac_contact
```yaml
role_id: ofac_contact
title: "OFAC Contact"
abbreviation: null
category: compliance
description: "Primary contact for OFAC sanctions compliance"
authority:
  - "Sanctions screening oversight"
  - "OFAC reporting"
  - "Blocked property handling"
reports_to: cco
bsa_related: true
signature_authority: false
optional_for:
  - company
```

#### privacy_officer
```yaml
role_id: privacy_officer
title: "Privacy Officer"
abbreviation: null
category: compliance
description: "Data protection and privacy compliance officer"
authority:
  - "Privacy program oversight"
  - "Data subject request handling"
  - "Breach notification decisions"
reports_to: cco
bsa_related: false
signature_authority: false
optional_for:
  - company
```

---

### External Roles

Third-party positions.

#### registered_agent
```yaml
role_id: registered_agent
title: "Registered Agent"
abbreviation: "RA"
category: external
description: "Statutory agent for service of process"
authority:
  - "Accept service of process"
  - "Forward official correspondence"
statutory_basis: "Montana Code Ann. § 35-8-205"
bsa_related: false
signature_authority: false
required_for:
  - company
  - protected_series
  - client_series
types:
  - individual: "Natural person with Montana address"
  - commercial: "Commercial registered agent service"
```

#### external_auditor
```yaml
role_id: external_auditor
title: "External Auditor"
abbreviation: null
category: external
description: "Independent auditor for financial or compliance audits"
authority:
  - "Access to books and records"
  - "Interview personnel"
  - "Issue audit reports"
bsa_related: false
signature_authority: false
optional_for:
  - company
engagement_basis: "Contract or regulatory requirement"
```

---

## Role Combinations

### Permitted Combinations

| Primary Role | May Also Hold |
|--------------|---------------|
| CEO | CTO, CMO, Secretary |
| CFO | Treasurer |
| Manager | Any officer role (small LLC) |
| Member | Any officer role |

### Prohibited Combinations

| Role A | Role B | Reason |
|--------|--------|--------|
| CCO | CEO | Independence requirement |
| CCO | CFO | Independence requirement |
| CCO | Treasurer | Independence requirement |
| BSA Officer | CEO | BSA independence |
| BSA Officer | CFO | BSA independence |

---

## Role Lifecycle States

```yaml
states:
  - appointed: "Currently holding the role"
  - resigned: "Voluntarily left the role"
  - removed: "Removed by Manager action"
  - succeeded: "Replaced through succession process"
  - interim: "Temporary appointment pending permanent"
  - suspended: "Temporarily unable to perform duties"
```

---

## Validation Rules

```yaml
rules:
  - id: ROLE-001
    description: "Company must have Manager"
    check: company.has_role(manager)
    severity: ERROR
    
  - id: ROLE-002
    description: "Company must have CCO"
    check: company.has_role(cco)
    severity: ERROR
    
  - id: ROLE-003
    description: "CCO must not be CEO or CFO"
    check: not (person.has_role(cco) and person.has_role(ceo, cfo))
    severity: ERROR
    
  - id: ROLE-004
    description: "Client Series must have BSA Officer"
    check: client_series.has_role(bsa_officer)
    severity: ERROR
    
  - id: ROLE-005
    description: "All entities must have Registered Agent"
    check: entity.has_role(registered_agent)
    severity: ERROR
```

---

## Document Cross-Reference

Which documents reference which roles:

| Role | Documents |
|------|-----------|
| manager | B1, B2, A1, A2, A3 |
| member | B1, A2, A3 |
| organizer | A1, E1 |
| ceo | B1, B2, B3 |
| cto | B1, B2, B3 |
| cmo | B1, B2, B3 |
| cfo | B1, B2, B3, B10 |
| cco | B1, B2, B3, B5, B7, B8, B9 |
| bsa_officer | B5, N5, E1 |
| registered_agent | A1, E1 |

---

## Change History

| Date | Change | Author |
|------|--------|--------|
| 2025-12-15 | Initial role registry created | Schema System |

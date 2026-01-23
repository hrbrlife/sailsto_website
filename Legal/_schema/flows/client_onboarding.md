# Client Onboarding Flow

> **Flow ID**: `client_onboarding`
> **Owner**: CCO
> **Trigger**: Prospective client inquiry qualified by sales
> **SLA**: 30 business days from CSA execution to ACTIVE status

---

## State Diagram

```
┌─────────┐
│  START  │
└────┬────┘
     │ Sales qualified
     ▼
┌─────────────────┐
│  INQUIRY        │ ←──────────────────────────────────────┐
│  (Initial)      │                                         │
└────┬────────────┘                                         │
     │ KYB documents received                               │
     ▼                                                      │
┌─────────────────┐     KYB fails                          │
│  KYB_REVIEW     │ ─────────────────────────────────────→ │
│  (P-1 Series)   │                                         │
└────┬────────────┘                                         │
     │ KYB approved                                         │
     ▼                                                      │
┌─────────────────┐                                         │
│  CSA_NEGOTIATION│                                         │
│  (Legal)        │                                         │
└────┬────────────┘                                         │
     │ CSA signed by both parties                           │
     ▼                                                      │
┌─────────────────┐                                         │
│  CSA_EXECUTED   │◄── Series code assigned (C-XXX)        │
│  (Milestone 1)  │                                         │
└────┬────────────┘                                         │
     │ Onboarding fee paid                                  │
     ▼                                                      │
┌─────────────────┐                                         │
│  EIN_PENDING    │                                         │
│  (Client task)  │                                         │
└────┬────────────┘                                         │
     │ Client provides EIN                                  │
     ▼                                                      │
┌─────────────────┐                                         │
│  FINCEN_PENDING │                                         │
│  (Client task)  │                                         │
└────┬────────────┘                                         │
     │ Client provides FinCEN registration                  │
     ▼                                                      │
┌─────────────────┐                                         │
│  FINCEN_VERIFIED│◄── Company verifies registration       │
│  (Milestone 2)  │                                         │
└────┬────────────┘                                         │
     │ Amendment filed with SOS                             │
     ▼                                                      │
┌─────────────────┐                                         │
│  SOS_PENDING    │                                         │
│  (Amendment)    │                                         │
└────┬────────────┘                                         │
     │ Amendment approved, ABN filed                        │
     ▼                                                      │
┌─────────────────┐                                         │
│  TRAINING       │                                         │
│  (Client team)  │                                         │
└────┬────────────┘                                         │
     │ Training complete, training fee paid                 │
     ▼                                                      │
┌─────────────────┐                                         │
│  INTEGRATION    │                                         │
│  (Technical)    │                                         │
└────┬────────────┘                                         │
     │ API integration tested                               │
     ▼                                                      │
┌─────────────────┐                                         │
│  COMPLIANCE_    │                                         │
│  REVIEW         │                                         │
│  (Final check)  │                                         │
└────┬────────────┘                                         │
     │ All checks passed                                    │
     ▼                                                      │
┌─────────────────┐                                         │
│  ACTIVE         │ ◄── Client can transact                │
│  (Terminal)     │                                         │
└─────────────────┘                                         │
                                                            │
┌─────────────────┐                                         │
│  REJECTED       │ ◄───────────────────────────────────────┘
│  (Terminal)     │     (KYB fail, compliance concern,
└─────────────────┘      client withdrawal)

┌─────────────────┐
│  SUSPENDED      │ ◄── From ACTIVE (compliance issue)
│  (Reversible)   │ ──→ Back to ACTIVE (issue resolved)
└─────────────────┘     or to TERMINATED
         │
         ▼
┌─────────────────┐
│  TERMINATED     │ ◄── From ACTIVE or SUSPENDED
│  (Terminal)     │
└─────────────────┘
```

---

## State Definitions

| State | Description | Entry Condition | Max Duration | Responsible |
|-------|-------------|-----------------|--------------|-------------|
| `START` | Flow initiation | - | - | - |
| `INQUIRY` | Initial contact, pre-qualification | Sales qualification | 5 days | Sales |
| `KYB_REVIEW` | KYC/KYB due diligence via P-1 | Documents received | 10 days | CCO |
| `CSA_NEGOTIATION` | Contract negotiation | KYB approved | 15 days | GC |
| `CSA_EXECUTED` | **Milestone 1**: Contract signed | Both parties sign | 1 day | Operations |
| `EIN_PENDING` | Awaiting client EIN | Onboarding fee paid | 5 days | Client |
| `FINCEN_PENDING` | Awaiting client FinCEN registration | EIN received | 30 days | Client |
| `FINCEN_VERIFIED` | **Milestone 2**: Registration confirmed | Company verification | 2 days | CCO |
| `SOS_PENDING` | Amendment filing in progress | FinCEN verified | 10 days | Operations |
| `TRAINING` | Client team training | SOS approved | 5 days | Operations |
| `INTEGRATION` | Technical integration | Training complete | 10 days | CTO |
| `COMPLIANCE_REVIEW` | Final compliance sign-off | Integration complete | 3 days | CCO |
| `ACTIVE` | **Terminal**: Client operational | All checks pass | - | - |
| `REJECTED` | **Terminal**: Onboarding failed | Various | - | - |
| `SUSPENDED` | Temporary hold (from ACTIVE) | Compliance concern | 30 days | CCO |
| `TERMINATED` | **Terminal**: Relationship ended | Various | - | - |

---

## Transition Rules

| From | To | Trigger | Action | Responsible | Document |
|------|-----|---------|--------|-------------|----------|
| START | INQUIRY | Qualified lead | Create client record | Sales | - |
| INQUIRY | KYB_REVIEW | Docs received | Initiate P-1 review | CCO | B9 |
| INQUIRY | REJECTED | Unqualified | Document reason | Sales | - |
| KYB_REVIEW | CSA_NEGOTIATION | KYB approved | Send CSA draft | GC | F1 |
| KYB_REVIEW | REJECTED | KYB failed | Document reason | CCO | B7, B9 |
| CSA_NEGOTIATION | CSA_EXECUTED | CSA signed | Assign series code | Operations | F1 |
| CSA_EXECUTED | EIN_PENDING | Fee paid | Send EIN instructions | Operations | N5 |
| EIN_PENDING | FINCEN_PENDING | EIN received | Send FinCEN guide | Operations | N5 |
| FINCEN_PENDING | FINCEN_VERIFIED | Reg received | Verify with FinCEN | CCO | N5 |
| FINCEN_VERIFIED | SOS_PENDING | Verified | File D1 amendment | Operations | D1, E1 |
| SOS_PENDING | TRAINING | SOS approved | Schedule training | Operations | B11 |
| TRAINING | INTEGRATION | Training done | Begin API setup | CTO | B6 |
| INTEGRATION | COMPLIANCE_REVIEW | Tests pass | Final review | CCO | B5, B7 |
| COMPLIANCE_REVIEW | ACTIVE | Approved | Enable transactions | CCO | - |
| ACTIVE | SUSPENDED | Issue found | Disable transactions | CCO | B7 |
| SUSPENDED | ACTIVE | Issue resolved | Re-enable | CCO | - |
| SUSPENDED | TERMINATED | Unremediated | Full offboarding | CCO | F1 |
| ACTIVE | TERMINATED | Termination notice | Offboarding process | Operations | F1 |

---

## Timeout Escalations

| State | Timeout | Escalation Action |
|-------|---------|-------------------|
| INQUIRY | 5 days | Auto-close, notify sales |
| KYB_REVIEW | 10 days | Escalate to CCO |
| CSA_NEGOTIATION | 15 days | Escalate to CEO |
| EIN_PENDING | 5 days | Reminder to client |
| FINCEN_PENDING | 30 days | Warning: registration required |
| FINCEN_PENDING | 45 days | Move to REJECTED |
| SOS_PENDING | 10 days | Check with SOS |
| SUSPENDED | 30 days | Review for TERMINATED |

---

## Checklist by State

### CSA_EXECUTED Checklist
- [ ] Client Services Agreement (F1) executed
- [ ] Series code assigned (C-XXX)
- [ ] Onboarding fee received ($10,000)
- [ ] Client record created in system
- [ ] EIN instruction packet sent (N5)

### FINCEN_VERIFIED Checklist
- [ ] Client EIN confirmed with IRS
- [ ] FinCEN registration number received
- [ ] FinCEN registration verified active
- [ ] Client MSB activities match approved scope
- [ ] No SAR/enforcement history found

### ACTIVE Checklist
- [ ] Amendment (D1) filed and approved
- [ ] ABN (C2) filed and approved
- [ ] Training completed and certified
- [ ] API credentials issued
- [ ] Test transactions successful
- [ ] Compliance sign-off documented
- [ ] Welcome packet sent

---

## Document References

| State/Transition | Primary Documents |
|------------------|-------------------|
| KYB_REVIEW | B9 (Screening), B7 (AUP) |
| CSA_NEGOTIATION | F1 (CSA), C3 (Pricing), B11 (Framework) |
| EIN/FINCEN | N5 (Filing Guide), E1 (Checklist) |
| SOS_PENDING | D1 (Amendment), C2 (ABN), E1 (Checklist) |
| TRAINING | B5 (BSA), B6 (IT), B7 (AUP), B11 (Framework) |
| COMPLIANCE_REVIEW | B5, B7, N3 (States) |

---

## MVP Validation for This Flow

```yaml
flow_mvp_conditions:
  - id: FLOW-ONBOARD-001
    name: fincen_before_active
    description: Client cannot reach ACTIVE without verified FinCEN
    check: path_to_ACTIVE MUST_PASS_THROUGH FINCEN_VERIFIED
    severity: ERROR
    
  - id: FLOW-ONBOARD-002
    name: kyb_before_csa
    description: KYB must complete before CSA execution
    check: path_to_CSA_EXECUTED MUST_PASS_THROUGH KYB_REVIEW
    severity: ERROR
    
  - id: FLOW-ONBOARD-003
    name: training_before_active
    description: Training required before going live
    check: path_to_ACTIVE MUST_PASS_THROUGH TRAINING
    severity: ERROR
    
  - id: FLOW-ONBOARD-004
    name: suspended_has_timeout
    description: SUSPENDED state must have resolution deadline
    check: state.SUSPENDED.max_duration <= 30 days
    severity: WARNING
```

---

## Metrics & Reporting

| Metric | Target | Measurement |
|--------|--------|-------------|
| Time to CSA_EXECUTED | < 20 days | From INQUIRY |
| Time to ACTIVE | < 45 days | From CSA_EXECUTED |
| KYB Approval Rate | > 80% | KYB_REVIEW → CSA_NEGOTIATION |
| Onboarding Completion | > 90% | CSA_EXECUTED → ACTIVE |
| FinCEN Compliance | 100% | All ACTIVE have verified FinCEN |

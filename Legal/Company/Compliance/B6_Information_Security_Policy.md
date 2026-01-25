# INFORMATION SECURITY POLICY
# SAILS DAO LLC - CYBERSECURITY AND DATA PROTECTION STANDARDS

**Document Number:** B6-SECURITY-v1.0  
**Effective Date:** [DATE]  
**Classification:** Internal Use Only  
**Related Documents:** [DOC:B1 §8] Operating Agreement - Compliance, [DOC:B8] Privacy Policy, [DOC:B4] Recordkeeping Policy

---

## ARTICLE 1: PURPOSE AND SCOPE

**1.1 Purpose**

This Information Security Policy ("**Policy**") establishes the security framework for Sails DAO LLC ("**Company**") to protect:

- Confidential business information
- Investor personal and financial data
- Platform infrastructure and systems
- Blockchain and smart contract operations
- Regulatory compliance requirements

The Policy implements requirements under:
- Gramm-Leach-Bliley Act (GLBA) Safeguards Rule
- FTC Safeguards Rule (16 CFR Part 314)
- SEC Regulation S-P
- State privacy and security laws
- GDPR (for international data)

**1.2 Scope**

This Policy applies to:

- All information systems and assets
- All employees, contractors, and agents
- All Series Issuers
- All third-party service providers with access to Company systems or data
- All data regardless of format (electronic, paper, verbal)

**1.3 Definitions**

- **Confidential Information:** Non-public information including NPI, business secrets, security configurations
- **Nonpublic Personal Information (NPI):** Any personally identifiable financial information (per GLBA)
- **Information Assets:** Hardware, software, data, networks, facilities supporting information processing
- **Security Incident:** Any event that compromises confidentiality, integrity, or availability of information

---

## ARTICLE 2: GOVERNANCE AND ORGANIZATION

**2.1 Information Security Officer**

**(a) Designation:**

The Company designates an Information Security Officer ("**ISO**") with overall responsibility for security program. For companies with fewer than 20 employees, the ISO may be an officer with additional duties.

**Designated ISO:** [NAME/TITLE]

**(b) ISO Responsibilities:**
- Develop and maintain security policies and procedures
- Conduct risk assessments
- Manage security operations
- Respond to security incidents
- Report to executive management and Board
- Ensure regulatory compliance
- Oversee vendor security
- Conduct training and awareness programs

**2.2 Security Governance**

**(a) Board Oversight:**
- Annual report on security program to Board/Managers
- Immediate notification of material security incidents
- Approval of security policy and risk acceptance decisions

**(b) Executive Management:**
- Allocate resources for security program
- Set risk tolerance
- Review and approve security policies

**(c) Department Heads:**
- Ensure department compliance with security policies
- Report security concerns
- Support security initiatives

**2.3 Security Committee**

Quarterly Security Committee meetings including:
- Information Security Officer
- Chief Compliance Officer
- Chief Technology Officer (if separate)
- Legal Counsel

Agenda items:
- Risk assessment updates
- Incident review
- Compliance status
- Policy updates
- Vendor security

---

## ARTICLE 3: RISK ASSESSMENT

**3.1 Risk Assessment Program**

**(a) Frequency:**
- Comprehensive assessment: Annual minimum
- Targeted assessments: Upon material system changes
- Continuous monitoring: Ongoing

**(b) Methodology:**

Risk assessment covers:
1. **Asset Inventory:** Identify all information assets
2. **Threat Identification:** Internal and external threats
3. **Vulnerability Assessment:** Technical and operational weaknesses
4. **Impact Analysis:** Potential harm from compromise
5. **Likelihood Assessment:** Probability of threat occurrence
6. **Risk Rating:** Combine impact and likelihood
7. **Control Evaluation:** Existing safeguards effectiveness
8. **Residual Risk:** Risk after controls

**(c) Risk Categories:**

| **Category** | **Examples** |
|--------------|-------------|
| Confidentiality | Unauthorized data access, data breach |
| Integrity | Data tampering, unauthorized modification |
| Availability | System downtime, ransomware, DDoS |
| Compliance | Regulatory violations, audit failures |
| Reputational | Negative publicity, loss of trust |
| Financial | Fraud, theft, operational disruption |

**3.2 Risk Treatment**

For identified risks:
- **Mitigate:** Implement controls to reduce risk
- **Transfer:** Insurance or contractual allocation
- **Accept:** Document acceptance for low residual risk
- **Avoid:** Eliminate activity creating risk

**3.3 Risk Register**

Maintain Risk Register documenting:
- Risk description
- Risk owner
- Risk rating
- Treatment approach
- Control status
- Residual risk
- Review date

---

## ARTICLE 4: ACCESS CONTROLS

**4.1 Identity and Access Management**

**(a) User Provisioning:**
- Unique user ID for each individual
- No shared accounts (except documented technical exceptions)
- Access based on job function (least privilege)
- Manager approval required for access grants
- Access provisioned within 24 hours of approval

**(b) Access Review:**
- Quarterly review of access rights
- Review upon role change or transfer
- Immediate termination of access upon separation
- Document access reviews

**(c) Privileged Access:**
- Elevated privileges require additional approval
- Privileged access limited to minimum necessary
- Enhanced monitoring of privileged accounts
- Separate privileged accounts for administrators (no daily use)

**4.2 Authentication**

**(a) Password Standards:**
- Minimum 12 characters
- Complexity required (upper, lower, number, special)
- No password reuse (24 previous passwords)
- Change every 90 days (or use MFA with longer validity)
- Account lockout after 5 failed attempts

**(b) Multi-Factor Authentication (MFA):**

**REQUIRED** for:
- All remote access
- All administrative/privileged access
- Access to systems with NPI
- Access to financial systems
- Cloud administration consoles
- Email (company accounts)

**(c) MFA Methods (in order of preference):**
1. Hardware security keys (FIDO2/WebAuthn)
2. Authenticator applications (TOTP)
3. Push notifications (approved apps only)
4. SMS (only where alternatives unavailable - deprecated)

**4.3 Network Access**

**(a) Network Segmentation:**
- Production systems isolated from corporate network
- Development/test environments separated from production
- Investor data systems in secured segment
- Guest networks isolated

**(b) Remote Access:**
- VPN required for remote network access
- VPN with MFA
- Split tunneling disabled for sensitive access
- Remote desktop via jump servers only

**(c) Firewall Rules:**
- Default deny (whitelist approach)
- Documented justification for allowed traffic
- Annual firewall rule review
- Change control for firewall modifications

**4.4 Physical Access**

**(a) Facility Security:**
- Locked facilities with access control
- Visitor sign-in and escort requirements
- Badge access for secured areas
- CCTV at entry points (where applicable)

**(b) Data Center/Cloud:**
- SOC 2 certified providers only
- Physical security certifications required
- Access audit trails required

---

## ARTICLE 5: DATA PROTECTION

**5.1 Data Classification**

| **Classification** | **Description** | **Examples** |
|--------------------|-----------------|--------------|
| **Confidential** | Highest sensitivity; significant harm if disclosed | NPI, investor SSN, authentication credentials, private keys |
| **Internal** | Business sensitive; not for public disclosure | Financial statements, contracts, employee data, internal reports |
| **Public** | Approved for public release | Marketing materials, public filings, website content |

**5.2 Encryption**

**(a) Data at Rest:**
- AES-256 encryption for Confidential data
- Full disk encryption on endpoints
- Encrypted databases for NPI
- Encrypted backups

**(b) Data in Transit:**
- TLS 1.2 minimum (TLS 1.3 preferred)
- No SSL, TLS 1.0, or TLS 1.1
- HTTPS enforced for all web applications
- Encrypted email for Confidential data (S/MIME or PGP)

**(c) Key Management:**
- Hardware security modules (HSM) for critical keys
- Key rotation per cryptographic standards
- Separation of key management duties
- Key escrow for critical keys
- Documented key recovery procedures

**5.3 Blockchain and Smart Contract Security**

**(a) Private Key Management:**
- Multi-signature wallets for treasury (3-of-5 minimum)
- Hardware wallets for private key storage
- No private keys in source code, configs, or unencrypted storage
- Geographically distributed key holders
- Documented recovery procedures

**(b) Smart Contract Security:**
- Security audit before deployment (production)
- Code review for all changes
- Upgradeable contract pattern where appropriate
- Emergency pause functionality
- Time-locks for critical operations
- Monitoring for anomalous transactions

**(c) Wallet Security:**
- Cold storage for reserves
- Hot wallets limited to operational needs
- Transaction monitoring and alerts
- Whitelist destination addresses where possible

**5.4 Data Retention and Disposal**

Per [DOC:B4] Recordkeeping Policy:
- Retain data per retention schedule
- Secure disposal upon expiration
- Destruction methods per B4 Article 3.5
- No disposal during legal hold

---

## ARTICLE 6: SECURE DEVELOPMENT

**6.1 Secure SDLC**

**(a) Security Requirements:**
- Security requirements in project planning
- Threat modeling for significant features
- Security design review

**(b) Secure Coding:**
- Follow OWASP secure coding guidelines
- Input validation
- Output encoding
- Parameterized queries (no SQL injection)
- Secure error handling
- No hardcoded secrets

**(c) Code Review:**
- Peer review for all code changes
- Security-focused review for sensitive functions
- Static analysis (SAST) in pipeline

**(d) Testing:**
- Security testing in QA
- Dynamic analysis (DAST) for web applications
- Penetration testing before major releases

**6.2 Change Management**

**(a) Change Control:**
- All changes through documented process
- Approval required before production deployment
- Rollback plan required
- Post-deployment verification

**(b) Emergency Changes:**
- Documented emergency process
- Post-implementation documentation
- Review in next change board

**6.3 Environment Separation**

- Development, test, staging, production separated
- No production data in development/test (use synthetic data)
- Separate access controls per environment
- Production changes only through CI/CD pipeline

---

## ARTICLE 7: VULNERABILITY MANAGEMENT

**7.1 Vulnerability Scanning**

**(a) Internal Scanning:**
- Monthly vulnerability scans (minimum)
- Weekly scans for internet-facing systems
- Scan after significant changes
- Use authenticated scans for accurate results

**(b) External Scanning:**
- Quarterly external vulnerability scans
- ASV scans if processing payment cards
- Scan after infrastructure changes

**7.2 Penetration Testing**

**(a) Frequency:**
- Annual penetration test (minimum)
- After significant changes
- After security incidents

**(b) Scope:**
- External network penetration test
- Web application penetration test
- Internal penetration test
- Social engineering (optional)

**(c) Testing Provider:**
- Use qualified third-party penetration testing firm
- CREST, OSCP, or equivalent certifications
- Different firm at least every 3 years

**7.3 Remediation**

| **Severity** | **Remediation Timeline** |
|--------------|-------------------------|
| Critical | 24-48 hours (emergency) |
| High | 7 days |
| Medium | 30 days |
| Low | 90 days |
| Informational | Track for review |

**(a) Remediation Process:**
- Prioritize by risk (severity + exploitability + asset value)
- Assign owner
- Track to completion
- Verify remediation
- Document exceptions with risk acceptance

---

## ARTICLE 8: SECURITY MONITORING

**8.1 Logging**

**(a) Required Logs:**
- Authentication events (success and failure)
- Authorization events
- Administrative actions
- System events
- Application events
- Network events
- Database access (sensitive data)

**(b) Log Standards:**
- UTC timestamps
- Unique event ID
- User ID
- Source IP
- Action performed
- Success/failure
- Sufficient detail for investigation

**(c) Log Protection:**
- Centralized log collection
- Log integrity protection (write-once or signed)
- Access controls on logs
- Retention per B4 (1-3 years minimum)

**8.2 Security Information and Event Management (SIEM)**

**(a) SIEM Requirements:**
- Centralized log aggregation
- Correlation rules for security events
- Alerting for security incidents
- Dashboard for security metrics

**(b) Use Cases (minimum):**
- Multiple failed authentication attempts
- Successful authentication after multiple failures
- Privileged account activity
- Access to sensitive data
- Configuration changes
- Malware detection
- Network anomalies
- Data exfiltration indicators

**8.3 Monitoring**

**(a) 24/7 Monitoring:**
- Critical systems monitored continuously
- Automated alerting for critical events
- On-call response capability

**(b) Response Times:**
- Critical alerts: 15 minutes acknowledgment
- High alerts: 1 hour acknowledgment
- Medium alerts: 8 hours acknowledgment

---

## ARTICLE 9: INCIDENT RESPONSE

**9.1 Incident Response Plan**

**(a) Incident Categories:**

| **Category** | **Examples** |
|--------------|-------------|
| Data Breach | Unauthorized access to NPI, disclosure of Confidential data |
| Malware | Ransomware, virus, trojan, cryptominer |
| Unauthorized Access | Compromised accounts, intrusion |
| Denial of Service | DDoS, resource exhaustion |
| Insider Threat | Employee misconduct, data theft |
| Physical | Theft, unauthorized facility access |
| Third-Party | Vendor breach affecting Company data |

**(b) Incident Severity:**

| **Severity** | **Description** |
|--------------|-----------------|
| Critical | Active compromise, data breach in progress, widespread impact |
| High | Confirmed compromise, limited impact, contained |
| Medium | Potential compromise, investigation required |
| Low | Security concern, no evidence of compromise |

**9.2 Incident Response Phases**

**(a) Preparation:**
- Maintain incident response plan
- Train incident response team
- Establish communication procedures
- Prepare forensic capabilities
- Maintain contact lists (legal, PR, regulators)

**(b) Detection and Analysis:**
- Identify incident indicators
- Determine scope and impact
- Classify severity
- Preserve evidence
- Document findings

**(c) Containment:**
- Short-term containment (stop bleeding)
- Long-term containment (stable state)
- Evidence preservation
- Affected system isolation

**(d) Eradication:**
- Identify root cause
- Remove threat actor access
- Patch vulnerabilities
- Reset compromised credentials
- Remove malware

**(e) Recovery:**
- Restore systems from clean backups
- Verify system integrity
- Monitor for recurrence
- Return to normal operations

**(f) Post-Incident:**
- Conduct lessons learned
- Update procedures
- Implement improvements
- Document incident fully

**9.3 Breach Notification**

**(a) Regulatory Requirements:**

| **Jurisdiction** | **Timeline** | **Authority** |
|------------------|--------------|---------------|
| SEC (if applicable) | Reasonable time | SEC |
| State AGs | Per state law (typically 30-60 days) | State AGs |
| GDPR | 72 hours | Data Protection Authority |
| Affected Individuals | Per state law (typically 30-60 days) | Direct notice |

**(b) Notification Content:**
- Description of incident
- Types of information involved
- Steps taken
- Steps individuals can take
- Contact information

**(c) Notification Process:**
- Legal counsel review before notification
- Coordinate with PR
- Document all notifications
- Offer credit monitoring (for SSN breaches)

**9.4 Incident Response Team**

| **Role** | **Responsibility** |
|----------|-------------------|
| Incident Commander | Overall coordination |
| Information Security Officer | Technical lead |
| Legal Counsel | Legal guidance, notifications |
| Communications | Internal/external communications |
| IT Operations | System recovery |
| Business Owner | Business impact assessment |
| HR | Employee-related incidents |

---

## ARTICLE 10: BUSINESS CONTINUITY AND DISASTER RECOVERY

**10.1 Business Continuity Planning**

**(a) Business Impact Analysis:**
- Identify critical business functions
- Determine recovery time objectives (RTO)
- Determine recovery point objectives (RPO)
- Identify dependencies

**(b) Critical Functions:**

| **Function** | **RTO** | **RPO** |
|--------------|---------|---------|
| Investor portal | 4 hours | 1 hour |
| Payment processing | 4 hours | 1 hour |
| Core platform | 8 hours | 4 hours |
| Email | 24 hours | 4 hours |
| Corporate systems | 48 hours | 24 hours |

**10.2 Disaster Recovery**

**(a) Backup Requirements:**
- Daily backups of critical data
- Weekly full backups
- Off-site/cloud backup storage
- Encryption of backup data
- Test restores quarterly

**(b) Recovery Procedures:**
- Documented recovery procedures
- Recovery runbooks for critical systems
- Contact information for vendors
- Alternative processing arrangements

**(c) DR Testing:**
- Annual DR test
- Tabletop exercises semi-annually
- Document test results
- Update procedures based on findings

**10.3 High Availability**

For critical systems:
- Redundant infrastructure
- Geographic distribution
- Failover capabilities
- Load balancing

---

## ARTICLE 11: VENDOR SECURITY

**11.1 Vendor Assessment**

**(a) Due Diligence:**

Before engaging vendors with access to systems or data:
- Security questionnaire
- SOC 2 report review (or equivalent)
- Penetration test results
- Insurance verification
- Reference checks

**(b) Risk-Based Assessment:**

| **Vendor Category** | **Assessment Level** |
|--------------------|---------------------|
| High-risk (NPI access, critical systems) | Full assessment, SOC 2 required |
| Medium-risk (internal data, supporting systems) | Standard assessment |
| Low-risk (no data access, commodity services) | Basic assessment |

**11.2 Contractual Requirements**

Per [DOC:N1] Partner Payment Processor Agreement (as template):

Required provisions:
- Confidentiality obligations
- Security requirements
- Right to audit
- Incident notification (24 hours)
- Data return/destruction
- Subcontractor restrictions
- Insurance requirements
- Indemnification

**11.3 Ongoing Monitoring**

- Annual reassessment of high-risk vendors
- Review of SOC 2 reports annually
- Monitor vendor security news
- Notification requirements in contracts
- Right to terminate for security failures

---

## ARTICLE 12: TRAINING AND AWARENESS

**12.1 Security Awareness Training**

**(a) Initial Training:**
- All employees within 30 days of hire
- Cover security policies and procedures
- Phishing awareness
- Data handling
- Incident reporting

**(b) Ongoing Training:**
- Annual refresher (required)
- Quarterly security updates
- Role-specific training for IT, developers
- Training upon policy changes

**(c) Training Topics:**
- Password security
- Phishing and social engineering
- Data classification and handling
- Physical security
- Remote work security
- Incident reporting
- Regulatory requirements

**12.2 Phishing Testing**

- Monthly simulated phishing campaigns
- Track click rates and report rates
- Additional training for repeat clickers
- Recognize good behavior

**12.3 Training Records**

Per [DOC:B4]:
- Maintain training completion records
- Track training effectiveness
- Document in annual self-certification [DOC:B11]

---

## ARTICLE 13: COMPLIANCE

**13.1 Regulatory Compliance**

This Policy addresses requirements of:

| **Regulation** | **Requirement** | **Section** |
|----------------|-----------------|-------------|
| GLBA Safeguards | Information security program | Articles 1-12 |
| FTC Safeguards (16 CFR 314) | Safeguards Rule compliance | Articles 2-9 |
| SEC Reg S-P | Safeguarding NPI | Articles 4-5 |
| GDPR | Technical/organizational measures | Articles 4-5, 9 |
| State privacy laws | Security requirements | Various |

**13.2 Annual Self-Certification**

Per [DOC:B11] Section 6:
- Annual certification of security program
- Document security controls
- Verify training completion
- Report incidents
- Confirm penetration testing

**13.3 Audit**

**(a) Internal Audit:**
- Annual security program review
- Control testing
- Policy compliance verification

**(b) External Audit:**
- SOC 2 Type II (if applicable)
- Regulatory examinations
- Customer audit rights (per contract)

---

## ARTICLE 14: POLICY MANAGEMENT

**14.1 Policy Review**

- Annual review and update
- Update upon material changes
- Update upon regulatory changes
- Approval by ISO and executive management

**14.2 Exception Process**

**(a) Exception Requests:**
- Business justification required
- Risk assessment required
- Compensating controls documented
- Approval by ISO and business owner
- Time-limited (maximum 1 year)

**(b) Exception Documentation:**
- Risk accepted
- Compensating controls
- Review date
- Approvers

**14.3 Enforcement**

Policy violations may result in:
- Disciplinary action
- Access revocation
- Termination
- Legal action

---

## ARTICLE 15: DOCUMENT CONTROL

**Version:** 1.0.0  
**Effective Date:** [DATE]  
**Document Owner:** Information Security Officer  
**Classification:** Internal Use Only  
**Next Review:** Annual

**Related Documents:**
- [DOC:B1] Operating Agreement
- [DOC:B4] Recordkeeping Policy
- [DOC:B8] Privacy Policy
- [DOC:B11] Annual Self-Certification Checklist
- [DOC:N1] Partner Payment Processor Agreement

**Amendment History:**

| **Version** | **Date** | **Changes** | **Approved By** |
|-------------|----------|-------------|-----------------|
| 1.0.0 | [DATE] | Initial version | [NAME] |

---

## APPENDIX A: QUICK REFERENCE - SECURITY STANDARDS

**Authentication:**
- 12+ character passwords
- MFA required for remote/admin/NPI access
- Hardware security keys preferred

**Encryption:**
- AES-256 for data at rest
- TLS 1.2+ for data in transit
- HSM for critical keys

**Access:**
- Least privilege
- Quarterly access reviews
- Immediate revocation on separation

**Monitoring:**
- SIEM with 24/7 alerting
- 15-minute response for critical alerts
- 1-year log retention minimum

**Testing:**
- Monthly vulnerability scans
- Annual penetration test
- Quarterly DR test

**Incidents:**
- Critical: 24-48 hour remediation
- Breach notification: 72 hours (GDPR), state-specific (US)

---

*END OF INFORMATION SECURITY POLICY*

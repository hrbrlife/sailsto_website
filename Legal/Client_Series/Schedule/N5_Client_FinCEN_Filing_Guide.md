# CLIENT FINCEN FILING GUIDE
## CCASH MONEY SERVICES (US) SERIES LLC

<!-- schema:doc DOC:N5 version:1.1 -->

---

**Effective Date:** December 21, 2025

**Document Version:** 1.1

---

## VERSION HISTORY

| Version | Date | Author | Summary of Changes | Breaking Change |
|---------|------|--------|-------------------|-----------------|
| 1.0 | December 14, 2025 | CCO | Initial version | — |
| 1.1 | December 21, 2025 | Compliance Fix | Added Section 9 De-Registration procedures for cessation of MSB activities (180-day requirement per 31 CFR §1022.380); renumbered Section 9→10 | No |

---

## SECTION 1: INTRODUCTION

### 1.1. Purpose

<!-- schema:flow FLOW:fincen_registration -->

1.1.1. This Guide provides Client Series [TERM:ClientSeries] with step-by-step instructions for obtaining and maintaining FinCEN [TERM:FinCEN] Money Services Business (MSB) [TERM:MSB] registration [FLOW:fincen_registration].

1.1.2. Each Client Series is an independent MSB and must maintain its own FinCEN registration. This is a regulatory requirement, not optional [OBL:FINCEN-REG-001].

1.1.3. The Company [TERM:Company] provides this Guide as a resource but does not file FinCEN registrations on behalf of Client Series. Each Client Series is responsible for its own registration and compliance.

### 1.2. Regulatory Basis

1.2.1. Under the Bank Secrecy Act (BSA) [TERM:BSA] and its implementing regulations (31 CFR § 1022.380), money services businesses must register with FinCEN.

1.2.2. Registration must be completed within 180 days of commencing MSB activities [OBL:FINCEN-TIMING-001].

1.2.3. Registration must be renewed every two years (biennially) [OBL:FINCEN-RENEWAL-001].

1.2.4. Changes to registration information must be reported within 180 days [OBL:FINCEN-UPDATE-001].

---

## SECTION 2: PRE-REGISTRATION REQUIREMENTS

### 2.1. Obtain an Employer Identification Number (EIN)

<!-- schema:flow FLOW:ein_application -->

2.1.1. Before registering with FinCEN [TERM:FinCEN], the Client Series [TERM:ClientSeries] must have an EIN [TERM:EIN] from the IRS [FLOW:ein_application].

2.1.2. **Online Application:** Visit irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online

2.1.3. **Application Process:**
   - Select "Limited Liability Company" as the entity type
   - Enter CCASH MONEY SERVICES (US) SERIES LLC [TERM:CompanyLegalName] as the legal name
   - Add the Client Series designation (e.g., "– [Client Name] Operations Series")
   - Complete responsible party information (typically the Client Series manager [TERM:Manager])
   - EIN is issued immediately upon completion

2.1.4. **Important:** The EIN is for the Client Series specifically, not the parent Company [TERM:Company]. Each Client Series must have its own unique EIN [OBL:EIN-UNIQUE-001].

### 2.2. Gather Required Information

2.2.1. Before beginning the FinCEN [TERM:FinCEN] registration, gather the following:

   (a) Client Series [TERM:ClientSeries] EIN [TERM:EIN] (obtained in Step 2.1)
   
   (b) Client Series legal name: CCASH MONEY SERVICES (US) SERIES LLC [TERM:CompanyLegalName] – [Client Name] Operations Series
   
   (c) Doing Business As (DBA) name: [Client's trade name as registered with Montana [TERM:MontanaState]]
   
   (d) Business address (Montana registered address)
   
   (e) List of MSB [TERM:MSB] activities the Client Series will conduct
   
   (f) Responsible party name, title, and SSN or ITIN
   
   (g) Ownership information (members holding 25% or more)
   
   (h) Agent information (if using a designated agent [TERM:RegisteredAgent])

### 2.2A. PII Security Requirements

2.2A.1. **Sensitive PII Handling.** The information collected for FinCEN registration includes highly sensitive personal information (SSN/ITIN, date of birth, address). Per the FTC Safeguards Rule (16 CFR Part 314) and [DOC:B8] Privacy Policy:
   (a) All SSN/ITIN data must be encrypted in transit (TLS 1.2+) and at rest (AES-256);
   (b) Access to filing information must be limited to personnel with a legitimate business need;
   (c) Paper documents containing SSN/ITIN must be stored in locked containers;
   (d) Electronic transmission of SSN/ITIN must use secure channels (encrypted email, secure file transfer);
   (e) Dispose of documents containing SSN/ITIN via cross-cut shredding or secure destruction per [DOC:B4].

2.2A.2. **Do not** email SSN or ITIN information in plain text. Use the Company's secure document portal or encrypted transmission methods.

### 2.3. Determine MSB Activities

2.3.1. FinCEN [TERM:FinCEN] requires identification of which MSB [TERM:MSB] activities the business will conduct. Check all that apply to the Client Series [TERM:ClientSeries]:

   - [ ] **Money transmitter:** Transferring funds on behalf of customers
   - [ ] **Currency dealer or exchanger:** Exchanging currency for currency
   - [ ] **Check casher:** Cashing checks for customers
   - [ ] **Issuer of traveler's checks, money orders, or stored value:** Issuing payment instruments
   - [ ] **Seller or redeemer of traveler's checks, money orders, or stored value:** Selling payment instruments
   - [ ] **Provider of prepaid access:** Providing prepaid access services
   - [ ] **Seller of prepaid access:** Selling prepaid access

2.3.2. Most Client Series will select "Money transmitter" at minimum. Consult with the Company's [TERM:Company] compliance team [TERM:CCO] if uncertain about classifications.

---

## SECTION 3: FINCEN REGISTRATION PROCESS

### 3.1. Access the FinCEN BSA E-Filing System

<!-- schema:flow FLOW:bsa_efiling -->

3.1.1. **Registration Portal:** Navigate to bsaefiling.fincen.treas.gov [FLOW:bsa_efiling]

3.1.2. **Create an Account:** If you do not have a BSA [TERM:BSA] E-Filing account, select "Enroll" to create one. You will need:
   - Valid email address
   - Password meeting FinCEN [TERM:FinCEN] requirements
   - Security questions

3.1.3. **Login:** Access your BSA E-Filing account.

### 3.2. Complete Form 107 (RMSB)

3.2.1. **Select Form:** From the BSA E-Filing system, select "File FinCEN Report 107 (RMSB)" for new registrations.

3.2.2. **Filing Type:** Select "New Registration" for initial filing or "Renewal" for biennial renewals.

### 3.3. Part I: Filer Information

3.3.1. **Item 1 - Type of Filing:** Select the appropriate option (New Registration, Re-registration, or Renewal).

3.3.2. **Item 2 - Prior Registration Number:** Leave blank for new registrations. Enter prior number for renewals.

### 3.4. Part II: MSB Information

3.4.1. **Item 3 - Legal Name:** Enter exactly as follows:
   ```
   CCASH MONEY SERVICES (US) SERIES LLC – [Client Name] Operations Series
   ```

3.4.2. **Item 4 - DBA/Trade Name:** Enter the Client's [TERM:ClientSeries] registered assumed business name (DBA).

3.4.3. **Item 5 - EIN:** Enter the Client Series' EIN [TERM:EIN] (9 digits, no dashes in the form).

3.4.4. **Item 6 - Address:** Enter the Montana [TERM:MontanaState] business address.

3.4.5. **Item 7 - MSB Activities:** Check all activities the Client Series will conduct (as determined in Section 2.3).

3.4.6. **Item 8 - Number of Branches/Locations:** Enter "1" unless the Client Series has multiple physical locations.

### 3.5. Part III: Owner/Controller Information

3.5.1. **Item 9 - Controlling Owner:** Enter information for each person who owns 25% or more of the Client Series [TERM:ClientSeries].

3.5.2. **Required Information:**
   - Full legal name
   - Date of birth
   - Social Security Number or ITIN
   - Address
   - Percentage of ownership

3.5.3. **If Owned by Another Entity:** Enter information for the controlling entity and then the individuals who control that entity.

### 3.6. Part IV: Designated Agent (Optional)

3.6.1. If the Client Series designates an agent [TERM:RegisteredAgent] to receive legal process or communications, enter agent information.

3.6.2. Most Client Series use the Company's [TERM:Company] registered agent. Consult with the Company before completing this section.

### 3.7. Part V: Certification

3.7.1. **Certifying Official:** The person signing must have authority to bind the Client Series.

3.7.2. **Read and Acknowledge:** Review the certification statement carefully.

3.7.3. **Sign Electronically:** Complete the electronic signature.

### 3.8. Submit and Confirm

3.8.1. **Review:** Review all entered information for accuracy before submission.

3.8.2. **Submit:** Click "Submit" to file the registration.

3.8.3. **Confirmation:** Save or print the confirmation page. The confirmation includes a temporary receipt number.

3.8.4. **Registration Number:** FinCEN will issue a permanent MSB registration number within 14-30 days. This number will be sent to the email address on file.

---

## SECTION 4: POST-REGISTRATION REQUIREMENTS

### 4.1. Provide Registration to Company

<!-- schema:flow FLOW:registration_verification -->

4.1.1. Upon receiving the FinCEN [TERM:FinCEN] registration confirmation and permanent registration number, immediately provide copies to the Company [TERM:Company] [OBL:FINCEN-NOTIFY-001].

4.1.2. The Company will verify registration before the Client Series [TERM:ClientSeries] may commence operations [FLOW:registration_verification].

4.1.3. Send registration documentation to: [compliance@ccash.us or designated contact]

### 4.2. Maintain Records

4.2.1. Maintain copies of:
   - Form 107 submission confirmation
   - FinCEN registration number
   - All renewal confirmations
   - Any correspondence with FinCEN

4.2.2. Records must be maintained for five years after the registration period ends [OBL:RECORD-RETENTION-001] [DOC:B4].

### 4.3. Display Registration

4.3.1. The FinCEN MSB [TERM:MSB] registration number should be available upon request.

4.3.2. Some state regulators may require the registration number in license applications.

---

## SECTION 5: BIENNIAL RENEWAL

### 5.1. Renewal Deadline

<!-- schema:flow FLOW:fincen_renewal -->

5.1.1. FinCEN [TERM:FinCEN] MSB [TERM:MSB] registration must be renewed every two years [OBL:FINCEN-RENEWAL-001] [FLOW:fincen_renewal].

5.1.2. The renewal window opens 180 days before the registration expiration date.

5.1.3. Renewal must be completed on or before the expiration date (the two-year anniversary of initial registration or prior renewal).

5.1.4. **Example:** If initial registration was effective January 15, 2025, the registration expires January 15, 2027. The renewal window opens July 19, 2026 (180 days before expiration), and renewal must be filed by January 15, 2027.

### 5.2. Renewal Process

5.2.1. Login to BSA E-Filing at bsaefiling.fincen.treas.gov

5.2.2. Select "File FinCEN Report 107 (RMSB)"

5.2.3. Select "Renewal" as the filing type

5.2.4. Enter the existing registration number

5.2.5. Review and update all information as needed

5.2.6. Submit the renewal

### 5.3. Company Monitoring

5.3.1. The Company [TERM:Company] tracks Client Series [TERM:ClientSeries] renewal deadlines and provides reminders 90 days, 60 days, and 30 days before due dates.

5.3.2. However, compliance with renewal requirements is solely the Client Series' responsibility [OBL:FINCEN-RENEWAL-001].

5.3.3. Failure to renew may result in suspension of access to Company services [TERM:Services].

---

## SECTION 6: UPDATING REGISTRATION

### 6.1. Reportable Changes

<!-- schema:flow FLOW:fincen_update -->

6.1.1. The following changes must be reported to FinCEN [TERM:FinCEN] within 180 days [OBL:FINCEN-UPDATE-001] [FLOW:fincen_update]:

   (a) Change in legal name or DBA
   
   (b) Change in address
   
   (c) Change in controlling ownership (25%+ owners)
   
   (d) Change in MSB activities
   
   (e) Change in agent information

### 6.2. Update Process

6.2.1. Login to BSA E-Filing

6.2.2. Select "File FinCEN Report 107 (RMSB)"

6.2.3. Select the appropriate update type

6.2.4. Enter existing registration number

6.2.5. Update the changed information

6.2.6. Submit the update

### 6.3. Notify the Company

6.3.1. Inform the Company [TERM:Company] of any changes to FinCEN [TERM:FinCEN] registration information [OBL:FINCEN-NOTIFY-001].

6.3.2. Provide updated registration documentation upon completion.

---

## SECTION 7: COMMON ISSUES AND TROUBLESHOOTING

### 7.1. EIN Issues

7.1.1. **Problem:** Cannot obtain EIN [TERM:EIN] online.
   **Solution:** Apply by mail using Form SS-4 or call the IRS Business & Specialty Tax Line.

7.1.2. **Problem:** EIN assigned to wrong entity name.
   **Solution:** Contact IRS to correct. Do not proceed with FinCEN registration until corrected.

### 7.2. E-Filing System Issues

7.2.1. **Problem:** Cannot access BSA E-Filing account.
   **Solution:** Use password reset function or contact FinCEN helpline at 1-800-949-2732.

7.2.2. **Problem:** Form submission error.
   **Solution:** Clear browser cache, try a different browser, or contact FinCEN technical support.

### 7.3. Registration Status Issues

7.3.1. **Problem:** Have not received registration number after 30 days.
   **Solution:** Contact FinCEN Regulatory Support at 1-800-949-2732.

7.3.2. **Problem:** Registration shows incorrect information.
   **Solution:** File an update using the process in Section 6.

---

## SECTION 8: RESOURCES AND CONTACTS

### 8.1. FinCEN Resources

8.1.1. **BSA E-Filing System:** bsaefiling.fincen.treas.gov

8.1.2. **FinCEN MSB Information:** fincen.gov/resources/statutes-and-regulations/administrative-rulings/money-services-business-definition

8.1.3. **FinCEN [TERM:FinCEN] Contact Center:** 1-800-949-2732

8.1.4. **Form 107 Instructions:** Available on the BSA [TERM:BSA] E-Filing system

### 8.2. IRS Resources

8.2.1. **EIN Online Application:** irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online

8.2.2. **IRS Business Line:** 1-800-829-4933

### 8.3. Company Contacts

8.3.1. **Compliance Questions:** [compliance@ccash.us] [TERM:CCO]

8.3.2. **Registration Verification:** [operations@ccash.us]

8.3.3. **General Support:** [support@ccash.us]

---

## SECTION 9: DE-REGISTRATION (CESSATION OF MSB ACTIVITIES)

### 9.1. When De-Registration is Required

9.1.1. If a Client Series ceases all MSB activities, it must notify FinCEN by filing a de-registration within **180 days** of cessation per 31 CFR § 1022.380.

9.1.2. De-registration is required when:
   (a) The Client Series terminates its Client Services Agreement [DOC:F1] and ceases operations;
   (b) The Client Series pivots to a business model that no longer constitutes MSB activity;
   (c) The Client Series merges with or is acquired by another entity; or
   (d) The underlying Series is dissolved per [DOC:B1] Article 16.

9.1.3. **Important:** Failure to de-register when required may result in regulatory penalties and affect the Client's ability to re-register in the future.

### 9.2. De-Registration Process

9.2.1. **Step 1: Notify the Company.** Inform the Company [TERM:CCO] of the intent to cease MSB activities at least 30 days before cessation when possible.

9.2.2. **Step 2: File Form 107 - De-Registration.**
   (a) Log in to the BSA E-Filing System at bsaefiling.fincen.gov;
   (b) Select "MSB Registration" and then "Registration Update";
   (c) In Item 1c, select "CHANGE" and proceed to indicate cessation of MSB activities;
   (d) Complete all required fields, indicating the effective date of cessation;
   (e) Submit the form and save the confirmation.

9.2.3. **Step 3: Record Retention.** Even after de-registration, maintain all records for **five (5) years** from the date of the last transaction or account closure per 31 CFR § 1010.410(e) and [DOC:B4]. This is a legal requirement that survives de-registration.

9.2.4. **Step 4: Provide Confirmation.** Provide the Company with a copy of the de-registration confirmation for Company records.

### 9.3. Self-Certification: Cessation of Activities

9.3.1. Upon cessation of MSB activities, the Client Series principal shall execute the following self-certification and retain a copy:

> **SELF-CERTIFICATION: CESSATION OF MSB ACTIVITIES**
> 
> I, [Name], as the authorized representative of [Client Series Name], certify that:
> 1. The Client Series ceased all MSB activities as of [Date];
> 2. FinCEN Form 107 de-registration was filed on [Date] (Confirmation #: [____]);
> 3. All transaction records will be retained for five years from the last transaction date;
> 4. All customer funds have been returned or properly transferred; and
> 5. The Company has been notified of cessation.
> 
> Signature: _________________________ Date: _____________

---

## SECTION 10: COMPLIANCE CHECKLIST

### 10.1. Initial Registration Checklist

<!-- schema:flow FLOW:client_onboarding -->

- [ ] Obtained EIN [TERM:EIN] for Client Series [TERM:ClientSeries] from IRS
- [ ] Created BSA [TERM:BSA] E-Filing account
- [ ] Gathered all required information (Section 2.2)
- [ ] Determined applicable MSB [TERM:MSB] activities (Section 2.3)
- [ ] Completed and submitted Form 107
- [ ] Saved confirmation receipt
- [ ] Received permanent registration number
- [ ] Provided registration to Company [TERM:Company]
- [ ] Received Company verification to commence operations [FLOW:client_onboarding]

### 10.2. Renewal Checklist

- [ ] Calendared renewal deadline (2 years from registration)
- [ ] Received Company reminder (90/60/30 days)
- [ ] Reviewed current registration for accuracy
- [ ] Submitted renewal Form 107
- [ ] Saved confirmation receipt
- [ ] Provided renewal confirmation to Company

### 10.3. Ongoing Compliance Checklist

- [ ] FinCEN [TERM:FinCEN] registration current and active [OBL:FINCEN-REG-001]
- [ ] All changes reported within 180 days [OBL:FINCEN-UPDATE-001]
- [ ] Records maintained for 5 years [OBL:RECORD-RETENTION-001] [DOC:B4]
- [ ] Company has current registration documentation

### 10.4. De-Registration Checklist

- [ ] All MSB activities ceased
- [ ] All customer funds returned or transferred
- [ ] Company notified of cessation
- [ ] FinCEN Form 107 de-registration filed within 180 days
- [ ] De-registration confirmation saved
- [ ] Self-certification executed (Section 9.3.1)
- [ ] Records retention plan in place (5 years from last transaction)

---

*This Guide is provided for informational purposes to assist Client Series with FinCEN registration requirements. It does not constitute legal advice. Client Series should consult with their own legal counsel for specific compliance questions.*

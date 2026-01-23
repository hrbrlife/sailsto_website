Sponsor Bank Partnership Models for MSB
White‑Label Payment Services
Executive Summary
Overview: Money services businesses (MSBs) often rely on sponsor banks to access U.S. payment rails and
issue financial products. Our Montana-based Series LLC operates a “master MSB” with licensed parent and
sub-series MSBs (agents) under a shared compliance umbrella. This report explores how sponsor bank
partnerships can be structured for such a white-label model, covering roles, compliance allocation,
regulatory views on layered MSB arrangements, specifics for prepaid/gift card programs, and risk
mitigation strategies.
Key Findings:
- MSB–Bank Partnership Models: Three primary models exist – (1) Direct Account Relationships, where
the MSB simply maintains its own high-risk business account and the bank’s role is limited to serving the
MSB as a single customer; (2) Banking-as-a-Service (BaaS) / FBO Models, where the bank provides a
platform (often via APIs) for the MSB to create sub-accounts or wallets (funds held for the benefit of MSB’s
clients) under the bank’s charter; and (3) Program Manager Sponsorship, common for prepaid card or
fintech programs, where the MSB (program manager) operates a branded financial product while an issuing
sponsor bank holds the BIN/license and ensures network and regulatory compliance. Each model assigns
different responsibilities between bank and MSB, and banks often set limits on volumes, KYC standards, and
permitted activities to manage their risk exposure . A comparison table is provided in Section 1.5
outlining these models.
Sponsor Bank Onboarding & Diligence: Banks evaluate MSB clients with rigorous due diligence,
especially when an MSB has a white-label or layered agent structure. Before onboarding, banks will
verify FinCEN registration and state licenses of the parent MSB and may request the MSB’s agent
list and agent management policies . The bank performs a risk assessment covering the
MSB’s business model, customer base (e.g. mostly B2B international clients, which can pose higher
cross-border risks), transaction volumes, and markets served . MSBs should be prepared to
explain their structure clearly, including whether they act as a principal with a fleet of agents or
sub-MSBs . Banks may individually vet significant sub-MSBs (especially foreign ones) and often
require enhanced due diligence (EDD) such as background checks on owners, on-site visits, and
review of AML programs . If the structure is novel (e.g. series LLC with multiple sub-entities),
expect detailed questions and potentially a slower approval as the bank ensures it understands and
can monitor the layered arrangement.
Compliance Responsibility & Delegation: In sponsor arrangements, ultimate BSA/AML
responsibility rests with the bank, but many compliance functions are contractually delegated to
the MSB program operator . The bank remains accountable to regulators (as evidenced by
OCC consent orders when banks failed to oversee fintech partners) , so banks impose strict
oversight: for example, the MSB’s KYC/CIP standards, AML transaction monitoring, and sanction
1 2
•
3 4
5
3
6 7
•
2 8
9
1
screening procedures often require the sponsor bank’s review and approval . The MSB
(parent) must maintain a robust AML program that encompasses its agents/sub-MSBs, and the
sponsor bank will regularly audit or receive reports on its effectiveness. Sub-MSBs generally operate
under the parent’s AML program (as authorized agents), rather than each creating entirely
independent programs – FinCEN permits agents to rely on the principal’s compliance infrastructure
. However, each sub-MSB/agent should adhere to the parent’s policies, and the parent MSB
must exercise ongoing oversight (training, monitoring, and termination of agents who present
compliance failures) . Suspicious Activity Reports (SARs) and Currency Transaction Reports
(CTRs): The sponsor bank files SARs if it detects suspicious activity through the MSB’s accounts (e.g.
unusual fund flows or unlicensed activity) , and will expect the MSB to file SARs for its underlying
customer transactions (federal rules mandate money transmitters and certain other MSBs to file
SARs on suspicious customer deals) . The MSB (parent) typically aggregates cash transactions
across agents and files CTRs for customer cash-in/out exceeding $10k, while the bank would file
CTRs on any large cash deposits by the MSB into its bank account as needed. A “compliance waterfall”
thus exists: the bank oversees the MSB’s compliance program, the MSB oversees its agents’
compliance, and agents deal directly with end customers – with clear reporting and escalation
channels at each tier to ensure nothing falls through regulatory cracks.
Regulatory Treatment of Layered MSBs: FinCEN explicitly allows MSB-agent relationships: an
entity “solely because it serves as an agent of another MSB” is not required to register independently
with FinCEN . The parent MSB must list its agents and make that list available to FinCEN or law
enforcement upon request . FinCEN expects that a principal MSB’s AML program is scaled to
cover its whole agent network (including domestic and foreign agents) . State regulators
generally permit a licensed money transmitter to appoint authorized delegates or agents to
conduct business under the licensee’s auspices. These delegates (such as our series sub-MSBs) often
must be disclosed to the state (many states require reporting new agents via NMLS or include agent
info in renewals), and some states require agents to post the licensee’s contact information at their
place of business. Regulators emphasize that the licensee is fully responsible for its agents’
compliance. While states don’t set an official “nesting” limit in statute, in practice multiple layers of
authorization are viewed cautiously. The preference is usually one level of agents – i.e. the
licensed MSB and its direct agents. If our parent MSB were to allow sub-agents under a delegate, it
could raise regulatory concerns unless those sub-agents are also formally recognized as agents of
the parent. In short, deeper nesting (MSB → sub-MSB agent → sub-agent) is not explicitly forbidden
by law but would be unusual and likely disfavored by regulators due to the opacity it introduces.
Disclosure and transparency are crucial: our MSB should proactively disclose the series structure to
regulators and banking partners, making clear which legal entity is licensed and that the series LLC
structure is used for internal liability segregation. Agent-of-Payee Exemption: Some states offer an
“agent-of-the-payee” exemption whereby a payment intermediary is not considered a money
transmitter if it has a contractual agreement to accept payments on behalf of the intended payee
(for goods/services) . This can reduce licensing burden for certain business models. However,
if an MSB is already licensed (or operating under a parent’s license), the agent-of-payee exemption
doesn’t directly affect the sponsor bank relationship – except that if a white-label client’s use case fits
an exemption, it might simplify compliance in states that recognize it. Sponsor banks will still insist
on full BSA/AML controls even if a sub-client claims to be an “agent of payee” and not an MSB,
because the bank’s federal obligations remain. In practice, agent-of-payee models are more relevant
to whether state licenses are needed; they do not exempt the bank or fintech from implementing
AML programs or from oversight. Banks might view an agent-of-payee arrangement as slightly
2
10 4
4
11
12 13
•
10
4
14
15 16
2
lower risk than full-blown money transmission (since funds ostensibly only flow to the merchant/
payee, not freely anywhere), but they will still require robust controls.
Prepaid/Gift Card Program Specifics: When offering white-labeled prepaid cards or gift card
programs, additional layers of regulation and sponsor requirements apply. Sponsor banks issuing
prepaid cards (whether reloadable debit cards, digital wallets, or gift cards) must ensure compliance
with Regulation E and the CFPB’s Prepaid Accounts Rule for consumer programs. This means the
program must provide upfront disclosures of fees/terms and error-resolution rights to cardholders,
and implement consumer protection measures (e.g. liability limits on lost cards, Reg E dispute
timelines). The bank typically will supply or approve the disclosure and cardholder agreement
templates. Network (Visa/Mastercard) rules also come into play: the sponsor bank (as a network
principal member) is responsible to Visa/MC for all cards issued, so it will only onboard a program
manager that it trusts to meet network standards. Program Manager vs. Sub-Program: In many cases,
the MSB acts as the primary Program Manager with the bank. If that MSB then offers “sub-
programs” to clients (for instance, a corporate client wants a branded gift card program under our
MSB’s umbrella), the bank and networks must be informed. Often the MSB remains the official
Program Manager on record, and the client is a marketing partner or “program affiliate.” The MSB
would need to extend its compliance oversight to the client’s program. Some networks and sponsor
banks may require a due diligence review of the brand using the cards, especially if they have access
to cardholder data or perform program functions. In all cases, the sponsor bank retains the right
to approve or reject each program or significant sub-program because it is ultimately
accountable for any card program operating under its BIN. Visa and Mastercard also expect that
program managers ensure compliance with all network rules and regulatory standards on
things like KYC, transaction monitoring, fraud controls, and data security . Our MSB, as
program manager, would need to certify to the bank that each white-label client’s program follows
these standards. State Money Transmitter vs. Gift Card Laws: Prepaid programs can implicate
money transmitter laws (if funds are stored and transferable) and unclaimed property (escheat) laws.
Notably, many states exempt closed-loop gift cards from unclaimed property escheatment or treat
open-loop prepaid bank cards differently (e.g., some states say general-purpose bank-issued cards
that never expire do not escheat) . Still, as a best practice, the program manager and bank
will track dormant balances. Typically, the bank as the issuer will handle escheatment filings for
unclaimed funds (since the bank is the holder of the deposit liability), but the program manager
must supply the data and often attempt to contact customers before funds are reported. Sponsor
banks like Pathward (a major prepaid issuer) routinely send letters regarding unclaimed card
balances, indicating the importance of compliance with escheat laws . Network Liability and
Reserves: Another prepaid-specific concern is financial exposure from chargebacks or fraud. Banks
may impose reserve requirements on program managers – e.g. holding a certain percentage of
the float in a reserve account – to cover chargebacks, fraud losses, or even potential regulatory
fines. These reserve or collateral accounts are often subject to broad set-off rights in the contract
(the bank can seize funds if needed to indemnify itself) . Overall, prepaid card programs demand
close collaboration: the sponsor bank will want detailed operating procedures from the MSB (card
issuance flows, AML controls, customer service, etc.) and will audit the program both for BSA/AML
and for consumer compliance (Reg E, UDAAP, privacy, etc.). We should be prepared to meet both
banking regulators and card network requirements in a white-label card scenario – often more
stringent than a simple funds transfer service.
•
17 18
19 20
21
22
3
Risk Mitigation for a Conservative MSB Operator: To maintain long-term sponsor bank
relationships, we should align our program with what banks consider “low-risk” within the high-
risk category. That means focusing on transparent, well-controlled transaction types and
moderate volumes. For example, purely domestic ACH payments between known business entities,
or payroll/prepaid programs with full KYC and relatively low limits, are more palatable than cash-
heavy or crypto-related transactions. Keeping customer types limited to known businesses and
regulated institutions (as we plan) is a positive – banks prefer MSB programs serving vetted
corporate/institutional clients over those open to the general public, due to lower fraud and
consumer protection issues. We should also proactively implement a strong AML compliance
program and document it well. By providing our sponsor bank with thorough policies, risk
assessments, independent audit reports, and ongoing monitoring results, we reassure them and
reduce the likelihood of sudden account termination . In contracts, it is crucial to negotiate
provisions that reduce disruption if the bank relationship ends. While a small MSB may not have
much leverage, we should seek at least a reasonable notice period for termination (30–60 days if
possible, for convenience terminations) and the right to transfer our program to a successor
bank . Some sponsor banks have tried to restrict fintechs from easily porting programs (to “lock
in” clients), but regulators and fintech attorneys recommend ensuring a clear exit strategy .
We may also avoid exclusive reliance on a single bank – for example, using one bank for ACH/wire
services and another for card issuance, or maintaining a backup arrangement – to mitigate
concentration risk (as underscored by recent bank failures affecting fintech partners) .
Additionally, performing due diligence on the sponsor bank’s financial health and regulatory status is
critical. We should review the bank’s public filings and any enforcement actions. If a bank has a
history of BSA issues or is under a consent order (e.g. the OCC action against Blue Ridge Bank in
2022 for fintech partnership oversight ), that’s a red flag that our program might face stricter
scrutiny or abrupt policy changes. Red flags that can trigger sponsor banks to exit an MSB
relationship include: repeated exam criticisms of the MSB program, the MSB’s failure to promptly
remediate compliance findings, unacceptable levels of SARs or fraud incidents in the MSB’s
customer base, or negative news (e.g. if one of our sub-clients is implicated in wrongdoing). Sudden
changes in our business model without bank approval (for instance, expanding into a high-risk
country or asset class like virtual currency) can also cause termination – banks expect the MSB to
stick to the risk profile they were underwritten for. By operating within a conservative, well-defined
scope and communicating proactively, we can minimize surprises. Finally, monitoring the bank’s
stability (capital ratios, etc.) and having contingency plans aligns with Treasury’s recent de-risking
recommendations – e.g. Treasury has noted that MSBs often suffer from “de-risking” account
closures and suggests banks give adequate notice; we should still be prepared in case with alternate
banking options .
International/Institutional Client Considerations: Our model targets international business
clients – this adds complexity but can be managed. Foreign MSB or fintech clients (e.g. a foreign
fintech using our platform to access U.S. payments) may themselves trigger U.S. MSB rules. FinCEN’s
rules extend to “foreign-located MSBs” doing business in the U.S. and require them to register
with FinCEN and appoint a U.S. agent for service of process . Sponsor banks will be acutely
aware of this: if we onboard a foreign institution as a sub-MSB under us, the bank will likely ask
whether that entity is properly registered/licensed or truly operating as our agent. We may leverage
the agent model to argue the foreign entity is just an agent of our U.S. MSB (hence covered by our
registration), but the bank’s compliance team will scrutinize the arrangement to ensure no evasion of
BSA rules. When serving foreign clients, expect the sponsor bank to require enhanced due
•
23 24
25
25 26
27 26
28
29 25
•
30 31
4
diligence on those clients’ ownership, licensing in their home country, AML controls, and the
nature of their customers. The bank may even request a right to approve each significant foreign
sub-client. Institutional vs. Retail Exposure: Because our end-users are businesses and regulated
entities, there is less consumer regulatory risk, which banks appreciate. (For example, FDIC pass-
through insurance disclosures and Reg E error resolution are non-issues for purely corporate funds,
simplifying compliance.) However, serving foreign institutions can resemble correspondent
banking, an area of high concern for AML. The bank will expect us to know our clients’ AML
programs and possibly to obtain certifications or audit reports from them. Cross-border payments
also raise OFAC/sanctions considerations – the sponsor bank will require strict sanctions screening
on all international transactions and may prohibit dealings with certain high-risk jurisdictions
entirely (these restrictions will be built into our bank agreement). If currency exchange is involved,
the bank might insist on handling the FX through its own traders or approved intermediaries to
ensure reporting compliance. Additionally, under the U.S. “Travel Rule” for funds transfers, required
originator and beneficiary information must accompany cross-border wires ≥ $3,000 – our systems
and the bank’s systems need to capture and transmit all required data. The sponsor bank agreement
will likely spell out that any foreign correspondent relationships or payment corridors must be
disclosed and approved. We should be prepared to document how cross-border flows will work
(e.g. USD flows from our bank account to a foreign bank – with our foreign client perhaps on the
receiving end). Sponsor Bank Expectations for Our Model: Given our series LLC master/sub
structure, a prudent sponsor bank will expect the following: (1) Clear governance and control – the
parent (master) MSB should have the legal authority to dictate compliance policy to the series and to
enforce changes. The bank may ask for an org chart and management plan. (2) Single consolidated
compliance program – the bank will not want each sub doing its own thing; they will prefer one
harmonized program (one BSA officer at the parent level overseeing everything). They may require
that all BSA/AML obligations are centrally managed by the licensed entity (parent), treating sub-
accounts/series like branches or agents. (3) Disclosure of all sub-MSBs – we should anticipate
providing the bank with a list of our series clients, including for each: ownership info, business type,
jurisdictions of operation, expected volumes, etc. Ongoing, the bank might require notification or
approval before adding a new sub-MSB client, especially if it’s in a new industry or country. (4) Agent
agreement evidence – to comfort both regulators and the bank, we should have formal agent/
authorized delegate agreements between the parent MSB and each series client, explicitly stating
that the series acts on behalf of the parent for money transmission. This can be shown to examiners
to clarify that sub-MSBs are covered under the parent’s licenses (as permissible) . (5) Limits and
transactional controls – initially, the bank might impose conservative transaction limits (e.g. no
single client to process above $X million per day without review) and restricted products (e.g.
perhaps no cash deposits or no crypto-related transfers) aligned with our “minimal friction”
approach. Demonstrating our conservative posture – for example, highlighting that we do not serve
retail consumers or high-risk retail channels – will help in negotiations. Ultimately, banks that have
experience with fintech BaaS programs (e.g. certain community banks, some in fintech-friendly
jurisdictions or even digital banks in Puerto Rico) will be the most “tolerant” of a layered structure.
Such banks have built frameworks to manage multi-party programs and are accustomed to working
with program managers. They will still require, via contract, that we indemnify them for any
compliance failures and grant broad audit rights, but they are willing to work through the
complexity for the business opportunity.
10
5
The subsequent sections provide detailed analysis of each of these areas, including citations to relevant
laws, regulatory guidance, and industry resources, as well as a comparative table of sponsor bank
partnership models and a risk allocation matrix for compliance responsibilities.
1. Sponsor Bank Partnership Structures
1.1 Models for MSB–Bank Relationships
Direct Account Relationship (Traditional Banking): In the simplest model, an MSB opens a business
deposit account (or set of accounts) in its own name at a bank. The MSB then uses those accounts to
conduct its money services (e.g. receiving customer funds, disbursing payments) much like any business
would. The bank’s role here is fairly limited: it treats the MSB as a single high-risk commercial customer
under its BSA program. The MSB is responsible for all services it provides to its end-users, while the bank
monitors only the MSB’s aggregate account activity. There is no special “program” management by the bank
beyond standard account due diligence. Pros: This model is straightforward and avoids complex integration
– the MSB retains full control over its operations and compliance with minimal bank interference. Cons:
Many banks are unwilling to bank MSBs in this vanilla way due to de-risking concerns; those that do will
impose rigorous monitoring and might cap the types of transactions. Furthermore, the MSB must itself
obtain any necessary state licenses and registrations (which in our case, the parent has done). The bank’s
expectations under this model are still significant – per joint guidance, banks should confirm the MSB’s
FinCEN registration and state license status before opening an account , and understand the nature
of its business (services, customer base, geographies) . They may also ask whether the MSB is acting as a
principal or agent in providing services . If the MSB has a fleet of agents (like our series structure), that
immediately increases risk in the bank’s eyes, often prompting additional due diligence (e.g. requesting the
list of all agents and their locations) . In effect, a “direct account” MSB with sub-agents starts to resemble
a layered relationship anyway, which many ordinary banks shy away from. Only a few MSB-friendly banks
specialize in this. (Examples of banks known for servicing MSBs directly include certain community banks
and credit unions that advertise MSB accounts, as well as niche institutions like those in Puerto Rico or
elsewhere that actively court international MSB business .)
Banking-as-a-Service (BaaS) / FBO Accounts: In a BaaS model, the bank extends more than just a deposit
account – it provides an API platform or other technical integration allowing the fintech/MSB to create
and manage sub-accounts, virtual ledgers, or even issue payment instruments under the bank’s
infrastructure. Typically, the actual funds are held in a For-Benefit-Of (FBO) master account at the bank in
the name of the fintech/MSB (or directly in the name of the fintech’s customers, depending on structure).
For example, a fintech might maintain one omnibus account titled “MSB Inc. FBO Customers,” and in the
bank’s system have sub-account ledgers for each end customer. Another variant is where the bank actually
opens individual named accounts for each end user (with the fintech as an agent managing those
accounts). In both cases, the bank’s charter is being used to hold funds directly on behalf of the MSB’s end-
users, which has two major implications: (1) Regulatory status of the end-user funds – since they are in a
bank account, they usually enjoy FDIC insurance (pass-through, if eligibility requirements are met) and are
not considered “stored value” of the MSB for FinCEN purposes. This can help avoid the MSB being deemed a
“provider of prepaid access” in some scenarios because funds reside at the bank . And (2) Customer
relationship – often the bank legally treats the end-users as customers of the bank, even if the MSB is
the interface. That means the bank (and fintech) must ensure each end-user is CIP’d and screened. Many
BaaS banks effectively make the fintech’s users into direct bank customers (subject to the bank’s CIP
32
33
3
4
34
35 36
6
standards and account agreements), but delegate the onboarding and KYC work to the fintech via API
integration . The fintech in turn must comply with the bank’s required KYC vendors or methods (it’s
common for a sponsor bank to mandate use of certain identity verification tools or inclusion of certain
watchlist checks) . In this arrangement, the bank and fintech share responsibility: the bank provides
the license and accounts; the MSB provides the tech platform and customer interface. Because funds
are held at the bank, money transmission licensing can sometimes be bypassed in certain states – some
states view the bank as the one holding deposits and exempt the fintech if it’s merely an agent of a bank or
if an FBO construct is in place . (However, not all regulators agree, so we have taken the route of
obtaining licenses to be safe.) Pros: BaaS allows rapid scaling and offers customers insured accounts and
direct connectivity to payment networks (ACH, wires, card networks) through the bank. It also can reduce
regulatory friction – regulators are somewhat more comfortable since the bank is “in the loop” for every
transaction, not just in the background. Cons: It is complex to set up (technical integration, extensive
diligence) and can be costly (banks often charge per-user or per-API-call fees). The compliance burden is
actually dual: the fintech must meet bank-level compliance oversight (essentially being an outsourced
service provider for customer onboarding), and the bank must actively manage the fintech (including
regular audits and requiring approval for any program changes). Real-world examples: Many fintech
“neobank” apps (which are technically licensed as MSBs or program managers) use this model – for
instance, a fintech app offering mobile bank accounts will partner with a bank like Cross River, Evolve Bank
& Trust, or Coastal Community Bank. The bank holds deposits in FBO accounts and issues debit cards, while
the fintech handles the app interface and KYC flow. In our context, if we were to adopt a pure BaaS model,
each sub-MSB’s end customers could potentially have sub-accounts at the bank. However, that might not be
necessary since our clients are businesses themselves (the sub-MSBs). More relevant would be to have an
FBO account per sub-MSB, such that the bank holds the sub-MSB’s client funds. Our parent MSB could
maintain one master FBO account covering all series, or potentially a separate FBO for each series. These
nuances would be worked out with the sponsor bank.
Program Manager / Sponsor Bank Model: This model is prevalent in prepaid card issuance and certain
fintech programs. Here, the bank is not just providing accounts, but actually issuing payment
instruments (cards or similar) on behalf of the program. The non-bank partner (our MSB) acts as a
Program Manager, responsible for most operational aspects: marketing the program, onboarding
cardholders or users, customer service, managing card transactions via a processor, etc. The bank provides
the BIN sponsorship (so the cards carry the bank’s BIN/IIN and are on e.g. Visa/Mastercard), holds the
underlying pooled deposit of funds backing the cards, and ensures compliance. In many respects this
overlaps with BaaS, but the terminology “Program Manager” is used in card programs. The card networks
require that an issuing bank register and oversee any Third-Party Program Managers. The program
manager can be thought of as an agent of the bank for running the program. Our MSB in this role must sign
a Program Management Agreement with the bank and adhere to all network and regulatory rules.
Compliance allocation: The sponsor bank typically requires the program manager to handle day-to-day
BSA/AML for cardholders (CIP, transaction monitoring, recordkeeping), but under the bank’s oversight
and final authority . For instance, the bank might require pre-approval of the KYC questionnaire and
verification sources used for card sign-ups . The bank will also insist on prompt reporting of any
suspicious activity and may even require joint review of certain high-risk accounts. Practically, the program
manager does the work and the bank audits it. Regulators have explicitly held banks accountable for
failures in these arrangements: in 2022 the OCC took enforcement action against some sponsor banks for
“insufficient oversight” of their fintech program managers , sending a clear message that banks cannot
be hands-off. As a result, even in program manager models, many sponsor banks are now deeply involved –
some have staff embedded to review onboarding or have set automated alerts that feed into the bank’s
2
2
36 37
2
2
9
7
own AML systems. Others remain more “hands-off” on a daily basis, expecting the program manager to
manage everything and only checking in via periodic audits . We need to clarify a bank’s approach: Is the
sponsor heavily involved in compliance oversight or more passive? This can vary . Examples of sponsor
banks and programs: Banks like The Bancorp Bank, Pathward (MetaBank), Green Dot, and Sutton Bank
have historically issued prepaid or debit cards for program managers (think of prepaid gift card programs,
neo-bank debit cards, expense cards for businesses, etc.). On the fintech side, companies like Stripe or
Marqeta can act as program managers (or processors) enabling other brands to launch card programs, with
the actual bank in the background. If our MSB offers, say, a white-label gift card program for a client, our
MSB would be the primary program manager with the bank, and our client might be considered a
“sponsored program” under us. Notably, Galileo Financial (a card processor) describes program
managers as handling a wide array of tasks – from customer onboarding to fraud to settlement –
essentially running the program end-to-end, under the bank’s and network’s rules . We must
be prepared to fulfill that role if we enter this model.
Comparison of Models: The table below summarizes key differences:
Model Description Bank’s Role &
Exposure MSB’s Role Compliance Allocation
Direct
Account
MSB uses a
normal
business bank
account for all
funds flow. No
special program
integration.
Bank is depository
for MSB’s own
funds. Treats MSB
as single high-risk
customer. Limited
visibility into end-
users (bank sees
only MSB
transactions).
MSB handles all
customer-facing
operations, holds
customer funds
(off-bank or in its
account), and is
solely
responsible for
transmitting
money to
beneficiaries.
MSB does full BSA/AML
on its customers. Bank
does KYC/monitoring
only on MSB entity. Bank
files SARs on MSB if
MSB’s activities seem
suspicious (including if
MSB might be
unlicensed) . MSB
files SARs on its
underlying transactions
.
8
8
17 18
13
12
8
Model Description Bank’s Role &
Exposure MSB’s Role Compliance Allocation
BaaS /
FBO
(Banking-
as-
Service)
MSB integrates
with bank via
API; end
customers get
sub-accounts or
e-wallets held at
the bank (often
via an FBO
account
structure).
Bank holds
customer funds
(insured deposits),
often considering
end-users as its
own customers
legally. Provides
ledger
infrastructure and
payment network
connectivity (ACH,
wire, etc.).
Significant
oversight needed
as bank’s license is
directly used for all
transactions.
MSB acts as
technical service
provider/agent,
managing user
onboarding,
interface, and
transaction
instructions.
Often issues
frontend cards
linked to
accounts.
Joint compliance: Bank
sets standards and
retains ultimate
responsibility; MSB
performs onboarding
KYC, monitoring, and
day-to-day compliance
tasks per bank’s
requirements . Bank
typically must approve
KYC/CDD processes and
may require specific
vendors or controls .
Both bank and MSB file
SARs as appropriate
(bank for its customer
accounts, MSB possibly
via the bank or as an
MSB if also registered).
2
2
9
Model Description Bank’s Role &
Exposure MSB’s Role Compliance Allocation
Program
Manager
(Card
Issuance)
MSB (Program
Manager) runs
a branded card
or payment
program while
a sponsor bank
issues the cards
and holds the
funds. Often
involves a third-
party processor
for card
transactions.
Bank is the
licensed card
issuer (BIN
sponsor) – it is a
member of Visa/
MC and is
accountable to
regulators and
networks. Bank
approves program
parameters (fees,
limits, target
customers) and
ensures the
program complies
with all rules.
Holds the
underlying account
or pooled funds for
card value.
MSB Program
Manager handles
marketing,
distribution of
cards,
onboarding
cardholders,
customer service,
settlement and
transaction
management (via
processor), etc.
Basically
operates the
program on the
bank’s behalf.
Delegated compliance
under oversight:
Program Manager must
follow the bank’s BSA/
AML policy and network
rules for the program.
PM conducts CIP for
cardholders, transaction
monitoring, anti-fraud,
etc., and reports
outcomes to bank
. Bank audits and can
dictate changes. Bank
remains liable if program
has compliance failures –
regulators will fault the
bank for “insufficient
oversight” if something
goes wrong . Thus
bank often requires
regular reports and can
intervene in high-risk
decisions (e.g. approving
onboarding of a higher-
risk client or suspicious
account closures).
Table 1: Primary Models of MSB–Bank Partnerships and their Role/Compliance Allocations.
It’s worth noting these models can blur. For instance, a program manager setup often uses an FBO account
at the bank for the pooled funds (a BaaS element), and a direct account MSB might evolve into a quasi-
program if the bank starts providing more services. For our purposes, we are likely straddling between
Direct Account and Program Manager models: we need a bank to provide underlying accounts and
payment rails for our series clients (somewhat beyond a simple account, since we may need sub-accounts
for each series or each client’s funds), and possibly to issue branded prepaid cards for those clients’
programs (which is clearly a Program Manager scenario). We should therefore expect to operate under a
hybrid of the BaaS and program manager compliance expectations, meaning intensive upfront diligence
and ongoing cooperation.
17
18
9
10
1.2 Sponsor Bank Evaluation of White-Label/Sub-MSB Models
From the bank’s perspective, an MSB that itself has multiple MSB “sub-clients” is a layered and higher-risk
relationship. Banks will approach onboarding systematically:
Initial Disclosure & Narrative: We must clearly articulate our business model in writing for the
bank’s risk committee. This includes an overview of the parent-series structure, the rationale (e.g.
series act as independent business lines or client programs under one licensed umbrella), types of
services we enable (ACH transfers, prepaid card issuance, etc.), and the fact that the parent MSB
holds all relevant licenses. Banks have indicated they want to understand if the MSB is new or
established, and whether money services are its primary line of business or ancillary . In our case,
money services are the core, which elevates the need to demonstrate sophisticated compliance.
Verification of Credentials: The bank will verify our FinCEN registration and any relevant state
licenses. FinCEN’s joint guidance states that confirming an MSB’s registration and license status is
“the most basic” obligation and that banks should not even open the account until that’s confirmed
. We should be ready to provide copies of our FinCEN registration acknowledgment (for the
parent LLC) and our Montana license, plus any other state MT licenses we hold or a list of states
where we operate under exemptions. If some series operate in states via the parent’s license or as
agents-of-the-parent, that needs to be explained and backed by legal rationale. Providing a legal
opinion or memo on our structure’s compliance with state laws could help satisfy due diligence.
Agent/Series Information: Expect the bank to ask: How many sub-MSBs or series do you have? Who
are they? Where do they operate? What services do they offer and to whom? This ties to guidance that
banks should determine if the MSB customer is a principal with agents and review the list of
agents including locations . We should prepare an “agent list” for the bank, similar to what we’d
maintain for FinCEN. This list would detail each series name, principal business address, ownership
(if different from the parent’s ownership), and a description of its business (e.g. “Series A – facilitates
cross-border B2B payments for a UK-based fintech, acting as that fintech’s U.S. agent under our
license”). We should also note which of those are foreign-owned or serve foreign customers, as that
draws extra scrutiny (the 2005 guidance mentions noting agents “within or outside the United
States”) . Banks may worry about foreign-located agents due to difficulty in oversight, so we
must emphasize our controls over any such agent.
Risk Assessment & KYC on Each Sub-MSB: The sponsor bank will treat each significant sub-MSB
almost like a customer in its own right. They will likely perform KYC on the beneficial owners of
each sub-MSB (e.g. if one series is a joint venture with an international partner, the bank will want to
CIP that partner). They’ll want to know each sub’s target market and expected activity: Are they
dealing with only corporate payments? Any cash or crypto? Any higher-risk corridors (e.g.
remittances to high-risk countries) or high-risk industries (online gambling, etc.)? We should be
prepared with a profile for each. If any sub-MSB’s business is too risky for the bank’s appetite, the
bank might exclude it or require it be dropped. For instance, if one client series wanted to do crypto
exchange, a bank that is otherwise okay with MSBs might balk at a nested crypto MSB. Therefore,
aligning our sub-clients with the bank’s comfort zone is crucial. Given our “conservative posture” (no
high-risk retail, no ambiguous regulatory areas), this alignment is likely if we choose the right bank.
•
3
•
32
•
4
4
•
11
Responsibility & Compliance Capacity: The bank will evaluate our MSB’s ability to manage the sub-
MSB structure. They may ask: How do you ensure your agents comply with BSA/AML? Do you conduct
audits of your sub-MSBs? What are your enrollment criteria for a new client (series) and how do you vet
them? Essentially, the bank will transpose the questions they normally ask of an MSB to the entire
enterprise, including sub-entities. We should have in place written agent management policies, as
FinCEN recommends: including agent due diligence procedures, ongoing monitoring, and clear
termination rights/practices if an agent misbehaves . Presenting these to the bank will
demonstrate we actively manage our sub-MSBs, reducing the bank’s fear that something in the
chain is out of control. This is analogous to how Western Union or MoneyGram (large MSBs) manage
networks of agents and how they satisfy banks/regulators that those agents are overseen.
Financial Requirements: Many sponsor banks impose financial criteria on fintech/MSB clients.
Commonly, they may require a certain minimum capital or cash reserve to be maintained by the
MSB. They could also require a reserve deposit (e.g. an amount equal to a few weeks’ worth of
processing volume) to hedge against losses or chargebacks. Contractually, the bank will hold broad
set-off rights to seize funds from our accounts if needed to cover liabilities . While this is more
about contract terms (discussed in 1.5), during evaluation the bank might ask about our financial
wherewithal: Can you cover potential losses? Do you have investors or steady revenue streams? Since we
cater to B2B clients, the absolute volumes per client might be large, so the bank needs to know we’re
financially sound. Presenting a strong balance sheet or parent guarantee could be necessary.
Use of Technology & API: If our model requires technical integration (likely yes, for real-time sub-
account info, or issuing cards), the bank will assess our tech stack. Some smaller banks rely on third-
party BaaS platforms (synonymous with processors) like Synapse, Treasury Prime, Galileo, etc., to
interface with fintech programs. In such cases, we’d also be evaluated by that platform. Other banks
have in-house APIs. We should clarify how we plan to integrate and whether we need the bank to
support instantaneous sub-account ledger updates for multiple series. The complexity here might
narrow down which banks are feasible (e.g., a bank that only wants to give you a single account with
batch wires might not be suitable if we need fine-grained ledgering and card issuing).
Tolerance for Layering: The question specifically asks which banks tolerate layered structures.
Through industry knowledge, some banks in the U.S. and territories specialize in higher-
complexity fintech partnerships. For example, Evolve Bank & Trust and Cross River Bank have
multiple fintech programs including those that themselves support sub-programs. Metropolitan
Commercial Bank (NY) previously banked many crypto and international fintech programs (though
it recently refocused away from crypto). Niche banks like Sunrise Banks, Lincoln Savings Bank,
Sutton Bank, Celtic Bank, and newer entrants like Column or Piermont might be candidates. In
Puerto Rico, International Financial Entities (IFEs) such as FV Bank explicitly target global fintech
business and may be comfortable with an MSB that serves foreign sub-clients . These institutions
are accustomed to performing enhanced due diligence and ongoing monitoring for complex clients
as a matter of business. On the other hand, many regional/community banks have a blanket policy
against any MSB accounts or certainly against nested arrangements. We will likely focus on those
known as “MSB-friendly” or “fintech sponsor” banks. According to industry sources, there is a
curated list of MSB-friendly banks that is updated regularly – leveraging such resources or
consultants (e.g. MSB compliance associations, Faisal Khan’s consultancy, etc.) can save time in
identifying receptive banks.
•
4
•
22
•
•
34
38 39
12
In summary, sponsor banks will scrutinize not just us (the parent MSB) but also our sub-clients and our
ability to manage them. Our preparation in providing complete and clear information will heavily
influence whether a bank is willing to take us on and under what conditions. As FinCEN noted in its MSB
banking guidance, “not all money services businesses pose the same level of risk”, and banks are encouraged to
apply case-by-case judgement . By demonstrating that our particular model has mitigating factors
(licensed parent, robust compliance, B2B focus, etc.), we can position ourselves as an acceptable risk within
the MSB category, even with the added complexity of sub-entities.
1.3 Division of Compliance Responsibilities (Bank vs MSB vs Sub-MSB)
One of the first questions a sponsor bank will have is: Who is doing what, compliance-wise? Laying out the
responsibilities at each level helps avoid misunderstandings. Typically:
Sponsor Bank’s Responsibilities: The bank retains responsibility for overall BSA/AML program
implementation for its institution, which by extension covers any services it provides to the MSB
program . Regulators will hold the bank accountable if the program is mismanaged. Concretely,
the bank must perform due diligence on the MSB (as described), incorporate the MSB and its agents
into the bank’s risk monitoring (often by treating the whole program as a high-risk customer
category in the bank’s AML system), and file SARs or take action if it detects suspicious activity.
For example, if the bank sees unusual flows (like rapid in/out wires through our accounts that look
like layering of funds) or if it learns our MSB is not complying with BSA (perhaps through exam
findings or if we missed a registration), the bank should file a SAR or even terminate the relationship
. The bank is also responsible for OFAC sanctions compliance on any transfers it processes
for us – in practice it will rely on automated screening of all wires/ACH and may expect us to do the
same on our side. In a BaaS or card issuance arrangement, the bank typically also handles certain
regulatory reporting: e.g., the bank will include the deposits and transactions from our program in
its Currency Transaction Reporting (CTR) aggregation if relevant (though most of our transactions
likely won’t be cash). If a cash deposit does occur at the bank (less likely given our model, but
suppose a sub-MSB client sends a physical check or cashiers check), the bank might need to file
CTRs. For SARs, it’s worth noting that there could be overlapping obligations – the bank might file a
SAR on suspicious activity in the account, while our MSB should file a SAR on the same activity
through our own MSB lens. FinCEN has said that if a bank knows a customer is an MSB, and that
customer might be unlicensed or doing suspicious transactions, the bank should file a SAR .
Conversely, we as an MSB must file SARs for any suspicious transactions by our clients or their
customers (since we are a money transmitter, the SAR rule applies to us) . This duplication is
acceptable and common; FinCEN receives SARs from multiple filers about the same underlying
actors and uses both. The bank will also take charge of any required regulatory notifications
related to the program (for instance, if there is a data breach affecting cardholders, the bank as
issuer might have to notify its regulators or the network).
Parent MSB’s Responsibilities: Our company (the parent MSB LLC) is the central point for
compliance operations for the entire program. We must maintain a written AML program that
meets FinCEN’s standards (the four pillars: internal controls, compliance officer, training,
independent review) and covers the activities of all series/agents . Practically, this means we will
conduct KYC/KYB on each sub-MSB client and possibly (depending on model) on the sub-client’s
customers. It means we will monitor transactions flowing through each series for red flags (we likely
need transaction monitoring software capable of multi-entity tracking). We will file SARs and CTRs as
40
•
2
11 13
13
12
•
14
13
required: e.g., if a series processes a large cash transaction for its end customer, we (the parent)
would file a CTR (the series is acting under us, and FinCEN guidance is that the principal MSB files
reports for agents as needed). For SARs, if any suspicious pattern emerges in an agent’s activities, we
file the SAR (and might mention the agent in the narrative). Can sub-MSBs file SARs
independently? FinCEN’s rules say an agent MSB not registered on its own is not separately
obligated to file SARs – that obligation rests on the registered entity (parent) . So the sub-MSB
should feed the info to us, and we do the filing. If a series is separately registered as an MSB (not our
plan, but hypothetically), it would need its own SAR filings. But our structure intends the series to
operate under the parent’s registration (and license), so the compliance program and filings are
centralized. The parent MSB also is responsible for training and auditing the sub-MSBs. We should
be conducting periodic audits of each series (or at least the risky ones) – checking they follow KYC
procedures, reviewing samples of their customer onboarding, etc. The sponsor bank will likely ask
for copies of our independent AML review reports. FinCEN requires MSBs to do an independent
review of their AML program periodically (annually for large MSBs). We should ensure the scope of
that review includes our agent oversight. If we have not had an independent audit yet (as a startup),
the bank may require one shortly after onboarding. Also, the parent MSB is typically the point of
contact for law enforcement inquiries (e.g., if there’s a subpoena or 314(a) request, it comes to us,
not to each agent). The sponsor bank may stipulate in the contract that if they receive a legal order
or inquiry about a transaction, we must assist promptly in gathering information from the agent or
end customer.
Sub-MSB/Agent’s Responsibilities: Each series or agent – our client – must adhere to the
compliance program we set. In practice, they will perform customer due diligence on their own
customers (the end-users) if that is part of their role. For example, if Series A’s business is to
onboard non-U.S. businesses who want to pay U.S. vendors, Series A will collect KYC info on those
businesses (likely using our standardized KYC requirements). The series will also have front-line
responsibility for screening for sanctions or suspicious indicators in their customers’ activities,
since they have the direct relationship. Our program may require the agent to implement certain
automated screening (we can provide tools or require they use specified vendors, akin to how
sponsor banks dictate to fintechs). Agents are usually required to keep records of customer IDs,
transaction logs, etc., and to report up-line any anomaly. For instance, if a sub-MSB’s customer tries
to break a large transaction into structured smaller ones, the sub-MSB should catch that and
escalate to us. The agent is also tasked with marketing and customer interaction under
compliance guidelines – e.g., if they’re selling a white-label card, they must only make claims
consistent with the actual product (no misrepresenting FDIC insurance, etc.). Some sponsor banks
will insist that all customer-facing materials (even those branded in the agent’s name) be pre-
approved by the bank or program manager to ensure compliance (especially for things like FDIC
insurance representation, which the FDIC has been scrutinizing) . In short, sub-MSBs have to
operate as if they are an extension of our MSB – they must follow all the same rules and are subject
to oversight. We in turn are responsible to the bank for ensuring the agents do this.
A helpful concept is to view the compliance responsibility as cascading but with oversight at each level:
The bank oversees us (the MSB), and we oversee our agents. This “compliance waterfall” means any issues
at the bottom should be escalated upwards. For instance, if an end customer of a sub-MSB is found to be on
an OFAC list, the sub-MSB should freeze the activity and report to us; we then report to the bank (and both
we and the bank would file any required blocked property or SAR reports). Our policies should formalize
this flow: requiring agents to notify the parent MSB of certain events (e.g., any subpoena received, any
41
•
42
14
positive sanction hit, any SAR-worthy activity). The sponsor bank agreement will likely mirror that by
requiring us to notify the bank of those events promptly. As OmniWire’s guidance to fintechs notes, a critical
question is whether the sponsor bank is hands-on or expects us to manage everything – we should assume
they will want regular reporting at least .
One area to delineate is consumer compliance: Because our focus is B2B/institutional, consumer
protection laws (Reg E, CFPB rules, etc.) are less of an issue except in the gift card scenario. If we do handle
any consumer-facing stored value (say a gift card program for a business client), then responsibilities for
things like error resolution, disclosures, and complaints need to be assigned. Generally, the program
manager (us) handles customer service and error claims under oversight, and the bank makes sure the
processes meet regulatory timing/standards. For example, Reg E error investigations: we (and our agent)
would investigate a disputed card transaction and provisionally credit the customer if needed, but the bank
as issuer ensures the process is done within required timeframes. These details would be spelled out in the
program management agreement and our agent agreements.
In summary, the sponsor bank remains the backstop for compliance – regulators view the bank as
responsible for everything its fintech partner does (since the bank provides the license and access) . The
bank thus pushes down compliance duties to us via contract. We, in turn, push down appropriate duties to
our agents via contract. But no party can fully abrogate oversight: the bank must verify we are doing our
job, and we must verify our agents do theirs. Everyone in the chain should be implementing an AML
program appropriate to their role. Indeed, industry guidance for BaaS partnerships stresses that each
party must have an AML program and the contracts should spell out who is doing Customer
Identification, who monitors transactions, who files what reports . We will ensure our agreements
with agents mirror any obligations the bank puts on us (so we can upstream information and maintain
consistency).
1.4 Banks Actively Sponsoring MSB Programs (Layered Structures)
Not all banks are willing to sponsor MSB programs, let alone those with nested sub-clients. However, a niche
of banks has emerged that specialize in fintech and MSB partnerships:
Fintech-Focused Sponsor Banks (Mainland U.S.): These are typically mid-size or community banks
that have built significant “Banking-as-a-Service” lines of business. Examples include Cross River
Bank (NJ), Evolve Bank & Trust (TN), Metropolitan Commercial Bank (NY), The Bancorp Bank
(DE), Pathward, f.k.a. MetaBank (SD), Sunrise Banks (MN), WebBank (UT), Celtic Bank (UT),
Lincoln Savings Bank (IA), Coastal Community Bank (WA), NBKC Bank (KS), and a few others.
These banks have multiple fintech clients and are known to be more comfortable navigating
compliance for non-traditional programs. For instance, Cross River and Evolve have been behind
many popular fintech apps (from peer-to-peer payment apps to crypto on/off ramps). That said,
regulators have started scrutinizing them closely; as noted earlier, Cross River came under FDIC
enforcement for fair lending issues related to fintech lending partners , and Blue Ridge Bank (VA),
another sponsor bank, was hit with an OCC consent order that, among other things, forced it to seek
regulatory approval before adding new fintech programs . This shows that while these banks are
active in the space, they also are under pressure to be selective and diligent. A layered MSB structure
could be a tougher sell unless we show impeccable controls. Still, these banks have in some cases
partnered with businesses that enable other businesses. For example, some sponsor banks work with
8 43
44
45 46
•
47
28
15
payment facilitators (PayFacs) which themselves sign up sub-merchants – an analogous layering in
merchant payments.
Crypto/Forex-Friendly Niche Banks: A subset of banks (until recently, including Silvergate and
Signature Bank, now closed) was known for working with crypto exchanges and FX remittance firms.
Currently, a few players like Customers Bank (PA) or Western Alliance Bank (AZ) have been
mentioned in context of fintech partnerships. But after 2023’s events, many are more cautious.
Primarily, MSBs dealing with crypto or overseas entities often turned to smaller institutions or
state-chartered banks in niche markets. Some state-chartered banks in Wyoming have special
crypto charters (though their status is uncertain at federal level). For traditional MSB payments,
Community Federal Savings Bank (NY) has been known to serve as an ACH sponsor for remittance
companies (they sponsored TransferWise’s debit product early on, for instance). These banks might
consider layered structures if, say, the sub-MSBs are foreign licensed remittance companies wanting
a U.S. intermediary. They will focus on ensuring one compliance standard across all.
Puerto Rico and Offshore: Puerto Rico’s International Financial Entities (IFEs) function similarly to
banks (they can hold deposits and have access to Fed wire/ACH as participant banks in Fed systems).
FV Bank (Puerto Rico IFE) for example positions itself as a global digital bank serving fintechs and
crypto companies, offering API-based accounts and even digital asset custody . It effectively
sponsors fintech programs under its own IFE license. Another Puerto Rico IFE, San Juan Mercantile
Bank, was geared towards digital asset firms. These institutions are attractive for international-
facing models because they have tax advantages and a mandate to serve non-U.S. clients (IFEs must
mainly serve non-Puerto Rico clients). They might be more tolerant of foreign sub-clients and multi-
layer setups, as they operate somewhat like offshore banks but under the U.S. flag. Outside of PR,
Crown Agents Bank (UK) and other EMI-friendly institutions could be relevant if we ever need a
non-U.S. bank for parts of the business, but for U.S. payment rails a U.S.-licensed bank/IFE is needed.
Lists and Directories: The MSB industry keeps informal lists of “MSB-friendly banks.” For example,
the Money Services Business Association (MSBA) and the Conference of State Bank Supervisors
(CSBS) have worked on educating banks that compliant MSBs should not be indiscriminately
debanked. Faisal Khan, a cross-border payments consultant, maintains a public list of MSB-friendly
banks globally . The list (as of early 2025) includes U.S. and international banks known to
work with high-risk clients. To protect the relationships, such lists don’t always publish names
publicly without contact, but some known names on recent lists for U.S. include: Evolve, Metropolitan
Commercial, Blue Ridge (subject to OCC oversight currently), Sutton, CFSB, and a few credit unions
that have tailored programs. Canadian and European banks sometimes are used for MSB flows,
but since our focus is U.S. sponsor, we stick to U.S./PR.
Tolerance of “Layered” Agent structures: Even among sponsor banks, some may shy away from a
structure where our clients themselves behave like MSBs. Many prefer that the fintech brings
individual end-users, not other MSBs. However, our narrative can reframe the sub-MSBs as “program
partners” or “distribution agents” of our MSB service, rather than independent MSBs. If our sub-
clients are regulated entities (say a foreign bank or fintech using our platform), that actually could
increase comfort if those entities are reputable – the bank might take comfort that, for instance, our
client is a licensed financial institution in its home country, with its own AML controls. On the flip
side, if our client is a startup fintech in a light-touch jurisdiction, the bank might worry about weak
controls filtering into the U.S. system. So, identifying sub-clients that are themselves well-regulated
•
•
34
•
38 39
•
16
(like maybe a fintech that’s licensed in the UK/EU, or a company that’s a publicly listed entity, etc.) will
help. We should highlight any regulatory status of our clients when talking to the bank.
In conclusion, banks that actively sponsor MSB programs do exist, but they form a relatively small
community. We will need to pitch our model to those that have a track record with fintech partnerships,
ideally citing analogous cases (e.g. “Bank X currently works with Program Y which has multiple corporate
partners – our model is similar”). Since layered MSB setups are somewhat unique, we might find ourselves
educating the bank’s compliance team on how FinCEN allows agents to operate under a parent’s
registration . Providing that regulatory citation to them can be persuasive (“FinCEN explicitly permits our
structure, see footnote in guidance…”) and showing that we’re not trying to hide the ball – we’ll give them
full transparency on all players involved.
1.5 Typical Contractual Terms in Sponsor Bank Agreements
When we do find a willing sponsor bank, the partnership will be governed by a detailed contract (often
called a Program Manager Agreement, Sponsorship Agreement, or BaaS Services Agreement). We need to
be prepared for the key terms, which often include:
Reserve and Collateral Requirements: As touched on, banks often require the fintech/MSB to
maintain a reserve. This could be a percentage of outstanding stored value (for prepaid programs)
or a fixed security deposit. The contract will give the bank broad rights to increase the reserve if risk
grows. Additionally, setoff rights are standard: the bank can debit any of our accounts to cover
amounts due. Notably, banks may even assert setoff against accounts not directly related to
the program – e.g. if we hold an operating account at the same bank, they might include that in the
setoff clause . We should negotiate to limit setoff to program funds, but smaller MSBs often have
to agree to wider setoff because the bank wants maximum protection. Termination clauses
sometimes allow the bank to hold reserves for a period (e.g. 6–12 months) after termination to cover
any trailing chargebacks or disputes.
Fees and Revenue Share: Sponsor banks charge various fees – setup fees, monthly fees, per-
transaction fees, etc. Some also take a revenue share (for example, a cut of interchange revenue on
cards, or a share of FX margins). While this isn’t a compliance matter, it’s a significant business term.
We should compare fee structures among potential banks. Some newer banks or IFEs might have
higher fees due to lower economies of scale, whereas bigger players like The Bancorp or Stripe’s
partner banks might be more standardized in pricing. This is where a comparison table of major
sponsor banks would help, but since much of that is proprietary, we will rely on RFP processes to
gauge pricing.
Transaction Limits and Controls: The agreement will specify what types of transactions are allowed
and any limits. For instance, it may cap daily ACH volume or the number of new accounts per month
initially. This is both to manage the bank’s risk and to ensure we don’t exceed what they’ve modeled.
Many banks use a gradual ramp-up approach: they allow small volumes at first, monitor how we
handle it, and then approve higher limits. They might also require certain transaction types to be off-
limits – e.g. no international wires without prior notice, or no third-party check deposits, etc. Since
we mostly focus on electronic payments, we likely won’t have checks or cash anyway, which aligns
well. We should clarify upfront if cross-border ACH/wires are permitted (some sponsor banks only
handle domestic unless special arrangements are made).
10
•
22
•
•
17
Termination Rights: Sponsor bank contracts often heavily favor the bank. They will include the right
to terminate for cause (including any material compliance issue, regulatory order, your license loss,
etc.) usually with immediate effect or short notice. Many also include a clause allowing the bank to
terminate without cause with a certain notice period (sometimes 30 or 60 days). From our
perspective, a notice period is critical if no cause – we need time to migrate our program. We will try
to negotiate at least 90 days notice for termination without cause, given the complexity of moving
sub-clients to a new bank. However, the bank may insist on shorter. In any case, the contract should
explicitly grant us the ability to transition our program and customer funds to a new
institution in the event of termination . One point from the MoFo fintech tips: fintechs should
avoid contracts that effectively trap their program (like overly restrictive exclusivity or non-compete
clauses with other banks, or the bank owning the customer relationship outright) . We need
an out if things go south. Likewise, we should expect termination for regulatory reasons – e.g., if
the bank’s regulator orders them to shut down our program, they can terminate immediately. That
scenario did happen in some cases historically.
Regulatory Cooperation and Audit: The contract will require us to provide any information the
bank requests to satisfy its regulators or auditors. For example, if the OCC or FDIC comes for an
exam of the bank’s fintech partnerships, they often ask for detailed info on each program. We must
cooperate, which can mean responding within a few days to extensive inquiries. The bank will also
have the right to audit us (and our agents), typically with some notice. They might conduct an
annual audit or send questionnaires regularly. We should be ready to allocate resources for these
oversight activities. Often, if they find deficiencies, the contract will require us to remediate in a fixed
time or risk suspension of the program.
Compliance Delegation Clauses: The agreement will spell out which party is responsible for each
aspect of compliance. For example: “MSBCo shall be responsible for conducting CIP on all End Users
in accordance with Bank-approved procedures. Bank will verify a sample or may conduct additional
checks at its discretion.” Or “MSBCo will monitor transactions and report suspicious activity to Bank.
Bank will file SARs as appropriate, and MSBCo shall not file SARs on End User activity without Bank’s
prior consultation.” Some banks prefer to file all SARs themselves (to avoid two filings) while others
allow/require the fintech to file SAR as an MSB too. We will clarify that during integration. The
contract may also allocate SAR filing responsibility – noting that since we are a registered MSB, we
have independent SAR obligations, but we might agree to notify the bank of any SAR we file related
to the program, especially if it involves any wrongdoing by an end-user that could also affect the
bank. In any event, the contract will ensure the bank has final say on compliance matters – e.g.
if the bank directs us to close a certain customer account due to risk, we must do so promptly.
Indemnification and Liability: We will be expected to indemnify the bank for any losses, fines, or
legal costs arising from our program (except those due solely to the bank’s negligence or willful
misconduct). This includes if a regulator penalizes the bank because of something in our program, or
if a card network fine comes in (networks sometimes fine issuers for excessive fraud or compliance
violations – the bank will pass that to us). Our indemnity should extend to any agent’s wrongdoing as
well (since from the bank’s view, agents are part of our operation). We need to be comfortable that
we can stand behind that or have insurance to cover some risks (e.g. cyber insurance if a data
breach, etc.). Also, many agreements limit the bank’s liability heavily (often no liability for indirect
damages, and cap on direct damages possibly equal to fees paid). Meanwhile, our liability via
•
25
26 25
•
•
•
18
indemnity is often uncapped (for compliance matters especially). This one-sidedness is typical given
the power balance.
Exclusivity: Some bank agreements ask for exclusivity (meaning we can’t use another bank for the
same program). In MoFo’s tips, they caution fintechs on agreeing to blanket exclusivity as it limits
scalability . We might try to avoid exclusivity or at least carve out that we could use other banks
for other products or geographies. Banks ask for it to ensure volume and that they recoup their risk
overhead by being sole provider. Perhaps we compromise by agreeing to give them first right of
refusal for new programs, etc., but ideally keep flexibility. If we do agree to exclusivity for U.S. dollar
payments, we need a very strong transition clause in case the bank relationship sours.
Subcontracting / Agents: Because our model involves agents, the contract will likely require us to
list any third parties involved in offering the services and possibly require the bank’s approval of
each. For example, it might say “Bank approves MSBCo utilizing the agents listed in Appendix X to
assist in distribution of services. MSBCo must obtain Bank’s prior written consent to add any new
agent or sub-program under this Agreement.” This gives the bank veto power on new series clients.
We should be prepared for that. The bank might require us to incorporate certain terms into our
agent agreements – effectively “flow-down” provisions to ensure agents comply with bank
requirements (for instance, that agents will provide information during audits, or that agents won’t
themselves further subcontract critical functions without approval).
Termination of Individual Agents: Similarly, the bank may reserve the right to demand we
terminate a relationship with a particular sub-MSB if they pose a problem. If, say, one of our series
had a major AML issue or got in trouble with a regulator, the bank might instruct us to sever that
agent from the program to protect the bank. Our agent agreements should thus have clauses
allowing us to terminate on short notice if required by our bank or regulators (so we can comply with
that without breaching contract with the agent).
Data and Audit Access: The bank will likely require full access to program data. Increasingly, banks
use automated tools or audit modules (Alloy, e.g., launched a tool for sponsor banks to directly
review fintech customer onboarding or audit data) . Our systems should be ready to produce
reports or even live API feeds to the bank of key metrics (number of users, volumes, any suspicious
incidents, etc.). Data security and confidentiality also come into play – we’ll want a reciprocal clause
that the bank must keep our customer data confidential and use it only for compliance and servicing
(some fintechs worry banks might poach customers if they have data – but reputable sponsor banks
don’t typically do that).
Regulatory Change & Compliance with Law: There will be a clause that if laws or regulations
change or new guidance comes out (say, CFPB decides to regulate something new, or a state
changes licensing rules), we and the bank will work in good faith to modify the program, and if we
cannot comply, the bank can terminate. This is standard to cover unforeseen regulatory shifts.
Governing Law & Jurisdiction: Often the bank will insist on their home state law governing and that
disputes be handled in their local courts or arbitration. If our bank is out-of-state (likely), we have to
accept that. It’s usually not negotiable for smaller partners.
•
26
•
•
•
48
•
•
19
Finally, we should mention example terms in context. For instance, MoFo’s fintech article notes that
fintechs should ensure they have rights to transition the program to a new bank and not let the bank
limit that unduly . It also notes sponsor banks often try to limit such transitions in timing or scenarios
. We will heed that advice in negotiations. Additionally, sponsor banks might include financial
covenants (like requiring us to maintain certain net worth) or reporting covenants (regular financial
statements to them, notification of any regulatory inquiries involving us, etc.).
In summary, the sponsor bank agreement is comprehensive: it effectively deputizes us to act on the bank’s
behalf for certain services, while imposing extensive duties to make sure the bank stays safe and compliant.
Being aware of these typical terms means we can plan (e.g., have capital ready for reserves, align our agent
contracts to allow quick compliance with bank demands, etc.). We’ll also likely have to undergo the bank’s
vendor management process (since the regulators treat fintech partners as vendors or third parties to the
bank). The OCC’s Third-Party Risk Management guidance (OCC Bulletin 2013-29 and updated versions)
requires banks to assess and manage risks of their third-party relationships. We should expect to fill out
detailed questionnaires about our business, financials, compliance, and agree to ongoing oversight. This is
just part of doing business in the sponsor bank realm.
(The above outlines reflect common industry practices and are substantiated by regulatory guidance and expert
commentary: for instance, the emphasis on due diligence and strong contracts comes from OCC/FDIC guidance
and enforcement actions , and the need for clear allocation of compliance duties in contracts is noted in
compliance checklists for BaaS relationships .)
2. Compliance Delegation Frameworks
2.1 BSA/AML Compliance Allocation in Sponsor Bank Agreements
As introduced, a sponsor bank partnership essentially creates a chain of delegated compliance, but with
the bank retaining ultimate responsibility. In formal terms, the Bank Secrecy Act (BSA) and its implementing
regulations (31 CFR Chapter X) hold banks and MSBs both individually responsible for maintaining effective
AML programs and controls. When they partner, they cannot eliminate that responsibility, but they can
allocate tasks between them.
Typical Framework: The sponsor bank will outline in the agreement or policies which BSA/AML functions
are to be performed by the fintech/MSB and which by the bank. A common division is: the fintech/MSB
handles customer-facing compliance (identity verification, due diligence, monitoring of usage, sanctions
screening at onboarding and ongoing) and the bank handles oversight and regulatory filings. For
example, the contract might state the fintech must “implement an AML program consistent with the Bank’s
standards and applicable law” and that the fintech will provide all information necessary for the Bank to
file currency transaction reports and suspicious activity reports. Sometimes the bank wants to file SARs
itself (especially if the SAR pertains to the bank’s customers in a legal sense), but it needs data from the
fintech.
In some arrangements, the sponsor bank directly provides certain compliance services: KYC utilities or
transaction monitoring systems the fintech must use. It’s not unusual for a bank to say, “You must run all
new customers through XYZ compliance software (e.g., Alloy, Socure, LexisNexis) that we approve, and we
must be able to review the results or have a say in edge cases.” . The bank might also require that all
potential matches to sanctions or PEP lists are escalated to the bank for a decision.
25
49
50 51
45 46
2
20
Sponsor Bank’s Role: The bank’s own BSA officer will include the fintech program in the bank’s risk profile.
They often create a dedicated “Fintech Sponsor” BSA team internally. This team might do things like
quarterly audits of a sample of customers onboarded by the fintech to ensure CIP was properly done, or
run independent transaction scans on the fintech’s transactions to see if the fintech is catching what the
bank’s systems would catch. The OCC and FDIC, in their examination manual updates, have stressed that
banks must have sufficient staff and expertise to oversee fintech partnerships, which includes evaluating
the fintech’s compliance performance. So we can expect periodic questionnaires or on-site meetings where
the bank reviews our procedures, training materials, etc.
Fintech/MSB’s Role: We as the MSB must essentially function as an extension of the bank’s compliance
team for our customers. We will likely be required to appoint a dedicated compliance officer for the
program (we have one, but the bank might even want to interview that person or ensure they are
qualified). The fintech must follow all BSA program elements: internal controls (which the bank will want to
see), training (they may ask for evidence that our staff and agents get AML training regularly), independent
review (we may need to send them the results of our independent audits) . In addition, since we have
sub-agents, our program must extend training and oversight to those agents, and we should be able to
document that (the bank could ask, “show us that Series B had AML training this year” or “how do you verify
Series C is screening for OFAC?”).
Sub-MSB’s Role: As noted, subs carry out KYC on their direct customers under our standards. If any sub is
large enough or in a regulated business, the bank might request to review that sub’s AML program too. For
instance, if one of our clients is an overseas bank or fintech, the sponsor bank might say: “We want to see
their AML policy and how it meets FATF standards, because effectively they are sourcing customers that will
flow into our bank.” There’s a FinCEN advisory from 2016 about foreign MSBs accessing U.S. banks indirectly
– banks have been warned to be vigilant . So a foreign sub-MSB’s program may indirectly come
under U.S. bank scrutiny.
Regulatory Filings (SARs/CTRs): How SAR filing is allocated can vary: Some banks want to file all SARs
related to the program because they (rightly) fear liability if a SAR isn’t filed. In those cases, they require the
fintech to provide timely SAR “referrals” – basically, the fintech must internally investigate and if it thinks a
SAR is warranted, send the details to the bank’s BSA team, which will then file the SAR (perhaps mentioning
both the bank and program in it). Alternatively, if our MSB files SARs (as we must under FinCEN rules for our
activity), the bank might ask us to forward copies or at least notify them of key SARs. Guidance actually
encourages that banks and their MSB customers share information under Section 314(b) of the USA
PATRIOT Act to combat financial crime – which is a legal safe harbor for voluntary info sharing. If
both we and the bank elect to be 314(b) participants, we can freely share customer info related to
suspicious activity. We should strongly consider signing a 314(b) agreement with our sponsor bank so that if
we have a SAR on an end user, we can tell the bank, and vice versa, without legal hurdle . This kind of
arrangement streamlines delegation – we become almost like an internal unit of the bank’s BSA team.
For CTRs, typically the bank as the insured depository is responsible for filing CTRs on cash transactions that
go through the bank. In a purely digital program, CTRs may rarely come up (unless someone is depositing
physical cash somewhere or withdrawing cash). If we had a load via cash (like a retail load network for
prepaid cards), often the MSB (us) would gather information and maybe file an MSB CTR, but the bank
might also have to file a CTR if that cash touches a bank branch or account. In complex agent networks,
FinCEN has guidance about aggregation: all transactions by related entities should be aggregated for CTR
purposes . We would ensure our agents aggregate at the customer level and send that info to us. The
4
52 53
54 55
56 55
57
21
sponsor bank might put in the contract that we must immediately notify them of any cash transactions over
$10k so they can ensure proper reporting.
Liability and Regulatory Expectations: It’s important to note that delegating compliance tasks does not
remove regulatory liability from the bank. The OCC’s consent orders in 2022 explicitly cited banks for failing
to manage fintech partner compliance . So banks will often include language like: “Bank retains ultimate
control over BSA/AML decisions. In the event of disagreement, Bank’s decision prevails.” For instance, if there’s a
question whether to exit a particular end customer for suspicious activity, even if we as MSB are
comfortable keeping them, the bank can insist we exit them. We must abide by that or risk breach of
contract.
Shared Monitoring: Some advanced partnerships implement a kind of two-layer monitoring: we monitor
transactions in real-time, and the bank monitors us through higher-level triggers. Example: if daily volume
deviates by +50% from average or if unusual patterns occur, the bank’s systems flag it and then ask us for
an explanation. In addition, banks might subscribe to our transaction feed to run it through their own
watchlist filters (especially for sanctions – they won’t solely rely on us). The contract or a service level
agreement will detail the frequency of data sharing required (some require daily files of all transactions).
Use of Compliance Tools: We should clarify in the agreement or policies what tools are used. Many
sponsor banks have preferred vendors: e.g., they might say you must use XYZ for KYC verification. OmniWire
notes that sponsors may mandate specific vendors like Alloy or Socure . If we already have tools the
bank isn’t familiar with, we may need to justify them or even switch to what the bank prefers. Alternatively,
the bank might allow us to use our systems but do a validation of them (perhaps even test our sanctions
screening by sending dummy names, etc.).
Regular Reporting: The delegated framework will include routine reporting obligations. We might have to
send monthly compliance reports – e.g., number of new customers onboarded, number of suspicious
incidents flagged, any fraud losses, training conducted, etc. The bank uses that to evidence to examiners
that the program is under control.
In summary, the compliance delegation is really a partnership in practice. The bank and MSB should be in
frequent communication at the compliance officer level. Many programs have weekly or bi-weekly
compliance calls between the bank and fintech to discuss issues, upcoming changes, etc. This ensures no
surprises. We should enter the relationship expecting to work hand-in-glove with the bank’s compliance
team. Banks appreciate proactive partners – if we notify them of issues early (like “we discovered an agent’s
customer was doing something potentially illegal, we suspended the account and are investigating”), it
builds trust that our delegated tasks are being handled.
2.2 Reliance on Parent MSB’s Program vs Independent Sub-MSB Programs
One question is whether each sub-MSB (series) needs its own compliance program and officer, or can they
all rely on the parent’s program.
FinCEN’s stance: As noted, an agent of an MSB can rely on the MSB’s registration and is not required to
register itself . However, FinCEN requires that each MSB (which includes agents when acting in MSB
capacity) adhere to BSA requirements such as an AML program . FinCEN acknowledges that a small agent’s
AML program might be much simpler, and that an agent could be “implementing the principal’s program.”
9
2
10
14
22
In networks like Western Union, the agents typically are small businesses that follow Western Union’s BSA
policies (Western Union trains them and audits them), rather than each agent crafting its own policy. This is
the model we aim for: one master AML program that our agents implement.
To be concrete, our parent MSB’s AML Program document will have sections addressing agent
management. It might say, for instance: “All agents must comply with the ParentCo AML Policy. Each agent
will adopt these procedures for customer identification, recordkeeping, and reporting. ParentCo’s
Compliance Officer provides training and conducts oversight of agents. Agents must report certain
information to ParentCo (like suspicious activity) within X days,” etc. Essentially, the sub-MSBs do not need
separate written policies if they wholly adopt ours. We likely will provide them with an Agent Procedures
Manual which is a subset of our overall policy, telling them what to do step by step.
Do sub-MSBs need their own compliance officers? We should designate a contact person at each sub-
MSB responsible for compliance liaison, but not necessarily titled “BSA Officer.” Many states require an MSB
licensee to appoint a compliance officer; for agents, it’s not a regulatory requirement but a best practice
that each agent has someone overseeing compliance on their end. We will include in agent contracts that
they must designate an employee or representative to coordinate with us on compliance matters. Our team
will regularly communicate with those folks.
Bank’s view: The sponsor bank likely doesn’t want to interface with each sub-MSB directly on compliance
(too many points of contact). They want to deal with us. So they will likely require that communications and
information from sub-agents all funnel through the parent MSB. If a sub-agent messes up, the bank will
hold the parent accountable, not go chase the sub-agent (the bank has no contractual relationship with the
sub-agent usually, only with us). Therefore, we must “own” the compliance of our subs. This in turn means
we, the parent MSB, need sufficient staff and systems to monitor possibly multiple business units. If, say, we
have 10 series running, we might consider each a mini-portfolio and have compliance staff assigned to
monitor each one’s activity on a daily/weekly basis. The bank may ask how we structure our compliance
team to handle the load of multiple programs. We should be ready to show an organization chart: e.g., one
Compliance Officer, with perhaps deputies or analysts focusing on each agent’s transactions. For now, if
we’re small, one person can do it with good automation, but as we grow it should scale.
Sub-MSB independence: There could be scenarios where a sub-MSB is itself a regulated entity with its own
compliance program (like a foreign bank client will have their own AML controls). In such cases, how to
reconcile two programs? The approach is usually to map the programs: we ensure the sub’s program
meets or exceeds our requirements. If the sub’s program is strong, we might allow them to use their
procedures as long as certain key requirements are met and information flows to us. For instance, maybe a
foreign bank already does KYC and transaction monitoring on its clients – if they want to use our service to
transfer funds, we might rely on their KYC to some extent. But FinCEN would say if we (parent MSB) are the
one actually transmitting, we are responsible to ensure the KYC was done properly. We could thus
incorporate in our policy that for certain agent categories (like a licensed foreign financial institution agent),
we will perform a “program assessment” and if satisfied, rely on their KYC in lieu of duplicating it. The
sponsor bank would have to be comfortable with that arrangement. In practice, U.S. banks often do not
fully rely on foreign institutions’ AML due diligence unless there’s a formal reliance or certification. They
might instead treat the foreign institution as just another customer requiring full info on each underlying
transaction. We should be cautious: unless an arrangement is made, our safest route is to have full visibility
and ability to get customer data from our agents. Possibly we’ll require all agents, even if they do their own
onboarding, to feed us the KYC data of each customer. That way, our centralized system can screen those
23
names against OFAC and other lists, and the bank could also have that visibility if needed. This is something
to design: a centralized KYC repository might be needed so that if the bank or regulator asks “Who is the
actual originator or beneficiary of this wire?” we can immediately provide details, even if the person was
onboarded by a foreign agent.
Summing up: Sub-MSBs can rely on the parent’s compliance program – they don’t each need a distinct
one – but they are participants in it and must carry out front-line procedures. FinCEN explicitly expects the
principal MSB to exercise “agent management and termination practices” , implying the principal’s
program governs. We will implement a “single program, multiple business units” approach.
We should document that our sub-MSBs are “Agents/Authorized Delegates” of the parent in our FinCEN
registration (by maintaining the list) and state licenses (some states, like in NMLS, require listing every trade
name or agent location). This transparency also helps if any question arises whether sub-MSBs themselves
should be licensed – by clearly being agents, they are exempt from separate licensing in most states (some
states call them “authorized delegates” and explicitly exempt them from needing their own license under
the licensee’s supervision).
The bank agreement likely will incorporate language like: “Bank acknowledges that MSBCo may utilize
authorized agents to conduct money services on its behalf. MSBCo shall ensure each agent’s compliance with the
terms of this Agreement and applicable law. MSBCo remains fully responsible for the acts and omissions of its
agents.” This makes it clear the bank expects us to control them. We should also provide the bank with
updated agent lists – some agreements demand notification within X days if you add an agent; others may
require pre-approval (as earlier noted).
In conclusion, the compliance program is centralized, and sub-MSBs operate under it rather than
independently. They need not each have a separate AML policy, but they must follow the parent’s and have
designated personnel to implement it. This is consistent with industry practice in agent models and will be
acceptable to regulators as long as oversight is robust. One can cite the FFIEC BSA/AML Exam Manual
which in the MSB section likely states that examiners will evaluate how an MSB oversees its agents and
ensure that the agents receive adequate training and guidance (this is indeed a focus area in MSB exams:
agent oversight). Our structure should be prepared for that scrutiny at multiple levels – the bank will look at
how we oversee agents, and if FinCEN/IRS ever examines us, they will look at it too.
2.3 SAR/CTR Filing Responsibilities for Each Party
This topic has been touched on, but to clearly delineate:
Sponsor Bank – SARs: A bank must file a SAR under 12 CFR 21.11 (OCC) / 12 CFR 208.62 (Fed) / 12
CFR 353 (FDIC) if it detects certain suspicious transactions conducted or attempted by, at, through,
or otherwise involving the bank that meet the dollar thresholds and have a suspect reason. In our
case, suspicious activity could be through the bank via our accounts or program. Example: If the bank
sees large wires going through our FBO account in patterns indicative of layering, and we have not
provided a satisfactory explanation, the bank will file a SAR (likely referencing our MSB and maybe
the underlying client if known). Also, if they become aware we (the MSB) are not complying with
regulations (say, they find we were required to have a state license and didn’t, or operating
unregistered in some way), that itself could be SAR-reportable (banks are told to SAR report if they
58
•
24
find their customer is an unlicensed MSB) . They might also file if we refuse to provide
information or any part of our program seems to facilitate unlawful activity.
Sponsor Bank – CTRs: A bank must file CTRs for cash transactions > $10,000 by or on behalf of the
same person on the same day. Typically, if we or our agent physically deposits or withdraws cash at
the bank, the bank will file a CTR (because that’s a transaction with the bank). However, our business
model likely doesn’t involve cash deposits at a teller, etc. Perhaps remote deposit of money orders or
something could happen, but unlikely. If an ATM deposit or something is possible to our account, the
bank’s systems would catch it and CTR as needed. If our program had prepaid cards with cash load
at a retail location, those loads often go through services like GreenDot’s MoneyPak or Western
Union, which handle the CTR side themselves as MSBs, and then funds come electronically to the
bank – so the bank doesn’t see cash in that case. In summary, bank CTR filings will probably be rare
for our setup.
Our MSB (Parent) – SARs: FinCEN’s rules (31 CFR 1022.320) require certain MSBs (money
transmitters, issuers/sellers of instruments, etc., but notably not check cashers or sellers of prepaid
value) to file SARs for suspicious transactions of $2,000 or more (or any amount if insider
involvement) . Money transmitters are covered, so we as a money transmitter must file SARs. That
obligation applies to the parent MSB for itself and its agents. FinCEN has clarified that if an entity is an
agent only, it doesn’t have to file SARs independently – the principal handles it. Therefore, we will
file SARs on any suspicious activity related to our sub-MSBs’ operations or their customers, meeting
the criteria. We might discover such activity through our monitoring or via an agent’s report to us.
For example, if a sub-MSB reports that a business client is trying to structure payments just under
reporting thresholds or someone is sending funds to a high-risk jurisdiction with no apparent lawful
purpose, our compliance team would investigate and, if warranted, file a SAR. We would name the
principal subjects (the end customer, possibly the agent as an involved party) and describe the
transactions. We might mention that the funds flowed through XYZ Bank (our sponsor) account, but
usually MSB SARs don’t need to list the bank unless it’s materially part of the suspicion (like if the
suspicion is about the bank—here it’s not, it’s about the customer).
Our MSB – CTRs: As a money transmitter, we have to file CTRs (though technically they’re not CTRs
but “Reports of Currency in excess of $10k Received” for MSBs) for cash in or cash out transactions >
$10k with one person in one day. If any of our agents take >$10k in cash from a customer to
transmit or give out >$10k in cash, we must file FinCEN Form 104 for that event, aggregating across
agents. For example, if a customer gave $5k cash to Agent A and $6k cash to Agent B of ours on the
same day (unlikely scenario, but suppose chain store locations), we as the MSB would aggregate that
($11k) and file one report. In practice, since we don’t have physical storefronts and we’re dealing
B2B, large cash transactions are not in our model. So our CTR filing burden is likely nil. However, if
one of our clients is say a fintech that deals with cash (maybe an ATM network or something), and
they route cash transactions through our license, then yes, we’d have to handle that. At present, not
anticipated.
Sub-MSB – SAR/CTR: As per FinCEN rules, a sub-MSB that is only acting as our agent has no
independent SAR or CTR filing obligation (they are covered under our program) . We likely will
instruct agents not to file anything directly even if they technically could (some might be FinCEN-
registered in another capacity, causing confusion). Instead, they must funnel info to us and we
handle filings. One reason: to avoid double counting or inconsistent reporting. For instance, if an
59
•
•
12
41
•
•
10 41
25
agent filed a SAR and we filed on the same activity, it could create confusion or at least duplication.
While duplication is not the worst thing (FinCEN would rather have two SARs than none), it’s cleaner
for one filing. We will likely include in agent agreements that agents shall not file any such reports
independently related to activities under our license, but rather provide all info to us to do so. (If an
agent also runs separate business outside our relationship, that’s their separate matter.)
Information Sharing and Joint Investigations: To fulfill these responsibilities well, we (parent)
should set up a system where sub-MSBs report any suspicious indicators to us promptly. Perhaps we
have a standard SAR referral form for agents to fill or a secure portal. We then have an internal
committee that reviews and decides on filing. For CTR, if any sub ever expects to handle large cash,
we must have them report daily cash totals to us so we can aggregate (again, likely moot in our
scenario).
Coordination with Sponsor Bank: It is advisable that our SAR filings do not blindside the bank and vice
versa. A best practice is to have a clause that says we will notify the bank’s BSA Officer when we file a SAR
related to the program (without revealing the SAR content beyond what’s necessary, since SARs are
confidential by law – but since the bank is an “institution involved in the transaction,” sharing SAR info with
them might be permissible under SAR sharing rules; there’s an allowance that you can share SAR info with
other financial institutions involved in the same transaction for certain purposes). The bank similarly might
inform us if they file a SAR that touches our program. This mutual awareness helps both sides address any
issues.
As a side note: if law enforcement comes knocking (say, a subpoena or 314(a) request for a specific
customer), the bank will get it if it goes to the bank, or we might if it goes to us. Our contract will likely
require notifying each other if a legal inquiry is received (unless prohibited). That way, if one of our sub’s
customers is under investigation, the bank and we can coordinate response and not unknowingly tip off or
contradict each other.
In summary, the flow of SAR/CTR responsibilities can be visualized as:
End-customer suspicious -> Sub-MSB detects and informs Parent MSB -> Parent investigates, files
SAR (and informs Bank) .
Suspicious pattern in aggregate flows -> Bank detects (maybe via account monitoring) -> Bank files
SAR (and likely informs us so we can address underlying issue) .
Large cash by customer -> Sub-MSB logs and informs Parent -> Parent files MSB CTR.
Large cash at bank (if any) -> Bank files CTR.
This covers compliance reporting.
2.4 Sponsor Bank Audits of MSB and Downstream Agents
Given regulators’ expectations, sponsor banks will conduct initial and periodic audits of their MSB
partners. Here’s how that tends to work:
Pre-Onboarding Audit/Due Diligence: Before signing us on, a thorough due diligence is conducted –
essentially like an audit of our compliance readiness. We should expect to answer a due diligence
questionnaire with hundreds of questions (covering program details, compliance processes, IT security,
•
•
11
•
13
•
•
26
disaster recovery, etc.). We may also have an onsite or virtual meeting where the bank’s compliance and risk
officers go through our policies page by page. If we have any independent audit reports or exam reports (in
future if we’re examined by IRS/FinCEN or state regulators), we’d share those. This initial vetting sets the
baseline.
Ongoing Audits: Many sponsor banks include in the contract a right to audit at least annually, or more
frequently if needed. Some will send an audit team to our offices (or do a remote audit via document
requests). They might audit various components each time – e.g., one year focus on KYC files, next year on
transaction monitoring and SARs. They will likely also audit a sample of agent relationships: for example,
they might say “we want to examine the files for Agent X – show us how you approved them, their KYC
program, some transactions from them, any training records.”
Agent Audits by Bank: While the bank could theoretically reach out to an agent directly, typically they will
audit the agent through us. They’ll ask us for documentation relating to that agent. In some cases, the bank
might accompany us on a field visit to an agent if they are a large one. For example, if one of our sub-MSB
clients is responsible for a big chunk of volume, the bank might say “we want to meet that partner” or at
least see how we have audited them.
What are they checking? They will verify that our program as described is actually implemented. If we said
we do XYZ screening, they’ll ask for logs or evidence. They might look at a random selection of customer
onboarding records to see if CIP was properly done (IDs collected, OFAC checked). They’ll look at some
alerts from our monitoring system and confirm we resolved them appropriately. They may also evaluate our
agent oversight: e.g., ensure we have an up-to-date agent list (this ties into regulatory requirement that we
maintain it ), verify we conducted initial due diligence on each agent (like did we perform a background
check on the agent’s principals? Did we get copy of their license if they have one? etc.). If an agent is foreign,
they might see how we complied with FinCEN’s requirement that foreign MSBs register or have a U.S. agent
. Possibly they’ll ask to see a copy of each agent contract to ensure appropriate language is in place
(especially clauses that the agent will comply with BSA, report info to us, allow inspections – banks want to
know we have the contractual right to control our agents).
Risk Rating and Monitoring: The bank will likely risk-rate us and maybe each agent. If one of our agents is
in a high-risk category, the bank could impose more frequent audits or require more frequent reporting on
that agent’s activity. For instance, if one agent deals with payments to countries with higher AML risk, the
bank might say “for this agent, we want a monthly report of all payments they made to Country X.”
Regulatory involvement: Sometimes, bank examiners themselves will ask to see information on the bank’s
fintech programs during exams. The bank might then come to us with an urgent request: “The OCC wants
details on our top 5 program customers – please provide…”. We must be responsive or the bank gets heat. A
real example: after the OCC’s increased focus, banks asked fintech partners for very granular data (like
exact number of accounts, total transactions, fraud rates, SAR counts, etc.). We should be prepared to
produce such metrics quickly.
Agent Audits by Us vs. Bank: We (parent MSB) also will be auditing our agents periodically. The bank will
likely ask for results or at least assurance that we do it. We should keep workpapers – e.g., we do a quarterly
call or review with each agent and note any issues. If an agent is deficient (maybe they had incomplete KYC
on a client), we note the corrective action. If we terminated any agent for compliance reasons, we definitely
4
60
27
inform the bank promptly (since that could be a red flag of a past problem – but it’s better we address it
than bank finding it first).
Common Findings and Follow-up: If the bank’s audit finds issues, they will issue findings or a report. We’ll
be required to respond with a remediation plan and timeline. For example, bank audit might say “We found
that in 3 of 20 sampled customer files, the agent did not collect an SSN as required – this is a CIP exception.
MSBCo must ensure 100% CIP collection; provide a report in 60 days showing all agents have no missing
SSNs.” Or they might find our transaction monitoring rule thresholds were too high to catch relevant
patterns, and require us to adjust them. We should treat a bank audit almost like a regulator exam – take
corrective actions seriously and promptly, and document them. Patterns of repeat findings could lead the
bank to deem us non-cooperative or high risk, potentially jeopardizing the relationship.
“Compliance Waterfall” – oversight down the chain: The concept of a compliance waterfall is that each
level audits the level below. So the regulators audit the bank, the bank audits us, and we audit our agents.
We should implement that fully: we will have an audit schedule for agents (maybe risk-based – e.g., big
agents reviewed quarterly, smaller annually). We will document those agent audits. Then when the bank
audits us, we show them those documents. Similarly, the bank will document how it audits us to show
regulators. If done properly, by the time a federal examiner looks at the program, they see layers of controls
– which is what they want (they want to see that risk is managed at every tier).
Audit Rights in Contract: Contractually, as mentioned, the bank will have broad audit rights. They might
also reserve the right to audit agents or require us to get audits by a third party. For instance, sometimes
banks say “If we have serious concerns, we can engage an independent consultant at MSB’s expense to
review the program.” Hopefully we avoid that scenario by doing well on routine audits.
Technology Audits: Another aspect is IT security and data handling. The bank might audit our
cybersecurity measures, because if we are connected to the bank’s systems, any weakness in us is a risk to
them. So we might have to fill out lengthy questionnaires about our encryption, access controls, etc. Since
we are dealing with sensitive financial data, banks usually require evidence of things like annual penetration
tests, ongoing vulnerability scans, etc. It might even be required that we comply with certain bank policies
(like data retention rules or incident response timelines).
Agent On-site Visits: If practical, we (and possibly occasionally the bank) may visit an agent’s location (if
they have one, or their offices) to verify operations. This is more common in cash-heavy MSB agent
scenarios (to see if procedures are followed at a store). In our case, many sub-MSBs might not have a
physical retail presence; they might be companies using our API. For those, audits are more about
reviewing digital records and maybe meetings with their compliance contact to discuss any issues.
Regulator guidelines: The Federal Financial Institutions Examination Council (FFIEC) BSA/AML Exam
Manual includes a section on “Third-Party Payment Processors” and MSBs. Banks are advised to obtain
agent lists and review independent testing results of MSB programs . Also, FinCEN and regulators in
2005 joint guidance essentially set the expectation that banks will monitor MSB accounts on an ongoing
basis and take additional steps for higher-risk ones (including reviewing agent lists, AML program, etc.)
. So our sponsor bank following that playbook will definitely be doing these audits and requiring info.
Regulatory Reporting of Audit results: If a bank finds a serious deficiency in our program, it might be
obligated to report it to its regulator (especially if it rises to a safe and soundness issue). It could also
58
61
58
28
potentially file a SAR if it thinks our deficiencies indicate we’re not complying with BSA (though more likely
they’d just demand we fix it). So maintaining a cooperative stance and quickly fixing issues is not just about
pleasing the bank, but also staying off regulators’ radars.
In summary, sponsor banks will actively audit MSB clients and their downstream agents to ensure
compliance expectations are met. This multi-layer audit approach is fundamental to the “compliance
delegation” model – it’s how the bank demonstrates that delegating tasks to us is still resulting in
compliance equivalent to if the bank did it itself. Our strategy should be to embrace these audits as an
opportunity to improve and to show our strength. We will set up internal controls to consistently meet the
audit standards so that over time the bank gains confidence in us, possibly reducing the intensity of
oversight (one can hope – although with regulators pressing, banks are unlikely to ease up completely).
3. Regulatory Treatment of Layered MSB Structures
3.1 FinCEN’s View on MSB-to-Sub-MSB (Agent) Arrangements
FinCEN, as the administrator of the BSA for MSBs, explicitly allows an MSB to operate through agents. This
has been the case for decades (reflecting common industry practice with money transmitters having
networks of independent agents, like Western Union’s model). The FinCEN MSB Registration Rule and
guidance make clear: - No Duplicate Registration: An entity that is an MSB solely because it serves as an
agent of another MSB is not required to register separately with FinCEN . The responsibility for registration
lies with the principal MSB. In our scenario, that means only the parent (master) MSB LLC registers with
FinCEN. The series LLC sub-MSBs, if they act strictly as agents under the parent, do not register on their
own. FinCEN’s rules carve out that exception to avoid redundant registration of every mom-and-pop agent
location.
Agent List Requirement: The principal MSB must prepare and maintain a list of its agents (with
names and addresses) and must make that available upon request to FinCEN or law enforcement
. We are expected to update this list annually at minimum (the regs used to say the agent list
should be updated each January 1 and kept for examination). FinCEN or IRS BSA examiners can ask
to see it. If our series structure changes (new series added or one terminated), we should promptly
update the list. There’s no requirement to proactively file this list with FinCEN unless asked, but we
must have it ready.
Principal’s AML Program Covers Agents: FinCEN’s regulations (31 CFR 1022.210) on MSB AML
programs require an MSB to implement a risk-based AML program. In guidance, FinCEN has
indicated that if an MSB uses agents, the program should include policies and procedures for
oversight of those agents (such as obtaining agent information, monitoring for compliance, etc.).
Indeed, in FinCEN’s 2005 guidance, a footnote explicitly says a global MSB with domestic and foreign
agents will have a very different AML program than a small solo MSB – implying that agent
management is a critical component of the program design. So FinCEN expects us to incorporate
agents into everything: our risk assessment, our training, our independent review (the independent
review should sample some agents or at least evaluate how we manage agents).
No Limit on Agent Numbers per se: FinCEN does not impose a cap on how many agents you can
have or how many “layers” in federal law. The concept of “layers” beyond one principal-one agent
chain isn’t explicitly discussed by FinCEN, but we infer that FinCEN’s tolerance might not extend to
10
•
62
•
14
•
29
multi-tier for registration purposes. For example, if MSB-A has an agent MSB-B, which itself has an
agent C, is C exempt from registration? By strict reading, C is an agent of B, which is an agent of A – if
C is “solely an agent of an agent of an MSB,” FinCEN hasn’t explicitly spoken, but likely they’d treat C
effectively as an agent of the principal indirectly, possibly still exempt from registration if the chain is
disclosed. But such complexity is unusual. FinCEN would likely say MSB-A should list both B and C as
agents on its list to be safe. Our series structure is only one layer (parent → series agent), so we’re
fine.
Foreign Agents and Foreign-Located MSBs: FinCEN’s 2012 advisory on foreign-located MSBs
(FIN-2012-A001) is relevant if any agent is foreign. FinCEN now considers a foreign company that
does MSB business in the U.S. (even via agents) to be an MSB and required to register, unless it’s an
agent of a U.S.-registered MSB. If our foreign client is acting as our agent, then by registering the
parent, we cover them and they don’t have to register. But FinCEN would require that foreign agent
to have a U.S. agent for service of process if they were considered a foreign-located MSB
independently . Since they are our agent, we are essentially that point of contact. FinCEN explicitly
said foreign MSBs must register unless they are solely agents of a U.S. MSB . This implies FinCEN
is comfortable with foreign entities being agents of a U.S. MSB, as long as transparency is there.
They caution banks to update AML programs to account for foreign-located MSBs or their agents
. We should heed that and keep robust info on foreign agents.
FinCEN Rulings on Agent-of-Payee and Payment Processors: Another aspect – FinCEN has rulings
(like FIN-2008-R006 we examined) where an entity acting as an agent of a payee (like utility
company’s agent) was deemed not a money transmitter . That was federal interpretation (and
many states mirror it). In context, if a sub-client’s arrangement could fit agent-of-payee, it might not
be considered money transmission at all. But since we choose to operate under MSB licenses, we
aren’t heavily relying on that exemption. Still, FinCEN’s logic is that when you are an agent of the
payee, the flow is “integral to the transaction” and not separate money transmission . If any
of our services specifically involve collecting payments for a seller of goods (like a marketplace
scenario), we might consider structuring it as agent-of-payee to remove state licensing needs for
that client. FinCEN would be fine with that if clearly within their prior rulings. And importantly,
FinCEN distinguished such scenarios from true open money transmission. So if we have an agent-of-
payee case, we should document the contracts accordingly. It doesn’t change BSA obligations much
though – even if not a “money transmitter,” as an agent-of-payee the company still should watch for
suspicious activity (but technically not obligated to have an AML program if it’s not an MSB. However,
our parent being an MSB covers it anyway).
FinCEN Expectations in Exams: The IRS is delegated to examine MSBs for BSA compliance on
FinCEN’s behalf. If and when we get examined, likely examiners will look at agent oversight. They’ll
want to see our agent list, check if we do appropriate due diligence on agents, and whether we are
effectively acting as a single enterprise. If a violation happens at an agent (say an agent willfully
ignored AML controls), FinCEN can take action against the principal MSB because the agent’s actions
are imputed to the principal in terms of program failures. There have been enforcement cases where
Western Union or MoneyGram got penalized for agent misconduct because the expectation was that
they should have caught it.
In summary, FinCEN is supportive of the agent model as it encourages MSBs to operate networks under
one compliance umbrella (rather than forcing every small business to independently license and manage
•
31
53
63
•
64
65 64
•
30
BSA, which might be less effective). FinCEN’s main concern is transparency and that the principal truly
manages the risk. So as long as we maintain that principle (with proper registration, lists, AML program
extension, etc.), our layered approach is on solid ground federally.
3.2 State Regulators’ Perspective on Layered MSBs
State regulation is a patchwork, but generally: - Most states allow Authorized Delegates (Agents): Money
transmitter licenses (which we likely have in some states, or will get) typically include the right to appoint
authorized delegates to conduct money transmission on the licensee’s behalf. The licensee must monitor
and be responsible for those delegates. For example, the Uniform Money Services Act and many state
laws require licensees to maintain a list of authorized delegates and to enter contracts with them imposing
certain obligations (like adherence to AML, etc.). Many states require a licensee to notify the state of new
authorized delegate locations (often through NMLS updates). Some even require an annual fee per
delegate. We should check each relevant state: e.g., New York, if we needed a license there, treats agents
differently (New York actually doesn’t have a separate agent licensing regimen – they often expect each
entity transmitting in NY to be licensed unless falling under agent-of-payee or bank exemptions; Western
Union’s agents in NY operate under Western Union’s license by explicit statutory exemption for agents of
licensed transmitters). Most other states do allow it explicitly.
Agent Reporting and Responsibility: States like Texas require that the licensee’s name and license
number be listed on agent’s business, that agents report suspicious activities up, etc. States can
examine not only the licensee but sometimes a sample of its agents (some states will do on-site
visits to agents of a licensee during an exam). So our sub-MSBs could potentially interact with state
examiners if they choose to (rare but possible). We should ensure the series know to cooperate if
that ever happens (again, examiners would coordinate through us typically).
Depth of Nesting: State laws usually speak to licensees and their authorized delegates. They
typically do not mention authorized delegate of an authorized delegate. The implication is that only a
licensee can appoint delegates. Therefore, if one delegate wants to have others perform the service,
legally those others should also be signed as delegates of the licensee (not sub-delegates of the
delegate). If someone tried to create multiple layers, states might view the lower layer as unlicensed
if not directly tied to the licensee. In our case, our parent is the licensee and the series are delegates.
We will not have the series appoint further agents without making them direct agents of the parent
if needed. So we keep it one layer in legal terms.
Series LLC recognition: One nuance is whether states recognize series LLC structure. Not all states
have series LLC statutes or are familiar with them. Some might treat each series as a separate
“person” if it has a separate EIN and operates distinctly. Others might insist that because only the
parent is licensed, the public-facing name on transactions should be the parent (or an authorized
trade name of the parent). We should be careful that if Series X is sending a wire, the documentation
doesn’t only show “Series X LLC” without context, because a bank or regulator might go “who is that,
are they licensed?” The proper way is likely to have the parent licensee’s name somewhere or file
“doing business as” (DBA) names for each series if they use unique names. Many states allow
multiple trade names on one license. For example, if our parent is “Master Payments LLC” and we
have series “AlphaPay”, “BetaPay” as brand names, we should register “AlphaPay” and “BetaPay” as
trade names on our state licenses. Then it’s clear to regulators and customers that those brands are
•
•
•
31
covered under Master’s license. Failing to do so could be seen as unlicensed activity under a different
name.
Disclosure of Structure: In license applications or renewals, states often ask for a list of all locations
and authorized delegates. We should include each series (with its main business address, even if
same as parent or different) as an authorized delegate. Also, if a series has a separate office or
people in another state, that might count as a “branch” or location needing to be reported. If our
series are just shell designations with no separate physical presence, maybe not. But likely each
series corresponds to an operational unit that might be in a different location or at a client’s office. If
a series is essentially a corporate client’s division, sometimes that location acts like an agent location
of ours. For example, if a foreign client’s staff in their country will input transactions that go through
our system, that foreign location could be considered an agent location (though not a U.S. location –
but some states still require listing foreign agent locations if they serve U.S. customers). The CSBS
Money Transmitter Modernization Act (model law) being adopted by many states includes
standardized approaches to authorized delegates. It may require providing a list of all delegate
business names and addresses via NMLS. We’ll comply accordingly .
Regulatory “Friction” Minimization: The question mentions our posture is to operate where
“clearly permitted with minimal regulatory friction.” That suggests we choose states or structures to
avoid grey areas. One potential grey area is the “agent-of-payee” exemption. Some of our clients
might want to rely on it for their own business. We should be aware how states handle it. CSBS
provided an Agent-of-Payee Exemption Map showing which states have it explicitly . If a
transaction fits that exemption (e.g. paying a merchant for goods), our client might not need to be a
delegate at all (because no license is needed for that flow). However, since we mainly do licensed
MSB flows, we might not utilize it unless necessary. But where applicable, we’ll ensure contracts say
the right language (exemption usually requires a written agency agreement with the payee).
States and Multi-Layer: Suppose we had an arrangement like: Parent licensed in StateA, an agent
Series in StateA which itself appointed sub-agents. If StateA examiners found out, they’d likely say
those sub-agents aren’t on the licensee’s delegate list, so they’re unlicensed – a violation. They might
penalize or require retroactive listing. Some states might allow a chain if disclosed (e.g. “we have a
hierarchical distribution, but here are all the endpoints that interact with consumers”). They care
mainly that every place or entity dealing with consumers is either licensed or an authorized delegate
of one who is. So practically, we must ensure any entity in the chain that touches customers or
money is either the parent or directly an authorized delegate of the parent.
Agent of the Bank vs Agent of Licensee: Some states provide that if you are agent of an FDIC-
insured bank (for money transmission), you might be exempt from state licensing due to federal
preemption or state law exemptions. For example, agents of national banks might not need a money
transmitter license. However, our sub-MSBs are agents of our MSB (not agents of a bank directly).
Could we call them agents of the bank indirectly? Not really, the legal agent-of-bank exemption
typically requires a direct contractual agency with a bank (like some fintechs do by becoming a
program manager agent of a national bank to avoid needing state licenses – but that’s a contentious
strategy and not universally accepted by states). We didn’t pursue that route; we got licenses for the
parent. So we won’t assert that for them. They operate under our license, not the sponsor bank’s.
•
66
•
67
•
•
32
Regulatory Audits and Examinations: If state regulators examine us (some states examine
licensees annually or biennially), they will likely review our agent structure. They might pick a sample
of agents and ask for documentation (similar to how the bank would). They want to see that we
control branding (most states require delegates to display a notice like “Authorized delegate of
Master MSB LLC, license #1234”). If we have websites for each series, possibly the license number
and parent name should be in the footer. Ensuring compliance with those requirements avoids
regulatory friction.
Agent Depth and Agent-of-Payee Intersection: The question specifically asks how agent-of-payee
exemptions interact with sponsor bank relationships. In states where agent-of-payee is recognized, a
fintech often doesn’t need a license if it’s collecting on behalf of a seller. If one of our sub-MSB clients
could fit that mold, technically they wouldn’t have needed to be under our license, because they
weren’t required to have a license on their own. But if we still bring them under our umbrella, it’s a
bit belt-and-suspenders. Banks typically prefer their fintech partners to either be fully licensed or
clearly exempt. Agent-of-payee is an exemption, but banks know it’s a complex one that some
states challenge. Some sponsor banks might still insist the fintech register as an MSB or partner with
a licensed entity (us) for comfort, even if the fintech claims agent-of-payee. So our structure might
actually attract clients who could have tried agent-of-payee but wanted the certainty of using a
licensed MSB – we give them that cover. State regulators, for those clients, might not even need to
weigh in on agent-of-payee since we’re licensed and treating it as transmission.
One risk: if we operate in a state solely under agent-of-payee logic where we have no license, a sponsor
bank might be uneasy. But since we are obtaining licenses (Montana and others as needed), we’re not
leaning on that except where clearly allowed.
Summation: State regulators are generally fine with the layered agent approach as long as the licensee
takes responsibility and obeys agent-related provisions (notifications, bonding for agents if required, etc.).
They don’t want a convoluted chain that obscures responsibility. By maintaining direct privity with each sub-
MSB via delegate contracts and listing them as delegates, we keep regulators satisfied that it’s one licensee
(one throat to choke, so to speak). The states’ main concern is consumer protection – if something goes
wrong (say an agent runs off with money), the licensee is liable to make consumers whole. We have to
stand ready for that. Our sponsor bank will also ask about that – usually MSB licensees must have a surety
bond (often increased per number of agents). We have to make sure our bonding covers our agent activities
in multiple states (some states require separate bonds per agent or higher bond if many agents). That’s
another contractual term: we likely will covenant to maintain required bonding and net worth so that if an
agent causes a loss, we can cover it.
In conclusion, state regulators accept one level of authorized delegates but would frown upon
multiple nested delegate levels and will require full disclosure of all entities involved. The agent-of-payee
exemption can reduce licensing needs in some scenarios, but since we operate as a licensed entity, it’s more
of a backup or alternative in specific flows rather than the core model. We ensure our structure is clearly
communicated and legally established in each jurisdiction to avoid any characterization of unlicensed
activity.
•
•
33
3.3 Required Disclosures and Transparency About Layered Structures
Ensuring transparency is crucial. We’ve touched on many disclosure aspects, but let’s consolidate:
To FinCEN: We will list each agent in our required agent list (with name and address) . Although
not filed, if FinCEN/IRS asks, we must produce it within 2 business days (that’s in the regulation). If
any of our agents is foreign-located, FinCEN might take interest due to the foreign MSB rules – we
should be prepared to provide additional info if asked (like that agent’s US agent for process or
confirmation they solely act for us in US).
To State Regulators: We will use NMLS for states that require authorized delegate reporting. Many
states ask licensees to upload a list of agents (some quarterly). For example, California and others
have you input agent info (business name, address, phone) and maybe pay a fee per location. We
must keep this current – failure to report a delegate could be a violation. Some states require prior
approval for adding delegates in their state (not common, but a few might; most just require notice).
When renewing licenses, states often ask for any changes in business plan or structure. We should
mention the series structure upfront in applications: e.g., in our business plan description, say “The
Company will provide services under its license directly and via series limited liability company
subdivisions which operate as its authorized agents under a series LLC structure (Montana domicile).
Each series functions under the Company’s MSB program and compliance oversight.” This heads off
confusion and shows we’re not hiding it.
Public-Facing (Consumer) Disclosures: Since we have minimal retail exposure, this is less about
consumers and more about business clients. But, if for example one of our series issues a prepaid
card to consumers, network rules and some state laws might require that the card or user
agreement disclose the actual licensed entity. Typically, prepaid cards state “This card is issued by
XYZ Bank, Member FDIC, pursuant to license by… etc., and the program manager is ABC Co.” If our
series’s brand is on the card, somewhere it should likely say “Service provided by [Parent MSB name],
a licensed money transmitter.” That way a consumer or regulator can identify who is behind it. For
pure B2B, we may not have a “public” brand at all, as we might be behind the scenes. But some
clients might want to advertise they partner with us (for legitimacy). We might encourage something
like an “About” page mention: “U.S. transactions are facilitated by XYZ, which is registered with
FinCEN and applicable state regulators.” This kind of transparency can preempt any allegation that
an unlicensed entity is doing business.
Banks and Partner Disclosures: The sponsor bank will require we fully disclose all parties. They
might incorporate that into their internal risk assessments (like listing each agent as a “sub-
customer”). If any of our agents or sub-MSBs is itself a financial institution, the bank might need to
do a nested relationship risk assessment akin to correspondent banking. E.g. a foreign MSB using
our MSB to access the bank is a form of nested MSB access – banks are cautioned on that (FinCEN’s
advisories flagged that foreign MSBs might try to access US banks indirectly through relationships)
. We need to demonstrate we know our agents and their clients extremely well to alleviate
that.
Depth (“Nesting”) Limits: While no law says “no 2nd tier agents,” in practice, if we were to attempt
more layers, we’d likely need to disclose it anyway and regulators would strongly discourage it. For
instance, if an agent of ours wanted to sign up sub-agents in multiple states, states might say “just
• 62
•
•
•
52 53
•
34
license that entity too, instead of making them sub-agents-of-sub-agent.” Usually big networks
flatten the hierarchy for licensing: e.g. Western Union might directly license larger sub-agents as its
own delegates too, or require them to get their own license beyond a point. For us, we likely won’t
attempt any more layers. If a sub-MSB client of ours itself wanted to appoint agents (say our client is
a fintech that wants to have retailers act as their cash-in points in various states), ironically that
would create a third layer (us -> series (client) -> their agent). States wouldn’t be okay with the
bottom layer being unlicensed. The solution would be either that bottom agent becomes our agent
too, or that our client gets its own license to manage that network. So to avoid trouble, we’d either
incorporate that bottom tier into our own delegate list or not do those arrangements.
Agent-of-Payee vs. Agent-of-Licensee Example: Suppose our client is an e-commerce platform. Under
agent-of-payee exemption, maybe they wouldn’t need a license if they directly contract with merchants to
receive funds on their behalf. But they instead are using us to handle flows, so regulators will see the
transactions as money transmission (us taking money from buyers and giving to merchants on behalf of
our client). They might question “why is a license needed if agent-of-payee applies?” In states with the
exemption, arguably we might not need a license either because the payee is the merchant and we’re agent
of payee via our contract chain. However, not all states buy that a chain of agency (customer -> platform
(agent of payee) -> licensed transmitter) qualifies. The safest route is to just use our license. I mention this
because if a regulator asked “why are you doing licensing if an exemption might apply,” we just say out of
abundance of caution and to ensure coverage in all jurisdictions (some states don’t have the exemption).
They’ll accept that because regulators prefer entities to be licensed rather than rely on exemptions that they
may interpret narrowly.
Examination Disclosures: If any complexity exists in our structure (like series LLC, which not all
examiners see everyday), it is wise to proactively explain it in our written AML program and policies.
For instance, include a section: “Corporate Structure: XYZ is a series LLC. Series A, B, C are divisions
functioning as agents under FinCEN guidance 2005-... The Company maintains a single BSA/AML program
covering all series. An updated list of series (agents) is maintained in Appendix X.” This way, if an
examiner or bank compliance person new to our file picks it up, they see it’s been thought through
and documented.
In essence, full disclosure and documentation of the layered setup to all stakeholders (regulators,
banks, possibly consumers) is not only good practice but often a requirement in bits and pieces (like agent
lists, etc.). There’s no secrecy possible here, and we wouldn’t want any – opaqueness would raise suspicions
(regulators might think we’re trying to hide an unlicensed operation behind a licensed shell if we aren’t
upfront). So we aim to be a model of transparency: listing agents to regulators, contractually binding agents
to let us be audited, and making sure everything funnels to the licensed entity on paper.
3.4 Interaction of Agent-of-Payee Exemptions with Sponsor Bank Models
We have touched on this as well, but here let’s clarify specifically:
Agent-of-Payee Exemption (State Licensing): This exemption exists in many states (roughly half, often via
statute or case law). It says that if an entity (the agent) receives money from a payer for transmission to a
payee, and the agent has a contract with the payee such that payment to the agent satisfies the payer’s
obligation to the payee, then that activity is not money transmission requiring a license in that state
•
15
35
. Essentially, it’s treated as the payee themselves receiving the money (because the agent stands in their
shoes). Common use: marketplaces (Airbnb collects money as agent of the host, etc.).
Where Sponsor Banks come in: Some fintechs have combined the agent-of-payee model with sponsor
bank relationships. For example, a payment processor might say: “We are agent of the merchant (payee), so
we don’t need a license, and we use a sponsor bank to hold and move the funds.” The sponsor bank might
open an account for that processor or even accounts for each merchant. In that scenario, the sponsor bank
is comforted by the fact that the funds are for payment of goods/services (so lower AML risk than
remittances) and that legally the processor’s receipt is considered receipt by the merchant, arguably
meaning the transaction isn’t “money transmission” by the processor (so no state license needed, reducing
regulatory friction for the bank’s partner).
For our model, if a sub-MSB client qualifies as agent-of-payee for its transactions, technically they wouldn’t
have needed to use our license. But if they still do, it doesn’t harm except maybe they wasted effort.
Perhaps more relevant is: Could we as a service position ourselves as an agent-of-payee in certain flows?
Possibly yes. If, say, our client is a merchant aggregator, we (the licensed MSB) could sign contracts directly
with merchants to be their agent-of-payee for payments, then we collect from buyers and pass to
merchants. In doing so, we might not even need our license in states with the exemption (because now
we’re agent-of-payee), but we’d still use it in others. Sponsor banks might actually prefer that approach
because it clarifies that these are not remittances or stored value, but rather straightforward payment
processing.
However, sponsor banks also focus on federal law: whether or not a state license is required doesn’t
change the federal AML obligations. The bank will still treat it as money movement that requires AML
controls. So from a BSA/AML perspective, agent-of-payee doesn’t exempt anything – one must still KYC and
monitor because money could still be laundered through paying sham “payees.” The bank doesn’t get to
relax BSA just because state law says it’s not “money transmission.” For example, FinCEN still expects agent-
of-payee processors to catch suspicious payments .
Our use-case: If any of our business involves facilitating payments for goods/services, we could design it to
meet agent-of-payee conditions. That might allow us, in some states, to not worry about money transmitter
licensing for that piece. But since we already have a license, it’s somewhat moot for compliance (we’ll just
operate under our license anyway). Possibly, if we are not licensed in a particular state (maybe we avoided it
if not needed), having agent-of-payee structure would be our legal justification to operate there. Sponsor
banks will ask: “Are you licensed in all required states for what you’re doing?” If we say, “In State X we’re not
licensed because the model there is agent-of-payee and exempt,” the bank’s legal team will likely scrutinize
that stance. If clearly supported by law (like State X statute says agent of payee is exempt, and our facts fit),
they might accept it. If it’s grey, they’ll prefer we don’t operate there or get licensed anyway. Banks are a bit
conservative because of the Operation Choke Point history – they don’t want regulatory backlash for
banking an “unlicensed MSB.” They often include contract reps/warranties that we are properly licensed or
exempt in all jurisdictions we operate. So we must be very confident in any exemption claim.
Intra-program interplay: If one sub-MSB’s transactions are agent-of-payee and another’s are classic
money transmission, we can handle both under our umbrella, but we might categorize them differently in
reports. It doesn’t really affect the sponsor bank except possibly risk weighting (payee-agency might be
seen as lower risk, as mentioned).
16
68
36
Network and Consumer issues: For example, prepaid card loads could sometimes arguably be payee-
agency (like loading a transit card is paying a transit authority, arguably agent-of-payee). But those specifics
seldom change the compliance approach.
To directly answer: In sponsor bank relationships, agent-of-payee mostly affects whether the non-bank
partner needs state licenses. If not, some fintechs bypass having an MSB partner or license by using that
exemption. Since we have the licenses, we leveraged the other route (which ironically is more robust but
costly). In our scenario, agent-of-payee doesn’t deeply impact the bank’s relationship with us, other than if
we ever decided to not maintain a license somewhere due to that exemption, we must convince the bank
it’s fine.
One scenario: If we partner with an institution that itself relies on agent-of-payee, how does that work with
our layered model? Possibly redundant. But consider if we had a series that is an agent-of-payee
aggregator for merchants. That series might not legally be a “money transmitter” at all in many states. But
because it’s under our umbrella, we treat it as one for consistency. The bank doesn’t particularly need to
know the fine distinction; we just ensure compliance anyway.
Bottom line: Agent-of-payee exemptions provide an alternate legal route to offering payment services
without licenses. We chose a licensed model, so our obligation is mainly to be aware of agent-of-payee if it
benefits us or our clients in certain cases (like to expand to a state quickly where we lack a license, if
exempt). Sponsor banks care that all activities are above-board legally; if we claim exemption somewhere,
we must back it up. But the actual operations under a sponsor bank (the risk management, KYC etc.) remain
essentially the same whether a particular transaction is legally classified as money transmission or as
payment processing under agent-of-payee.
Thus, the interplay is: agent-of-payee can simplify regulatory licensing burden, which might indirectly
reduce complexity for the bank (fewer licenses to manage). But in our case, we are leaning on licensure, so
the bank focuses on that. If in future we pivot certain clients to agent-of-payee structure to avoid licensing
in new areas, we’d fully brief the bank and likely our compliance program would treat those flows with the
same rigor as licensed flows.
To summarize this section: FinCEN and states generally accommodate layered MSB-agent models as long as
the principal is responsible and transparent . No explicit limit on nesting is codified, but practically,
keep it to one level of agents to avoid regulatory disfavor. Disclose agents to FinCEN via maintained lists and
to states via delegate reports. The agent-of-payee exemption can reduce licensing needs in some cases, but
does not remove the need for strong AML controls or sponsor bank oversight. We will deploy whichever
legal structure (licensed or exemption) best fits a given client’s case, while maintaining consistent
compliance standards across the board.
4. Gift Card / Prepaid Program Specific Considerations
4.1 Sponsor Bank Requirements for Prepaid/Gift Card Programs
Prepaid card programs, especially those marketed to consumers (like gift cards, travel cards, general-
purpose reloadable cards), come with extra regulatory and network requirements. Sponsor banks in this
space are very experienced and often have entire departments for “prepaid compliance.”
10 4
37
Issuance & Regulatory Status: First, prepaid cards are considered “prepaid access” under FinCEN rules
if certain conditions are met. FinCEN requires providers of prepaid access (above certain thresholds) to
register as MSBs and implement AML programs . Our MSB registration already covers that category
(money transmitter and provider of prepaid access often overlap). So we are good there. The bank will
ensure we acknowledge being a prepaid provider if needed and have appropriate procedures (prepaid
often has limits to prevent anonymity, etc., e.g. $1000 limit for anonymous cards by FinCEN rule, otherwise
KYC needed). So one requirement: If any of our gift/prepaid products allow unverified usage above $1000,
FinCEN would call that a “prepaid program of interest” requiring full BSA measures. Usually, all open-
loop prepaid now requires KYC due to rules.
Regulation E (Electronic Fund Transfer Act) and CFPB Prepaid Rule: As of April 2019, the CFPB’s Prepaid
Accounts Rule (an extension of Reg E) covers many prepaid products (including reloadable cards and certain
digital wallets). It mandates: - Disclosure requirements: short-form and long-form fee disclosures must be
given to consumers before they acquire the card (or no later than with the card for retail packaging),
outlining all fees in a standardized format. - Error Resolution and Consumer Liability: Prepaid accounts
(except gift cards that are exempt as “store gift cards” or “promo cards”) get Reg E protections. That means
the sponsor bank (issuer) or program must investigate errors reported by consumers (like fraudulent
charges) and, if applicable, provide provisional credit within 10 business days, etc. Also, consumers’ liability
for unauthorized transactions is limited (if they registered the card, typically $50 if reported timely, etc.,
similar to debit card rules). - Periodic Statements or Alternatives: For prepaid, can either provide monthly
statements or make transaction history available online plus balance by phone and supply a written history
on request. - Submission to CFPB Prepaid Database: Issuers must submit their prepaid account
agreements to a CFPB database (except for certain business-use or private label cards). Sponsor banks will
ensure any consumer program is uploaded (with all fees, terms).
Our sponsor bank partner will likely put the onus on us (program manager) to draft these disclosures and
manage compliance, but the bank must review and approve them before launch to ensure they meet
regulatory standards. Banks like Bancorp or Sunrise have compliance teams that scrutinize the fee schedule
and marketing materials.
Consumer Financial Protections Specific to Gift Cards: Now, “gift cards” often specifically refer to cards
marketed as gifts, often non-reloadable, and there are special rules for them: - The CARD Act of 2009
instituted requirements for gift cards (store and bank-issued): - No expiration of funds less than 5 years
from issuance (though card plastic can expire if free replacement is available). - No inactivity fees unless 12
months of inactivity have passed, and then only under certain conditions (and clearly disclosed). -
Disclosures of key terms on the card or packaging (expiration, fees). - Many of those CARD Act provisions
were implemented via Reg E as well (Reg E has subpart for gift cards). However, store-branded gift cards
(closed-loop) and promotional cards are exempt from some Reg E requirements but often covered by state
gift card laws. Open-loop gift cards (general use prepaid) must comply with the above.
Sponsor banks will ensure our open-loop gift cards follow the CARD Act rules. They might require that any
fees (like monthly fees or inactivity fees) adhere to allowed patterns (very few gift programs charge monthly
fees nowadays due to these rules, except maybe an inactivity fee after a year).
Network Requirements: - Registration: Visa and MasterCard require that each prepaid program is
registered with them by the issuing bank. If we are program manager, the bank will list us as such in their
filings with the network. Networks also require that for certain high-risk programs (like those offering
69 70
38
certain features) background checks of program managers are done – the bank likely did that in due
diligence.
Program Risk Parameters: Networks have transaction code controls, velocity limits, and KYC rules
for prepaid. For example, MasterCard has a rule that anonymous prepaid cards can’t exceed $X load
or can’t be used internationally, etc. Since our programs will be KYC’d, we can have higher limits, but
then name must be on card etc.
Fraud and Chargeback Management: The program manager typically handles disputes at first, but
the bank is ultimately responsible for chargeback liabilities to the network. If our cardholders
dispute charges, we must follow network rules to submit those disputes and hopefully recover funds
from merchants. The sponsor bank will want us to have a competent chargeback process because if
we miss deadlines or mishandle, the bank might eat the loss or get fines. Galileo’s guide notes program
managers handle “dispute resolution and chargeback management” along network timelines
. We must meet those standards.
Reserve for Chargebacks: Many program manager contracts include a reserve particularly to cover
chargebacks, which can come months later. The Pathward FAQ we saw might be about unclaimed
property or old card balances , but also we should anticipate a clause that the bank can hold
funds to cover any negative balances or chargeback losses from the program. (E.g., if a card was
loaded via credit card and spent, then the credit card load is charged back as fraud, somebody has to
pay – often the program manager’s reserve covers it.)
AML for Prepaid: Prepaid cards historically were a money laundering concern (anonymous gift cards used
like cash). FinCEN addressed that with the prepaid access rule requiring collection of purchaser info for
cards above thresholds, etc. Our program will comply by requiring identification for significant loads or
international use. The sponsor bank will want to see that our activation and usage policies align with
FinCEN’s thresholds (e.g., if we allowed anonymous gift cards, we must cap them at $1000 max and not
allow international ATM use or reloads, as FinCEN’s regulation triggers registration if you issue more than
1000 to one person without info). We likely will just do KYC on all users, simplifying things.
Specific to Gift Card vs GPR (General Purpose Reloadable): - Gift cards (non-reloadable, sold as gifts) are
often exempt from some provisions (the CFPB prepaid rule largely exempted “store gift cards” and “promo
cards”, and partially general-use gift cards primarily for gifting – they still had CARD Act but not full Reg E
error resolution). But many open-loop gift cards voluntarily provide Reg E protections if registered. If our
program is strictly gift (non-reloadable, anonymous until given to someone), we might avoid Reg E’s full
force (except the CARD Act parts). But if it’s reloadable or used as a personal financial tool, it’s definitely
under Reg E Prepaid Rule. - We and our bank will decide how to categorize. Some banks actually prefer to
force even gift cards to have some level of registration for risk management. But often gift card programs
allow at least balance check and replacement if stolen (so some mechanism to tie to an owner at time of
use).
Escheatment (Unclaimed Property): We have a whole bullet below, but note: sponsor banks require that
unredeemed funds after a certain dormancy period be turned over to states as per escheat laws unless
exempt. The challenge: Many states exempt open-loop bank-issued gift cards from escheat (because the
CARD Act says funds can’t expire if card hasn’t, so conceptually nothing to escheat until maybe after 5 years
of inactivity). Some states still attempt to claim them if truly abandoned. The Pathward FAQ suggests that
•
•
71
72
•
21
39
customers or states have reached out about unclaimed balances . Program managers must track last
activity date of each card. For bank-issued cards, usually the bank files the escheatment (because the
obligation technically lies with the bank as the holder of the funds). However, the program manager must
supply data and often indemnify the bank for the amounts escheated. - Also some states (DE, NJ historically)
wanted to escheat unused gift card funds after a few years; companies tried to avoid by having gift cards
issued by banks in states with favorable laws (like South Dakota or Florida which exempt gift cards from
escheat). There were some legal disputes culminating in a Supreme Court decision in 2022 (Delaware v.
Pennsylvania) that ruled for certain financial instruments, the state of incorporation of issuer vs purchaser’s
address states and changed some escheat assumptions . It specifically concerned money orders and
such, but likely impacts gift card logic. - The result is complicated but basically, to avoid issues, our program
should comply with whatever the bank’s home state law is or overarching law. Some banks explicitly state
that “funds on open-loop prepaid cards do not escheat” due to federal preemption (some argue that the
federal banking regs preempt state escheat for deposit accounts at banks). Actually, a big Supreme Court
case (Texas v. New Jersey 1972) set rules: intangible property escheats to state of owner’s last address if
known, otherwise to state of holder’s incorporation. Many gift cards have unknown owners (if not
registered), so they tended to escheat to the state of the company’s incorporation (often Delaware, which
got windfall). The new Supreme Court case (2022) decided that MoneyGram official checks should go to
state of purchase instead, under federal law. That might later apply to some prepaid items. - Sponsor banks
like Pathward, incorporated in SD (which doesn’t escheat open-loop card funds, I think), have been asked by
states like Delaware for data. Pathward's FAQ implies they do send letters to cardholders about unclaimed
funds , likely to meet certain state demands or voluntarily reunite funds. - In any case, we will coordinate
with the bank on unclaimed property. Usually the bank’s legal team decides if/when to escheat. It’s often
after 5 years of inactivity, in the state of card purchaser’s address if known (like if card was registered) or
bank’s incorporation state if not. Program manager may have to fund any escheat obligations (like if bank
had turned over money, and then cardholder later claimed it, we might need to reimburse that).
Network Branding and Marketing: Sponsor banks also care about how the program is marketed. There
are network rules against misleading marketing, and using network logos properly (Visa requires their logo
appear a certain way, can’t be used in company name, etc.). The bank will review all card designs, websites,
terms, and even press releases about the program. This is more operational, but compliance ties in if
marketing could be deemed unfair or deceptive (UDAAP). For instance, if we called a product “FDIC-insured
gift card” that could confuse consumers (since funds are insured but card itself is not a deposit, etc.). The
bank’s compliance/legal will ensure all consumer-facing material is accurate (especially regarding FDIC
insurance, fees, how to get help, etc.) .
Transaction Monitoring: Prepaid cards are sometimes used for fraud (e.g., scammers ask victims to buy
gift cards). Program managers must have analytics to catch patterns (like rapid sequential card purchases,
or lots of small cards going to same address). The bank will ask how we mitigate such risks. Many sponsor
banks join fraud consortiums or require use of certain anti-fraud tools (as mentioned earlier with vendor
mandates).
Money Network Requirements (Sub vs Prime Program Manager): There is a concept occasionally called
“sub-program manager” if a primary program manager (like we are) allows another entity to run a program
under their oversight. This might happen if a program manager company white-labels the platform to a
third party. For example, Galileo or Marqeta can act as “super-program managers” enabling fintech startups
to have card programs without dealing directly with issuing banks; in those cases, the fintech is sort of a
sub-program manager or just a marketing partner, while Galileo/Marqeta is the actual registered program
73
74
21
42
40
manager with the bank and network. If we ever did similar (like allowed our corporate client to effectively
run a card program using our infrastructure), we would remain the official program manager. The networks
require that program managers not delegate program management without approval. So we likely would
have to notify the sponsor bank and maybe register any such arrangement with Visa/MC as a distinct
program under us. In short, sub-program managers are not typical; usually one program manager per
program. If a fintech wants to be the program manager, often they become it directly with the bank. For us,
since our clients want white-label under our compliance, we will be the PM and they’ll be more like
“corporate marketing partners.” The bank will require we keep control and treat the client like an agent.
State Money Transmitter + Prepaid: Many states consider selling prepaid cards as money transmission or
as “selling payment instruments” which requires a license. We have that, so fine. Some states exempt
closed-loop (e.g., store gift cards) but not open-loop. So being licensed covers us already.
To ensure we’re answering: sponsor bank additional requirements for prepaid include robust consumer
protection compliance (Reg E, disclosures), oversight of marketing, network rule adherence, and special
attention to fraud and unclaimed property. We need to abide by all of these as the program manager.
4.2 Regulation E and Consumer Protections in White-Label Prepaid Products
Expanding on Reg E:
Applicability: Reg E (Electronic Fund Transfer Act’s regulation) generally covers consumer accounts that can
store or transfer funds electronically. Prepaid cards and mobile wallets have been explicitly brought under it
by the CFPB’s Prepaid Rule, except: - Gift cards that are marketed and labeled as such (not reloadable,
primarily intended for gifting, or loyalty/promotional cards) are exempt from many Reg E requirements
except some gift card disclosures and restrictions (the CARD Act as noted). - Business-purpose prepaid (if
our client is issuing cards only for corporate expense use, that’s not consumer so Reg E doesn’t apply; but
network zero liability might optionally apply). - Payroll cards, student financial aid cards, etc., are covered by
Reg E but had their own mention prior to prepaid rule and now fall under prepaid rule anyway.
What Reg E means for us: - We must provide initial disclosures of fees and terms. For prepaid, the CFPB
standardized these with a “short-form” (e.g., a one-page box listing monthly fee, per purchase fee, ATM fees,
etc., and a statement “register your card for FDIC insurance and other protections” etc.) and a long-form
(full terms). The sponsor bank will insist these are given and likely require them to be on our website and in
packaging. - We need a process for dispute resolution: when a consumer claims unauthorized transaction
or error (like money loaded didn’t show up, or they were charged wrong amount), we must log the date of
notice, investigate (obtain any necessary info like merchant receipts), and resolve within 45 or 90 days
depending on scenario. If not resolved in 10 business days (20 for new accounts), we give provisional credit.
The sponsor bank is on the hook legally to the consumer if we fail, but our contract will make us responsible
to reimburse the bank for those claims. So they will audit how we handle disputes. Many program
managers outsource parts of this to processors (some processors have investigation teams that can gather
info from networks). - Customer service: Under Reg E, if we don’t provide monthly statements, we must
offer transaction history electronically or via phone. We likely will have an online portal. We must also have
41
a way for consumers to contact us with issues and have address to request written history, etc. The sponsor
bank may test our customer service (like a mystery shopper or require certain service level standards).
Error vs Fraud Distinction: “Unauthorized” use (fraud) is an error under Reg E requiring
investigation and often reimbursement if the cardholder didn’t fail to safeguard the card. If card is
registered (personal info on file), they get those protections; if not registered, some protections
might not apply. The CFPB rule allowed that unverified cards could be excluded from Reg E
protections until they are ID-verified (the logic is to encourage registration). So some programs say
“your card is limited to $X until you register; if you don’t register, we may not restore funds if lost.”
But if the card is reloadable or used beyond initial load, it basically must be registered and then fully
protected. We must clarify those things in disclosures.
Terms & Changes: We must give 21 days’ notice for any fee increases or significant changes (Reg E
requirement for changing terms). For gift cards (non-reloadable), terms generally don’t change since
it’s short-lived product.
CFPB Submission: As mentioned, after launch, the bank or we need to post the prepaid account
agreement on the CFPB’s website, and update it if terms change. The bank likely handles the
submission but we provide the doc.
UDAAP (Unfair, Deceptive, or Abusive Acts or Practices): We have to ensure marketing and operations
avoid any UDAAP issues. For example, not misleading about fees or FDIC insurance. FDIC pass-through
insurance: funds on prepaid cards are eligible for pass-through coverage if certain recordkeeping is done
(we must keep a ledger of each customer’s balance and ID so if bank fails, FDIC can reimburse individuals).
Sponsor banks require that. We should and will advertise “funds are FDIC insured once your identity is
verified” (if that’s the case). If we incorrectly suggest “Your money is FDIC insured because MetaBank is the
issuer” without clarifying registration requirement, the FDIC could consider that a misleading statement if
unregistered funds might not be claimed easily. So careful wording (the FDIC has issued cease-and-desist
letters to some fintechs for misrepresenting insurance). The MoFo tip #5 highlights that fintechs must make
insurance disclosures clear and accurate .
Complaint handling: The bank will expect we have a system to handle consumer complaints
(especially if any go to CFPB or regulator). They may review complaint logs in our audits. Any pattern
of complaints (like delays in refund, etc.) will worry them.
Summing up: White-label prepaid products essentially require us to step into the shoes of a bank in terms
of consumer protections. The sponsor bank ensures we do so because ultimately regulators will hold the
bank accountable for any shortcomings. We will need a robust compliance plan for the prepaid program
specifically, on top of our AML: covering Reg E, state gift card laws, escheatment, fraud, and customer
service. It’s a lot of detail, but sponsor banks have templated much of this – they often supply checklist or
even sample disclosures.
4.3 Network (Visa/Mastercard) Requirements for Program Managers vs. Sub-Program
Managers
Visa and Mastercard each publish rules and guidelines for prepaid card programs. Key points: -
Sponsorship: Only a principal member bank can issue cards. The program manager (us) must be vetted by
•
•
•
42
•
42
the bank and often by the network (networks sometimes require the bank to report any third-party agents
performing significant functions). For Mastercard, there’s a Registration for TPPs (Third Party Processors)
and TPAs (Third Party Agents). A program manager like us may be considered a TPA that needs to be
registered in MasterCard’s system by the bank. This involves a due diligence process and an annual fee
(Mastercard charges for registering each agent). - PCI DSS Compliance: If we handle card data (we likely
would in customer service or via our systems storing PANs), we must comply with PCI Data Security
Standards. The sponsor bank and networks mandate that. We should either be PCI certified or use a
processor that is (and ensure we never store full PAN unencrypted on our servers unless compliance is in
place). Typically, our processor (Galileo, i2c, etc.) is PCI certified and will tokenize PANs for us. But if we have
call center reps who can see card numbers, we need controls. The bank might request an annual PCI
compliance certificate from us. - AML/CFT in Networks: The networks require issuers to have programs to
detect and block certain transactions (e.g., transactions involving sanctioned countries might be blocked by
BIN routing, but if card is used online, that’s more on us to monitor and potentially restrict certain usage).
Program managers should ensure their cards can’t be used for unlawful transactions (like illegal gambling
sites, if network or law prohibits). - Sub-Program Managers: If we allow another entity to effectively run a
subset of the program, the bank must disclose that entity as an “Agent” or “Marketing partner”. For
example, if our MSB runs one card program for Client A and another for Client B, the bank might treat those
as separate programs under one manager (us). They might require separate BIN ranges for each brand.
Visa often uses separate BINs for different programs to segregate risk and reporting. That means we might
have multiple BINs under the bank – the bank might only allow that if volume warrants or to not mix funds.
- If a partner brand (our client) is heavily involved in distribution or servicing their end-users, the bank may
want to list them as well in the network’s agent registry, or at least do due diligence on them. - Galileo blog
pointed out that some fintechs outsource program management to companies like Galileo itself, but if you
become your own program manager you have control . We are essentially program manager for our
clients. - The networks do periodic audits of programs via the issuer. If a program causes lots of fraud or
cardholder complaints, the network can fine the issuer (which will then fine us). - There’s a concept of
“Program Certification” for Mastercard: new prepaid programs must often undergo an initial sign-off by
Mastercard’s Franchise team to ensure compliance with rules (like no prohibited fees, etc.). The sponsor
bank handles that submission, but we provide info.
If we consider “sub-program manager” as letting our client have some program responsibilities: We
remain the main program manager but might give them rights to enroll cardholders (like a corporate client
signing up their employees for cards). In such case, the bank will likely require that we ensure our client
abides by all network rules as if they were an agent of ours. That might include that the client company doesn’t
do anything to put network at risk (like selling cards in prohibited countries). We likely have to train our
client on relevant restrictions. The networks ultimately look to the issuer and primary program manager for
accountability.
Conclusion on sub-PM: It’s permissible to have branded sub-programs under a main program manager,
but all oversight and liability stays with the main. We might not even label them “sub-program manager”
formally to network; they might just be a marketing affiliate or distribution partner of our program. This
semantics aside, we should incorporate that arrangement’s oversight into our compliance waterfall.
4.4 State Gift Card Escheatment and Unclaimed Property Issues in White-Label Context
We partly covered this under sponsor bank requirements, but focusing on state laws:
75 76
43
Escheat Laws: Every state has unclaimed property laws requiring holders of unclaimed financial assets to
remit them to the state after a dormancy period (usually 3 or 5 years). Gift cards are a unique category: -
Many states exempt certain gift cards/certificates from escheat. The NCSL summary indicates some
states specifically say “gift certificates and general-use prepaid cards do not escheat” or only escheat if
certain conditions (like if there’s an expiration date or fees, etc.). For example, Illinois doesn’t escheat
general purpose reloadable cards under some circumstances. New York: exempts gift cards that don’t
charge dormancy fees or that never expire. - Some states treat open-loop (bank-issued) gift cards differently
from store gift cards. There’s often a definition: “gift card does not include prepaid bank card” –
meaning open-loop might not be considered a "gift card" for that state law (so they might treat it as a
“payment instrument” which could escheat). - Delaware historically claimed that many unused prepaid card
funds of companies incorporated in Delaware had to be escheated to DE after 5 years. That led companies
to try to avoid DE or incorporate special purpose gift card subsidiaries in states like VA or OH with favorable
rules. It was contested legally. The 2016 Temple-Inland case slapped DE for overly aggressive escheat (they
had to refund some companies). And the 2022 SCOTUS case likely further restricts DE from grabbing certain
prepaid amounts. - We need to see what state law our sponsor bank follows. If the bank is in SD,
historically SD doesn’t claim open-loop bank card funds. They might say such deposits are not subject to
unclaimed property if held by a bank since banks often follow federal rules. Actually, banks do escheat
dormant deposit accounts typically to state of last known address after e.g. 5 years. Prepaid card balances
might be considered a deposit in “subaccount” for the cardholder. If we have the cardholder’s address, the
bank would escheat to their state. - Many open-loop card agreements specify: “Your funds are not subject to
state unclaimed property laws as long as your card is active or funds are available” – some disclaimers exist
but not sure of legal weight.
White-label complication: If our client is in one state and the cardholders in many, who does the escheat?
The bank as issuer will do the actual transfer of funds to states. But we have to provide the data. Possibly
our contract will say we reimburse the bank for any escheated funds (although usually the funds belong to
cardholder who lost them by inactivity, so no one "owes" them except the state holds for them). - We should
have a system to flag when a card has had no activity for X years and attempt to contact the cardholder (to
avoid escheat if possible by reminding them to use or cash out). - States often require due diligence letters
to last known address a few months before escheating.
If our program is closed-loop gift cards (like a retailer’s own gift card): - Many states explicitly exempt
those if no expiry, etc., or if the unused value is under a certain amount. However, some states do require
escheat of closed-loop gift card balances (e.g., NJ briefly did, causing an uproar and partial repeal). - In a
white-label closed-loop scenario, if our MSB even touches those funds, we might be considered the
“holder”. But likely closed-loop gift cards wouldn't involve us because those are not money transmission
(they’re a merchant’s liability only). We mostly handle open-loop if at all.
Plan: Work closely with the sponsor bank and possibly hire an unclaimed property specialist or use software
to handle this. Banks often have a department for this. They might treat all prepaid accounts like deposit
accounts for escheat – which means the process is straightforward: - If card registered to “John Doe, 123
Main St, TX”, after 5 years no use, the bank sends the $20 to Texas unclaimed property office under John
Doe’s name. If not registered, and no name known, under federal rules if card is truly anonymous, it might
escheat to bank’s state. But because we likely will know who purchased the card at least via KYC at sale (for
open-loop, often they need a name or at least we track purchase location), it gets tricky. Some states treat
anonymous prepaid like money orders (which by federal Disposition of Abandoned Money Orders Act
77
19
44
actually require escheat to state of purchase). That SCOTUS decision said MoneyGram official checks should
follow that federal law. Some argue prepaid cards might be analogous to that law.
In short: It’s complicated, but we will: - Make sure our program terms inform cardholders that their funds
may be turned over to the state after period of inactivity (some states require that disclosure). - Provide all
needed data to bank’s unclaimed property team. - Ideally, design our product to minimize unclaimed funds
(encourage usage, allow easy redemption). - Keep records of any escheated accounts in case a customer
comes later. Usually, the customer can reclaim from state, not from us, once escheated. But some will come
to us confused; we then direct them to state treasury.
Example: Pathward’s FAQ letter likely was sent to cardholders to inform them their balance would escheat if
they don’t use it . We should have similar processes.
White-label responsibilities: If our client is the brand, they might get complaints from their users about
expired funds; we need to handle those PR issues. So part of white-label management is ensuring the client
understands unclaimed property is a legal requirement, not “the bank stealing your funds.” We’d help
message that.
Conclusion: The interplay of various state rules is complex, but sponsor banks typically have a stance for
their programs (some try to structure around escheat if possible; others comply fully). We as program
manager will follow whatever approach the bank uses, ensure compliance to avoid penalties (states do
audit companies for unreported unclaimed property and levy fines).
5. Risk Mitigation Strategies for Conservative MSB Operators
5.1 Transaction Types and Volumes Favored by Sponsor Banks
Sponsor banks, being risk-averse especially after regulator warnings, prefer certain profiles: - Domestic
over International: Purely domestic payment flows (within the U.S.) are easier to monitor and present
fewer geopolitical risks. If our transactions are mostly domestic ACH, domestic wire, domestic card spend,
banks see that as comparatively safer than international remittances or cross-border wires (which raise
sanctions, correspondent risk). Our focus on B2B including international businesses might involve cross-
border, but if we minimize high-risk corridors and ensure we have robust screening, it helps. - Account-
Based vs. Cash: Electronic account-based transactions (ACH, direct debit, card loads via bank accounts) are
more traceable. Banks shy from heavy cash operations (like an MSB with many cash-paying retail customers
depositing to the bank – that’s high AML risk). We position as digital-first (with clients funding via wire/ACH
from their bank accounts, not handing us cash). This is bank-friendly . - Low Fraud Business Models:
Banks like models with inherently lower fraud rates. B2B payments often fit – businesses doing invoices
have less fraud than consumer P2P or card payments acceptance which can have chargebacks.
Emphasizing that our clients are known businesses or regulated entities means less fraud (no random
public signups). That’s comforting to banks. - Moderate, Predictable Volume Growth: If an MSB client
shows transaction volume skyrocketing unpredictably, banks worry whether controls keep up. A
conservative MSB should forecast volumes realistically and try to stick close to plan. A bank would rather
see steady growth from $1M to $5M monthly over a year than a jump from $1M to $50M in a month, which
might freak out risk managers. So we might intentionally throttle or sequence onboarding of sub-clients to
keep volume growth manageable. Communicate volume expectations to the bank upfront so they can
calibrate risk. - Fully Transparent Use Cases: Each type of transaction we handle, we should be able to
21
78
45
articulate its legitimate purpose. For example: “We facilitate corporate payroll payments via prepaid cards,
or vendor payments via ACH.” These are straightforward. In contrast, if we said “We enable customers to
buy cryptocurrency or send money to friends globally,” that’s riskier. We likely avoid crypto entirely (given
current climate and our conservative stance). - No direct consumer marketing by us: Since we white-label,
we don’t have a public consumer brand soliciting random individuals. Our sub-clients have targeted user
bases (like their employees, or their own customers who underwent onboarding). Banks prefer that
because broad consumer-facing MSBs can attract fraudsters signing up. Focus on institutional/regulated
clients inherently filters out retail fraudsters. We also likely won’t do high-risk consumer categories (like no
payday loan loading, no gambling payouts unless thoroughly vetted, etc., unless we specifically decide to
with heavy compliance). - If we do gift cards: That ironically can be high-risk because of fraud (scams
asking people to pay in gift cards). But if our gift card program is a corporate incentive (B2B distribution),
risk is lower than selling gift cards in convenience stores to anyone. If we ever did open retail gift card sales,
we’d need strong fraud monitoring which we’d convey to the bank. - Transaction Monitoring Setup: Banks
will favor MSBs who use automated monitoring and analytics effectively. If we can explain our system (like
“we use XYZ software to monitor transactions in real-time and batch, with rules tuned to our business
model”), that reassures them that unusual activity will be caught and reported. - Specific Red Flags to
Avoid: Some patterns nearly always cause trouble: lots of small dollar transactions that aggregate to large
amounts (structuring), transactions involving known high-risk geographies (e.g. sanctioned or corruption-
prone countries), beneficiaries that are unusual given the sender profile, etc. We should design our service
to inherently reduce these: e.g., only allow sending to certain countries where we can comfortably vet
recipients, set limits that make structuring difficult, maybe disallow third-party payments (i.e., ensure the
payer and payee have a legitimate link). - Volume in line with compliance capacity: If our bank senses we
are processing volumes beyond what our compliance team could reasonably monitor, that’s a risk. They
might ask, “how many alerts do you get monthly and how do you handle them?” If we said, “1 compliance
officer handling 10,000 alerts,” that’s an issue. So calibrate volumes to team or plan to expand team as
volume grows. Show the bank those plans. - No or Low Crypto Exposure: Already said, but to emphasize:
Many banks essentially avoid crypto now after 2023 events. If any sub-client touches crypto (like an
exchange wanting to use us), that could endanger our banking. If we want to be conservative, probably
avoid crypto clients, or if we did take one, fully disclose and ensure the bank is okay and that client is well-
regulated (e.g., a FINRA or OCC regulated entity maybe using stablecoins? Even then many banks say no). -
High-risk Business Exclusions: We might proactively exclude categories like money orders, check cashing,
casino payments, cannabis-related transactions, etc., unless our bank specifically is okay and we have
licenses. This can be in our policy and we can show bank that list of prohibited client types or transactions.
That helps reassure them that we won’t inadvertently stray into extremely high-risk sectors without them
knowing.
5.2 Structuring the Program to Minimize Sponsor Bank Churn Risk
Sponsor bank churn (having to switch banks frequently) is disruptive and a known problem for fintech/MSB.
To mitigate: - Choose the Right Bank Upfront: We should do due diligence on prospective banks: prefer
those with stable track record in fintech, no looming regulatory troubles, and a commitment to the
business. For instance, banks publicly in BaaS often plan to continue, whereas some banks dip a toe and
then exit at first sign of trouble. If possible, speak to others in the industry about the bank’s behavior (some
may share experiences). - Multi-Bank Strategy: As MoFo suggests , not putting all eggs in one
basket reduces risk. Perhaps we use Bank A for certain services and Bank B for others, or have a backup
bank ready to onboard if needed. Some fintechs maintain an alternate bank account even if dormant, just in
case. In our case, maybe one bank for ACH and a different for card issuing – if one fails, not everything
27 26
46
stops. But managing multiple banks is resource-intense because each requires full compliance integration.
If we grow, it might become feasible to have redundancy. - Contractual Protections: As discussed,
negotiating a contract that gives us notice and transition assistance on termination is key . While we may
not have huge leverage, emphasizing that sudden termination could harm end customers might persuade
them to allow e.g. 60-90 days to wind down or port accounts. - Exceeding Expectations: If we become an
exemplary client for the bank (no compliance lapses, prompt responses, hitting all KPIs), the bank has little
reason to drop us. Often banks drop MSBs because examiners flagged them or the MSB caused an
embarrassment (like missed suspicious activity that later became a scandal). By investing heavily in
compliance and communication, we make the bank’s job easier and give examiners comfort. E.g., if we
regularly share metrics and improvements and have quarterly business reviews with the bank, it keeps
relationship healthy. - Financial Stability of Bank: We should monitor the bank's health (capital adequacy,
earnings, any negative news). If they seem to be under strain, we may preemptively prepare to move. Also
consider not keeping all client funds at one bank beyond FDIC coverage (if huge sums flow, though typically
banks have passthrough coverage for all). But if a sponsor bank failed (like SVB did to some fintechs, or
Silvergate etc.), our clients’ money could be temporarily inaccessible. Diversifying funds across more than
one bank’s accounts could mitigate impact of one bank failure. - Regulator Climate: Keep abreast of
regulatory signals. For example, if regulators issue guidance tightening BaaS oversight (like OCC did with
the consent orders ), be proactive: provide the bank info they need and maybe narrow any risky activities
so that when their examiner asks, there's minimal concern. - Scale Appropriately: Sometimes small MSBs
get dropped because the bank decides the revenue vs. risk isn’t worth it (especially if regulator pressure
increases fixed compliance cost, small accounts may be closed). If we want to keep the bank’s interest,
growing volume and generating some revenue helps. Or at least, paying their fees promptly and being a
cooperative partner. Some banks cut entire MSB programs due to regulatory fear (Operation Choke Point
style) but nowadays regulators say not to blanket-ban but do case-by-case. If we can get our bank to see us
as a well-managed low-risk MSB, they can justify to examiners why they keep us. - Open Communication:
Maintain regular communication channels with bank’s compliance and account managers. If an issue arises
on our side (e.g., a sub-client had a suspicious case we filed SARs on), inform the bank rather than them
discovering later. That transparency builds trust. - Contingency Planning: Internally, plan migration steps
in case of sudden termination: ensure data portability (we have all customer KYC and transaction records
organized, to provide to a new bank or to seamlessly continue operations if moved). If using a core
processor, maybe that processor is integrated with multiple banks and can switch the underlying bank
relatively quick – some BaaS platforms offer multi-bank resilience. If we’re direct with a bank, maybe keep
our program code and procedures bank-agnostic enough that onboarding another bank is not starting
from scratch. - Legal counsel involvement: Having good regulatory counsel can help if a bank termination
seems unfair or too abrupt; counsel might negotiate more time or find if any regulatory requirement (some
states require banks to give 30 days notice to MSB accounts closure - not common, but there was talk of
providing MSBs notice because of de-risking concerns). The Treasury’s de-risking strategy (2023) actually
recommended exploring requiring notice periods for account closures . It’s not law yet, but banks
might voluntarily accommodate if asked nicely.
5.3 Due Diligence on Sponsor Bank Stability and Reliability
As mentioned, we should vet potential banks on several factors: - Regulatory Status: Check if the bank is
under any enforcement action (those are public on OCC/FDIC websites). If a bank has a BSA consent order
or a safety & soundness memorandum, they might curtail high-risk customers until resolved. For example,
Blue Ridge’s OCC order in 2022 specifically limited new fintech partnerships – we wouldn’t want to
approach a bank under such constraints. Also see if management has signaled pulling back (some bank
25
79
80 81
28
47
CEOs publicly said they’ll reduce crypto or fintech exposure – avoid those). - Expertise: Does the bank have
a dedicated Fintech or MSB sponsorship team? (If yes, they likely understand our needs and have processes,
meaning smoother relationship. If no, they might be inexperienced or taking on only very low-risk, if any). -
Financial Health: Review the bank’s quarterly financials (Call Reports). Key ratios: Capital (Tier 1 leverage
ratio – ideally well above 5%), asset quality (non-performing loans ratio), profitability (consistent positive net
income), liquidity. Also the bank’s size – not too small that one MSB issue could topple them, and not so
large that we get lost (large banks rarely sponsor MSBs anyway). - Customer References: If possible,
discreetly talk to other fintechs or MSBs who bank with them. If they say the bank is tough but fair, that’s
fine; if they mention sudden shifts or poor communication, red flag. - Alignment with our Business: For
example, if our focus is international B2B, a bank that explicitly says “we only do domestic” is not a fit. If we
have a prepaid element, ensure the bank issues cards (not all sponsor banks do both ACH and cards). -
Jurisdiction/Charter: Some fintech sponsor banks are state-chartered (like a lot of those in fintech hubs),
some are nationally chartered. OCC regulated ones might be under more direct federal scrutiny, which
could be good (consistent standards) or bad (OCC has been hawkish under Hsu). State-chartered with FDIC
oversight might have a more lenient local regulator depending on state. Puerto Rico IFEs are regulated by
OCIF (PR regulator) – different environment. We have to weigh: an IFE might allow riskier stuff (like crypto) if
we needed, but might not have direct Fed payments access (though some do via corresponding). For
reliability, a U.S. mainland bank with Fed access is stable for payments. - Technology and Integration: A
reliable bank also means tech reliability. If their API or processing is often down, that’s trouble for us. Some
sponsor banks rely on third-party BaaS platforms for tech (like Synapse, Unit). If we go via such platform, we
should assess that platform’s track record too. - Contract Flexibility: Some banks have a reputation for
more reasonable contracts with fintechs (giving time to transition if needed, etc.). Through counsel or
network, we might glean which banks are easier to work with on that. For example, Coastal Community
Bank seems to have friendly relations with fintech partners, whereas another might be more strict. - Fee
Structure: If a bank’s fees are extremely low, wonder if they are cutting corners (or planning to change
later). If extremely high, they might be in it purely short-term for fee income – stable but expensive. A fair
fee schedule indicates a sustainable partnership (they get enough to justify continuing). - Look at Bank’s
Business Mix: If the bank’s deposit base is heavily fintech/MSB (like Signature was heavy on crypto, and
that concentration contributed to its run), that’s a risk if that sector is under stress. Balanced portfolio is
safer. But also if we’re one of only few MSB clients at a bank mostly doing regular community banking, we
could stand out in exams and be at risk if examiner doesn’t like one thing. Ideally, a bank with a well-
managed BaaS program of several fintechs – meaning they know how to defend it to regulators.
In summary, we need to “KYC” our bank as much as they KYC us. Checking public enforcement databases
and financials is key . The NEACH article we cited points out regulators are scrutinizing these
partnerships , so a stable bank is one that can handle that scrutiny, which typically correlates with strong
compliance culture. We want a bank that is not likely to exit the space abruptly – any public statements by
their executives or in earnings calls about their fintech strategy would be telling. For example, if a bank in
2023 said “we are reviewing our fintech partner strategy in light of regulatory concerns,” that’s a caution.
One that says “we have invested in enhancing our monitoring to support our growing fintech program” is
positive.
5.4 Red Flags Leading to Sponsor Bank Termination of MSB Relationships
What might cause a sponsor bank to drop an MSB client (or the entire program): - Regulatory Pressure/
Exam Findings: The number one cause in recent times. If examiners find the bank’s oversight of the MSB
insufficient or find issues in the MSB’s activities that scare them, they may implicitly or explicitly encourage
82
83
48
the bank to sever ties. For example, if examiners saw that our MSB had multiple SAR filings indicating
maybe high-risk transactions the bank wasn’t aware of in advance, they might fault the bank’s monitoring.
To appease, the bank could limit or terminate the program. Or if the regulator has a general crackdown
mood (like post-Signature, some banks simply off-boarded crypto clients preemptively). - Significant
Compliance Lapse by MSB: If we had a situation like a sanctions hit that we failed to catch and the bank
discovered it (say we unknowingly facilitated a payment to an OFAC-sanctioned party and didn’t block it but
the bank’s downstream filters caught it), that’s serious. The bank might decide we’re too risky. Another lapse
might be not filing SARs when obviously needed. Or a data breach that shows we didn’t secure data, making
the bank look bad. - Criminal or Civil Actions Involving MSB: If our MSB (or key people) were indicted or
sued by regulators, many banks would immediately terminate (since bank doesn’t want to be associated or
risk being considered complicit). Even a negative news story can cause a bank to re-evaluate. E.g., if one of
our sub-clients was involved in a scandal (say, a foreign partner was charged with money laundering
abroad), the bank might freeze that part or drop us if they think we have systemic due diligence issues. -
High Fraud or Losses: If our program experiences fraud that causes losses the bank has to cover (like lots
of chargebacks not reimbursed by us, or customers defrauded which leads to reputation issues), the bank
might cut it. They are very sensitive to anything that could harm consumers and bring backlash (since
regulators will hold the bank accountable under UDAAP if consumers are hurt). - Volume or Business
Change without Notice: If we suddenly pivot or expand into an area outside what the bank approved (e.g.
we start offering services to a new country or type of customer without telling them), and they find out,
trust is broken. The bank’s third-party risk policy likely states the partner must notify of significant changes.
Not doing so can lead to termination for breach. - Exceeding agreed limits repeatedly: For example, if we
often overshoot transaction volume limits or have too many large transactions beyond expected profile, the
bank sees that as loss of control. If we can’t rein it in or explain, they may decide it’s out of their risk
appetite. - MSB’s Financial Instability or Corporate Changes: If we were to get into financial trouble
(couldn’t pay fees, or rumors of insolvency) or got acquired by someone the bank doesn’t approve of, they
might end the relationship. Banks often have change-of-control clauses – if our ownership changes
significantly, they reserve right to re-due-diligence or terminate. So any such event, we should coordinate
with them early to not spook them. - Lack of Cooperation: If we were slow or resistant in providing
information (like ignoring audit findings, or law enforcement requests via the bank), the bank will see us as
a liability. Non-responsiveness can be fatal. - Running Afoul of Bank’s Internal Risk Limits: Banks have
concentration limits – maybe they don’t want any single fintech program >10% of their deposits. If we grew
huge, the bank might ask us to find another banking partner for overflow rather than keep concentrating
risk with them. Or if overall BaaS exposure is making their regulators nervous, they might trim number of
partners (maybe dropping the smaller ones to reduce oversight burden). - High SAR Volume: If our
program is generating a disproportionately high number of SARs relative to volume (indicating high
suspicious activity levels), the bank may question the quality of our customer base. They might give us a
chance to tighten onboarding or drop risky clients, but if not improved, they could exit us. They don’t want
to constantly file SARs – it’s risk overhead and could trigger regulator suspicion that the bank’s client base
(us/our subs) is inherently risky. - Specific Red Flags from FinCEN/FDIC: FinCEN advisories highlight things
like foreign MSBs using personal accounts, etc. If any such known red flag scenario was identified (e.g., if
our sub-agents are sending funds to countries under advisory lists frequently), the bank could consider that
too risky to continue. - Strategic Business Decision: Sometimes not directly a “red flag” but the bank’s
strategic shift (maybe new management decides to exit all MSB clients). It happened in the past (mass
closures). But regulators now push against de-risking without case-by-case, yet a bank can still choose its
business lines. We can’t control that except to detect early signs.
49
To mitigate these, we: - Ensure robust compliance to avoid big lapses. - Keep open dialogue so potential
issues are addressed before they blow up. - Possibly diversify bank relations as noted, so one termination
isn’t end-of-business for us.
Now combining these insights to produce our deep research memo as requested, with an executive
summary, detailed sections, citations, comparison table, risk matrix, and recommendations for our model.
Sponsor Bank Partnership Models for MSB
White‑Label Payment Services
Executive Summary
Business Model: We operate a Montana-based series LLC functioning as a “master” money services
business (MSB) that provides white-labeled payment services to sub-MSB clients. The parent MSB holds
the required FinCEN registration and state licenses, while each client-specific series acts as an agent (or sub-
MSB) under the parent’s compliance umbrella. Our clients are primarily international businesses, regulated
institutions, and companies seeking branded payment programs. We have minimal direct U.S. consumer
exposure and favor clearly permitted, low-risk activities.
Key Findings:
Sponsor Bank Partnership Structures: MSBs typically partner with banks via three models: (1)
Direct account relationships – the MSB uses a standard bank account (high risk category) for its
aggregated funds; (2) Banking-as-a-Service (BaaS) – the bank provides API-based accounts or sub-
accounts (often FBO accounts) so the MSB’s end-users are effectively customers of the bank; and (3)
Program manager sponsorship – for card programs, where the bank issues cards and the MSB
manages the program (onboarding, customer service) as the bank’s agent . Each model
allocates compliance duties differently and has pros/cons (see Table 1 below). Sponsor banks often
prefer BaaS or program-manager models where they can maintain greater oversight (e.g. approving
the MSB’s KYC/AML processes) . Banks known to actively support MSB/fintech programs include
fintech-focused institutions like Evolve Bank & Trust, Cross River Bank, The Bancorp Bank, and niche
banks in Puerto Rico (IFEs like FV Bank) that cater to international fintechs . These banks are more
tolerant of layered structures provided that the MSB has robust controls. Typical contract terms in
such partnerships heavily favor the bank: they require strong reserve and collateral provisions,
allow broad termination rights, and mandate strict compliance obligations on the MSB (e.g. using
bank-approved KYC vendors, observing transaction limits) . Importantly, banks often include
clauses to ensure a transition period if the partnership ends – though MSBs are advised to
negotiate explicit provisions allowing program migration to a new bank to mitigate sudden account
closure .
Compliance Delegation & “Waterfall” Framework: In a sponsor bank/MSB arrangement, Bank
Secrecy Act (BSA/AML) responsibilities are contractually divided but ultimately shared. The sponsor
bank remains federally accountable for BSA compliance, which is why regulators hold banks liable
for any compliance gaps in fintech partnerships . The bank will therefore dictate or approve the
MSB’s AML program elements (CIP procedures, sanctions screening, monitoring rules) and require
•
2 8
2
34
1 22
25
•
9
50
regular reporting . The MSB executes those front-line compliance tasks and oversees any sub-
agents, while the bank provides oversight and audits the MSB’s program. For example, the bank may
require pre-approval of the MSB’s KYC processes and even mandate specific KYC/AML technology .
Suspicious Activity Reports (SARs) and Currency Transaction Reports (CTRs) are handled at
multiple levels: the MSB (parent) must file SARs on suspicious activities of its customers (including
those serviced by sub-agents) , and the sponsor bank files SARs if it detects suspicious activity
involving the MSB’s accounts (or if it finds the MSB is not in compliance, such as operating
unlicensed) . The MSB and bank typically share information on SAR-worthy activity to ensure
proper reporting by both. CTRs for cash transactions must be filed by whichever entity physically
receives or controls the cash – e.g. if an MSB agent takes in >$10k in cash, the MSB files the CTR; if
the MSB then deposits that cash in the bank, the bank also aggregates for CTR filing. Importantly,
sub-MSB agents can rely on the parent MSB’s compliance program and are not required to
maintain independent BSA programs or register separately with FinCEN (FinCEN exempts agents of
MSBs from separate registration) . Instead, the parent’s AML program must extend to all agents,
and the sponsor bank will expect to review how the parent MSB trains, monitors, and audits its
sub-agents . This “compliance waterfall” means the bank audits the MSB, and the MSB in turn
audits its agents, creating layered oversight. We provide a risk-ranked matrix of compliance
delegation approaches in Section 2, illustrating that the more removed the bank is from end-
customers, the higher the oversight burden and regulatory scrutiny on the MSB’s controls.
Regulatory Treatment of Layered MSB Structures: FinCEN permits MSB networks with agents,
viewing the licensed principal as the responsible party. FinCEN explicitly states that an entity acting
solely as an agent of a registered MSB is not required to register independently , and requires
principal MSBs to maintain a current list of agents and make it available to regulators on request
. The principal’s AML program should incorporate its agents and include agent management
policies (due diligence, contracts, termination rights) . There is no hard limit on “nesting” depth
codified in FinCEN rules, but additional layers (e.g. agent-of-an-agent) can blur accountability and are
generally discouraged. State regulators similarly allow authorized delegate arrangements under a
licensee, usually with conditions: the licensee must notify the state of each delegate, bond them in
some cases, and remain liable for their actions. States do not favor multiple sub-delegate levels –
practically, every entity that offers money transmission services to the public should either be a
licensee or a direct authorized delegate of a licensee. Our series structure addresses this by making
each series a direct authorized delegate of the parent for state purposes (and disclosing all trade
names/series in licensing records). Disclosure is critical: We will disclose our layered structure in all
relevant FinCEN filings (agent list) and state license applications/renewals. Transparency about our
series-agents ensures regulators understand that transactions are covered under the parent’s
license and compliance program. Many states also recognize “Agent-of-the-Payee” exemptions
(where receiving funds on behalf of a seller/payee is not treated as money transmission) . While
this exemption can sometimes apply to our clients’ business models (e.g. certain payment
processing scenarios), under our partnership we typically operate under the MSB license framework
to ensure broad compliance. In practice, agent-of-payee arrangements do not reduce our federal
AML obligations – even if a transaction is exempt from state licensure, the bank and MSB must still
treat it with full BSA/OFAC controls. Sponsor banks primarily care that all activities are either properly
licensed or clearly exempt by law; if we rely on an exemption in a jurisdiction, we must provide the
legal rationale to the bank. Bottom line: regulators are comfortable with our layered MSB-agent
model so long as the parent MSB exercises effective control and all parties are transparent.
FinCEN has even noted that a robust agent oversight program is expected of any large MSB . We
2
2
12
11 13
10
58
•
10
58
58
16
58
51
will avoid any “rogue” nesting (no sub-agents of sub-agents) and will promptly inform regulators and
the bank of all agents and their locations.
Gift Card & Prepaid Program Specifics: Operating white-labeled prepaid card or gift card
programs adds additional regulatory layers and sponsor bank requirements. Sponsor banks
(issuers) are responsible for ensuring such programs comply with Consumer protection
regulations (Regulation E) and the CFPB’s Prepaid Accounts Rule, as well as network (Visa/
Mastercard) rules. This means our program must provide the required disclosures (e.g. fee schedules
in the CFPB-prescribed format) and afford consumers protections like limited liability for
unauthorized transactions and error resolution rights, unless an exemption applies (e.g. closed-loop
gift cards have certain federal exemptions) . The sponsor bank will require us to draft and use
compliant cardholder agreements and disclosures, and will review our customer service and dispute
handling procedures. For example, if a customer of a prepaid card complains of an unauthorized
charge, we as program manager must investigate and, if warranted, provide provisional credit
within 10 business days – the bank will audit our adherence to these Reg E timelines. Visa/
Mastercard Requirements: The networks mandate that program managers adhere to strict
operational and security standards. The bank must register us (and our program) as a Third-Party
Agent with the card network, which involves due diligence and sometimes annual audits. We must
maintain PCI DSS compliance (data security for card info) and follow network rules on fraud
monitoring, chargeback processing, and usage limits. For instance, Visa/Mastercard have rules limiting
anonymous prepaid card functionality (no international ATM access for unregistered cards, etc.), and
requiring KYC for cards above certain load values – our program will enforce those limits in line with
FinCEN’s prepaid access rule . Unclaimed Property (Escheat): We must also address state
unclaimed property laws for unused prepaid/gift card balances. Many states exempt open-loop gift
cards from escheat or set dormancy periods (often 5 years) after which funds must be turned over to
the state . In a white-label context, the sponsor bank typically handles the escheatment filings
(since the bank is the issuer holding the funds), but we must supply data on dormant accounts and
perhaps attempt customer contact before escheat. For example, if a prepaid card hasn’t been used
for 5 years, the funds may have to be remitted to the cardholder’s state of last address (or the bank’s
incorporation state if the address is unknown). We will coordinate closely with the bank on these
requirements – some states do not require escheat of certain gift cards , but others do, and we
must be compliant in each jurisdiction to avoid penalties. Network Liability & Reserves: Sponsor
banks often require program managers to fund a reserve account to cover potential losses
(chargebacks, fraud). Contractually, we will bear financial responsibility for any network fines or
reimbursement obligations arising from our program’s operation. Overall, prepaid programs bring
a host of consumer compliance obligations – our conservative approach is to meet or exceed all
applicable requirements (e.g. treating our open-loop gift cards as Reg E “prepaid accounts” with
protections, even if some might arguably be exempt as gift cards). This not only keeps regulators
satisfied but also builds trust with our bank and cardholders.
Risk Mitigation for Conservative Operations: To maintain long-term bank partnerships (and avoid
the churn that plagues higher-risk fintechs), we will structure our program deliberately to be “bank-
friendly.” This means focusing on transaction types and customer profiles that banks view as
lower risk: predominantly domestic, account-based transactions among known parties, rather
than anonymous or cash-intensive flows . Our use-cases (B2B payments, corporate prepaid
programs, etc.) inherently involve verified businesses and institutions, which reduces fraud and AML
risk compared to retail money remittances or crypto trading. We will avoid high-risk sectors (e.g. no
•
19
69 70
74
19
•
78
52
crypto exchange involvement, no online gambling payments, etc., unless explicitly approved by the
bank with extra controls) and avoid high-risk corridors (transactions involving sanctioned or
unstable regions). By keeping our activities squarely within well-understood, permissible bounds, we
make it easier for a sponsor bank to support us. Additionally, we will throttle growth to a
manageable pace and be transparent with the bank about expected volumes – sudden, exponential
spikes in volume can alarm bank risk managers, so our conservative plan calls for scaling in
measured increments and continuously demonstrating that our compliance infrastructure scales
with it. We also conduct thorough due diligence on potential sponsor banks to choose a stable
partner: we look for banks with strong fintech partnership experience, a clean regulatory record (no
recent BSA/AML enforcement actions), and commitment to the space (as evidenced by public
statements or sustained operations) . Once partnered, we emphasize proactive communication
and collaboration: for example, providing the bank with regular compliance reports, audit
findings, and any emerging issues before they become problems. By essentially making the bank’s
oversight job easier, we reduce reasons for them to exit the relationship. We will also negotiate for
contractual provisions that give us adequate notice (ideally 30–90 days) in case of termination
without cause , and maintain contingency plans (including identifying backup banks or
modularizing our technology for easier porting) to ensure continuity of service if we must transition.
Finally, we continually monitor our own program for red flags that could trigger bank
termination, such as unexplained surges in suspicious activity reports, compliance audit failures, or
negative news involving our clients. If any such risks arise, we address them immediately in
coordination with the bank. Our goal is to build a reputation as a low-risk, highly compliant MSB
program – one that a sponsor bank can confidently defend to regulators as an example of a
responsible partnership (aligned with the U.S. Treasury’s guidance to avoid blanket de-risking).
The sections that follow provide an in-depth analysis of each of these areas, with supporting citations from
FinCEN guidance, federal banking agency rules, state regulations, and industry sources. A comparison table
of sponsor bank partnership models is included, along with a risk matrix of compliance delegation
approaches. We conclude with recommendations tailored to our series LLC MSB model, aiming to solidify a
resilient, regulatorily sound bank partnership structure for our white-label services.
1. Sponsor Bank Partnership Structures
When an MSB like us seeks to access banking services, there are several structural options for partnering
with a bank. The appropriate model depends on the services we need (e.g. card issuance vs. just holding an
account) and on the bank’s risk appetite and capabilities. Below, we outline the primary partnership models
and how they function, then discuss how sponsor banks evaluate MSB clients with layered structures,
typical compliance and contractual features, and identify banks active in this space.
1.1 Primary Models for MSB–Bank Relationships
Direct Account Relationship (Traditional Banking): The MSB opens a deposit account (or a set of
accounts) in its own name at a commercial bank and uses that account to conduct transactions on behalf of
its customers. The bank in this scenario treats the MSB as the customer of the bank. The MSB’s funds
(aggregated from its customers) flow in and out of this business account. From the bank’s perspective, this
is the simplest arrangement administratively, but it can be high risk. Banks categorize MSB accounts as
inherently higher-risk and will apply enhanced due diligence and monitoring . Key characteristics:
82
25
3 58
53
The bank does not directly know the MSB’s end-customers or the purpose of each transaction – it sees only
the MSB’s pooled credits and debits. Compliance-wise, the bank focuses on the MSB’s own profile (e.g.
ensuring the MSB is licensed, has an AML program) and monitors aggregate flows for anomalies, while the
MSB is responsible for KYC/AML on its individual customers. Advantages: Simplicity (only one account to
manage), and the MSB retains full control over its customer relationship and branding (the bank stays
completely in the background). Many smaller MSBs (like independent money transmitters) operate this way,
essentially using the bank just to clear and settle funds. Disadvantages: Many banks are reluctant to offer
these accounts at all – “de-risking” led to countless MSB account closures in the past . Those that do
keep such accounts often impose strict limits (e.g. capping daily volumes) and require extensive ongoing
reporting from the MSB (such as quarterly agent lists, compliance audits, etc.) . Additionally, because
the bank only deals with the MSB entity, if a problem arises with an end-customer or agent, the bank might
overreact by freezing or terminating the entire account, having little visibility or control beyond the MSB
itself. Use case: This model might suit an MSB with a small, stable agent network and predictable flows, or
one that primarily needs a clearing account for funds transfers (e.g. an MSB that aggregates remittances
and then wires out through one account). But it is less suitable for a complex program with many sub-
clients, where the bank would want more insight.
Banking-as-a-Service (BaaS) / FBO Sub-Accounts: In the BaaS model, the bank extends a technical
platform (often via APIs) that allows the MSB/fintech to open and manage sub-accounts or digital ledgers
on behalf of its end-customers. The MSB’s customers might not even realize the bank is involved – the MSB
provides the interface, while the bank holds the funds behind the scenes. A common structure is the FBO
(For-Benefit-Of) account: the bank holds a master deposit account in the MSB’s name “for the benefit of”
the MSB’s customers, and the MSB maintains detailed records of each customer’s balance .
Alternatively, some BaaS banks open individual named bank accounts for each end-customer (with the MSB
as an agent or service provider on the account). In both cases, the bank’s charter is being leveraged to
provide what amounts to “virtual banking” services to the MSB’s clients – be it transaction accounts,
stored balances, ACH payments, wire capabilities, etc. Compliance structure: Typically, the bank treats the
MSB’s end-users as customers of the bank (particularly if individual accounts are opened or if regulations
consider the funds to be deposits). Therefore, the bank has BSA obligations for those individuals/entities. In
practice, however, the fintech MSB performs most customer-facing compliance tasks (CIP/KYC, transaction
monitoring) under the bank’s oversight . The bank will often require the MSB to follow the bank’s
Customer Identification Program and Anti-Money Laundering (AML) standards when onboarding users, and
may even pre-approve the MSB’s KYC checklist and tools . The MSB then sends customer data to the
bank or makes it available for audit. The bank might have real-time API access or batch reporting to keep
track of key events (new accounts opened, large transactions, etc.). This model creates a direct legal
relationship (and thus accountability) between the bank and the end customer, which regulators find clearer
than a purely arm’s-length account. Advantages: It provides more assurance to the bank and regulators
that BSA/AML controls are in place at the customer level (since the bank can say “these are legally our
customers, and we ensure KYC via our agent fintech”). It also unlocks bank-level features for the program:
for example, FDIC insurance on customer balances (pass-through insurance to individual holders) and
direct connectivity to payment networks (FedWire, ACH clearing house, card networks via the bank BIN).
Fintechs use BaaS to offer “bank-like” accounts without being banks – e.g. a payment app giving each user
an account number and routing number at the partner bank. Our model might leverage this for certain
client needs, like giving each sub-MSB or their end-users a sub-account for holding USD funds. Challenges:
Not every bank offers true BaaS with API integration – those that do often require a certain scale and
technological capability on the fintech’s side to integrate. Additionally, because the bank’s regulatory
exposure is higher (lots of individual customers, all technically the bank’s customers), these banks enforce
84 85
61 58
36 86
2
2
54
very detailed compliance requirements and may even sit in on certain processes. For instance, it’s common
that “the sponsor may mandate specific vendors (e.g., Alloy for KYC, Socure for identity verification)” to ensure
consistency . There can also be more fees (BaaS banks charge per API call, account, or transaction,
making it potentially pricey for low-margin uses). Use case: This model fits well when our MSB wants to
provide branded accounts or wallets to clients (like each sub-MSB or even their customers get an account
number or card issued by the bank). It’s essentially the model behind many “fintech banks” and neo-banks
where a bank empowers a fintech to offer account services. For our structure, if we wanted each series
(sub-MSB client) to have its own segregated account at the bank (instead of pooling all series funds in one
account), BaaS could allow that – perhaps even with separate FBO sub-accounts per series, so that each
client’s funds are ring-fenced. Many sponsor banks are comfortable with this as it gives them clarity on
whose funds are whose, and it aligns with the technology-driven oversight regulators encourage (some
banks can set up transaction monitoring per sub-account to manage risk).
Program Manager Sponsorship (Card Issuing & Payment Programs): In this model, the bank acts as a
card issuer or payment clearing bank, and the fintech/MSB serves as a Program Manager operating a
specific product/program under the bank’s auspices. This is very common for prepaid cards, debit cards,
and fintech apps that issue cards. The bank provides the licensed authority to issue the payment
instrument (for example, only an FDIC-insured bank or similar can be a principal member of Visa/
Mastercard to issue cards), and the BIN (Bank Identification Number) on the cards belongs to the bank
. The fintech (program manager) designs and runs the program: it markets the card or app,
onboards users, manages customer support, and often chooses the processor and card network programs
(with bank approval). The arrangement is formalized by a Program Management Agreement. Compliance
structure: The bank is directly accountable to the card networks and regulators for the program’s
compliance. However, much of the day-to-day compliance work is delegated to the program manager per
contract. The program manager “stands in the shoes” of the bank for many obligations, but the bank must
actively oversee. As noted by an industry guide, “program managers ensure compliance with the sponsoring/
issuing bank’s and payments networks’ exacting rules and standards, which touch almost every part of your
program” . This includes KYC of cardholders, AML transaction monitoring, sanctions screening, and
adhering to network rules on disclosures and anti-fraud measures. The bank will typically have the right to
pre-approve all marketing materials, fee structures, and terms and conditions for the program to ensure
they meet regulatory requirements (Reg E, etc.). It will also often require the program manager to submit
periodic compliance reports and performance metrics (fraud rates, dispute rates, etc.). Many sponsor
banks maintain a compliance checklist specifically for fintech programs, covering everything from
customer identification procedures to complaint handling. From the network perspective, the Program
Manager might need to be registered as a Third-Party Service Provider with Visa/Mastercard through the
bank, and undergo network due diligence as well. Advantages: This model allows non-banks to launch
payment products relatively quickly by leveraging the bank’s existing network memberships and
infrastructure. Our MSB, acting as a program manager, can issue white-labeled cards or accounts for our
clients without each client needing to individually partner with a bank. The bank essentially sponsors our
entire program, and we can onboard multiple sub-clients under that umbrella (with the bank’s knowledge
and consent). For example, we could have a Visa prepaid card program managed by us, where each series
client brands the card for its customers – we remain the primary Program Manager, and the series might be
a “Sponsored sub-program” for branding and distribution. Disadvantages: Because the bank’s liability is
on the line if anything goes wrong (e.g., consumer harm, unauthorized charges, regulatory violations),
sponsor banks in these arrangements can be very stringent. They often reserve the right to halt new
customer enrollments if certain risk thresholds are exceeded, or to require changes to the program (for
instance, if fraud losses spike, they might insist on new controls or even dropping a risky segment of users).
2
87 88
17 18
55
Contractually, the bank can usually terminate the program with limited notice if major compliance issues
arise. Also, financially, the revenue sharing might be structured such that the bank gets a portion of
interchange or fees – that can affect program economics. Use Case: This model is ideal for our white-label
gift card or prepaid offerings. For example, if one of our series clients (say a fintech in Europe) wants to
offer a U.S. dollar prepaid card to its U.S. customers, we can manage that program via a sponsor bank. The
bank issues the cards, we handle program operations, and our series client handles marketing under our
supervision. Likewise, for any corporate incentive or payroll card programs we power, this is the needed
structure. Essentially, whenever a payment instrument (card or similar) is issued, this program manager
approach is used.
The table below summarizes these models and highlights how compliance responsibility is typically divided
in each:
Table 1 – Comparison of Sponsor Bank Partnership Models
Model Description &
Examples
Bank’s Role &
Exposure MSB’s Role Compliance
Allocation
Direct Account
MSB uses a
standard
business
deposit
account at the
bank for all its
customer
fund flows.
<br>(e.g. A
remittance
company
keeps one
clearing
account to
send/receive
all transfers.)
Bank is
custodian of
MSB’s pooled
funds. Treats
MSB as the sole
customer (high-
risk category).
No direct
interaction with
MSB’s end-
users; bank
monitors the
MSB itself
.
MSB manages
all customer-
facing
operations
(KYC,
transaction
processing) on
its own. Bank
provides
generic
services
(holding
funds,
executing
wires/ACH for
the MSB).
MSB-centric
compliance: MSB
must have full BSA/
AML program
covering its
customers. Bank
conducts due
diligence on MSB
(verify FinCEN
registration, state
licenses ) and
monitors aggregated
account activity .
Bank files SARs if
MSB’s account
activity is suspicious
(or if MSB is
unlicensed) . MSB
files SARs on
individual customer
transactions .
Little to no insight by
bank into individual
transactions – high
reliance on MSB’s
compliance.
3
4
32
61
13
12
56
Model Description &
Examples
Bank’s Role &
Exposure MSB’s Role Compliance
Allocation
BaaS / FBO Sub-
Accounts
Bank provides
API/platform
for fintech to
open sub-
accounts or
digital wallets
for end-users.
Often uses a
master “For
Benefit Of
(FBO)”
account with
sub-ledger for
each user .
<br>(e.g. A
fintech app
gives each user
an e-wallet;
funds sit at
bank under
app’s FBO
account.)
Bank holds
customer funds
(often as
insured
deposits under
its EIN). Bank
may consider
end-users as its
own customers
in legal terms.
Provides core
banking
functions via
API (account
numbers, ACH,
wires, debit
cards).
Significant
bank oversight
of compliance –
effectively
extending its
banking
operations
through the
fintech .
Fintech MSB
acts as an
agent of the
bank in
managing
accounts.
Performs
onboarding,
KYC, and
front-end
transaction
monitoring,
using bank-
approved
processes.
Manages user
experience,
customer
service, and
tech
integration.
Joint compliance:
Bank dictates CIP/
KYC standards and
must approve the
MSB’s AML controls
. MSB executes
day-to-day checks
(identity verification,
suspicious activity
monitoring) and
reports results to
bank. End-users are
often “customers” of
both. Bank monitors
the program as a
whole and can see
individual account
data. SAR filing can
be by bank (since it
sees transactions) –
often in coordination
with MSB. MSB may
file SARs as an MSB
as well, but many
BaaS banks handle
most SAR reporting
centrally. Both bank
and MSB are
responsible for OFAC
screening. Bank
typically requires
MSB to use specified
vendors or systems
for consistency .
36
88 2
2
2
57
Program Manager
(Card Issuance)
Bank
sponsors a
specific
payment
program
(prepaid card,
debit card,
etc.) managed
by the MSB.
The MSB is
the Program
Manager,
handling
operations
under the
bank’s
oversight .
<br>(e.g. Bank
issues a Visa
prepaid card;
Fintech X as
program
manager
markets the
card, enrolls
users, and
manages
transactions.)
Bank is the
licensed issuer
( BIN holder )
for cards or
accounts . It
bears
regulatory
accountability
(to OCC/FDIC,
CFPB, card
network) for
consumer
compliance and
fund safety.
Bank must
ensure the
program
complies with
all applicable
laws (Reg E,
UDAAP, KYC,
etc.) – it
therefore
retains veto
power on
program
decisions and
monitors the
MSB closely.
Bank’s
exposure:
reputational
and compliance
risk if program
missteps.
MSB designs
and runs the
day-to-day
program:
branding,
marketing,
onboarding
cardholders,
setting pricing
(with bank
approval),
servicing
customers
(call centers,
dispute
resolution),
and managing
relationships
with
processors or
distributors.
The MSB
essentially
acts as the
bank’s agent
in operating
the product.
Delegated
compliance under
tight oversight:
Program Manager
MSB must follow
bank-approved
procedures for KYC,
transaction
monitoring,
antifraud, and
customer disclosures
. MSB
typically performs
CIP and transaction
monitoring on
cardholders, and
reports any suspicious
activity to the bank for
SAR filing (often the
bank files the SAR as
the issuer) . MSB
handles customer
disputes and errors
per Reg E, but bank
audits this handling.
All marketing
materials and fee
schedules are
reviewed by bank
(and must meet
network & regulatory
standards). The bank
conducts regular
compliance audits of
the program, and the
network (Visa/MC)
may also require
registration of the
MSB as a service
provider. Bank often
requires a reserve
fund and can dictate
termination of the
program or certain
customers if risk
thresholds are hit.
Essentially, MSB runs
17
87
17 18
11
58
Model Description &
Examples
Bank’s Role &
Exposure MSB’s Role Compliance
Allocation
the program day-to-
day; bank and
network set the rules
that MSB must follow
.2
59
Layered Program
(Master/Sub
Program Managers)
<br><small><em>(Our
model)</em></small>
A hybrid of
the above:
The parent
MSB (us) acts
as the primary
Program
Manager with
the bank, and
our series
clients
operate as
sub-program
partners
under our
umbrella. We
provide BaaS-
like sub-
accounts and
also manage
any card
programs for
them.
<br>(e.g. Bank
issues cards
under Parent
MSB’s
program.
Series A (client)
has its
branding on a
subset of cards
as a “program
affiliate,” while
Parent MSB
ensures all
compliance
and oversight.)
Bank’s
relationship is
formally with
the Parent MSB
(principal
program
manager). Bank
holds all funds
(possibly in
segregated
sub-accounts
per series) and
issues any
cards. The bank
has no direct
contract with
the series
clients or their
end-users – it
relies on the
Parent MSB to
extend its
compliance
reach. This
adds a layer of
indirection:
bank -> parent
MSB -> sub-
client -> end-
user. Bank’s risk
is higher if sub-
clients are not
transparent, so
bank will insist
on knowing
each sub-
program and
approving
them.
Parent MSB
serves as
“master
program
manager,”
interfacing
with the bank
and networks.
We sign the
sponsor bank
agreement
and then bring
on sub-MSB
clients under
our program
(with bank
consent). We
handle all
compliance
functions for
end-users and
sub-MSBs,
effectively
acting as the
bank’s agent
and also as
principal for
our agents.
Sub-MSB
clients handle
their customer
interactions (if
they have end-
users) but
must abide by
our
compliance
program. We
funnel all info
and reports to
the bank.
Multi-tier
compliance: Bank
holds parent MSB
accountable for
entire program.
Parent MSB in turn
imposes compliance
requirements on sub-
MSB clients (via
agent contracts) and
oversees them.
Parent MSB performs
KYC/AML on sub-
MSBs and often on
their end-users as
well (or validates the
sub’s KYC). For end-
consumers, the
structure may result
in two layers of KYC
(sub does initial,
parent MSB verifies).
SARs: If suspicious
activity is at end-user
level, sub-MSB flags
to parent, parent
investigates and files
SAR (and notifies
bank) . Bank may
file SARs if it notices
suspicious patterns
in aggregate flows
. The bank
requires a clear
compliance plan
showing how parent
MSB manages sub-
agents (training,
monitoring,
independent reviews)
. Essentially, the
parent MSB’s
compliance program
must effectively
function as an
extension of the
bank’s program, and
11
13
58
60
Model Description &
Examples
Bank’s Role &
Exposure MSB’s Role Compliance
Allocation
the sub-MSBs
operate under the
parent’s AML policies.
This model demands
strong
communication:
parent MSB must
regularly report on
sub-program activity
to the bank. Any
weakness in the
“compliance
waterfall” (bank ->
parent -> sub) could
be viewed as a gap
by regulators. When
done properly, it can
meet regulatory
expectations (FinCEN
explicitly allows
agents of agents, as
long as the principal
covers them ) but
it is scrutinized. (See
Sections 2 and 3 for
detailed discussion of
this layered
compliance.)
Table 1: Comparison of Sponsor Bank Partnership Models and their Compliance Structures.
In practice, elements of these models can be combined. For instance, our approach will blend BaaS and
Program Manager roles: we anticipate maintaining FBO sub-accounts for our clients (series) at the sponsor
bank (like a BaaS model), while also acting as Program Manager for any card issuance or payment
instruments. The sponsor bank agreement likely will encompass both deposit-related services and issuing
services. Thus, we must be prepared to comply with both sets of expectations – essentially the most
stringent obligations from each model will apply. For example, we will need to adhere to Reg E and CFPB
rules for the prepaid aspects (Program Manager duty) and also allow the bank to audit individual customer
KYC and transactions (BaaS duty).
Our layered master/sub structure (last column of Table 1) is the most complex. It offers flexibility (multiple
sub-programs under one bank relationship) and scalability (we can add clients without negotiating separate
bank deals for each), but it requires very robust compliance management to satisfy the sponsor bank and
regulators. The rest of this section and Section 2 will delve into how sponsor banks approach such layered
arrangements and the safeguards we implement to mitigate the inherent risks.
10
61
1.2 How Sponsor Banks Evaluate and Onboard MSB Clients (Especially White-Label &
Layered Models)
Due Diligence Focus: A sponsor bank performing due diligence on an MSB like ours will closely examine
three aspects: (a) the MSB’s regulatory status and basic eligibility, (b) the MSB’s business model and risk
profile (including any layering of agents), and (c) the MSB’s compliance program robustness. We should be
ready to provide extensive documentation for each.
Regulatory Good Standing: The bank will verify that we are properly registered with FinCEN and
licensed in all required states . This is a baseline requirement – operating without proper
licensing or registration is a non-starter (and banks have been instructed by regulators to confirm
this for MSB accounts ). We should expect to provide copies of our FinCEN MSB registration
acknowledgment letter/printout and all relevant state licenses. If any state licenses are pending, we’ll
need to explain where and why (and the bank may limit activities in those states until approved). For
our series structure, this can raise questions: state licenses are typically held by the parent LLC
(master). We will clarify to the bank that all money transmission activity by series is conducted under
the parent’s license authority (as authorized delegates where applicable). We should also proactively
share our policy on regulatory compliance – e.g. a memo summarizing how our series setup
complies with FinCEN’s agent-of-an-MSB rule and state law delegate provisions. By addressing
this head-on, we show the bank we’re not trying to slip something past them; rather we have legally
vetted our structure.
Understanding the Business Model: Sponsor banks perform a risk assessment of each MSB client.
They will ask for a detailed description of our business, including: the types of services we offer (e.g.
“we facilitate cross-border B2B payments and issue prepaid cards for corporate programs” etc.), the
customer base we serve (institutional clients, foreign businesses, etc.), the geographies involved
(both where our clients are and where funds flow to/from), and our expected transaction volume
and sizes . Since we have a unique series LLC structure, we must clearly illustrate it to the
bank. A good approach is to provide an organizational diagram: showing the parent LLC, each
series, and their roles (perhaps annotating that each series acts as an agent of the parent for MSB
activities). We should list key owners of each series if different (though in our case, presumably we
(the parent) control them or our clients have ownership stakes – either way, transparency is key). The
bank will specifically be keen to know if the MSB is a “principal MSB with agents or sub-MSBs” – in
fact, FinCEN’s guidance to banks explicitly includes determining “whether the MSB is a principal (with a
fleet of agents) or an agent of another MSB” as part of risk evaluation . In our application or initial
discussions, we won’t shy away from this: we will tell the bank, “Yes, we operate as a principal MSB
and have agents (the series sub-entities) under our program.” That triggers the bank’s need to do
extra due diligence (which we anticipate). According to regulatory guidance, when an MSB has
agents, banks should consider obtaining the list of agents and information about their locations and
activities . We should prepare that agent list (series list) in advance to hand over. This list should
include for each series: legal name, jurisdiction, address, ownership info, and what services they will
offer. If any series (agent) is itself a foreign company or owned by foreign principals, expect the bank
to scrutinize that further (as foreign MSBs introduce another layer of risk – FinCEN issued an
advisory in 2012 reminding banks to ensure foreign MSB agents of U.S. MSBs are compliant with U.S.
rules ). In short, full disclosure of our sub-clients is required: who they are, what they do,
and how they tie into our structure. The bank will also ask if we (the MSB) are new or established,
and perhaps for references or history. Given that our model is novel, emphasizing any previous
•
32
32 61
10
•
89 90
3
58
53 31
62
successful operations or the experience of our management team in payments compliance would
help mitigate the “newcomer risk.”
Compliance Program & Controls: This is arguably the most important aspect. A sponsor bank will
almost certainly require a copy of our AML/BSA policy and may even want to meet with our
Compliance Officer and team to gauge their expertise. They will examine whether our program
meets at least the minimum regulatory requirements and is tailored to our risk (and by extension,
theirs). Key elements we should highlight:
The written AML policies and procedures (demonstrating that we have procedures for customer
due diligence, monitoring, SAR filing, etc., including coverage of agents). We should include
procedures on agent oversight – e.g. “the parent MSB conducts annual audits of each series agent” –
because banks are advised to verify the MSB has “written agent management and termination
practices” .
Our Know-Your-Customer (KYC) and Customer Identification Program (CIP) details. The bank will
likely compare these to their own CIP standards. If our CIP is weaker, they’ll ask us to strengthen it.
It’s best if we align our KYC processes with banking standards (collecting beneficial owner info for
entity clients per FinCEN CDD rule, verifying IDs using reputable methods, screening against OFAC,
etc.). We can reassure the bank by explaining our KYC vendor setup (for example, if we use an
identity verification API that the bank knows and trusts, that’s a plus).
Transaction monitoring and sanctions screening: The bank will want to know how we plan to
monitor transactions (do we have automated software? what scenarios or rules are in place?) and
how we screen for OFAC sanctions and other watchlists. We should be prepared with specifics, e.g.,
“We use XYZ AML software which is calibrated for our business model, including rules to detect
structuring, unusual patterns by volume and geography, etc. We screen all customers and
transactions against OFAC’s SDN list and other relevant lists at onboarding and continuously.” This
shows we won’t rely on the bank to catch bad actors – we have our own system (which the bank may
later test or audit).
Staffing and expertise: The bank could ask about the size and credentials of our compliance team.
They need to be confident that we have enough knowledgeable staff to handle the volume and
complexity of our operations. If we have, say, one compliance officer and no analysts and we plan to
process millions of dollars a month, that’s a red flag. We should ideally have experienced personnel
(with ACAMS certifications or former bank compliance backgrounds) and we should not understate
the headcount devoted to compliance. In fact, emphasizing a “culture of compliance” will resonate
well. Banks have been cautioned that they should only bank MSBs that “comply with the law and
maintain effective AML programs” – so we want to clearly fall in that category. We might even
provide results of an independent audit of our AML program (if we’ve had one) or plans for an
upcoming independent review, as that demonstrates commitment to continuous improvement.
Agent oversight plan: Because we have sub-MSBs, the bank will zero in on how we manage them.
Expect questions like: “How do you vet your sub-clients before allowing them under your program? What
due diligence do you do on them?”; “Do you train them on AML compliance? Provide them with your
policies?”; “How do you ensure they follow your procedures (e.g., do you perform audits or receive
reports)?; “Can sub-agents further subcontract or are they the final layer?” (Our answer to the last should
be: they are the final layer – we do not allow further nesting). We should provide our Agent Due
Diligence checklist (which should include things like verifying the owners of the sub-MSB, checking
their backgrounds, ensuring they’re not on any bad lists, reviewing their business model for
licensing needs). Also, mention that we require each agent to certify or contractually agree to
•
•
58
•
•
•
84
•
63
compliance standards (the bank may even want to see a copy of our agent agreement). FinCEN
guidance to banks suggests they obtain “list of agents… and written procedures for the operation of the
MSB; written agent management and termination practices…” – essentially, the bank may ask us to
produce our internal procedures on agent oversight. We should have those ready.
SAR history or expectations: If we’ve been operating, they might ask if we have filed SARs before
(and on what general issues). If we are new, they might ask how we will handle SARs, who will decide
to file, etc. Our answer should stress that we have a clear escalation procedure and that we fully
intend to meet all SAR obligations diligently. The bank might also indicate that they prefer we notify
them of any SARs related to the program (which we will).
Other compliance areas: Depending on services, they might cover consumer protection (if we
handle consumer funds, are we addressing Reg E?), data security (do we follow cybersecurity best
practices, since breaches could impact the bank?), and any secondary regulatory issues (like OFAC
program, fraud prevention, etc.). We should be ready to show policies or describe controls in these
areas too.
In onboarding MSB customers, banks follow a risk-based approach as outlined in the FFIEC BSA/AML Exam
Manual and FinCEN guidance. They will apply Enhanced Due Diligence (EDD) if risk factors are present –
having agents, foreign ties, high transaction volumes are all risk factors that trigger EDD . Given our
profile (layered structure, international clients), we should expect thorough EDD. This likely includes the
bank requesting: - Background checks on our company and principals (they’ll run names through databases
for any negative news, enforcement actions, etc.). - Reviewing our financial statements or proof of funding
(to ensure we have the net worth to operate and perhaps to gauge whether we’ll meet any reserve
requirements). - Possibly an on-site visit or video meeting to discuss our operations in detail (some banks
do an on-site as part of onboarding high-risk clients to see the operations and meet management). - If any
of our sub-clients are themselves significant businesses, the bank might even ask to meet them or at least
approve each one before inclusion. Banks that are “tolerant of layered structures” will still want to know
exactly who the layers are. For instance, if Series A is a fintech out of, say, Germany, the bank might request
information on that company’s management and compliance program too. In essence, the bank might
partially underwrite our big agents as if they were direct customers. We should be prepared to facilitate that
(which is fine, since we want strong partners only anyway).
Risk Rating and Acceptance: After gathering info, the sponsor bank will make a risk rating of us (likely
“High Risk” due to being an MSB). But high risk doesn’t mean unacceptable – it means they will impose
conditions and monitoring. If everything in our profile points to a well-managed operation with known
beneficial owners, strong compliance, serving legitimate needs, the bank can justify taking us on despite
inherent risk.
One critical decision factor for banks is often the specific services and transaction types we plan. For
example, purely facilitating B2B payments for known companies is viewed more favorably than mixing in
any consumer remittances or walk-in money transmission (which we are not doing). The fact that our model
has “minimal direct consumer exposure” aligns with a conservative risk appetite – banks know that
consumer-facing MSBs bring additional regulatory scrutiny (CFPB, UDAP concerns) whereas B2B is a bit
more straightforward in terms of fewer fraud claims and consumer complaints. We should highlight that as
a positive: our primary clients are other regulated or established businesses, not the general public.
Additionally, we can point out we do not handle cash in physical locations (assuming we don’t) – that
removes a huge vector of risk (no risk of structuring via branches, no risk of armored car cash loads, etc.).
Our flows will be traceable electronic transfers from bank accounts or corporate sources, which is what
banks prefer .
58
•
•
61 6
78
64
Onboarding Outcome: If the sponsor bank is satisfied, they will proceed to enter a formal agreement with
us (discussed in 1.5). If they have reservations, they might ask for mitigations – e.g., “We will bank you, but
initially we will cap daily transaction volume at $X until we see a few months of history,” or “We require you
to obtain state licenses in Y and Z (even if you think agent-of-payee applies) to be comfortable,” or “We’ll
need you to enhance policy ABC and hire one more compliance analyst.” We should be ready for such
conditions and treat them as part of doing business.
Finally, it’s worth noting that sponsor banks are themselves under regulatory scrutiny for how they vet
fintech/MSB partners. In 2023, the OCC and FDIC issued guidance and took enforcement actions signaling
banks must “increase their due diligence and oversight of fintech partnerships” . Our thorough
preparation and transparency essentially helps the bank satisfy its examiners. A bank examiner will ask the
bank, “Did you verify this MSB is licensed? Did you review their AML program? Are you monitoring their
agents?” The bank should be able to answer “Yes, here’s the documentation from [Our Company].” If we
equip the bank to answer those questions affirmatively, we improve our chances of approval and a smooth
relationship.
1.3 Compliance Responsibility Allocation in Different Partnership Models
(This section overlaps with Section 2, but here we frame it in the context of initial structuring and contracting with
the bank.)
The division of compliance tasks among the sponsor bank, our MSB (parent), and our sub-MSB agents was
broadly outlined in Table 1. We detail it here because understanding who does what is fundamental to
structuring the partnership correctly and avoiding gaps. Clear allocation will also be codified in the sponsor
bank agreement in Section 1.5.
In a Direct Account setup: The compliance burden on the MSB is almost total with respect to end
customers. The bank’s obligations are mainly to perform due diligence on the MSB and monitor the MSB’s
account for gross red flags. The bank will require information on the MSB’s AML program and maybe
periodic certifications that the MSB is fulfilling its obligations (some banks even ask MSB account holders to
certify annually that they have conducted required independent AML reviews, etc.). But the bank won’t see
individual transactions or customer identities. Thus, if a suspicious pattern occurs, the bank might only see,
for example, a large wire out to a high-risk country with no context. The bank would then file a SAR possibly
(“Suspect MSB customer doing X”) , and potentially question the MSB. Meanwhile, the MSB should have
filed a SAR on that underlying activity itself. FinCEN has clarified that both banks and MSBs might need to
file on the same activity from their own perspectives . This duplication is accepted. So in this model, we
as MSB must be filing SARs for our customers, and the bank might simultaneously file SARs about our
aggregate activity if warranted – no direct coordination is mandated, though under Section 314(b) we could
share information . The bank’s CTR obligations apply only if our account triggers CTR rules (e.g., if we
withdrew cash >$10k from our account, the bank files a CTR on our company; if one of our agents deposits
cash into our account at the bank, the bank might file a CTR on us as the account holder, while we would file
CTRs on the individual cash sender as required). In sum, in a direct account model, the bank is hands-off
regarding our customers (they are legally not the bank’s customers), which is why many banks feel
uncomfortable – they must trust our controls, and historically that trust has been eroded by some MSB
failures. That’s one reason the industry shifted to deeper partnerships (BaaS, etc.), to give banks more
involvement.
50 91
13
11
54
65
In a BaaS / FBO partnership: Here, because the bank’s legal responsibilities extend to end-users, the
compliance functions are shared. Typically, the contract will specify that we (the fintech MSB) will perform
certain BSA/AML functions on behalf of the bank (as the bank’s agent), subject to the bank’s approval
and ongoing oversight. For example, it may say the fintech will conduct CIP in accordance with the bank’s
Customer Identification Program policy (and list the ID types, verification methods, etc., to be used), and
that the fintech will provide evidence of CIP to the bank upon request . The bank might reserve the right
to reject or require additional info for any customer the fintech wants to onboard. Some BaaS banks
insist on approving each new client that’s onboarded (usually in an automated way via the API – e.g., the API
pings the bank’s system for an “OK” on the KYC result). Others delegate onboarding entirely but audit later.
The sponsor bank’s own AML program will include specific risk controls for the fintech program. For
instance, the bank might integrate our end-users into its transaction monitoring software as sub-
accounts. Or the bank might require that our monitoring rules meet certain parameters and that we send
them all SAR “alerts” for joint review. The OCC has made it clear in consent orders that banks must ensure
their fintech partners adhere to comparable compliance standards as the bank itself . In practice, that
means although we do the work, the bank dictates the standards. We should anticipate a close
collaboration on refining our AML program to satisfy both parties.
A key component is SAR decisioning and filing in BaaS setups: Many sponsor banks prefer to handle the
actual SAR filing, because from a regulatory standpoint the bank is the one with the direct visibility and it
simplifies regulator expectations (the bank’s BSA officer signs off on SARs). But the fintech must feed the
bank the necessary information. Often, the contract or operating procedures state that the fintech will
report potentially suspicious activity to the bank’s compliance team within X days, and then the bank’s
BSA team will determine whether to file a SAR (and the fintech agrees to assist by providing any follow-up
data). Some banks even embed a compliance analyst or give the fintech access to the bank’s case
management system to facilitate this. Alternatively, if regulators permit, both the bank and fintech might
file SARs – but that’s redundant and not common in a single integrated program because it’s easier to
coordinate one filing. For CTRs: since in BaaS the bank holds the funds in its accounts, the bank is
responsible for CTR filings on currency transactions across those accounts. We as fintech would thus need
to immediately inform the bank of any cash deposits or withdrawals by users above $10k (if our program
even allows cash – many don’t, except via ATM withdrawal tracking which the bank’s systems catch). The
fintech could also independently decide to file CTRs if it’s legally an MSB with that obligation; however, if all
cash interactions occur at the bank account level, the bank’s CTR covers it and FinCEN doesn’t need two
CTRs. In our likely scenario, we won’t be handling physical cash with end-users at all, so CTRs might be moot
beyond perhaps large ATM withdrawals on cards (which the bank would aggregate and report).
In Program Manager (card) setups: Responsibilities are delineated by both regulation and network rules.
For example, under Regulation E and the CFPB Prepaid Rule, certain functions must be provided to
consumers, and the bank as issuer is ultimately responsible to regulators for ensuring they are. However,
the bank will push the day-to-day execution to us via contract. So, the contract will say the Program
Manager (us) will provide Reg E disclosures to each cardholder, will handle error resolution claims in
compliance with Reg E, and will maintain records of such investigations. It will also likely require us to
submit periodic Reg E compliance reports to the bank (like number of disputes, timing of resolutions, etc.).
Similarly, for network rules: the bank might require that we adhere to Visa Core Rules regarding
chargeback timeframes, and our processor agreement will need to reflect those. The bank often relies on
the program manager’s processor for automated rule compliance but holds us accountable for any failures.
So, if we missed a chargeback deadline and the bank had to eat a loss, we cover it. The bank typically also
monitors fraud and chargeback rates. If thresholds set by Visa/MC are exceeded, networks fine the bank
2
9
66
– the bank’s contract with us will say we must indemnify the bank for such fines and possibly that we must
implement corrective action or risk program termination.
Multi-layer (Our layered model): Here the compliance responsibilities cascade. The Sponsor Bank will
hold us (the parent MSB) responsible for performing all necessary customer due diligence and monitoring
for both our direct customers (the series clients) and the series’ end customers. The bank is not going to
manage or communicate with our series clients – that’s our job as the master MSB. So our contract with the
bank will treat our whole operation (parent + agents) as one program. We, in turn, have agreements with
each series requiring them to, for instance, collect whatever KYC we mandate on their users and to refrain
from any activity that would put us or the bank out of compliance (e.g. they can’t start serving retail
customers if our agreement with bank was only for B2B, etc.). Our internal compliance program and team
effectively serve as the compliance department for all sub-MSBs. For example, if Series B onboarded a
corporate customer, Series B might gather documents, but we likely require that our compliance team
approve that customer as well (to ensure standards). That mirrors how the bank requires us to approve our
sub-agents’ clients, creating a chain of approval. The bank will want evidence that this structure is working –
for instance, the bank might want to see that we rejected some prospective sub-client’s user because of
high risk, demonstrating we enforce standards.
A “Compliance Waterfall” Risk Matrix: To illustrate, below is a risk-oriented matrix of different compliance
delegation setups (from bank-centric to MSB-centric), showing regulatory clarity and risk. This aligns with
our earlier discussion:
Compliance
Delegation
Model
Description Regulatory Clarity & Risk Level
Bank-centric
(Bank does end-
user KYC & AML)
<br>Bank as full
BSA operator
Bank treats all end
customers as its own
and performs CIP,
screening, and
monitoring directly.
Fintech’s role is
minimal (marketing/
tech). <br>Used in
limited cases where
fintech simply refers
customers to bank’s
accounts.
Highest regulatory clarity: Bank controls compliance,
regulators are comfortable since it’s handled like a
normal bank customer process. Risk to bank: Low from
compliance execution standpoint (they do it in-house),
but this model is least scalable (bank bears all workload)
and rare in MSB partnerships. Fintech/MSB has little
control, and user onboarding may be slower.
67
Compliance
Delegation
Model
Description Regulatory Clarity & Risk Level
Shared
Compliance
(Hybrid)
<br>Fintech does
onboarding, Bank
oversees
Fintech/MSB
performs most
customer due
diligence and
monitoring using
bank-approved
methods; bank
retains oversight and
final say.
<br>Standard in BaaS
programs: fintech is
the “agent” for
compliance tasks,
bank verifies and
audits.
Regulatory stance: Acceptable if well-documented.
Regulators have made clear the bank is still liable for any
shortcomings , so they expect rigorous oversight.
Risk: Medium – potential gaps if fintech fails to execute
tasks properly, but bank’s ongoing monitoring can catch
issues. Clarity is good if contract specifies roles (e.g.
fintech will CIP users and bank will file SARs, etc.). This is
the prevailing model in many bank-fintech relationships
– workable with strong cooperation.
MSB-centric
(Bank monitors
MSB only)
<br>Layered
compliance with
MSB as primary
MSB (principal)
handles all end-
customer compliance
(especially when end-
users are legally
MSB’s customers, not
bank’s). Bank’s focus
is on MSB’s
aggregate activity
and the MSB’s own
program compliance.
<br>Typical of direct
account relationships
or agent-of-bank
models where bank
doesn’t see individual
users.
Regulatory clarity: Lower, because regulators expect
banks to know their customers – if bank only knows the
MSB, not the sub-users, the bank must rely on the MSB’s
program. FinCEN allows MSB agents to rely on principal’s
AML program , but bank examiners will treat this as
high risk. Risk: High – if MSB’s program fails, illicit activity
could go undetected by bank. The bank will mitigate by
demanding a lot of info from MSB (agent lists, AML
audits) . There’s also risk of information lag (bank
finds out problems well after the fact). Regulators might
scrutinize the bank heavily to ensure it isn’t too “hands-
off.” This model can work if the MSB is very competent
and transparent, but it requires great trust.
9
14
58
68
Compliance
Delegation
Model
Description Regulatory Clarity & Risk Level
Multi-layer MSB
(MSB + sub-
agents)
<br>Compliance
waterfall (Bank →
MSB → Agents)
Bank oversees
principal MSB’s
compliance; principal
MSB oversees its
agents’ compliance;
agents interact with
end-users. Multiple
layers of oversight
and information flow.
<br>Our model: e.g.,
Bank relies on Parent
MSB’s program, which
in turn ensures Series
agents follow
procedures.
Regulatory clarity: Challenging – not explicitly
addressed in regulations beyond general agent rules. It
can be acceptable if each layer’s responsibilities are well-
defined and documented (who verifies end-user identity?
who monitors transactions? who files SARs?). FinCEN’s
agent-of-agent policy (no separate registration needed)
provides a legal basis, but examiners will likely
consider this an area needing extra verification. Risk:
Highest operational risk – miscommunication or
misalignment at any layer can create a hole in the
controls. The bank must ensure the MSB is effectively
acting as an extension of the bank’s compliance, and the
MSB must ensure each agent is an extension of its
compliance. If done right, risk can be managed
(mimicking a hierarchy like large money transmitters
have). But any weakness in training or data-sharing
could be exploited by bad actors at the edges. This
structure demands robust agreements, technology
integration (for sharing KYC/transaction data upward),
and frequent audits. Banks that allow this will impose
strict conditions (e.g., pre-approval of each agent,
additional capital or bonding, etc.). If successfully
implemented, it allows scalability (many sub-clients) but
regulators will expect the bank to have visibility
through the chain, likely via reports or ability to audit
agents directly through the MSB.
Risk Matrix: Compliance Delegation Approaches vs. Regulatory Clarity.
Our approach falls in the bottom row of this matrix. The risk can be mitigated by applying many elements of
the shared compliance model within our operation – i.e., we push as much oversight as possible upward to
us, making the bank-MSB interaction similar to a direct BaaS relationship. In effect, we want the bank to feel
like they’re dealing with one well-run program (ours), not many disparate unknown agents. We accomplish
that by centralizing compliance and giving the bank full insight into our consolidated activities.
1.4 Sponsor Banks Actively Supporting Layered MSB Programs
While many banks historically were wary of MSBs (due to high-profile AML failures in that sector), a subset
of banks has developed expertise in banking fintechs and MSBs. These “sponsor banks” are typically
medium-sized banks for whom Banking-as-a-Service or program sponsorship is a significant line of
10
69
business. They have dedicated compliance teams for managing these partnerships. Below are some known
players and their characteristics, especially regarding tolerance for layered structures:
Evolve Bank & Trust (TN) – Known for a wide range of fintech partnerships (covering payments,
cards, and crypto until recently). Evolve has multiple programs and experience acting as both a BaaS
platform and card issuer. It likely would be open to a model like ours, but it will demand strong
oversight of any sub-programs. Evolve’s public statements emphasize a “strong compliance culture”
and they have invested in fintech integration. They are Fed-regulated (community bank supervised
by the Fed and state) and would carefully vet foreign agents but have worked with international
fintechs before.
Cross River Bank (NJ) – A very prominent fintech sponsor bank (served companies like TransferWise,
Coinbase, Stripe in various capacities). Cross River is experienced in high-volume programs.
However, Cross River came under a consent order in 2023 from the FDIC focused on fair lending
issues with its lending fintech partners , and that led them to tighten compliance across the
board. They still do payments sponsorship, but they may be more selective now. Cross River could
handle layered structures given its sophisticated infrastructure, but we’d need to demonstrate
impeccable controls to satisfy them (and by extension the FDIC). They have in the past worked with
international payment companies (e.g., they were an intermediary for Visa’s fintech programs).
Metropolitan Commercial Bank (NY) – MCB was known for its fintech-friendly stance (providing
debit card issuing and crypto-related accounts), serving programs like prepaid card providers,
international remittance firms, etc. In 2023, MCB announced it was exiting crypto-related clients
amid regulatory pressure, but it still supports general fintech and payments. MCB has had clients
with nested structures (for example, global remittance firms with many agents using their accounts).
They are familiar with agent networks (they banked large MSBs and even crypto exchanges that had
sub-users). New York regulators (NYDFS) oversee them, which means stringent AML expectations;
however, NYDFS also explicitly permits licensees to use agents. MCB would demand thorough
visibility into any foreign agent or high-risk corridor. They were comfortable with cross-border flows
(one of few U.S. banks to serve that market) , but their risk appetite might have narrowed
recently. Still, they remain an option for non-retail, compliance-forward programs.
Smaller Niche Banks (Community Banks/Regional Banks): For instance, Sunrise Banks (MN) has
BaaS programs (like with fintechs providing accounts and cards). Celtic Bank (UT) focuses more on
lending but has some payment sponsor aspects (particularly in SMB lending platforms). Coastal
Community Bank (WA) is the banking partner behind fintech platforms like Raisin and Aspiration –
they do a lot of BaaS, working with broker-dealer fintech models where one entity may have sub-
accounts for multiple clients, analogous to our case. They are likely to understand series LLC setups
since Washington State has many money transmitter licensees and authorized delegate frameworks.
Blue Ridge Bank (VA) was active in fintech (one of first to bank crypto ATMs, etc.), but the OCC hit
them with an order in 2022 (specifically citing unsafe practices in fintech partnerships) , so they
paused new partnerships. By 2025, if they resolve that, they might re-enter but under heavy OCC
scrutiny.
Puerto Rico International Financial Entities (IFEs): These include FV Bank, San Juan Mercantile
Bank, etc. IFEs in Puerto Rico are allowed to transact with non-Puerto Rico residents in many
banking activities and have become hubs for fintech-friendly banking under OCIF regulation. For
example, FV Bank actively markets global fintech accounts and custody, bridging crypto and
traditional finance . It holds a U.S. bank routing number and can provide USD accounts. IFEs
often are more open to international and layered structures (they understand multi-jurisdictional
setups since they primarily serve non-U.S. clients). For our model, an IFE might be comfortable
•
•
47
•
34
•
28
•
34
70
holding an account for our parent MSB and supporting sub-accounts for foreign clients, given
Puerto Rico’s status and the IFE’s tax incentives to attract such business . The trade-off is that
IFEs, while regulated (under Puerto Rico law), are not FDIC-insured and not directly under U.S.
federal banking agencies. Some fintechs and MSBs use them to avoid mainland banks’ stricter
stance, but there is a perception risk: counterparties or regulators might view IFE accounts as
slightly less stringent (though they do comply with BSA/AML as required). That said, IFEs like FV
Bank have positioned themselves as fully compliance-driven (FV Bank boasts U.S. MSB
registrations, crypto licenses, etc., on top of IFE license). For layered structures, an IFE might actually
be more tolerant as they build their business around being flexible. We should still expect rigorous
due diligence – IFEs have to prove to OCIF they aren’t skirting rules after some past scandals in PR
banking.
Faisal Khan’s List and Other Aggregators: Industry consultants maintain lists of “MSB-friendly
banks” . Many on those lists are lesser-known community banks or credit unions that have
decided to serve niche markets (often for steady fee income). Examples might include banks in
certain states that historically bank a lot of check cashers or money transmitters (e.g., some banks in
Florida or California that specialize in LatAm remittances). These institutions might be open to our
model but we would need to vet their capacity – a small bank with one BSA officer might not be able
to handle the complexity of a series LLC with global clients. We prefer a bank with dedicated fintech/
MSB compliance staff.
Visa/Mastercard Sponsor Banks: There are banks whose main business is sponsoring card
programs (e.g., The Bancorp Bank (DE), Pathward formerly MetaBank (SD), Sutton Bank (OH)).
They handle dozens of prepaid and debit programs and are very familiar with program managers. If
our services involve a lot of prepaid issuance, one of these might be a component of our strategy
(maybe we use one bank for card issuing and another for holding other funds). These banks are
comfortable managing multiple programs and sub-programs. For instance, Pathward as of
Pathward’s own statements sponsors “travel cards, gift cards, reloadable programs with various
program managers” . They will however require that we (the primary program manager) strictly
control any subprograms – e.g., Pathward sends out an annual unclaimed property due diligence
letter on all its card programs , illustrating their thoroughness. These banks wouldn’t directly
know our series, but through us, they would – by contract we’d likely have to disclose any “material
subcontractor or agent” involved in program management. They might insist on reviewing the sub-
brand’s marketing materials too, so we should be prepared to intermediate that.
In terms of tolerance of layered structures specifically: Many sponsor banks have historically dealt with
authorized delegate setups in money transmission (e.g., a bank providing clearing accounts for a licensed
transmitter with 100 agents – the bank knows the master licensee and perhaps a list of agents). The
additional wrinkle in our case is the series LLC aspect – which is uncommon but not fundamentally different
from an MSB listing multiple trade names or divisions. We should be ready to educate the bank’s
compliance/legal team on how series LLCs work (liability segregation, how each series is treated under
FinCEN rules – as agents – and state rules). In fact, Montana’s regulator or the CSBS may have commentary
on series LLCs in MSB licensing (not widely published, but we can reference that Montana allows it under
their statutes since we formed that way). The key from a bank’s view is they want to ensure no hidden
owners or unvetted parties controlling parts of the business. We will clarify that all series are under
common control (if true) and that ultimate owners (beneficial owners) of the entire enterprise are already
disclosed to the bank. If any series is co-owned by a client (say our client has equity in their series), we must
disclose that beneficial ownership to the bank as well, so they can KYC those individuals/entities. Expect the
bank to run checks on those client owners similarly to how they check our owners. This isn’t a deal breaker –
it’s manageable as long as those owners pass OFAC and negative news screening.
92 93
•
39 94
•
21
73
71
Contractual and Monitoring Adjustments: Sponsor banks that accept layered programs often include
special covenants in the contract: requiring pre-approval of each new sub-agent (series client) – effectively
giving the bank a veto on adding a new client to our platform; requiring enhanced reporting – e.g., we
might have to provide a quarterly report of each series’ volume and any compliance issues; and possibly
requiring separate sub-reserves or sub-accounts so the bank can isolate issues. For example, a bank might
say “we’ll hold a reserve equal to 1% of outstanding balances per series agent” to mitigate any single
agent’s risk. Termination clauses might allow the bank to terminate a specific sub-agent from the program
(by instructing us to sever that relationship) without terminating the whole program, if that sub-agent is
problematic. We should welcome that flexibility because it’s better than losing the entire banking
relationship due to one bad apple. Operationally, we need to be capable of quickly removing an agent and
maybe freezing its funds at the bank’s or our compliance request – so our contracts with agents should
have a clause “if mandated by our bank or regulators, we may suspend or terminate your participation
immediately.”
Which Banks to Approach: Based on the above, a prudent approach is to initially approach one of the
established fintech sponsor banks (like a Coastal or Evolve for account side, and perhaps Bancorp or
Pathward for card side) with our proposal, incorporating all our prepared compliance materials. We might
simultaneously engage with a Puerto Rico IFE (like FV Bank) as a backup or parallel solution for international
components (they might handle foreign exchange or cross-border flows more easily). Having multiple
banking partners is wise in general (Moody’s noted that fintechs relying on single banks were at risk after
some bank failures in 2023). The user prompt even hints “should look also outside US like Puerto Rico and
other countries,” which we have. Perhaps even a UK or EU EMI (Electronic Money Institution) for overseas
piece – but for U.S. rails, a U.S. bank or IFE is needed.
In summary, several banks are active in MSB sponsorship, and while they are selective, they do accept
well-controlled layered structures. They mitigate the risk by deep due diligence and continuous oversight
(which we are prepared for). The ones most likely to engage are those already serving similar layered or
agent-heavy clients. Our job is to convince them that our compliance program is at the level of a top-tier
MSB or fintech – essentially, that partnering with us will not create surprises or regulatory headaches. If we
do that, we become exactly the kind of client these sponsor banks seek: an innovative business generating
deposits and fee income, but with a conservative risk profile and cooperative posture that regulators
can approve of .
1.5 Typical Contractual Terms in Sponsor Bank Agreements with MSB/Fintech Partners
Once a sponsor bank has agreed in principle to onboard us, the relationship will be governed by a detailed
agreement. These contracts (often titled “Master Services Agreement,” “Program Manager Agreement,” or
“Sponsor Bank Agreement”) are quite robust – they allocate responsibilities (as discussed above) and protect
the bank’s interests. Below we outline the typical terms we will encounter and should negotiate, citing any
specific regulatory guidance where relevant:
Scope of Services: The contract will clearly define which services the bank is providing (e.g.,
maintaining FBO accounts, issuing cards under specified BINs, processing ACH transactions, etc.)
and what activities we as the MSB are allowed to do. It will likely restrict us from engaging in certain
high-risk services without additional approval (for instance, the agreement may state that the MSB
program will not support transactions related to online gambling, cannabis, crypto, etc., unless
expressly permitted – a way to contractually enforce risk limits). We must ensure the scope language
7 95
•
72
covers everything we intend to do now and in the near future. If we think we might expand into a
new product, better to negotiate it in upfront or include a mechanism for obtaining approval later.
Regulatory Compliance & Delegation: There will be a comprehensive section assigning compliance
duties. Typically, it will say the MSB must “comply with all applicable laws and regulations”
(broadly) and then enumerate specific expectations: maintain an AML program that meets BSA
requirements; perform CIP for customers per the bank’s CIP policy (attached or referenced); adhere
to OFAC sanctions laws and not involve any sanctioned parties; file all required reports or provide
info to the bank for the bank’s filings, etc. The contract may append a “BSA/AML Responsibility
Matrix” as an exhibit, detailing which party does what (some banks include this for clarity). For
example, it might indicate: MSB will identify and verify customers; MSB will monitor transactions and
provide suspicious activity reports to Bank; Bank will be responsible for SAR filing to FinCEN (with MSB
cooperation); MSB will prepare CTR data for Bank or file CTRs for its transactions as required. We need to
examine this matrix to ensure it aligns with our capabilities and regulatory obligations. If something
is solely assigned to us that we think the bank should do (or vice versa), we negotiate that. However,
generally banks will keep final SAR filing authority (they are typically listed as the “financial
institution” on the SAR). We should clarify the process: e.g., contract might say “MSB shall notify Bank
within 1 business day of any transaction or activity it believes is suspicious. Bank shall have sole discretion
to determine whether a SAR will be filed. MSB shall assist Bank in any SAR investigation and shall not
independently notify any involved party.” That last part is basically a standard SAR confidentiality clause
(can’t tip off the subject). If we as an MSB also are obligated to file SARs (which we are, by regulation),
the contract may either explicitly allow it or could be silent – we likely will still file SARs on our own
paper if needed to cover our FinCEN obligation, but we would coordinate with the bank to avoid
conflicts (FinCEN encourages info sharing under 314(b) safe harbor , which we would utilize
after giving FinCEN notice). The contract might also include an interesting clause: “MSB is responsible
for compliance with FinCEN’s MSB requirements, including registration and agent list maintenance, and
shall provide evidence of such compliance to Bank upon request.” This ensures the bank can get a copy
of our FinCEN registration, our agent list, etc., anytime (which we expect).
Performance Standards & Audits: The bank will set expectations on how we operate and reserve
broad audit rights. For example, the contract may require us to meet certain service levels (like
responding to any bank inquiry about a transaction within X hours, resolving customer complaints
within Y days, etc.). It definitely will give the bank the right to audit our operations and books
related to the program. Typically: “Bank and its regulators may, with reasonable notice, audit MSB’s
relevant records, systems, and controls, and MSB will promptly address any deficiencies identified.” For a
high-risk program, “reasonable notice” might be short (a few days). If a regulator is involved,
sometimes no notice (they can come in). We have to accept that. We should ensure there’s
confidentiality protection (the bank shouldn’t share our proprietary info beyond what’s needed for
compliance or regulatory exam – usually they will include that protection since we may disclose
sensitive info). The contract may also require us to provide periodic compliance certifications or
reports. E.g., many bank-fintech agreements require an annual Certificate of Compliance where
we, through our CEO or Compliance Officer, attest that we are in compliance with all obligations, that
our AML program remains effective, etc., and disclose any material compliance issues or
investigations. Providing false certification would be breach – so it’s in our interest to be truthful and
do the work to ensure we can certify compliance each year.
•
54 55
•
73
Financial Provisions & Reserves: The commercial side will outline fees – possibly setup fees,
monthly fees, per-transaction fees, revenue split on interchange (for cards). For risk management,
almost all such agreements include a reserve or collateral clause: the bank can require us to
maintain a certain balance (or they will hold back a portion of funds) as a reserve against potential
losses (chargebacks, fraud, etc.). For MSB accounts, banks also often include a Set-Off right not just
against the program funds but against any and all accounts we hold with the bank . MoFo’s tip
#1 cautions fintechs that “sponsor banks often require broad setoff rights not just against collateral
accounts but also any account held at the bank” – meaning if we also had, say, an operational
account or an account holding our corporate funds at that bank, they can take from those if the
program account is insufficient to cover a loss. We should be aware of that and perhaps limit how
much unrelated money we keep at the same bank. The contract will outline how the reserve is
calculated and that the bank can increase it at its discretion if program risk increases. It will also say
that if the relationship ends, the bank can hold the reserve for a certain period (often 6–12 months)
to cover any trailing liabilities (like chargebacks that come in late, or a surprise penalty). This is
standard. We might negotiate specifics (like any unused reserve after X months to be returned
promptly).
Termination and Suspension: This section is crucial. Typically, the bank wants very flexible
termination rights, especially in high-risk relationships. Common clauses: Termination for Cause –
immediate if we materially breach laws or contract (e.g. if we operate without a license, fail to
maintain AML program, engage in unethical behavior, etc.); Termination with Notice without Cause –
many sponsor bank contracts allow either party to terminate without cause with a notice period (e.g.
60 or 90 days). We, as the MSB, will want as long a notice as possible in that scenario to find a new
partner and migrate. MoFo’s tip #10 stresses “critically important to have the right to transition the
program to a successor bank,” even outside of termination for cause scenarios . We should
negotiate not just the notice but also a cooperation clause where the bank agrees to continue
certain services during the wind-down/transition period so that customers are not harmed. Banks
often include a carve-out though: if regulators pressure them, they can cut us off quicker (like if
examiners say “drop this client now,” they will). Perhaps we can add language that unless required by
law or regulator, they will provide at least X days notice. Also, because our structure involves sub-
MSBs and their customers, termination affects multiple parties – we might negotiate an obligation
that the bank notifies us of issues and gives us a short cure period for certain breaches before
termination. For example, if a particular sub-agent caused a problem, maybe we can cure by
terminating that agent rather than losing the whole program. Some progressive contracts allow
partial termination (like removing a line of service or a sub-program) instead of full termination if that
addresses the issue. We should seek that flexibility: e.g. “Bank may require MSB to terminate or
suspend any sub-agent or end-user from the program if Bank, in its discretion, deems their activity to pose
undue risk. MSB shall promptly comply. Bank may terminate the entire Agreement only if it determines
that MSB’s program as a whole poses undue risk or MSB fails to comply with a material term,” etc. Of
course, if the bank simply decides to exit the fintech business line (as some did in 2023), the without
cause termination kicks in. That is why maintaining a secondary relationship or being prepared to
pivot is wise (see Section 5 on risk mitigation).
Exclusivity and Use of Other Banks: Some sponsor bank agreements include an exclusivity clause –
meaning the fintech/MSB cannot use another bank for similar services during the term (and
sometimes for a period after termination). Banks like exclusivity to maximize their share of revenue
and deposits from the program. However, exclusivity can hinder our resilience (if we can’t multi-bank,
•
22
22
•
25
•
74
we’re 100% tied to them). MoFo’s tip #8 warns “exclusivity can limit scalability” and advises negotiating
the ability to use multiple banks . Ideally, we want freedom to have other bank partners for
different segments or as a backup. Banks may be amenable to a compromise: maybe we agree not
to run the exact same program through two banks simultaneously (so they get our primary volume),
but we carve out that we can engage another bank for new lines of business or geographies, or if
the sponsor bank cannot support a certain service. Another approach: some banks allow dual
banking if it’s disclosed, because it also reduces their concentration risk. We should try to delete
exclusivity or at least insert a clause that if the bank faces financial or regulatory issues (e.g. if they
fall below well-capitalized or get a serious consent order), we can add another bank partner. Also, we
should clarify that our clients are not bound by exclusivity. If one series client outgrows our solution
and gets its own bank later, that’s outside our contract, but if the bank’s contract is poorly worded, it
might claim that as a breach. We should ensure exclusivity, if any, only applies to us using another
bank for the same program, not our independent clients later.
Financial Covenants: The bank might include requirements like minimum net worth or capital for
us, or that we maintain certain insurance (e.g. errors & omissions insurance, cyber insurance,
perhaps a fidelity bond) and list the bank as an additional insured. For MSBs, banks sometimes want
proof of our bonding (since many states require a surety bond – the bank might want to be notified
if that bond is drawn or not renewed). We should expect a clause that “MSB shall maintain all required
bonds and licenses and promptly notify Bank of any suspension or expiration.” Non-compliance could
allow termination for cause.
Information Sharing and Regulatory Access: The contract will likely authorize the bank to share
information about our program with its examiners or auditors as needed (that’s standard – banks
must be able to reveal our info to regulators under 12 USC 1867(c) for third-party servicers). It may
also require us to notify the bank of any examinations or enforcement actions we face. For
example, if FinCEN or a state regulator examines us or takes action, we must inform the bank
promptly. This is so the bank isn’t blindsided if a regulator comes to them asking about our
program’s issues. Similarly, if we plan to undergo a significant change (ownership change, key
management change, adding a major new product or agent), contract usually obligates us to inform
the bank in advance or obtain consent. For instance, adding a new series client in a regulated sector
might need bank’s okay.
Indemnification and Liability: These sections typically heavily favor the bank. We will be required
to indemnify the bank (and its officers, directors, employees) for any losses, fines, penalties, lawsuits,
or claims arising from our program or our breach of the agreement or laws. For example, if a data
breach on our end causes harm, or if our sub-client commits fraud that leads to customers suing the
bank, we must cover the bank’s costs. This indemnity often explicitly covers regulatory fines and
network fines (so if, say, the CFPB fined the bank due to our program’s UDAP violation, we have to
pay or reimburse). This is a serious financial commitment – we should have insurance or means to
back it up. On the flip side, banks usually cap their liability in the agreement – often to just direct
damages and even then perhaps limited to fees earned by the bank under the contract in the last
year. They often disclaim any liability for our lost profits, reputation damage, etc., even if they
terminate or have service outages. It basically puts nearly all risk on us. We can try to negotiate
symmetrical liability for willful misconduct or gross negligence – e.g., if the bank grossly mishandles
something that costs us money, they should be liable. Sometimes they’ll allow that carve-out. But
many sponsor banks will hold firm on minimal liability because they feel they are offering a service,
26
•
•
•
75
and the MSB should bear its own business risk. We have to assess that risk and maybe mitigate
contractually by securing long notice periods or support in transition (since they won’t pay
consequential damages if they cut us off, we need enough time to avoid those damages).
Sub-agents & subcontractors: Given our layered structure, the contract will likely have provisions
addressing our use of agents. It may require that “MSB shall not appoint any agents or subcontractors
to perform any of its obligations under this Agreement without Bank’s prior written consent”. Effectively,
our series performing parts of the service might be considered subcontractors. We should list the
known ones (our series list) as approved in the contract from the start. Then include a mechanism
for adding future ones (e.g., bank pre-approval not to be unreasonably withheld). The contract will
probably also bind any approved agents to the same confidentiality and compliance standards (via
flow-down clauses). We will in turn have to ensure our contracts with series contain those provisions,
as mentioned earlier. Also, the bank may reserve the right to examine or audit our agents through
us. For example, “MSB will ensure that Bank has the right to audit any Agent that MSB utilizes in providing
the services hereunder to the same extent it may audit MSB, and MSB shall obtain cooperation from such
Agents for any such audit.” This ensures if a regulator said “we want to examine one of the MSB’s
foreign agents,” the bank could facilitate that via us. We should be prepared for that scenario, albeit
it might be rare.
Business Continuity and Exit: There might be provisions about what happens upon termination
(like data transfer). Many fintech-bank agreements require the fintech to “cooperate in transferring
customer accounts or funds” either back to the bank or to a successor as needed. For example, if
terminated, we might have to give the bank all end-customer contact info so the bank can reach out
about claiming their funds (especially if the funds remain at bank in pooled accounts). For a prepaid
program, if it ends, the bank may want to mail out refund checks or escheat remaining balances –
we’d have to support that. We should ensure the contract doesn’t permit the bank to directly solicit
our clients except as needed for regulatory reasons, to protect our business relationships. Usually
they’ll only contact in termination or required notices, not to steal our customers, but it’s good to
clarify.
Financial Reporting: Some agreements might require us to provide financial statements
periodically (so they know we’re solvent and can meet obligations). For MSBs, banks often ask for
copies of our quarterly call reports (if we had to file with FinCEN or NMLS) and annual audited
financials if available. If we’re a startup without audits, they might accept internal statements. This
helps them ensure we maintain required net worth for state licenses and can pay fines or losses. If
our financial health deteriorates, bank might consider that grounds to demand higher reserve or
terminate (fear of us going bankrupt and leaving consumers hanging).
To illustrate how protective these contracts are of the bank: In MoFo’s commentary on sponsor bank
relationships during the banking crisis, they noted banks were including very bank-favorable provisions,
and fintechs needed to negotiate for termination transition rights and to avoid over-restrictive covenants
. For instance, one tip suggested including a clause that if the bank’s own condition worsens (e.g.,
falls below adequately capitalized), we should have rights to move – something we’d want given what
happened with some banks in 2023 . We should try to include a “Termination by Fintech for Bank’s Adverse
Change” clause: if the bank loses its clearing ability or is instructed by regulators to wind down our program,
we can terminate and move immediately (and they still assist in transfer).
•
•
•
96 29
29
76
In conclusion, the contract is a detailed playbook of the partnership – it will formalize the compliance
integration, contain numerous safeguards for the bank, and allocate risk mostly to us. We will review it with
counsel to ensure we can live up to every obligation and that we have no untenable liabilities (for example,
infinite indemnification without recourse – we will likely accept that, but we mitigate by insurance and
controls to prevent anything catastrophic). The bank’s regulators may even review the contract (OCC and
FDIC have in some cases looked at banks’ fintech contracts to ensure there are provisions ensuring bank
access to data, etc., which ours will). We should assume the contract terms are non-negotiable on key
points for big sponsor banks (they have templates blessed by their examiners), but smaller ones might
negotiate more. Either way, understanding these terms helps us prepare to comply with them from day one
– because once signed, any breach could threaten the relationship.
With this comprehensive understanding of partnership structures and expectations, we can proceed to
structure our compliance program and operations (Section 2) to align with the chosen model, ensuring that
both we and our sponsor bank meet our regulatory obligations and maintain a strong, low-risk partnership.
2. Compliance Delegation Frameworks
(This section examines in depth how compliance responsibilities are divided and managed in our sponsor bank
partnership, building on the terms and models from Section 1. It is tailored to ensure clarity in a layered MSB
context.)
Effective compliance is the cornerstone of a successful MSB-bank partnership. Both the bank and our MSB
carry regulatory obligations under the Bank Secrecy Act (BSA) and related laws, and failing to fulfill them
can result in enforcement actions (for the bank and/or us), not to mention potential exploitation by bad
actors. Thus, having a clear compliance delegation framework – who does what and how results are
shared – is critical. We also must consider how our sub-MSB clients fit into this framework.
2.1 BSA/AML Compliance Responsibilities: Bank vs. MSB vs. Sub-MSB
Ultimate Accountability: No matter what tasks are delegated contractually, regulators maintain that the
sponsor bank is ultimately accountable for ensuring BSA/AML compliance in the partnership . The
OCC has explicitly stated that a bank cannot abdicate its responsibilities simply by relying on a third party –
it must “ensure the third party operates in a safe and sound manner and in compliance with laws”
(OCC Bulletin 2013-29, 2020-10, etc.). In practice, this means the bank must actively oversee our MSB’s
compliance performance. However, day-to-day operations can be handled by the MSB if proper controls and
reporting are in place.
Bank’s Responsibilities: The sponsor bank will typically retain control or final decision authority in certain
critical areas: - Customer Acceptance & KYC Standards: The bank sets the minimum standards for KYC/
CIP. Even if we execute it, we must do so to the bank’s specs . The bank may require approval of our CIP
policy and any changes. The bank often also reserves the right to reject any proposed customer. For
example, if we onboard an entity and during a subsequent audit the bank finds that entity high-risk beyond
their comfort, they can insist we off-board them. This right will be in the contract and is part of the bank’s
obligation to “know its customer’s customers” in a risk-based fashion. Many banks also run their own
checks on at least a sample of end users (they might periodically take a list of all active customers from us
9
2
77
and do OFAC screening or negative news searches as a double-check). - Transaction Monitoring & SARs:
The bank must ensure suspicious activity is detected and reported. They will decide who files SARs (often
themselves). They may integrate our transaction flow into their own AML monitoring systems. Alternatively,
they rely on ours but then require us to escalate any suspicious cases for their review . If something slips
through and later is identified (say by law enforcement subpoena), the bank is on the hook to explain why it
wasn’t caught. So banks often have a belt-and-suspenders approach: they expect us to monitor and they
also do some monitoring. For instance, a bank might have an alert if our FBO account has an unusual
pattern even if we didn’t flag it – then they’ll ask us for an explanation. We need to cooperate fully and
promptly on such inquiries (likely contractually obligated to respond within e.g. 2 days to any compliance
inquiry). - Regulatory Filings: The bank retains responsibility for certain filings. CTRs: if funds are in the
bank (as deposits or cash withdrawals from the bank’s accounts), the bank will file CTRs . We will assist
by providing needed data (like if one of our sub-MSBs accepted $15k cash from a customer and then
deposited it in the bank account, the bank might not know the customer’s details – we’d have to provide
that if requested for CTR aggregation). SARs: As discussed, the bank usually wants to file SARs to FinCEN for
consistency (and to avoid duplicate filings) . We will be required to supply detailed narratives and
evidence for the bank’s SAR filings. In some cases, both may file (particularly if it involves activities beyond
the bank’s purview), but typically we’d coordinate a single filing. OFAC Blocking/Reporting: If a transaction
hits an OFAC sanctions match, the bank, as the institution processing payments, likely has to do the official
blocking report to OFAC. For example, if we attempt to initiate a wire that the bank’s filter catches as a hit
(maybe a payee in a sanctioned region), the bank will freeze it and file the report. We must not override or
circumvent such blocks. Our role would be to gather any additional info the bank needs (like why we
attempted that, what customer is involved, etc.) so the bank can include it in their report. - Overall
Program Oversight: The bank will conduct periodic reviews of our program (essentially mini-exams). They
might align these with our quarterly business reviews or an annual audit. They’ll look at key risk indicators:
e.g., number of SARs filed, high-risk customer count, any compliance incidents, training completion, etc.
The bank’s compliance committee might also require internal reporting on our program. If something
worrisome appears (like our SAR filings spike sharply), they could require a meeting with our compliance
team to discuss remediation. The bank’s regulators will also examine how the bank oversees us. They might
even interview our compliance officer during the bank’s exam (it’s happened in some fintech
partnerships). We should be prepared to interface professionally with the bank’s regulators if invited –
always with the bank present, of course.
MSB (Parent) Responsibilities: We, as the MSB program manager, carry out most front-line compliance
tasks: - Customer Due Diligence (CDD): We identify and verify all customers (this includes our sub-MSB
clients and any end-users if we have direct contact with them in the model). For sub-MSB clients, we treat
them as higher-risk institutional customers – we gather their ownership info, regulatory status, AML
program details, etc., akin to how a bank would risk-rate a corporate MSB client . For our clients’ end-
users (if we ever onboard them directly, say for a prepaid card program), we’ll perform CIP and screening
and maintain those records. We must apply the bank’s standards as noted. We’ll maintain a KYC database
and provide the bank access or data as needed. Also, we do Enhanced Due Diligence (EDD) on higher-risk
customers. For example, if one of our series clients is in a high-risk jurisdiction or is itself an MSB, we will do
deeper vetting (the bank will likely demand evidence of that). - Transaction Monitoring & Investigations:
Our team will monitor all transactions across the program (all sub-accounts, card usage, etc.) on a daily or
real-time basis using our AML software. We will investigate any red flags per our procedures (contacting our
client or end-user for information, etc.). If we deem something suspicious, we escalate to the bank as
required and prepare a draft SAR narrative for the bank’s use. We also handle sanctions screening in real-
time for all transactions (the bank probably also does at least real-time screening at the wire stage, but we
8
13
11
3 58
78
need to screen names in our systems on initiation to catch things early). We will document all investigations
thoroughly, because the bank or examiners may review our case files. We also have to ensure feedback
loop: if the bank asks us about an alert they found, we should incorporate that scenario into our monitoring
rules going forward to catch it ourselves next time. The regulators expect both the bank and MSB to
continuously refine controls. - SAR Documentation & Drafting: If, for instance, one of our sub-MSB clients
had a customer engaging in suspicious layering of funds (maybe many small transfers coming in and one
large going out offshore), our compliance team will do the investigation (gather info from the sub-client,
attempt to determine purpose, etc.). We then decide if it’s SAR-worthy. We notify the bank: “We intend to
file/ recommend a SAR on XYZ activity.” The bank’s BSA Officer will likely concur (or ask for more info). We
might then either file our own SAR (copy to bank) and/or provide a SAR write-up to the bank for them to file
(depending on arrangement). FinCEN encourages sharing SAR information between banks and MSB
counterparties when appropriate , and our contract will basically make it mandatory internally. So
we’ll have an internal policy that any SAR we file that involves the bank’s accounts, we inform the bank (and
vice versa). This ensures consistency and that SARs don’t conflict or miss relevant info. - Sub-MSB Agent
Compliance: As the parent MSB, we take on the responsibility of ensuring each sub-agent (series) also
upholds compliance. Practically, this means we require each series to implement our AML policies for its
operations and we monitor their adherence. We might centralize certain tasks: e.g., we (parent) might
directly screen all end-user transactions even if a sub-agent is the one with customer contact – likely we
have to, because the bank will hold us accountable, not the sub-agent. So for efficiency and control, we will
perform sanctions screening and monitoring at the top level using consolidated data. Sub-agents are
responsible for initial customer interactions (maybe collecting KYC info or handling customer service
questions), but we prescribe how they do it. They must send all KYC info to us for approval. We likely
maintain the master KYC record for all customers, regardless of which sub-agent enrolled them. This way, if
a customer is involved with two sub-agents, we see it (the sub-agents themselves might not know, but we
would and so would the bank via us). This holistic view is important to avoid “stove-pipes” where each agent
only sees its slice. Many money transmitter failures happened because agents only monitored their own
customers and no one looked at patterns across agents – our design should avoid that by centralizing the
data. The bank will appreciate that, as it mimics how a large MSB (like Western Union) has a central
monitoring center watching all agents. - Maintaining Agent List & Regulatory Interactions: We must
keep the formal agent list as required by FinCEN and provide it to the bank or regulators on request.
Also, we handle our own FinCEN registration and renewals (the bank may ask for proof each renewal cycle).
We’ll also handle any state exams of our license – but possibly coordinate with the bank if, say, a state
examiner wants to also review our bank account records. Similarly, if FinCEN’s IRS examiners audit us, we
should inform the bank (per contract) and possibly share exam results. If any compliance issue arises from
our regulators, the bank must know immediately (both as a contractual requirement and courtesy). -
Reporting to Bank: On a routine basis, we likely owe the bank certain reports – e.g., SAR Activity Report
(listing all SARs filed or under investigation), High-Risk Customer List (e.g., if any of our sub-client’s
customers are PEPs or from high-risk countries, list them and monitoring outcomes), and Compliance
Audit Reports (like summary of our independent AML audit findings and how we addressed any issues).
Providing these proactively can satisfy the bank’s requirement to monitor our compliance.
Sub-MSB Agent’s Responsibilities: Each sub-MSB (series) under us must abide by the compliance program
we set and by any specific instructions from the bank that filter down. In practical terms, a sub-MSB will: -
Perform Customer Due Diligence on its direct customers under our supervision. For instance, if a series
signs up a business to use the platform, the series collects the KYC info (ownership, IDs, etc.) and passes it
to us for verification. The series might also do an initial sanctions scan (especially if the customer is foreign
– better to catch obvious hits early). But they shouldn’t approve the customer until we give the green light.
11 13
62
79
Our compliance manual for agents will say “parent must approve all new customers and any high-risk
designations.” - Ensure transaction data is fed to our monitoring systems in real time. In a software
sense, if sub-agents have their own interface or if customers transact via sub-agent’s app, all those
transactions must hit our central system immediately for screening. We may handle this by having one
unified transaction system that sub-agents use (maybe a web portal or API that logs everything centrally).
That is ideal because it reduces chances of an agent failing to report something. Many big MSBs lost track
when an agent ran separate systems – we won’t allow that: our agents will use our platform for any
transaction processing so we see it instantly. - Implementing Compliance Controls Locally: If a sub-agent
is customer-facing (say a client runs a payment app in another country under our umbrella), that agent has
to implement certain controls on the ground: e.g., they must train their staff to recognize suspicious
behavior in their client base and escalate to us, they must comply with any local KYC rules in addition to
ours, and they must not deviate from our procedures (like they can’t onboard someone with insufficient ID
because they felt like it – our rules are mandatory). - Reporting and Cooperation: The agent needs to
report any unusual activity of which they become aware (even qualitatively, like if their staff suspects a user
is doing fraud, even before a system alert triggers, they should inform us). They also must respond quickly
to our requests – e.g., if we ask an agent for more information about a customer (perhaps our monitoring
flagged something and we need context from the relationship manager at the agent), they must provide it
within, say, 24 hours. We will enforce that through contract and oversight. - No Independent Filing of
Regulatory Reports: Typically, our agents will not file SARs or CTRs themselves (unless required by local law
separately). FinCEN rules don’t require an agent of an MSB to register or file independent SARs .
Instead, they pass info to the principal (us) to handle BSA filings. We make that clear in training: if an agent’s
employee thinks a transaction is suspicious, they don’t file a SAR to FinCEN – they escalate to us and we
handle it. This avoids duplication or messy, potentially conflicting reports. It also ensures quality – we have
the more experienced compliance officers writing the SAR narrative with full context from all agents if
needed. - Compliance Certification to us: Just as the bank makes us certify compliance, we might make
each sub-agent annually certify that they followed all procedures, had training, didn’t knowingly do
anything illegal, etc. This creates accountability at the agent level. The bank may ask if we do this – it’s a
good practice, and we will maintain those certifications on file (so the bank can see that we hold our agents
to a documented standard). - Agent Termination: Our agents are required to accept that we or the bank
can terminate their participation for non-compliance. We have a procedure for that: if an agent seriously
violates policy or if the bank instructs, we will swiftly terminate the agent and perhaps even take over any
customer relationships that agent was managing (or wind them down). Agents need to agree to an orderly
transition of their customers if they are terminated (so customers aren’t harmed). This will be in agent
contracts. This way, if the bank spots, say, Agent X as a weak link, we can remove Agent X without drama,
and either service Agent X’s customers directly or shut those accounts as appropriate.
Communication Flow: It's useful to visualize how information flows in this compliance waterfall: - End-
users → Sub-agent (initial info and activity) → Parent MSB (aggregated info, oversight) → Bank (ultimate
oversight, filings to regulators) → Regulators. - Conversely, guidance or actions flow down: Regulators
(laws/guidance) → Bank (internal policies & exam directives) → Parent MSB (our policies, which incorporate
bank’s) → Sub-agents (implement on ground). - If a warning or red flag arises at any level, it escalates
upward: e.g. agent sees weird customer behavior → notifies parent → parent maybe detects broader
pattern → notifies bank → bank possibly sees systemic issue and might notify regulators if needed (like a
SAR or if immediate threat, law enforcement).
This chain must be tight. To keep it so, we plan regular compliance meetings: e.g., monthly calls with each
sub-agent compliance point-of-contact to discuss any issues and review their customers or transactions of
10 41
80
interest. And separately, at least quarterly (if not monthly) calls with the bank’s compliance team to do the
same for the whole program. These standing meetings ensure nothing festers silently. The bank will
appreciate such proactivity – it shows we are self-monitoring effectively.
Documentation: We will maintain comprehensive documentation for all compliance activities – customer
due diligence files, risk assessments, alert investigation memos, SAR drafts/final, training logs, agent audit
reports, etc. The bank or examiners may request any of these. For instance, if a regulator asks the bank
“how does MSB ensure its agents follow procedures?”, the bank can show them our agent audit checklist
and perhaps an example audit report we provided . That kind of evidence is crucial to satisfy regulators
that the layering is under control.
By delineating responsibilities as above and rigorously following through, we aim to meet the “well-
controlled” partnership model that regulators like to see: the sponsor bank knows what its MSB partner is
doing at all times, and the MSB partner effectively extends the bank’s compliance program to every end-
user or sub-agent. FinCEN in its 2005 guidance lauded MSB industry efforts when principals “diligently
implement BSA requirements” across their agent networks – that’s exactly what we commit to do, and our
sponsor bank will expect nothing less.
2.2 Reliance on Parent’s Compliance vs. Sub-MSB Independent Programs
A critical question in our layered model is: can sub-MSBs rely entirely on the parent’s compliance
infrastructure, or do they need their own mini compliance programs? The short answer, as implied above, is
that sub-MSBs operate under the parent’s compliance program – they are effectively part of one program –
rather than maintaining separate, autonomous programs. Here’s why and how we implement that:
FinCEN’s Stance on Agents: FinCEN explicitly allowed that an MSB agent need not have a separate AML
program if it is implementing the principal’s AML program . In fact, in the MSB Exam Manual, examiners
are instructed to evaluate how the principal MSB’s program covers its agents (training, monitoring, etc.) .
The assumption is the principal’s program envelops agents. FinCEN even stated “the anti-money laundering
program of a small MSB with only agents will differ dramatically from [a global one] with domestic and foreign
agents” – meaning they expect the principal’s program is the one in effect, just scaled appropriately.
Our Implementation: Each sub-MSB (series) will adopt our AML/BSA policy in full. We will distribute a
controlled version of our compliance manual to each sub-MSB’s compliance officer. We might allow minor
addenda for specific local requirements (for instance, if a sub-MSB is operating in the EU, they might have
to collect additional info under EU AML directives; they can do so as a complement to our requirements).
But they are not to deviate on core standards. We will formalize this via an Agent Compliance Agreement
stating the agent agrees to abide by parent’s compliance program and all instructions from parent or the
bank.
No Independent Registration or Regulator Interface (for BSA): Since our agents are not separately
registered MSBs , they don’t directly deal with FinCEN on AML program matters – we do on their behalf.
E.g., if FinCEN had an inquiry, it would come to us. Agents won’t file SARs, as noted, and they won’t have to
produce an agent list (they are the agent list). The one area they might engage separately is any state/local
AML obligations – e.g., if an agent is in a foreign country with its own laws, they must comply with those
locally, but that can be done in tandem with our program.
58
97
14
58
14
10
81
Centralized vs. Decentralized Work: The advantage of our model is we centralize as many compliance
functions as possible to ensure consistency and quality. For example: - Screening/Monitoring: Per above,
all transactions across agents go through one monitoring system (run by parent compliance). So an agent
isn't separately tuning rules – we, the parent, set the rules (with bank’s input) for everyone. - SAR
decisioning: lies with parent compliance, not an individual agent. An agent may recommend or suspect,
but parent decides and prepares the report. - Training: we (parent) provide standardized AML training to all
agent staff. Maybe we hold webinars or require them to complete our e-learning modules annually. That
way, everyone receives the same message about risk tolerance and procedures. Agents can add a
supplement if needed for something like their local law, but we prefer to cover that in one unified training if
possible. - Independent Review: We will conduct (or hire an external auditor to conduct) an independent
test of our AML program annually. That review will cover a sample of agent operations as well. We might
include in its scope visiting or auditing one or two agents to ensure they follow program. The results of that
independent audit are a single report (with sections on agents) that we share with the bank . We likely
wouldn’t encourage each sub-agent to hire its own auditor for separate AML testing – that’d be duplicative
and inconsistent. Instead, we coordinate one audit. (The bank might, however, independently audit one or
more agents if they choose. That’s outside our audit, but we facilitate it.)
When a Sub-MSB Needs Internal Compliance Staff: Even though the parent program is the one in effect,
each sub-MSB should have a designated compliance officer or point person who internally ensures that
location/business is following the program. For example, if a series has an office and staff, one person there
would liaise with us, ensure that staff complete our training, and implement our procedures day-to-day (like
checking IDs if they meet customers, securing records, etc.). But that person doesn’t create a new policy;
they enforce ours and handle tasks as assigned by us (like gathering info for an investigation we’re doing).
We will list those designated persons and their qualifications in our documentation to the bank, showing
that every agent location has a competent individual in charge of compliance under our supervision. FinCEN
recommends that “MSB’s agent management practices” include screening agents’ personnel for reliability
– we do that by vetting the compliance reps of agents (maybe require they have a certain training or
background, or at least we interview them to gauge understanding). If an agent’s compliance person is not
up to par, we might require the agent to replace or augment them.
Parent vs. Agent Independent Decisions: Generally, no agent should make an independent compliance
decision that could impact the whole program or create risk, without parent oversight. For instance, if an
agent encountered a suspicious customer, they cannot decide “We won’t report this because he’s my best
client” – they must escalate to us. Or if a law enforcement request comes to an agent (maybe local police
ask an agent for info on a user), the agent should notify us and we handle response (possibly through the
bank if needed, to ensure legal process is correct). So part of training is drilling: “Always escalate up – do not
handle serious compliance matters alone.” This top-down control ensures consistency and also protects
agents (they might not know how to respond properly; we do).
Sub-MSB’s Independent Program Elements: There are a few areas where a sub-MSB might need its own
procedures, albeit aligned with ours: - If an agent is in a different jurisdiction with additional requirements
(like data privacy, or maybe they must file something like local cash transaction reports in their country), the
agent can have an addendum to our policy for that. But they must inform us and ensure it doesn’t conflict
with U.S. requirements. Usually, we incorporate those into the unified policy if critical. - Agents might have
their own internal escalation paths (like within their org) before hitting us – e.g., an agent’s employee sees
something, maybe they tell their manager, then manager informs us. That’s fine as long as it’s quick and
doesn’t drop the ball. We can outline that in the agent’s SOP (Standard Operating Procedure) that fits under
58
58
82
our policy. But ultimately our policy will say “the agent’s compliance officer shall notify parent’s compliance
officer immediately of X” – so it doesn’t matter what internal chain they have, the end result must meet our
requirement.
Regulator and Bank View: Both FinCEN and our bank would prefer a single, integrated compliance
program because it’s easier to evaluate and ensures uniformity. If each agent had its own distinct program,
the risk of inconsistency is huge and the oversight burden on the bank (and us) multiplies. Instead, we
effectively operate as one MSB in multiple locations – which is exactly the model Western Union or
MoneyGram use: one global AML program, applied at all agents (with agents essentially just being outlets
following central directives). We will cite that precedent to the bank: that we are following industry best
practice by centrally controlling AML and not leaving it siloed at sub-entity level.
Conclusion on Reliance: Sub-MSBs will rely on the parent’s compliance program entirely for guidance and
direction. They act as the “ears and eyes on the ground” (since they might have the customer relationship),
but the parent brain analyzes and decides. FinCEN’s rule that agents of MSBs need not register separately
essentially implies that the government looks to the principal MSB as the party responsible for compliance.
And that’s how we and the bank will operate. Our sponsor bank will not approve a setup where each sub-
MSB runs its own little AML program that the bank can’t directly see – they will want everything channeled
through the parent’s program which they review. So by structuring it as one program, we meet that
expectation.
We will document explicitly in our BSA/AML policy that “This program applies to all business units and series
under [Parent MSB]. Agents and series are prohibited from deviating from these policies without written approval
from the Parent MSB Compliance Officer.” And similarly, our agent agreements will bind them to follow our
compliance policies and the sponsor bank’s requirements. This way, all parties (including regulators) are
clear that there is no ambiguity: the parent MSB’s program is the one in effect across the board.
2.3 SAR/CTR Filing Responsibilities Across the Partnership
Proper reporting of currency transactions (CTRs) and suspicious activity (SARs) is a joint responsibility in our
MSB-bank partnership and must be carefully coordinated. We’ve touched on this earlier, but here we lay out
how we handle SAR/CTR obligations at each level and how we coordinate to ensure nothing slips through
and no double-reporting confuses regulators:
SAR (Suspicious Activity Report) Responsibilities:
Sponsor Bank: The bank, as a federally regulated financial institution, has its own SAR filing
obligation (31 CFR 1020.320 for banks). It must file SARs if it knows, suspects, or has reason to
suspect that any transaction (or attempted transaction) through the bank involves funds from illegal
activity, evades regulations, or has no lawful purpose, etc., above $5,000 (or any amount for insider
abuse) . In context of our program, this means if the bank detects suspicious activity either in our
program’s aggregate flows or by our MSB organization, they need to file. Examples: if the bank
noticed our main FBO account doing large in-and-out transfers with unclear purpose (like classic
layering) and we hadn’t reported it to them, the bank would file a SAR on “Activity through [MSB]
account appears suspicious” referencing us and whatever details they have . Also, if the bank
became aware we (the MSB) were not complying with BSA (say we failed to register with FinCEN or
operate unlicensed somewhere – essentially if we were an “unregistered MSB” in some area),
10
•
11
13
83
guidance says banks should file a SAR on that too . The joint FinCEN guidance from 2005 explicitly
instructs banks to file SARs if they become aware their MSB customer is unlicensed or doing
something illegal . So the bank kind of “polices” us as well. We of course will ensure we give them
no such reason by staying fully compliant.
On end-customer suspicious activity: if the bank’s monitoring systems flag an individual transaction
or user that we didn’t report, the bank may file a SAR because it flows through their system. But
typically, in a good partnership, the bank will bounce it to us first: “hey, we see this pattern, are you
looking at it?” If we then investigate and say “Yes, we are filing a SAR on it,” the bank might include
our info or let our SAR suffice. But formally, the bank still might file their own to cover themselves,
but they can reference that the fintech partner is also filing – FinCEN doesn’t mind multiple SARs
(they often get duplicates from banks and MSBs for the same underlying activity).
Finally, if law enforcement or regulators come to the bank about a suspicious incident in our
program that wasn’t SAR’d, the bank could be in hot water. So they are motivated to ensure proper
SAR coverage and will err on the side of caution by filing if uncertain. Our job is to keep them fully
informed so they never have to guess.
Parent MSB (Us): We have a SAR obligation under FinCEN rules as an MSB (31 CFR 1022.320 for
Money Transmitters and providers of prepaid access). For money transmitters like us, the SAR
threshold is $2,000 (or any amount if we suspect terrorist financing) . We must file SARs on any
known or suspected illicit activity involving our MSB or happening through our services. This covers
suspicious activity by sub-agents and end-users as well. FinCEN expects that if one of our agent’s
customers is laundering money, the principal MSB will file the SAR (agents don’t file separately) .
So practically:
If our monitoring flags suspicious transactions by an end-user (like structuring, fraud scams, unusual
cross-border flows), our compliance team will do the investigation (often with the sub-agent’s help)
and decide on filing a SAR. If criteria met, we draft a SAR narrative detailing the who, what, when,
where, and why (suspicion) and file it electronically with FinCEN, listing our MSB as the filer and
describing the role of any agents or banks involved.
We should include in the SAR narrative that transactions flowed through X bank account etc., so
FinCEN can connect it if the bank files one too. FinCEN’s guidance encourages including as much
detail as needed including referencing another SAR if we know of one (we might not always know if
the bank filed separately, but likely we will coordinate).
We then inform the bank of the SAR filing (not the SAR itself in detail, since SAR content is
confidential – but the rules allow sharing SAR info with other institutions that are involved in the
same transaction for AML purposes ). Because the bank is involved in these transactions and is
effectively our “other institution” under 314(b) or under joint filing guidance, we can share the SAR or
at least the gist. Often, sponsor banks want a copy of the SAR form we filed. Under the law, a SAR
can be shared between a bank and its MSB partner if both have SAR requirements and it relates to
common customers/activities (this falls under the 314(b) safe harbor typically, which our contract
would note we both opted into ).
After we file, we maintain that SAR and supporting documentation in our records for at least 5 years
as required. We also track if law enforcement inquires on it later.
Sub-MSB Agent: The agents (series) do not have an independent SAR filing requirement in FinCEN’s
regime (since they didn’t register). FinCEN clarified that an MSB agent who is not separately
13
59
•
•
•
12
68
•
•
•
11
54
•
•
84
registered is not mandated to file SARs . The obligation falls on the principal. So our sub-
agents should not be filing SARs to FinCEN. Instead, their duty is to identify and escalate suspicious
activity to us. We instruct them clearly: if you (agent) detect something suspicious, do not attempt to
“resolve” it or suppress it – report to parent compliance immediately with all details. We then handle
the SAR decision and filing as above. In some cases, an agent might be concurrently something else
(like maybe one of our series has its own MSB registration for a different business line). If,
hypothetically, a series was itself an MSB for separate reasons, it could have SAR obligations in that
other capacity. But for activities under our umbrella, they funnel it to us. This avoids double counting
or confusion.
Example: Series A is a foreign payment company that has to file suspicious transaction reports (STRs)
to its local regulator for anything in its operations. If an STR event happens in the context of the US
program, we’d coordinate with them – they might have to file locally, but we file the US SAR. We
would share info so each report is accurate in their jurisdiction. But this is a corner case. None of our
series likely have separate SAR duties in US.
CTR (Currency Transaction Report) Responsibilities:
CTR rules require reporting cash transactions over $10,000 in one day by or for one person (31 CFR
1010.311 etc.). How this applies in our layered context: - Sponsor Bank: The bank will file CTRs for any cash
transactions that occur through the bank. For instance, if our program allowed customers to deposit cash at
a branch or withdraw cash, the bank would see that and aggregate it. Commonly: - If an end-user of our
program walks into the sponsor bank’s branch (if that’s even allowed) and deposits $15,000 into our FBO
account referencing their name, the bank would file a CTR with themselves as financial institution, listing
the individual as conductor and our MSB perhaps as beneficiary (depending how deposit was structured).
But normally, end-users wouldn’t deposit directly at the sponsor bank (most BaaS setups don’t support
random branch deposits by app users). - More likely scenario: cash enters via our agents. Example: a sub-
agent might accept $12,000 in physical currency from a client for a transaction. That agent is required by
FinCEN to record that and inform the principal. We as principal should aggregate across agents too –
FinCEN clarifies that multiple cash transactions through different agents for one person in one day should
be aggregated for CTR (the MSB must do so) . So we would file an MSB CTR in that case. The bank may
only see one aggregated deposit (if the agent deposited to our account), or might not see cash at all if
agent uses that money to pay out another customer locally. If cash is retained in the agent’s ecosystem and
not physically moving through bank, the bank doesn’t file a CTR. It’s on us. - If the agent eventually deposits
that collected cash into the sponsor bank (say an armored car brings a load of cash from agents to bank to
credit our account), the bank when receiving that bulk deposit might file a CTR on “MSB depositing X cash”
since it’s over $10k to our account. But it lacks individual details. Meanwhile, we as MSB should have filed
CTRs for the individual customers that gave the cash at agent level. - Parent MSB (Us): We have a CTR
obligation (as a “financial institution” under BSA) to aggregate and report cash transactions of >$10k by
person per day across our agent network (FinCEN MSB regulations incorporate this). That means: - We
instruct agents to log all cash-in and cash-out over $1,000 (which they should anyway for recordkeeping,
and $10k for CTR threshold). At end of day, or in real time, our system aggregates if Customer John Doe
gave $6k at Agent X and $5k at Agent Y on same day (maybe trying to evade detection by splitting – classic
structuring attempt). Our system catches that sum $11k for John Doe and triggers a CTR. - We then file a
FinCEN CTR (via Form 112) listing John Doe as the person on whose behalf the transactions were conducted,
each agent location as where cash was received if needed, etc. FinCEN has guidance on MSB CTR
aggregation – we follow it strictly. Typically, MSBs file one CTR per person per day listing all agents/locations
involved. - Because our series are essentially like branch locations for CTR purposes, we absolutely have to
10 41
•
68
85
consolidate that info. (If we didn’t, we could get slapped with a structuring violation for failing to aggregate
– FinCEN has fined MSBs in the past for each agent doing under-$10k to avoid CTR and the MSB not
aggregating). - When we file these CTRs, the sponsor bank might not even be aware of those individual cash
transactions if they occurred solely at agent premises. But we keep records. We must make the CTR filings
accessible to the bank if they want them (they might not explicitly ask, but in an audit they could). - Sub-
MSB Agent: Agents themselves are required to collect data for CTRs (like get ID for a cash transaction
>$10k), but not to file. FinCEN’s reg says an MSB agent making a transaction “as agent for the MSB” doesn’t
do a separate CTR – the principal does. We ensure each agent transmits the required info (customer details,
amount, etc.) to us promptly so we can meet the 15-day CTR filing deadline. - If an agent somehow
independently filed a CTR (maybe not understanding that we do it), it could confuse matters (two reports
for same cash, or incomplete if they only see their piece). So we train them: do not file; send to us. (If an
agent is in a foreign country, they might have local cash reporting – fine, they do that to their government,
but that doesn’t count for FinCEN. We still do our US CTR for aggregated global if it’s part of our US
program). - CTR Example: Suppose one of our series in Texas handles cash from a client. The client one day
goes to two different authorized agent offices (maybe two different series under us) and pays $8,000 at
each to send money (maybe he’s trying to avoid a single $10k record at one location). Each agent logs it and
sees $8k < $10k so not individually CTR-reportable, but both send records to us. Our system sees the same
sender name on two transactions on same day totaling $16k. We promptly complete a CTR listing that
sender and both agent locations as transaction locations. We file to FinCEN. We also flag this pattern as
suspicious (structuring), so likely we file a SAR as well on the structuring attempt, referencing in the SAR
that a CTR was filed . We then also notify the bank of this SAR because it indicates someone abusing our
service – they may want to block that person’s ability to interact with the bank in future. But the CTR itself
we do not necessarily send to the bank (though no harm if they see it; CTR data isn’t confidential like SAR).
The bank would appreciate a heads-up that, “hey we had a structured cash situation and reported it.” - If
Cash enters via Bank vs via MSB: If an end-user somehow deposits cash directly at the bank (rare as said),
the bank files CTR and we wouldn’t, because in that scenario the MSB (us) didn't “receive” the cash first, the
bank did. If an agent receives and then deposits to bank, ideally we file on the receipt and the bank on the
deposit (could be double counting unless one clearly for agent deposit for multiple customers). Actually,
FinCEN has guidance: if an MSB deposits into its bank account $X that represents aggregated funds from
multiple customers, the bank’s CTR on that deposit doesn’t relieve the MSB of its own CTR duty for each
customer’s cash intake. Both file for their respective triggers. The bank’s CTR might just list “MSB company
depositing $X” – if asked, we should have records to break that down for law enforcement, tying into our
CTRs. We and the bank can also share CTR info if needed under 314(b) since it’s BSA info. But CTRs aren’t as
sensitive as SARs. - 314(a) Requests: Not exactly SAR/CTR, but worth noting: FinCEN sends biweekly lists of
suspects (314a) to banks and MSBs to check against their records. We will handle 314(a) queries as an MSB
(we get them via FinCEN secure portal). The sponsor bank will also check its accounts (which includes our
FBO account records). If a name matches one of our end-users, the bank won’t see it unless they have those
names. So likely we as MSB will catch it (we’ll run the list against our user database). If we find a match, we
must report to FinCEN, and we should inform the bank because it involves an account at the bank.
Conversely, if the bank sees a match on something in our account (like if one of our sub-MSB entities or
something was on a list), they’d tell us. Coordination is key here too. We likely sign an info-sharing
agreement to cover this as well.
Summary: We will maintain a SAR/CTR responsibility matrix (possibly part of our agreement with the
bank) that essentially says: - MSB (us) will monitor and identify suspicious activity at user and agent level;
MSB will draft SAR information and either MSB or Bank will file SARs as agreed (with mutual notification). -
Bank will monitor MSB’s aggregate flows and any other info it has and file SARs as needed (notifying MSB if
68
86
appropriate). - MSB will aggregate and file CTRs for cash transactions by its customers through agents. -
Bank will file CTRs for cash transactions conducted at or through the bank (like deposits to the MSB’s
account). - Both parties will maintain records and share information to ensure all required reports are filed
without omission or undue duplication.
By adhering to these practices, we ensure compliance with BSA reporting requirements across our layered
operation, and we demonstrate to regulators that even though multiple parties are involved (bank, MSB,
agents), nothing falls through the cracks due to clear assignment and communication. FinCEN examiners
will expect to trace a suspicious or cash transaction from agent level all the way to filings and see it was
done properly. With our framework, they will be able to: agent logs it → parent records & aggregates →
SAR/CTR filed by appropriate party → bank aware and also filed if needed. That audit trail will be intact.
2.4 Sponsor Bank Audits and Oversight of MSB and Sub-Agents
As emphasized earlier, sponsor banks do not simply trust – they verify. The bank’s ongoing oversight
program for us will involve various audits, exams, and information requests, not only of us (the parent MSB)
but potentially extending to our sub-MSB agents. We need to be prepared to undergo and support these
audits regularly.
Initial Onboarding Audit: Before go-live, the bank may do an in-depth review (audit-like due diligence) of
our policies, systems, and maybe even an onsite visit to our office. They will want to verify that all the
controls we described on paper are actually in place. For example, they might test-run a fake customer
through our onboarding to see if we catch a synthetic ID, or they might ask to see a demo of our
transaction monitoring dashboard. We should treat this almost like a regulatory exam – answer fully,
provide evidence (like sample reports from our systems), and show openness. Passing this “audit” is often
the final hurdle to launch.
Periodic Audits by Bank: Typically, sponsor banks perform a formal audit or examination of each fintech/
MSB partner at least annually (some do it more frequently, e.g., quarterly reviews plus an annual deep dive).
These audits can cover: - BSA Program Audit: The bank will audit our BSA/AML program similarly to how
they audit an internal business unit. They may use their internal audit team or an external reviewer. They’ll
examine our risk assessment, our policies, training records, independent audit results, etc. They’ll sample
customer files (to see if CIP was done right), alert cases (to see if we investigated properly and timely),
SAR decisions (to see if we missed any obvious SARs or filed inadequate ones). They’ll specifically check on
how we oversee agents – e.g., they might follow up on our agent audits: “The bank’s audit team wants to
accompany your team on an audit of Agent X.” We must facilitate that. - IT and Data Security Audit:
Because we handle sensitive customer data and connect to the bank’s systems, the bank will audit our IT
controls – cybersecurity, data encryption, access controls, etc. They might send a security questionnaire or
even do a penetration test with our permission. We should have robust IT policies (which we should anyway
as a fintech). The bank’s vendor risk management team often handles this part, separate from BSA. We can
anticipate this by having our network diagrams, incident response plans, etc., ready to show. - Compliance
Key Metrics Monitoring: The bank might not wait for an annual event; they could have us report key
metrics monthly and only audit if those raise concern. Key metrics could include: number of new customers
onboarded, number of high-risk customers, SARs filed (and brief descriptions), cases of fraud, any
compliance breaches, training completed %, etc. We should gather these metrics for our own management
anyway; sharing them builds trust. If a metric goes out of expected range (say SAR count doubles one
month), we should proactively explain to the bank why (e.g., maybe we had a one-off fraud ring we
87
discovered, now addressed). - Agent-specific Audits: The bank may sometimes want to inspect a specific
sub-agent. This could happen if, for example, one agent has an outsized share of volume or risk (maybe one
series is doing transactions with higher risk countries more than others). The bank might say, “We’d like to
review the controls at Agent Y.” That might entail meeting that agent’s team or at least reviewing how we
audited them. Possibly, the bank’s compliance people might even travel to that agent’s location alongside
us to see operations. We need to accommodate that. Our agent contracts will include: “Agent shall
cooperate with any reviews or inspections by [Parent] or its banking partners or regulators.” If an agent
balks, we can enforce contract or drop them. - Remediation and Follow-up: After an audit, the bank will
issue findings (like internal audit does). We should expect something – no program is perfect, especially
early on. They might say, “The MSB’s alert investigation documentation is insufficient – please improve
documentation” or “We found CIP exceptions not resolved for 3 of 50 files – need a tighter process.” These
findings will come with recommended corrective actions and a timeline. We must respond with a written
plan or acknowledgment and then implement fixes swiftly. The bank will follow up, possibly with a targeted
re-audit on those points or asking for evidence of correction (like new policy sections, training logs, etc.). If
we treat their findings seriously and resolve them timely, we build credibility and they’ll be more
comfortable. Conversely, if we were defensive or slow to fix, trust erodes and next audit might escalate or
they could even restrict new business until we fix issues. - Regulator Involvement: Sometimes, the bank’s
regulators (OCC/FDIC/State) ask to join or observe an audit of a significant fintech partner. We should not be
surprised if one day we find ourselves in a meeting with, say, an OCC examiner present. They may ask us
questions directly. We should answer candidly (but likely through the bank – often examiners direct
questions at the bank who then asks us, but in some cases they might ask us on the spot). Always tell truth
and don’t hide issues – if something went wrong, say how we addressed it. It’s better they hear it from us
with solution in hand than discover it themselves. - Continuous Monitoring: In addition to formal audits,
banks now use technology to monitor fintech programs continuously. Some require real-time data feeds or
read-only access to the fintech’s databases (or at least daily batch data). For instance, Alloy (a compliance
tech company) launched a product to let sponsor banks directly audit fintech customer onboarding in real-
time . If our bank uses such, they may plug into our onboarding API to sample accounts or to
automatically flag anything not meeting CIP. We should be open to that – it actually helps catch any
slippage early. Similarly, for transactions, some banks get a copy of all transactions in near real-time. That
means if our monitoring misses something, the bank’s systems might catch it concurrently. We should
embrace these “second-line” checks – it’s like having an external QA on our compliance. It might feel like
duplication, but given the stakes, it’s understandable. - Document Provision: The contract will likely require
us to provide various documents regularly: e.g., updated agent list (quarterly or upon change), updated
AML policy (annually if changed), results of our independent AML audit (annually) , financial statements
(quarterly/yearly), etc. If we fail to provide these timely, that itself could raise a red flag to the bank’s
compliance. We should diary all those deadlines and meet them proactively. For example, if our
independent audit finishes in October, by early November we send the bank a copy with a letter
summarizing how we’ll address any recommendations. This saves them the trouble of chasing us and
shows professionalism.
Sub-Agent Involvement in Bank Oversight: We must prepare our sub-agents for the possibility of bank/
examiner inquiries. We'll inform their management that as part of operating under our program, they
might be subject to: - Occasional interviews by our bank or regulators (with us present) about their
procedures. - Possibly providing documents (like an agent might need to show local licenses or a suspicious
activity log). - Possibly site visits. For a foreign agent, a US regulator might not travel there, but they might
do a video call or ask us to gather info. However, if a foreign agent is critical and high volume, the bank
48
58
88
might even send a compliance rep overseas to check (especially if the foreign agent is a subsidiary or joint
venture of ours, then it’s partly us).
We will make sure agents understand that cooperating in these oversight activities is not optional – it’s a
condition of being in the program. If any agent is reluctant or uncooperative, that’s grounds for termination
because it threatens the whole program’s integrity. We’d rather remove a problematic agent than jeopardize
the banking relationship or attract regulatory ire.
Areas of Focus: Both our internal audits and the bank's will likely focus on historically problematic areas in
MSB networks: - Agent Compliance with KYC: Are agents properly verifying IDs as per policy? (We might
require them to scan IDs and our system auto-verifies, so we can audit that centrally). - Structuring
Patterns: Are agents possibly colluding with customers to evade reporting? (This was an issue historically in
some remittance networks – agents would help break transactions to avoid CTRs or get around limits). Our
monitoring and agent audit should catch if, say, an agent consistently has many customers doing $9k
transactions – sign of maybe advising them to keep under $10k. If we found that, we’d investigate and
possibly discipline that agent. The bank would look for these patterns too. - Timeliness of Reporting:
Check that when suspicious activity was noted, did we escalate and file SARs within the required 30 days? If
we took too long or missed a filing, that’s serious. We must maintain a SAR log tracking dates of detection,
investigation, decision, and filing. - Consumer Compliance: If we have consumer products, examiners will
check that error resolution (Reg E) was done right, that disclosures were given, etc. The bank’s consumer
compliance examiners might review our customer complaints or how we handle cardholder disputes. We
should have that in impeccable order to not cause UDAAP issues for the bank. For B2B mainly, this is less of
a focus, but if any sub-agent deals with small businesses or individuals, treat them like consumers for
compliance cautiousness. - Agent List Accuracy: FinCEN and examiners love to spot-check agent lists. They
might pick a random transaction from a SAR and say “was this agent on your list provided to FinCEN and the
bank?” If we forgot to update FinCEN or bank about a new agent, that’s a hit. We will maintain the list
meticulously – as soon as we onboard a new series agent, we update our FinCEN agent list (not filed but
kept, maybe share annually with FinCEN as required) and send an updated list to the bank contact. That
way, no surprise unapproved agent operating. - Licensing and Registrations: They’ll verify we have all
needed state licenses and renewals in effect, and that any foreign licenses (if required for agent abroad) are
held. We should keep a compliance calendar and show bank that we renew on time. Bank might actually
condition maintaining the account on us maintaining licenses (they often write that in contract). - Financial
Crime Incidents: If any actual fraud or money laundering event occurred (e.g., we discovered an insider at
an agent was complicit in something, or a large fraud ring used our service before detection), the bank and
regulators will scrutinize how we responded: Did we cut it off promptly? Did we remediate to prevent
recurrence? Document any such incidents with root cause analysis and fixes, and share with the bank
proactively. It shows we’re learning organization. - Training and Culture: Examiners often ask front-line
staff or agent staff about their understanding of AML obligations. We need to ensure even agent employees
can answer basics (“What do you do if someone tries to break a transaction into 2 parts? – I would recognize
structuring and report to compliance.” etc.). If a bank auditor visited an agent location and asked a teller
about AML, we want them to give a confident answer. Achieving that means we push training and short
refresher reminders frequently. We might do surprise agent “mystery shopping” ourselves – e.g., have an
internal person simulate a suspicious request at an agent and see if they handle it right. Report those
results to the bank to show proactive stance.
In essence, we aim to foster a no-surprises environment for our sponsor bank. Through robust internal
auditing and active cooperation with the bank’s oversight efforts, we ensure that any compliance issue is
89
caught and addressed early – ideally by us before the bank finds it, or if the bank finds it, we respond
swiftly. This level of diligence is necessary given our layered structure: we must convincingly demonstrate
that we have effective control over our sub-agents and program, because the bank’s regulators will assume
initially that layering = higher risk of something slipping. We have to prove through audit results and
performance that our compliance program is as tight as – or tighter than – many single-entity MSBs. If we
can do that, over time the bank will gain comfort and perhaps lighten intensive audits (though regulators
likely keep them annual regardless).
By having gone through this detailed dissection of compliance roles and oversight, we lay the groundwork
for operating our program in a safe, sound manner that satisfies both FinCEN’s expectations and our
sponsor bank’s regulatory obligations. The next sections (Section 3 onward) will examine how regulators
view layered structures and how we align with those views, and specific programmatic areas (like prepaid
compliance in Section 4) that we must handle in addition to core BSA/AML.
3. Regulatory Treatment of Layered MSB Structures
Both federal and state regulators have grappled with the concept of layered MSB arrangements – where
one MSB works through subordinate entities or agents – and their stance can be summarized as cautious
acceptance: it’s legally permitted, but it must be transparent and well-controlled. In this section, we discuss
how FinCEN and state regulators approach MSB-to-sub-MSB setups, what disclosures and structural limits
they impose, and how that interacts with our bank partnership. We also touch on the agent-of-payee
exemption in relation to bank-sponsored programs, as our scenario might brush against it in certain flows.
3.1 FinCEN’s Perspective on MSB Principal-Agent (and Sub-Agent) Arrangements
FinCEN Policy & Rules: FinCEN, as the administrator of BSA for MSBs, explicitly allows MSBs to operate
through authorized agents. The key regulatory basis is in FinCEN’s MSB registration rule (31 CFR 1022.380)
and guidance: - An agent of an MSB is not required to register separately with FinCEN, so long as the
agent exclusively provides MSB services on behalf of a registered MSB . FinCEN’s rule states: “a person
that is an MSB solely because it serves as agent of another MSB is not required to register” . This is exactly our
case for series agents – they are MSBs only by virtue of acting for the parent, and thus we do not register
them individually. FinCEN even carved that out as an exemption from registration. (However, if an agent also
conducts MSB activities on its own account outside the agency, it would have to register – but that’s not our
scenario). - FinCEN requires that the principal MSB maintain a list of its agents (with names and
addresses) and update it periodically . We must produce this list to FinCEN or any law enforcement upon
request within 2 business days. This implies FinCEN expects us to always know who our agents are
(obviously) and treat that list as part of our compliance records. We have that list ready. FinCEN doesn’t
require us to submit it routinely (though in past they had considered requiring filing of agent lists –
currently, it’s just “maintain and produce on request”). We will proactively share it with our bank as well for
transparency. - FinCEN expects the principal MSB’s AML program to cover agents. 31 CFR 1022.210 (d)
says an MSB’s AML program shall be “designed to ensure compliance with BSA requirements”; while it doesn’t
explicitly mention agents in the rule text, FinCEN’s guidance and exam manual do. For example, the MSB
section of the FFIEC BSA/AML Exam Manual (which FinCEN co-authors) has an entire section on “Agent
Monitoring” and examiners are told to assess how the MSB principal: selects, trains, and audits its agents,
including whether it has written agent management procedures and termination policies . FinCEN’s view
is that the principal MSB must actively manage agents to ensure BSA compliance at those outlets. In 2004,
FinCEN fined Western Union $10 million for compliance failures largely related to not adequately
10
10
62
58
90
overseeing agent activities that allowed structuring by customers. That set a precedent: principal MSBs will
be held accountable for their agents’ failings. We take that lesson to heart in our program: any compliance
lapse by an agent is essentially our lapse in FinCEN’s eyes. Therefore, we implement the strong oversight
described in Section 2. - Depth of Agent Networks: FinCEN’s rules and guidance don’t explicitly forbid
multiple layers of agency (e.g., agent-of-an-agent). They even acknowledged scenarios of domestic and
foreign agents (sub-agents) in commentary . FinCEN’s MSB definitions focus on whether a person is
acting on behalf of a principal or on their own. If an MSB has an agent, and that agent in turn uses
subagents, presumably FinCEN would treat those subagents also as agents of the principal by extension
(since ultimately they’re providing the principal’s services). FinCEN has not published separate guidance on
“agents of agents,” but logically, we could list sub-agents on the principal’s agent list as well. For example, if
Western Union’s agent is Company X, and Company X has sublocations run by subagents, Western Union
typically includes all those locations/names in its agent list to FinCEN. FinCEN examiners would then
consider all of them under Western Union’s program. So, FinCEN doesn’t encourage long chains, but they
implicitly allow it as long as registration and program obligations are met at the top and information can be
provided. They stress though that if an entity does MSB activity on its own behalf too, it can’t hide behind
agent status – it must register. In our case, our series strictly act for parent, so no issue.
FinCEN Rulings and Advisories: FinCEN has issued rulings that illustrate how they differentiate agents vs.
principals: - FIN-2008-R006 (the authorized agent for utility payments ruling) concluded that a retail
business taking bill payments as an agent of utility companies is not a money transmitter requiring MSB
registration or SAR filing, because it’s agent-of-payee. That’s a different use of “agent,” but it shows FinCEN’s
logic: when acting solely as agent for the actual service provider (the payee), they don’t consider you a
separate MSB. Similarly, they don’t consider our series separate MSBs – we cover them. The utility ruling
essentially aligns with us claiming agent-of-MSB status for series (which FinCEN explicitly allowed in reg). -
FIN-2012-A001 (the Foreign-Located MSBs advisory) is relevant because it reminds that if any of
our sub-MSBs are foreign companies doing business in the US (like serving US customers or acting as our
agent with US customers), they are considered MSBs “in substantial part in the US” and would normally
have to register. But as our agents, they don’t (the reg exempts them) – however, FinCEN in that advisory
said foreign MSBs (including agents) must appoint a US legal agent for service of process and comply with
BSA as if domestic . They basically extended US BSA obligations to foreign MSB participants. In our
setup, we as the principal fulfill those obligations for the whole program. FinCEN admonished banks in that
advisory to ensure their foreign MSB customers are registered or legitimately agented and to file SAR if not
. So, as long as we list any foreign agent in our agent list and treat them under our program, FinCEN is
satisfied. They just don’t want unregistered foreign MSBs sneaking in. In our documentation to FinCEN (if
asked) and to banks, we clarify that any foreign entity in our chain is an authorized delegate under us and
thus covered by our FinCEN registration (this is exactly how many global MSBs operate, with foreign agents
not separately registering with FinCEN). - SAR obligations for agents: FinCEN Ruling 2003-8 and echoed in
2008-R006 mentioned earlier essentially held that if an agent is just acting for a principal MSB, the
principal is the one with SAR obligations. FinCEN concluded in those rulings that the principal MSB’s BSA
program and SAR filing covers those transactions. They reasoned that multiple SAR filers for the same
activity could cause confusion, and that the party with the most complete picture (the principal) should file.
This justifies our approach where series agents do not file SARs independently but feed info to us.
Our compliance with FinCEN expectations: We ensure: - We are properly registered (we have our MSB
registration renewed each 2 years, listing ourselves as provider of money transmission and/or prepaid
access if applicable). On that registration form, we indicate we have agents and commit to maintaining an
agent list . - We maintain the agent list meticulously and can deliver it rapidly to FinCEN or IRS
14
68
53 31
98 31
13
68
62
91
examiners. We should also include foreign agent addresses if any, and update whenever an agent is added/
removed. FinCEN's rule expects it to be updated within 30 days of a change (as a best practice, though not
explicitly in reg, FinCEN has wanted timely updates). We likely have to show this list to the IRS MSB
examiners in any audit. - Our AML program document explicitly addresses agent oversight (so if FinCEN
examiners read it, they see pages on agent due diligence, training, transaction limits, etc.). That
demonstrates we integrated agents into our risk assessment and controls – a point FinCEN focuses on . -
We have a zero tolerance policy for agent misconduct and documented procedures to terminate agents
that pose risk (and FinCEN will want to see that if an agent is found complicit in a money laundering
scheme, we will cut them off immediately – which we will). We keep records of any such actions and report
to FinCEN or law enforcement as necessary (maybe via SAR). - FinCEN examiners will likely sample some
agent transactions in an audit. They’ll check if CTRs/SARs were filed as needed. We should be ready to
provide cross-references (like “Transaction on this date at Agent Q, we filed SAR #123, here’s the
documentation.”). - Because FinCEN can directly penalize the principal for agent failures (as happened in
Western Union’s case with Arizona agents facilitating fraud), we treat every agent issue as if it’s our own
branch issue. Documenting our agent training and monitoring is key. FinCEN often asks for evidence of
training materials and schedules in exams – we’ll have logs of each agent’s staff trained and tests passed.
Sub-Agents / Sub-Agents of Sub-Agents: If one of our series agents wanted to appoint its own sub-agent
(like franchise out our service further), that would introduce a “third layer.” FinCEN hasn’t clearly outlawed it,
but it becomes unwieldy. Many states do restrict that (e.g., some state laws say an authorized delegate of a
licensee shall not appoint sub-delegates without licensee’s consent). From FinCEN’s perspective, if we
allowed it, those sub-sub-agents effectively also become our agents (just twice removed). We then should
add them to our agent list as well to be safe. This could blow up the complexity (imagine hundreds of sub-
sub-locations). For now, we plan not to allow that – each agent is directly contracted with us and cannot
sub-contract further without permission. If we ever did (maybe in an international market it’s common to
have tiered distribution), we would have to ensure we know those sub-agents and treat them as we do first-
tier agents. FinCEN likely would hold us responsible for them too. To avoid confusion, we likely simply won't
permit further delegation in our standard agent agreement. That’s also what our sponsor bank would
prefer (the fewer layers, the better).
Public Figure: FinCEN’s synergy with Sponsor Banks: FinCEN expects banks to know if their MSB clients
use agents and to get that agent list . Our bank likely will share our agent list with FinCEN or examiners
as part of their bank exam. FinCEN (which often participates in those bank exams for MSB accounts via the
FFIEC exam team) will be pleased if they see our agent list and it matches the one we have on file for our
registration. Any discrepancy (like if we had agents not on the list or vice versa) might raise questions. We
will keep those in sync.
Conclusion FinCEN: FinCEN basically allows our model as long as: - We register and list agents (done). - We
have a unified AML program covering all activity (done). - We ensure all BSA reporting is done (we do CTRs
and SARs as needed). - We can provide info quickly on any part of the network (we can, via our centralized
database). - We cooperate fully with law enforcement (we will via 314(a) responses, SARs, etc.).
Thus, FinCEN should be satisfied with our approach. In fact, FinCEN likely prefers an MSB using agents
under one umbrella to those agents trying to operate independently unlicensed. Our strategy keeps
everything under one accountable entity (us), which is what FinCEN’s MSB regs are designed for. We just
need to uphold our end by making sure none of our series do rogue MSB activities outside our oversight
(which is more a licensing issue too).
58
58
92
3.2 State Regulators’ View on Layered MSB (Licensee-Authorized Delegate) Networks
State Money Transmitter Licensing: Most states allow a money transmitter licensee (like our parent LLC)
to appoint authorized delegates (agents) to conduct money transmission on its behalf. This is codified in
state laws (many following the Uniform Money Services Act). We have obtained our licenses accordingly and
disclosed our business model in those applications. Key state regulatory points: - The licensee (parent MSB)
is fully liable for the actions of its authorized delegates. This is usually explicitly in state law or rule. For
example, Texas regulations say the license holder is responsible for the compliance and actions of its
authorized delegates (and Texas even allows revocation of a delegate authorization if issues). We accept
that responsibility (we already do per FinCEN; states reinforce it). - Many states require the licensee to
report and maintain the list of authorized delegates (often through the NMLS system now). Some states
require notice within a certain period when you add or drop a delegate location. We will keep our NMLS
records up to date. If our series structure changes (say we add a new series in a new state), we might have
to add a “location” or “trade name” to our license or get state approval. For example, if series use different
names, we need to list those as DBAs on our licenses. We did that in initial licensing if known. If a new client
wants a unique brand not initially listed, we may need to add a DBA to relevant licenses before using it. We’ll
coordinate that carefully. States like California require every agent location’s information filed and an initial
delegate fee paid. We will do so if needed for each series and even each physical location if relevant. Non-
compliance (like an unreported agent operating) can lead to fines or license issues. So we treat that with
high importance (like FinCEN’s agent list, but at state level too). - Some states limit agent activities: - Net
Worth and Bonding: The licensee typically must include the business from agents in its own financial
calculations (like required net worth, permissible investments equal to outstanding transmission liability,
etc.). We have to ensure our bonding covers agent transactions too. Some states require listing agent
locations on the bond. We’ve set our bond amounts with an eye to covering potential agent liability. The
bank might ask to see our compliance with state bonding – we can show our bonds and that they account
for our total volume (the volume includes what agents do as it’s all our volume). - Prohibited agent
practices: A few states explicitly say an authorized delegate cannot itself authorize others to do money
transmission on behalf of the licensee (no sub-delegation) without licensee’s direct appointment. So legally,
a chain beyond one level might not be allowed. E.g., Illinois statute implies you must be either the licensee
or an authorized seller directly. We will abide by those – we treat all effective outlets as directly authorized
by us. - Agent-of-Payee vs License: Some states have the “agent of payee” exemption for money
transmission, meaning if you are collecting payment as agent of the intended recipient (payee), you don’t
need a license. Our clients might sometimes claim that if they were on their own. But since we are licensing
to provide clarity, we likely aren’t relying on agent-of-payee for our core. We might, however, use agent-of-
payee logic to mitigate licensing in states where we want to not individually license a particular flow. For
example, California has an agent-of-payee exemption by case law (the Commissioner v. Checkfree case). If
one of our services clearly fits agent-of-payee (like paying merchants on behalf of consumers), we might
choose to run it under that exemption to avoid having to treat those transactions as “money
transmission” (and thus maybe outside our license’s scope). But in practice, since we already have CA
license, it might not matter, except for compliance differences. We mention agent-of-payee specifically in 3.4
below. - Disclosure and Signage: Many states require that authorized delegates display a notice that they
are an authorized delegate of [Licensee], including the license number and sometimes a consumer
assistance phone number. We ensure our series (especially if any have a public-facing aspect or website)
display the required info. For example, if series ABC runs a website to onboard users, the site should say
“ABC is an authorized agent of [Parent MSB], which is licensed in [list states].” The bank and state regulators
like to see that, as it informs consumers who is ultimately responsible. - Supervision/Examination: State
regulators (often through the Multi-State MSB Examination program) can and do examine licensees. They
sometimes also visit agent locations as part of an exam to test procedures. If our program is examined,
93
examiners might request to visit or call a sample of our agents (maybe domestic ones). We will
accommodate that. We will also let our bank know if a state exam is happening – bank might get a heads-up
via NMLS too. If a state finds issues with an agent, they can demand we fix it or even ban that agent from
operating in their state (e.g., if an agent had a principal convicted of a felony, a state might not want them
selling money services). We then must comply (we could drop that agent or have them remove that
principal). We’ll communicate any such restrictions to our bank as well, to keep them in the loop. -
Authorized Locations vs. Legal Entities: Some states consider each legal agent entity as one “authorized
delegate” even if it has multiple outlets. Others require listing each outlet. For series, each series is a
separate legal entity – we treat each as a separate delegate in states. If a series has multiple offices, some
states might require listing each location where money services are offered. We will do so if applicable
(though likely our series operate mostly online, but if any have a physical branch, that counts). - Multi-
Jurisdictional Issues: Our structure might have an agent in a state where we (parent) don’t yet have a
license (maybe because that agent only handles certain exempt transactions). We have to be careful: many
states say you can only have agents in their state if you are licensed there or exempt. If we found a business
in a state where we lack a license wants to be our agent, we must either get licensed there or ensure an
exemption covers it (like agent-of-payee or if all activity is federal covered, etc.). Our conservative posture is
to not operate in a state without either a license or clear exemption. So we likely have already pursued
needed licenses (the business context said we operate where required, with minimal friction, implying we
avoid gray areas). - Agent Depth: If we attempted a multi-layer beyond one level, some state regulators
might object as it complicates who is responsible. E.g., New York (NYDFS) doesn’t allow an unlicensed sub-
agent to transmit unless directly as an agent of a licensee. We will avoid multi-layers to keep states
comfortable. If we ever needed it, we might have to license that intermediate entity too (costly, so better
not). Thus, each series is directly under us and no further sub-delegation without converting them to direct
agents or obtaining state approvals.
State vs. FinCEN Focus: States care not just about AML but also consumer protection (like safeguarding
customer funds, fee disclosures, etc.). For example: - Safeguarding and Permissible Investments: We
must have eligible investments equal to all outstanding money transmission obligations (which includes
money collected by agents but not yet delivered). We track that on a consolidated basis. Agents presumably
forward funds to us quickly (or to the beneficiary). Our bank accounts or trust accounts likely hold these
funds. We must ensure at any time if an agent owes money (like collected but not remitted yet), we include
that in our daily settlement, and our permissible investments cover it. The bank might ask for our
permissible investment calculation – we likely keep mostly cash or cash equivalents, which is the safest
permissible investment, making state regulators comfortable that even if an agent defaulted, we have the
funds to pay customers. The bank too cares because if an agent ran off with money and we didn't cover it,
customers might sue all parties including the bank. So we absolutely maintain that coverage. - Consumer
Complaints at Agents: If an agent’s customer complains (say they weren’t paid timely), states say the
licensee must handle it. We'll intake any complaints centrally (we have a toll-free number on receipts, etc.).
The bank might also monitor complaints forwarded through them or CFPB. We record and resolve them
(state regulators often review complaint logs in exams). - Money Laundering vs. Consumer Fraud: Many
states (and FinCEN too) are very concerned with MSB agents being used for fraud – e.g., scammers who
have victims wire money through an agent, or agents colluding in fraud (like not requiring proper ID so
scammers pick up funds under false names). We set policies at agents to mitigate fraud (like require
thorough ID checks for pickups, awareness of common scam signs, etc.). This protects consumers and helps
AML (as fraud often ties to ML). State regulators have penalized licensees for agent failures that let
consumer fraud happen (Western Union’s settlement with states in 2018 for scam facilitation by some
agents). So our compliance extends to training agents on detecting and preventing consumer scams (like
94
the classic grandparent scam, etc.). This is not strictly AML, but regulators treat it as part of MSB compliance
(it's under UDAAP/consumer protection). The sponsor bank will also want to know we handle that because
banks are liable under UDAP if their agents allow fraud unchecked. We will likely implement an anti-fraud
program aligned with FinCEN Advisory FIN-2017-A1 (which addressed MSBs and fraud schemes) and share
that with both states and bank.
Regulatory Communication: We intend to be transparent with state regulators about our structure. In
license applications, we likely described the series LLC and how it operates as a single MSB. Some less
familiar regulators might have had questions, but since Montana and others allow series LLC, they accepted
it. We'll keep regulators informed if we make changes (like if we add a new series doing business in their
state). It's better they hear from us proactively than find out via exam or complaint. An open line with
regulators also gains trust – if something tricky arises (like a new use case that might or might not need a
license in a state), we can ask them for guidance. - Example: Suppose one series wants to begin an “agent-
of-payee” type service in a state – do we need a license or can we rely on exemption? We could ask that
state regulator’s opinion. If they bless agent-of-payee, we proceed but still keep oversight as if licensed (to
maintain uniform practices). - Sponsor banks appreciate when the MSB partner has good rapport with its
regulators, because it means lower risk of state enforcement or surprises that might entangle the bank. If
any state regulator had an issue (like they think one of our agents was acting improperly), we’d immediately
address it and inform the bank of resolution.
Summation on States: State regulators acknowledge layered structures by their provisions for authorized
delegates, but they demand: - Full disclosure of all who’s involved and where, - Licensee’s proactive
control over those delegates, - Financial responsibility on licensee for any delegate misstep (like
refunding consumers if delegate fails to pay out, etc.), - No dodging licensing via multi-nesting or misusing
exemptions.
We design our operations to meet these expectations. By listing and bonding our agents, training them,
and keeping all obligations centrally, we put state regulators at ease. Our sponsor bank in turn will ask us to
confirm we meet all state requirements (they often do an initial legal review of which states we need
licensing in and ensure we have them – banks have been burned by banking an MSB that said they didn’t
need a license in X state but did – so they double-check). We will supply them with copies of all our licenses
and a memo on our multi-state compliance plan. That way the bank sees we’re squared away with states,
reducing one vector of risk (no fear of a sudden state cease-and-desist against us that could disrupt the
program).
3.3 Required Disclosures and Structural Transparency
To avoid regulatory and partner issues, we must be very transparent about our layered structure in all
contexts: - Disclosures to FinCEN/Regulators: As noted, we maintain agent lists for FinCEN and license info
for states. If FinCEN or a regulator asks "list your series or DBAs," we provide it. We do not hide behind
separate series in communications – we make it clear they are part of one program. For example, in our
FinCEN MSB Registration, we listed any trade names (maybe each series uses parent’s name or their own).
FinCEN’s MSB registry allows listing trade names. We likely added an entry for each distinct brand (with
parent’s EIN, etc.). This means if someone searches FinCEN’s MSB registry by a series brand name, it will
show up under our registration. This helps banks or others verify that brand is legitimately covered. We
ensured to do that. - To Sponsor Bank: We gave the bank full information on each series (ownership,
location, compliance contact) . They probably included those details in their internal risk assessment. We3
95
might even sign a representation in the contract that we have disclosed all agents and will disclose new
ones before using them (some agreements require pre-approval of new agents by bank, as said). - To
Consumers/Clients: If any end-customer interacts with an agent, they should be made aware of the
licensed entity behind it. Many states require that receipts or websites show something like “Money
transmission services provided by [Parent MSB Name], a licensed money transmitter, through its authorized
agent [Agent Name].” We'll do that. On any user-facing app that a series runs, a footer can say “XYZ
Payments (Series of ABC LLC) is an authorized delegate of MasterMSB LLC (NMLS 123456), which is licensed
as a Money Transmitter by the [list of states].” This not only meets some states’ requirements but also
fosters trust – users can verify our license on state websites or NMLS. - On Instruments: If we issue any
instruments (like prepaid cards or payment vouchers), they might include our parent’s name or the sponsor
bank’s name as issuer. E.g., open-loop prepaid cards must list the issuing bank. But we may co-brand it with
our program/agent brand. We need to ensure any cardholder agreement clearly states that [Parent MSB] is
program manager and is responsible for oversight, and that the sponsor bank is the issuer. Some states
(like Florida) require that every money transmitter’s payment instrument (like a money order) have the
licensee’s name and address. For digital receipts, similar info. We'll incorporate that so regulators pulling a
sample see it’s properly labeled. - Public Clarity: Even though not legally mandated, we might have a page
on our website explaining our series structure (maybe in an “About Us” or “Legal” section) to avoid
confusion. If someone tries to figure out “who is handling my payment,” they should be able to find the
licensed parent easily. This also preempts suspicion – in the past, shady MSBs tried to use different names
to dodge complaints or enforcement. By being overt that all series are part of one licensed entity,
regulators see we aren’t playing shell games.
Limits on Depth (“nesting depth”): Regulators haven’t set a numeric limit (like “no more than 2 layers”).
But from practical standpoint, beyond one layer, it becomes very hard to manage and examine. We
ourselves limit to one. If we absolutely needed a second (say a foreign agent that by law can only operate
through a local sub-agent), we’d approach regulators for case-by-case permission. Possibly they'd require
that sub-sub-agent to also become an authorized delegate directly of us in that region. We can avoid that by
directly contracting wherever possible.
Agent-of-Payee Interaction (how layering meets that exemption):
Many fintech payment models rely on the agent-of-payee concept to avoid money transmitter licensing. In
our context: - If we were doing pure agent-of-payee, we might not need licenses in some states, and
possibly not even be considered an MSB by FinCEN (if all flows were payments for goods/services). However,
we proactively got licenses and set up as an MSB to cover broad use cases. - We might have a client series
where technically the transactions are agent-of-payee: e.g., a series facilitates bill payments as agent of
merchants. In such transactions, by state law they might not be “money transmission” requiring a state
license. But since our parent is licensed anyway, it covers them. Still, for that client’s operations, we could
take advantage of not being subject to certain escheat rules for gift cards, or not needing to adhere to
money transmitter rules on refunds because agent-of-payee transactions might be regulated differently. -
From a sponsor bank view, agent-of-payee vs MSB licensing is somewhat moot – either way, BSA/AML must
be done. The bank doesn’t care if an activity is exempt from state licensing; it cares that all flows are
monitored. So agent-of-payee doesn’t change our compliance partnership with the bank except that the
bank might ask “why do you not have a license in X state?” We’d answer “because those transactions are
agent-of-payee under state law and exempt – here’s the statute. Nonetheless, we treat them under our
compliance program equally.” Usually that suffices. If the bank was unsure, they might consult legal and
possibly ask for a legal opinion letter for that exemption. We should be ready to provide one if needed for a
96
given state. Or simply avoid relying on it if not necessary. - Sometimes MSB bank agreements explicitly
forbid relying on uncertain exemptions without informing the bank. MoFo’s tip #3 notes regulators expect
banks to examine if their fintech partner should be licensed and if not, why not (like relying on agent-of-
payee, etc.) . So the bank will definitely ask about each area we operate, “Are you licensed there? If
not, why do you not need one?” We have clear answers (either we are licensed, or if not, the activity is
through an FDIC-insured bank partner or agent-of-payee or under threshold in that state, etc.). We should
memorialize that in a memo to the bank so they can show examiners. For example, if we do an Amazon-like
payee agent model in a certain state that exempts marketplace payments from licensing, we’ll note that. - If
any agent-of-payee flows exist, we will ensure they still meet BSA requirements. FinCEN clarified that agent-
of-payee transactions can still be considered money transmission federally if not integral to a separate non-
financial service (but typically they say it's integral to goods/service, thus not primarily MSB activity).
However, since we have an MSB program anyway, we simply run those through our program. The bank
might not care if a transaction is agent-of-payee or not, they just want to know it's legal in that state and we
are handling compliance. So we brief them if any of our series is using that model, and that it’s allowed.
Agent-of-Payee Example with Sponsor Bank: Suppose one series handles payments for ride-share drivers
(drivers are “payees” for services to riders). Many states exempt that under agent-of-payee (like drivers
appoint the platform as agent to collect from rider). That series might not require a state license on its own.
But under our licensed umbrella, it doesn’t hurt that we have one; we just are technically “over-licensed” for
that specific flow. Some banks actually prefer their fintech partners to be licensed even if arguably exempt,
as a risk mitigant. We took that approach (licensing everywhere feasible) for “minimal regulatory friction” as
the context says. So we likely don’t heavily lean on agent-of-payee with our bank, except to explain maybe
why some states weren’t critical or if our client specifically structured themselves as agent-of-payee for
merchants. - The interplay: If we said to bank "We don't have a license in Alabama because all our
transactions there are agent-of-payee," the bank might ask for our legal analysis and ensure it's solid. If
comfortable, they'd proceed but monitor any regulatory changes. If not comfortable, they might insist we
not operate in Alabama or get licensed anyway. Since we want to avoid conflict, we might just get the
license to reassure them (assuming volume there was enough to matter).
Summation on agent-of-payee and layering: Agent-of-payee is a way to sometimes avoid being labeled a
money transmitter at state level. However, since we already operate as a registered MSB with agents,
invoking agent-of-payee doesn’t change much for FinCEN or the sponsor bank. It mainly affects state
licensing. In our scenario, we likely use it sparingly if at all, because we chose to maintain licensing to be
safe. - One area it could help is gift card programs (some states exclude gift cards from unclaimed property
if considered agent-of-payee of merchant, etc.). We will consult with legal counsel on each specific program
to optimize compliance posture, but always keeping the sponsor bank informed so they aren’t surprised by
any different treatment or risk.
3.4 Gift Card/Prepaid Program Regulatory Specifics and Sponsor Bank Relationships
(Combining with Section 4 content to maintain flow as needed, because objective 4 is about gift card/prepaid
specifics – I'll integrate it into this context as well.)
(I see the structure included objective 4 specifically for prepaid, which is addressed in section 4 after risk 3. Let’s
keep this separate: Section 3 focusing on regulators in general, Section 4 on specifics of prepaid compliance. I'll
proceed accordingly.)
99 95
100 68
97
Given the already extensive detail, I will ensure Section 4 covers remaining parts from the user question 4
like Reg E, network requirements, etc., and Section 5 covers risk mitigation points (point 5) which I did
thoroughly in the preceding content (analysis portion). Then Section 6 on international client considerations
which I also covered along the way, but I will consolidate. Finally, recommended partnership structures
(point 6) I implicitly gave but maybe a final recommendation in conclusion style is needed.
3.4 Gift Card / Prepaid Program Regulatory Specifics in a White-Label Context
When our MSB program involves issuing prepaid or gift card products (whether open-loop Visa/
Mastercard cards or closed-loop stored value), it triggers additional regulatory regimes and sponsor bank
requirements on top of standard BSA/AML. These ensure consumer funds are protected and consumer
transactions are handled fairly. Key considerations include Regulation E compliance, CFPB Prepaid Rule
requirements, network (Visa/Mastercard) rules for program managers, and state unclaimed property
(escheatment) obligations for gift card balances. We outline how we address each, in cooperation with our
sponsor bank:
Sponsor Bank’s Role in Prepaid: In any prepaid or debit card program, the sponsor bank is the actual
issuer of the cards (the entity with the network license). As such, the bank is directly subject to Regulation
E (Electronic Fund Transfer Act) for those card accounts and to the CFPB’s Prepaid Accounts Rule (which
became effective 2019). The bank will therefore insist that our program (which it sponsors) fully conforms to
these rules, and it will actively oversee our compliance. Typically, the bank provides or approves the
cardholder agreement and disclosures we use, dictates certain customer service and error-resolution
processes, and ensures that cardholder funds are handled in an FDIC-insured account structure. We as
program manager implement these requirements on the ground.
Regulation E and CFPB Prepaid Rule: - Disclosure Requirements: We must provide a short-form and
long-form disclosure of fees and key terms to consumers acquiring the prepaid card, as mandated by 12
CFR 1005.18 (Reg E’s Prepaid Rule section). The sponsor bank will often have templates for these
disclosures. For example, our card packaging or online sign-up must display a CFPB-model fee chart (short-
form) showing common fees (monthly fee, per purchase fee, ATM withdrawal fee, balance inquiry, customer
service fee, etc.) in a standardized format . The long-form (complete terms and all fees) must be
available digitally or in writing. We will prepare these and the bank’s compliance team will approve them to
ensure they include all required language (e.g., how to access account information, FDIC insurance
eligibility, error resolution rights, etc.). - Consumer Financial Protections: Prepaid card holders (except
certain limited exceptions like some gift cards) get Reg E protections similar to bank debit card users. This
includes: - Limited Liability for Unauthorized Transactions: If a customer’s card is registered (identity
provided) and it’s lost or stolen or otherwise used fraudulently, their liability is capped ($50 or $0 depending
on timing of report) as long as they report timely. We must make provisional credit within 10 business days
of notice for disputes (or 5 business days for Visa Zero Liability, which our sponsor bank may voluntarily
offer). - Error Resolution Investigation: When a customer disputes a transaction (e.g., “I didn’t receive
goods I paid for” or “Unauthorized charge”), we as program manager must follow Reg E §1005.11 –
investigate promptly, report results within 10 business days (we can extend to 45 days for certain cases if
provisional credit given). The sponsor bank will require detailed procedures on this. We likely handle the
investigation (gather merchant info, etc.) and submit our findings to the bank. The bank may have us send
the resolution letter to the customer on bank’s behalf. The bank’s examiners will audit some dispute files to
ensure we adhered to timing and provided provisional credits correctly. We thus maintain a dispute log
showing date of claim, provisional credit date, resolution date, etc., to prove compliance . - Access to
101
42
98
Account Information: Under the Prepaid Rule, since we may not issue periodic paper statements by
default, we must provide free electronic account histories (e.g., through an online portal) and also a
method for customers to get a 60-day written history on request. We have our app/website show
transaction history and a phone line for balance inquiries (this is a rule requirement). Sponsor banks check
that our tech meets this. - Submission to CFPB Prepaid Agreement Database: The CFPB requires issuers
to submit new prepaid account agreements to its online database. The sponsor bank (as issuer) will do the
filing, but they will rely on us to provide the finalized agreement text. We must notify the bank of any
changes so they can re-submit within 30 days of change. We’ll coordinate this to ensure the bank stays
compliant with that rule . - Network Zero Liability & Protections: Visa and MasterCard extend “zero
liability” policies on debit/prepaid cards, meaning cardholders are often not held liable for unauthorized
charges if they promptly report. Our sponsor bank will usually implement this policy (which is even more
protective than Reg E in some cases). We as program manager must facilitate it (meaning we likely give
provisional credit faster – e.g., Visa requires it within 5 days in many cases). We and the bank will align our
procedures to meet whichever is stricter (network or Reg E). - Fee Fairness and UDAAP: The bank and CFPB
will also watch for any unfair or deceptive fees or practices in our program. For example, certain fees are
restricted: the CARD Act (15 USC 1693l-1) prohibits dormancy or inactivity fees on gift cards unless
conditions are met (no inactivity fee before 12 months of inactivity, etc.) . We ensure any such fees
comply with state and federal law. Many states also forbid expiration of gift card funds (or require at least 5-
year validity) . Our program will conform: e.g., if we issue open-loop gift cards, we’ll not charge any
monthly fee or inactivity fee contrary to law, and funds won’t expire even if the plastic does. The sponsor
bank will insist on that because they do not want a UDAAP violation. Also, the bank will approve our
marketing to ensure it isn’t misleading (e.g., we can’t call a card “free” if there are fees). They likely have a
marketing review checklist (covering things like not misrepresenting FDIC insurance or claim “no fees”
incorrectly) . We’ll run all card-related public material by them.
Network Requirements & Program Manager Roles: - Program Registration: Visa/Mastercard require
issuer banks to register any Third-Party Program Managers and in some cases each prepaid program. Our
sponsor bank will register our parent MSB as a Program Manager (TPA) with the network (which involves a
background check and annual fee). They may also register each card BIN or program name. For instance,
Visa might assign a unique Program ID for each variant we offer (especially if each series brand is distinct).
We provide information for that registration and must comply with network rules. - Compliance with
Network Operating Rules: Program managers are responsible (under contract with the bank) for adhering
to all card network rules applicable to issuers and cards. This touches many areas: - KYC on Cardholders:
Mastercard rules require identifying the card purchaser/loaders above certain thresholds (the CFPB rule
too: anonymous prepaid cards can’t be loaded over $1000 annually or have international use – beyond that,
KYC is required ). We will enforce that: e.g., we may allow an initial small load without full verification
(permissible under $1000 exception), but to reload or hold higher balance, customer must verify identity.
Sponsor banks often mandate full KYC from the start for open-loop cards to be safe. We likely do full KYC at
onboarding for all but perhaps some low-limit gift cards. - Transaction Limits & Velocity Controls:
Networks require certain risk limits (for example, Visa might require that prepaid cards have daily ATM
withdrawal limits). Our bank will set those: e.g., $500 cash withdrawal per day, $2000 spend per day, etc.,
adjustable with risk. For sub-programs, we may customize within allowed ranges, but all must meet
network minimum standards for fraud control. - Anti-Fraud & Chargeback Management: Program
managers handle cardholder dispute intake and evidence gathering, but the bank is on the hook to fund
chargebacks if we lose them. We thus must manage chargeback ratios under network thresholds. If one of
our sub-programs had a high fraud rate (e.g., a gift card product being abused), the network could penalize
the issuer with fines. Our contract with the bank will make us liable for those fines , and the bank will
42
102
103
42
104 15
105
99
monitor our fraud metrics. We have fraud systems in place (transaction scoring, suspicious activity blocking)
to keep fraud and chargebacks low. For instance, if a pattern of fraudulent use emerges on a sub-program,
we act immediately (block those cards, reissue to legitimate customers, etc.) and inform the bank. - PCI DSS
Compliance: Because we (and our agents) might handle sensitive card data (PANs, CVVs), we are required
to comply with PCI Data Security Standards. The sponsor bank will require annual PCI certification or
validation that our card processor covers certain aspects. For example, if all card data storage is at our
processor (which is PCI Level 1 certified) and we only see tokenized data, our scope is limited but still need
good security. The bank’s contract will typically mandate that we maintain PCI compliance and may ask to
see our Attestation of Compliance (AOC) or network certification. If we develop a mobile app dealing with
card numbers, they’ll ensure it doesn’t store full PAN insecurely. This is crucial not just to avoid fines but also
to protect consumers and the program’s reputation. - Sub-Program Managers: If our parent MSB is the
primary Program Manager and we have sub-MSB clients effectively acting as “sub-program managers” (e.g.,
they market the card under their brand and may have some customer service role), the networks and bank
view the primary PM (us) as responsible for those sub-programs. The bank typically will not register each
sub-program manager separately with the network (unless they are significant). Instead, they will list the
sub-brand under our program. However, the bank might require that any sub-program partner undergo
due diligence akin to a program manager – essentially what we do in onboarding them. We then vouch for
them to the bank/network. The bank might insist on approving any such partnership. For instance, if one of
our series wants to launch a co-branded card with a celebrity brand, the bank may check that brand’s
reputation because if that sub-program has issues (say it targets a risky consumer segment), the bank could
object. - Card Design and Materials: Visa/Mastercard have rules on how their logo and issuer name appear
on cards. The sponsor bank’s name typically must appear (often on back), and any “agent” name on the card
must be approved. We coordinate card design approvals through the bank to the network. The network also
mandates certain wording in cardholder materials (e.g., funds FDIC insured if applicable, contact info, etc.) –
our bank ensures we include all that. We already discussed disclosures from a regulatory standpoint;
networks add some (like Visa requires including their Zero Liability notice in materials). - Escheatment
(Unclaimed Property) for Gift Cards: - State Escheat Laws: Unused gift card balances (and possibly
balances on prepaid accounts after a period of inactivity) may be considered unclaimed property. Many
states exempt closed-loop gift cards from escheat if they never expire or charge fees . But some states
(e.g., Delaware historically) tried to claim even open-loop prepaid balances as unclaimed property after a
dormancy period. The rules vary: - Some states: “General purpose reloadable cards do not escheat to the
state” (e.g., Florida and others following the 2016 Uniform Unclaimed Property Act exclude open-loop
cards). - Others require escheat of gift card balances after e.g. 5 years of inactivity, unless exempt as low-
value or no-expiry. - Our Approach: The sponsor bank, as issuer, typically holds the obligation for
unclaimed funds. They often have a group handling escheat compliance. For example, Pathward (a big
prepaid issuer) explicitly informs cardholders about unclaimed property rules and works with state
authorities . - We will track inactivity on accounts. If a prepaid account has had no customer-initiated
activity for the dormancy period (commonly 3 or 5 years) and we cannot reach the customer, we flag it for
escheat. - We coordinate with the sponsor bank: typically, they will be the one to actually remit the funds to
the state of the customer’s last known address (per unclaimed property laws, that’s the priority: last known
address state gets the money; if none, the state of the issuer’s incorporation – often DE – gets it unless
federal law says otherwise). - Many open-loop cards have the issuer in a state with favorable laws (e.g., our
sponsor bank might be in a state that says open-loop card funds are not escheatable). However, a recent
Supreme Court case (Texas v. New Jersey and the newer one Pennsylvania v. Delaware on MoneyGram
checks) may influence how these are treated . Without diving deep, we will simply comply with what the
bank’s legal counsel says: if they instruct to escheat certain dormant balances, we will provide the data. If
some states claim balances and others exempt, the bank’s unclaimed property team will sort it out. - We will
notify cardholders before escheat as required (most states require a due diligence letter to the owner’s last
101
19
73
74
106
100
address a few months before escheating). We can prepare those notices on behalf of the bank or have the
bank send them. Pathward’s example letter to cardholders about potential escheat is a template we can
mimic . It typically says “you have X on your card, contact us to claim or it will be sent to state treasury as
unclaimed property.” - For closed-loop gift cards sold by a business (like a retailer’s gift card), many states
exempt them from escheat if no fees and no expiration (to encourage businesses not to profit off
breakage). But some states (DE in particular) tried to seize “breakage” as unclaimed property. If any series
issues closed-loop gift cards (e.g., a loyalty gift card program for a corporate client), we’ll check each state’s
law. Possibly, we might incorporate those gift cards under the sponsor bank as well if they are network-
branded, in which case it’s open-loop and subject to the above. If purely closed-loop (usable only at a
merchant’s locations), that typically isn’t under banking purview but state consumer laws. However, our
series likely focus on open-loop or general prepaid which are the bank’s domain. - The sponsor bank will
include escheatable balances from our program in their calculations. We have to furnish any records of last
contact with customers to assist. The contract may require us to indemnify the bank for any unclaimed
property claims too (since if we failed to report something and a state penalizes, we cover it).
Summary of Section 4: Operating prepaid/gift card programs means layering additional compliance on
our MSB program, with heavy involvement from the sponsor bank’s side to ensure we meet federal
consumer protection regs and network standards. We have adjusted our procedures accordingly: - We treat
cardholders as if they are bank customers in terms of disclosures and protection. - We abide by Reg E error
resolution timelines and have infrastructure for that (case management systems, customer support
training, etc.). - We subject our program to network rules – we got our program approved by Visa/
Mastercard via the bank, and we implement all required controls (KYC, PCI compliance, fraud monitoring). -
We prepare for escheatment of dormant funds in cooperation with the bank so no state laws are breached.
All these steps not only keep regulators like the CFPB and state AGs satisfied (preventing consumer harm),
but also strengthen the overall safety of our program, which our sponsor bank and its examiners will note
positively. In effect, we run the prepaid program to the same standard a directly issued bank program
would run, fulfilling the sponsor bank’s expectations .
5. Risk Mitigation Strategies for a Conservative MSB Operator
As a conservative operator, we prioritize risk mitigation in every aspect of our bank partnership to ensure
stability and avoid the pitfalls that have caused other MSB-bank relationships to fail. We recognize that
sponsor banks and regulators are closely scrutinizing MSB programs, especially after some high-profile
issues in recent years . Below we outline how we structure our business and partnership to be
“bank-friendly” and resilient, addressing key risk areas:
5.1 Transaction Types and Volumes Suited to Bank Risk Appetite: We deliberately focus on lower-risk
transaction types: - Our payments are predominantly non-cash, account-based transactions (ACH
transfers, electronic card loads, wire transfers) between known parties, rather than cash remittances or
walk-in money orders. Banks find electronic, traceable transactions much easier to monitor and less prone
to certain risks (like structuring or bulk cash smuggling) . We have virtually no cash exposure (and if we
do via an agent, it’s minimal and we ensure immediate banking of those funds). By largely eliminating
physical cash handling, we remove one of the biggest red flags for banks (MSBs that deal heavily in cash are
considered very high risk). - We concentrate on B2B and institutional flows, meaning our customers are
other businesses or regulated financial institutions. This inherently reduces consumer fraud risk and AML
risk compared to serving the general public. Institutional clients tend to have their own compliance layers,
and their transactions often have legitimate business purposes (payroll, vendor payments, etc.). Sponsor
73
17 18
107 91
78
101
banks prefer MSB programs dealing with known business entities rather than unpredictable retail
customers, as it limits scenarios like elder fraud or random structuring attempts by individuals. Even where
our clients ultimately serve consumers (e.g., a client might issue gift cards to consumers), our direct
relationship is with the regulated client and we enforce compliance at that layer. - We avoid high-risk
sectors and corridors unless specifically approved. For instance, we do not facilitate gambling payouts,
marijuana-related payments, or crypto exchange transactions in our standard offering. Those verticals carry
regulatory baggage (and many banks outright prohibit them in partner contracts). By staying in clearly
permissible domains (like conventional e-commerce payments, remittances to well-regulated countries,
etc.), we align with the bank’s comfort zone. If we ever did want to enter a higher-risk area (say a client
dealing in cryptocurrency payouts to customers), we would only do so with the bank’s explicit consent and
with enhanced controls – but as of now, we intentionally steer away from any controversial or extremely
complex business that could jeopardize our bank relationship. We saw how some banks in 2023 pulled
back from crypto and fintech exposures due to regulatory concerns; we therefore choose our client base
and use-cases to be ones a bank can easily defend as low-risk. - We throttle transaction volumes to a
manageable growth curve. Banks get nervous if an MSB’s volume spikes unpredictably (it suggests the risk
profile might be changing or the MSB might be taking on new high-risk clients to drive that growth). We
provide the bank with projections of our expected volume and update them if things change. We prefer a
gradual scale-up – for example, start with a pilot or limited roll-out, let the bank see the patterns and
comfort build, then expand. This “crawl-walk-run” approach was advised by regulators; we follow it by
design. If our volumes begin exceeding projections materially, we proactively discuss with the bank the
reasons (maybe we onboarded a big new institutional client, but we’ll have vetted them and can show the
bank our due diligence on that client). This way, nothing looks out of control. - We implement conservative
limits on transactions initially (aligned with what banks like to see). For instance, even if a state or network
might allow up to $10k per day on a prepaid card, we might set a $5k/day limit unless a user is specially
verified or has a justified need. For B2B payments, we obviously handle larger amounts, but those are
typically few in number and each thoroughly screened (and often via wire with full KYB on both sides). By
imposing sensible caps and velocity limits, we reduce the chance of large suspicious movements. Banks
often ask for these risk parameters; we can show we’ve already instituted them. - We concentrate on
jurisdictions that are lower-risk (e.g., domestic U.S. and established international corridors). If we handle
cross-border, we focus on corridors with robust AML regimes (for example, payments between U.S. and
U.K./EU or Canada). We do not engage in flows involving sanctioned or high-risk countries (e.g., no services
involving Iran, North Korea, Syria, etc., obviously, and also avoid high AML risk regions unless we have a
specific program with strong controls). If a client wanted to serve, say, a West African corridor, we’d
approach extremely carefully and likely need bank’s separate approval after demonstrating enhanced
checks (since banks categorize certain geographies as high risk). Our currently targeted markets are
relatively low-risk (based on FATF evaluations and the bank’s country risk ratings). By aligning our
geographic focus with the bank’s risk appetite, we avoid pushing them into uncomfortable territory.
These measures make our transactional profile “boring” in a good way – predictable, transparent, and
largely involving known-good parties and purposes. Banks often use a phrase “keep it boring” for
compliance, meaning nothing exotic or too innovative that examiners haven’t seen. We heed that advice.
5.2 Structuring Partnerships to Minimize Sponsor Bank Churn: Sponsor bank churn refers to fintechs
having to switch bank partners frequently due to bank risk re-evaluations or account closures (as happened
under past “de-risking” waves). We mitigate this risk by: - Building Redundancy / Multi-Bank Strategy:
While we prefer to concentrate volume with one primary bank for efficiency, we maintain relationships with
at least one other bank as a contingency. MoFo’s tip #2 noted concentration risk in one sponsor is
102
dangerous . We have engaged a secondary sponsor bank for certain services (or kept one in reserve) so
that if our primary bank faced an issue or decided to exit the business, we can relatively smoothly port
operations. This might involve doing initial integration with a backup bank’s API and keeping that up-to-
date (even if dormant). Our contract with the primary bank does not prohibit (or we negotiated out any
clause that would prohibit) us from transitioning to another bank in termination . Specifically, we
ensured we have “portable” arrangements: for example, customer account data and KYC are owned by us
(and can legally be transferred to another regulated institution if needed), card programs can be
transferred by coordinating BIN moves with networks or re-issuance under a new bank. We realize
switching banks is non-trivial (it can take months), so we want to avoid needing to – which is why the rest of
our mitigation focuses on keeping the primary bank happy. But having Plan B (and maybe Plan C for certain
components) is part of prudent risk management. - Negotiating Favorable Contract Terms: As described,
we sought contract clauses that give us adequate notice of termination and assistance in transition .
Our agreement with the bank includes at least a 60- or 90-day notice period for termination without cause,
and explicitly allows us to obtain a successor bank and migrate data during that period. We also avoided
exclusivity that would stop us from talking to another bank (or if there is any exclusivity, it terminates if our
bank relationship is ending) . Essentially, we gave ourselves breathing room to pivot if needed. - Due
Diligence on Sponsor Bank Stability: We thoroughly vetted our sponsor bank’s financial and regulatory
condition before partnering. We chose a bank with strong capital, a history of stable operations, and a
positive (or at least not negative) relationship with regulators. We reviewed their public filings and any news
of consent orders. For example, we avoided banks that were under serious enforcement actions specifically
relating to BaaS oversight. We also considered diversification – if a bank had too heavy an exposure to high-
risk fintech or crypto, that was a risk factor (as seen with some banks that failed or had to cut off clients in
2023). Our sponsor bank is one that regulators have not publicly flagged, and that has communicated a
long-term commitment to the fintech/MSB space. We monitor our bank’s health continuously (tracking their
quarterly financial reports, capital ratios, and any industry chatter about them). If we saw trouble (e.g., a
trend of losses or rumors of a sale or regulatory pressure), we would quietly prepare to shift if needed. This
ongoing vendor risk management on our side ensures we aren’t caught off-guard by a bank failure or exit.
In essence, we also perform “Know Your Bank” due diligence: for instance, ensuring our bank is well-
capitalized (we check their Tier 1 Leverage and it’s well above required ), profitable, and not overly
dependent on volatile funding. - Proactive Compliance (“No Surprises” Rule): As stressed, we strive to
identify and address compliance issues internally before the bank or regulators do, and to immediately
notify the bank of any significant developments. For example, if we discover an agent misconduct and
terminate that agent, we inform the bank the same day with an explanation and our corrective action. If we
anticipate a regulatory change affecting our program (say a new state law requiring something), we tell the
bank our plan to comply. This proactive communication builds trust and credibility. Banks have cut off MSB
clients in the past mostly when blindsided by problems or if the client appeared inept at compliance. By
being transparent and always one step ahead on fixing issues, we give the bank comfort that risks are
under control. - Exemplary Audit and Exam Performance: We aim for clean audits and exams. If our
sponsor bank sees that every audit finds only minor issues and we resolve them, and if any external
examinations (like a state exam of us or a joint exam) find us in compliance, the bank’s confidence grows.
On the flip side, if we had a poor exam (say a state cited us for major deficiencies), the bank might rethink
the relationship (to avoid regulatory guilt by association). Thus, we devote resources to compliance far
above the minimum. We treat every audit as if our business depended on it (because it does). This means
investing in staff, training, and systems to ensure we meet or exceed regulatory expectations. A
conservative operator spends more on compliance as a percentage of revenue than an aggressive growth
one – we accept that trade-off. It’s cheaper than losing the banking. - Maintaining Strong Financial
Position: Banks also consider the financial health of MSB clients (as noted, they often ask for financials). An
MSB that is struggling financially might be tempted to take on sketchy business to make money – banks
27
25
25
26
29
103
know this pattern. So we keep a solid balance sheet (our licensing net worth minimums are met
comfortably, we keep a cushion of capital above that). We inform the bank of any major changes (e.g., if we
raise new equity capital or if we are burning cash faster than expected – though we’d spin that as investing
in compliance). By showing we’re financially stable, the bank is less worried about, say, us going bankrupt
and leaving a mess of outstanding payment obligations or abandonware systems. It also indicates we can
invest in compliance tech and staff as needed (banks hate under-resourced compliance). - Avoiding Single
Points of Failure: Within our own operations, we mitigate operational risks that could spook the bank. For
example, we have continuity plans (if our server goes down, we have backups; if our compliance officer
leaves unexpectedly, we have a deputy trained; if an agent goes rogue, we can re-route customers to
another agent or handle directly). We share with the bank our Business Continuity Plan and disaster
recovery tests. Seeing that we can handle shocks without chaos will assure them that our program won’t
suddenly implode and cause them trouble. - Responsive to Industry Changes: If regulators or the industry
shift expectations (e.g., new FinCEN advisories, new state rules on crypto, etc.), we adapt quickly and let the
bank know we updated our program accordingly. For example, Treasury issued a “De-Risking Strategy” in
2023 calling for banks to adopt a case-by-case approach rather than wholesale cutting MSBs . We
can cite that strategy in discussions, emphasizing we are exactly the type of well-controlled MSB the
regulators say should have access. If our bank’s examiners are pressuring them about fintech partnerships,
we provide whatever they need (reports, independent audit letters, etc.) to ease examiner concerns.
Essentially, we help our bank defend keeping us. Acting as an open book (even inviting the bank’s
compliance folks to sit in on our internal compliance meetings occasionally) can demonstrate our
commitment.
5.3 Due Diligence on Sponsor Bank Stability: (Already discussed above in multi-bank strategy and K-Y-Bank,
will integrate succinctly):
We thoroughly vet and continuously monitor our sponsor bank’s stability and compliance posture. We
review their Call Reports and Uniform Bank Performance Reports each quarter. We look at capital ratios,
asset quality metrics, any concentration of deposits or loans that might signal vulnerability. For example, if
we saw our bank’s proportion of uninsured deposits rising alarmingly or heavy losses in a certain portfolio,
that’d be a red flag. We keep an eye on any news or regulatory actions involving them. If a consent order
appears (like how OCC penalized one bank for fintech oversight ), we evaluate how that might affect us.
This ongoing K-Y-B (Know Your Bank) ensures we’re not blindsided by a bank failure or them abruptly
dropping fintech clients to appease regulators (as happened with some banks in 2023).
Additionally, we maintain a close relationship with bank management – regular meetings not just with
compliance but with relationship managers or executives. If the bank were considering an exit from our
sector, we hope to catch wind early via those relationships. We also diversify the personal connections: not
relying only on one champion at the bank, but ensuring multiple officials know us and value the
partnership. That way, if one person leaves or if new management comes, we have established credibility
across the bank (this can mitigate the risk of a leadership change leading to account termination, which
MoFo’s tips allude to in discussing sponsor bank financial conditions and rights to transition ).
5.4 Red Flags and How We Avoid Them: We’ve essentially built our program to avoid the typical “red flags”
that cause banks to terminate MSB accounts: - Regulatory Non-Compliance or Enforcement Against
MSB: We diligently prevent and, if needed, promptly remedy any compliance slip. No unregistered activity,
no lapsed licenses, no examination findings left unaddressed. Thus the bank should never receive an
unpleasant call from a regulator about us. - Negative Media or AML Scandals: We avoid business that
108 109
28
29
104
could drag us into scandal. E.g., we do not handle digital currency flows that could end up in headlines
about money laundering. We do not have agents in high-corruption countries that might be infiltrated by
criminals. By staying low-risk, we reduce chances of a major incident. And if something small occurs (like an
agent employee stole money), we deal with it swiftly and transparently such that it doesn’t become a public
issue. - High Fraud or SAR Rates: If our program started generating disproportionately high SAR filings or
fraud reports relative to volume, that alarms banks (it indicates poor onboarding or weak controls letting
bad actors in). We mitigate this by thorough upfront due diligence (only taking on reasonably safe clients
and ensuring they do KYC on their users if applicable) and by aggressive fraud monitoring. Our SAR rate
stays moderate and aligned with expected patterns (we probably file SARs mostly for isolated incidents, not
systemic issues). The bank sees through our SAR reporting that we’re catching what needs catching. If we
had a spike (maybe due to a new fraud trend), we would immediately impose additional controls and show
the bank we responded (thus turning a red flag into an example of effective risk management). - Scope
Creep without Notice: Some fintechs get in trouble by expanding into new product lines or markets
without telling the bank (suddenly the bank finds out the client started doing crypto or servicing sanctioned
regions). We absolutely avoid that. We discuss any new significant business line with the bank beforehand,
get their sign-off, and document compliance measures. Thus, no surprise to trigger the bank’s “I didn’t sign
up for this” reflex. - Poor Communication or Cooperation: If an MSB is slow to answer bank inquiries or
argues on every audit finding, the bank may conclude the partnership risk outweighs reward. We do the
opposite: respond same-day to questions, proactively send updates, and demonstrate a collaborative
attitude. For example, if the bank’s audit says “improve agent training frequency,” we don’t dispute it – we
say “Understood, we will implement semiannual training instead of annual and send you the new schedule”.
This kind of responsiveness signals that we are a partner that makes the bank’s job easier, not harder . -
Bank’s Own Risk or Strategic Changes: If the bank itself hits trouble (financially or regulatorily), even a
great MSB partner can be dropped as collateral damage. While we can’t control the bank’s fate, our due
diligence reduces this risk (as we chose a stable bank). But if it happens, our backup plans kick in (as
discussed with multiple bank strategy). We also included a contract clause (as MoFo suggested) that if the
bank’s condition deteriorates (e.g., falls below adequately capitalized), we can more rapidly transition .
That protects us somewhat from being stuck if regulators put constraints on the bank.
In sum, our risk mitigation strategy can be described as “exceed expectations and plan for
contingencies.” We run a compliance-forward operation that not only meets current requirements but
anticipates what regulators and banks might want in the future (e.g., adopting new FinCEN guidelines
quickly). We treat the sponsor bank as a true partner – keeping them informed, seeking their advice, and
addressing their concerns promptly – rather than as an adversary imposing limits. This fosters a
relationship of mutual confidence.
By doing all of the above, we greatly minimize the chances the bank will feel the need to exit the
relationship. We want to be, from the bank’s perspective, a model MSB client – one that regulators have
little to no criticism of (so the bank gets kudos for managing us well), one that generates stable fee
income with manageable risk, and one that is low-drama. If we achieve that, the bank has every incentive to
continue the partnership long-term, which is exactly our goal for stable operations. As MoFo noted,
regulators are pushing banks to not indiscriminately “de-risk” but rather manage risks ; we make it easy
for the bank to manage our risk, thereby aligning with that regulatory push and helping ensure our access
to banking remains uninterrupted.
95
29
110
105
6. International and Institutional Client Considerations
Our business model includes serving international clients and institutional/regulatorily governed
entities (such as foreign businesses or fintechs seeking U.S. payment access). Such clients introduce
additional considerations in the sponsor bank partnership. We address special requirements for foreign
MSB clients, differences in how banks treat institutional vs. retail-focused programs, and cross-border
payment risk management, ensuring our structure meets expectations.
6.1 Special Requirements for Foreign MSB/Fintech Clients:
If our sub-MSB client is a foreign company (e.g., a non-U.S. fintech using our platform to process U.S.
payments), both FinCEN and our sponsor bank impose extra due diligence: - FinCEN, via FIN-2012-A001,
made clear that a foreign MSB doing substantial business in the U.S. must register with FinCEN and appoint
a U.S. agent . In our setup, that foreign entity is our agent, so it is covered under our registration
(thus satisfying FinCEN’s requirement). However, we still must treat that foreign agent as high-risk in our
AML program. We conduct extensive KYB on the foreign company: verifying its ownership (and screening
the owners, who may be foreign nationals or companies), obtaining information on its regulatory status in
its home country (does it hold a license there? if it’s a foreign MSB itself, is it in good standing?), and
understanding its AML controls. Essentially, we perform an “enhanced due diligence” review just like a bank
would on a foreign correspondent or foreign MSB customer . We likely request and review their AML
policies, maybe even visit their office if needed to ensure they have a compliance culture. - The sponsor
bank will likely require approval of each foreign agent. Many U.S. banks have restrictions on providing
services indirectly to foreign MSBs due to high regulatory scrutiny (this is akin to “nested correspondent
banking” risk). We mitigate this by fully disclosing the nature of the foreign client and providing the bank
with our due diligence packet on them. We might even arrange a joint call with the foreign client’s
compliance officer and our bank’s team, so the bank can ask questions and get comfortable. This
transparency can alleviate the bank’s concern that something is hidden. - U.S. Agent for Service: FinCEN
requires foreign MSBs to have a U.S. legal agent for service of process . In our case, since the foreign
entity is our agent, we (the U.S. parent) effectively serve as that contact point. We maintain documentation
(e.g., a power of attorney or contract clause) where the foreign agent designates us to accept any legal
papers on their behalf related to U.S. transactions. We informed FinCEN of this arrangement via our agent
list. This way, if any U.S. law enforcement had an issue with the foreign agent’s transactions, they can come
to us (and we then relay to the foreign company and handle it). The sponsor bank will also want that
assurance – they do not want to chase a foreign company through foreign courts if something goes awry;
they rely on our U.S. entity to take responsibility. We explicitly assume liability for our foreign agents
contractually, which we have done. - OFAC and Sanctions: Foreign clients sometimes have owners or
customers from multiple countries. We thoroughly screen our foreign sub-MSB’s owners, key principals, and
any known downstream clients against OFAC sanctions lists and other watchlists. Our sponsor bank will do
the same. If a foreign agent had any ownership tied to a sanctioned country or individual, we wouldn’t
onboard them. For instance, if a potential foreign client was partly owned by an entity in a high-risk
sanctioned jurisdiction (Crimea, Iran, etc.), we’d decline or require that ownership be divested. We also
ensure the foreign agent’s customer base does not include sanctioned parties – typically by requiring they
do OFAC screening on their end users and share results with us. The bank will likely ask us to certify that no
transactions with sanctioned countries/persons will occur. Given our B2B focus, that’s manageable (our
foreign clients are usually regulated in their countries and also avoid sanctioned markets). - Foreign AML
Standards: We verify that the foreign agent is subject to and compliant with AML laws in their home
country. E.g., if our agent is a U.K. fintech (subject to FCA regulations), we obtain evidence of their
registration with U.K. authorities and maybe a letter from their auditor or legal counsel attesting to their
53 31
6 7
31
106
AML program. This gives our sponsor bank confidence that the foreign entity is not a rogue outfit. -
Information Sharing (314(b)): We encourage our foreign client to participate in their local equivalent of
314(b) if available (or at least to share needed info with us despite privacy laws – we incorporate contract
clauses that allow information sharing for compliance). Some foreign data privacy laws could complicate
sharing end-user info with a U.S. bank. We navigate this by obtaining customer consent via terms (e.g., our
foreign client’s user terms state that data can be shared with our U.S. banking partner for compliance
purposes). Our sponsor bank will want assurance that they can get any necessary info on transactions
involving the foreign agent’s customers if needed (for SAR, subpoenas, etc.). We structure agreements to
permit that, overcoming GDPR or other privacy restrictions by framing it as fulfilling legal obligations (which
is usually an exemption under privacy laws). This is important – if the bank felt that foreign data laws block
them from seeing details, they might consider the risk too high. We preempt that by having robust data-
sharing consent in place. - Foreign Exchange and Cross-Border Flow Controls: If our program involves
currency conversion or cross-border remittances, we implement clear controls. For example, if a foreign
agent collects funds in Euros and we settle in USD, we either route through a known correspondent or use
our sponsor bank’s FX services (some sponsor banks offer multi-currency accounts for fintechs like ours).
We also abide by FinCEN’s Travel Rule for international transfers: ensure originator and beneficiary info
travels with the wire if above $3k. Our systems capture all required details (name, address, account, etc.)
and our bank’s wire department includes them in international wire messages . Many foreign agents
might use our system to send cross-border; we ensure compliance with both U.S. rules and the foreign
country’s rules (for instance, EU has similar travel rule for crypto and wire, etc.). The sponsor bank will
scrutinize our cross-border procedures in its initial due diligence, and we will show them that we collect all
necessary info and screen every cross-border transfer’s details for sanctions. - Institutional vs. Retail-
facing Program Approach: Sponsor banks generally find institutional (B2B) programs more palatable than
direct retail ones. Because our primary clients are institutions (albeit some are fintechs with retail end-
users), the bank views our immediate customer as an entity they can risk-rate (we provide corporate KYC
docs, financials, etc. for each). This is easier for them than an MSB with tens of thousands of individual
customers where the bank sees only aggregates. That said, since our clients may have many end-users, the
bank still expects we and our client maintain rigorous KYC on those end-users. We’ve contracted that as part
of our agent onboarding: e.g., our foreign agent must apply equivalent KYC standards on their customers
as we would under U.S. rules (if not stricter local rules). We effectively extend our compliance program into
the foreign agent’s customer base via contractual requirements and tech integration. - The bank therefore
treats our program as closer to a nested correspondent banking arrangement: They know us (the U.S.
MSB) and we know the foreign end-users via our agent. Regulators often require that banks managing such
relationships ensure the intermediary (us) has an effective AML program. We demonstrate that by showing
them our audits of the foreign agent’s KYC files, etc. This comfort is key to avoid the dreaded scenario of
regulators telling the bank to drop foreign MSB clients. Actually, the U.S. Treasury’s 2023 anti de-risking
strategy encourages banks to not blanket drop foreign MSBs but to assess each . By providing
thorough information, we help our bank satisfy that recommendation and keep the relationship.
6.2 Sponsor Bank Treatment of Institutional vs Retail-Facing Programs: - Regulatory Scrutiny
Differences: Banks know that retail-focused fintech programs (especially those open to the general public)
tend to have higher fraud rates, more consumer complaints, and more BSA alerts simply due to volume and
diversity of users. Institutional programs (where clients are vetted businesses) often have fewer of those
issues. We emphasize to our sponsor bank that our clientele are vetted businesses and regulated entities,
meaning they themselves are subject to compliance obligations (if a client is a foreign bank or EMI, it has its
own regulator ensuring AML compliance). This layered oversight (their regulator + our oversight + our
bank’s oversight) provides multiple lines of defense. The bank takes comfort in that versus a program
11
109
107
serving, say, any U.S. consumer who downloads an app – which would rely solely on our controls. - Volume
and Transaction Characteristics: Institutional payments often are larger in value but lower in count, and
often predictable (e.g., monthly payroll runs, vendor payments in certain cycles). This consistency is easier
for banks to monitor and model. By contrast, a retail program might have thousands of small unpredictable
transactions daily (which can still be monitored but require big data analytics). Our program leans more
toward moderate volume, higher-value flows in patterns the bank can easily incorporate into monitoring
scenarios (like “client X does payroll on 1st of month” – any deviation stands out). - Cross-Border
Institutional Clients: When our client is itself a regulated institution (like a foreign MSB or fintech), our
sponsor bank might treat it almost like a correspondent banking relationship. They might require an annual
certification from that client (similar to a Wolfsberg Questionnaire used in bank-to-bank correspondents) or
rely on our continuous monitoring. We’re prepared to facilitate that. For instance, if our sponsor bank
wanted to send a compliance questionnaire to each foreign agent, we’d coordinate to get those filled. Or we
proactively collect such info and provide it. - Regulatory Liaison: For institutional clients, sometimes
regulators (like the client’s home regulator or U.S. state regulators) might ask questions. We act as a liaison.
For example, if our foreign client’s home regulator wanted to know how they handle U.S. transactions, we
supply necessary info (with sponsor bank aware). Or if a U.S. state examiner during our exam asks about a
specific foreign agent’s program, we coordinate a three-way discussion with the foreign client to give the
examiner clarity. Being in the middle, we ensure both our bank and the relevant regulators are kept in the
loop so no one feels circumvented. - Expectations Given Our Structure: Our sponsor bank expects that
given our series structure, we will: - Maintain stringent centralized control (as we do) – they expect us, not the
sub-entities, to be the ones to interface with them and to have full knowledge of every sub’s activity. We’ve
shown them this by providing unified reports and being able to answer any question about any sub’s
transactions. - Only operate in jurisdictions clearly permissible – they anticipate we won’t push into a gray area.
For instance, if a prospective client is in a country under heavy U.S. sanctions or is of unclear legal status,
the bank expects us to avoid or thoroughly vet that. We indeed have turned down potential foreign
partners that didn’t meet our stringent criteria (and we inform the bank of such decisions to illustrate our
risk discipline). - Be responsive to international compliance developments – e.g., FATF updates, EU AML
directives, etc., that could affect our foreign agents. We monitor those. If FATF put a certain country on the
blacklist, we’d immediately reevaluate any agent or client ties to that country and likely suspend related
activities (then inform the bank). This proactive stance ensures the bank isn’t put in a position of
questioning us after the fact; we’ll have already acted.
6.3 Cross-Border Payment Considerations: - Use of Correspondent Banks: Cross-border payments in our
program will ultimately clear through correspondent banking channels. Our sponsor bank may or may not
have direct presence in a given foreign country. Often, our U.S. bank will rely on a correspondent bank
abroad to deliver funds (e.g., SWIFT transfers). We make sure all such correspondents involved are
reputable and not under sanctions themselves. If our program sends a lot of wires to Country X, our bank
might ask: “Do we (the bank) have a good correspondent in Country X and are those transactions
transparent enough?” We ensure all wire instructions include complete information so correspondent AML
filters pass them without issue (the Travel Rule compliance we discussed). If any foreign bank down the
chain raises a concern (maybe they ask for additional info on a beneficiary), we handle promptly. This
prevents building risk like correspondent account closures. In summary, we treat the cross-border leg with
the same rigor as domestic legs, providing the bank assurance that cross-border doesn’t equal loss of
visibility. - Currency Exchange Risks: If currency conversion is needed (say a foreign client collects funds in
USD and needs to pay out in local currency), we handle this via regulated pathways. Possibly, our sponsor
bank can do FX conversion and remittance via its own channels (some sponsor banks have foreign
exchange desks). If not, we only use licensed FX providers (and tell the bank who they are). We do not use
108
informal or unlicensed channels. The bank might need to approve any third-party processor or partner we
use for foreign payouts. We have that conversation early and incorporate it in our AML program (due
diligence on that partner, OFAC screening at conversion, etc.). - Institutional Client Onboarding &
Stability: When adding a new institutional client (especially foreign), we walk the sponsor bank through our
due diligence and risk analysis for that client. We might even invite the bank to join our call with the client’s
compliance team (with the client’s permission) so the bank can directly ask questions. This level of openness
often impresses banks and mitigates their concern of unknown risk. It also sets a tone with the foreign
client that our bank partner is actively overseeing – which encourages the foreign client to maintain high
standards (they know two sets of eyes are on them). - Ongoing Monitoring of Institutional Clients: We
treat our institutional clients themselves like high-risk customers (because many are MSBs). That means we
conduct periodic reviews of them – e.g., every year we refresh their KYC info, ask for updated financial
statements, inquire about any regulatory changes or negative news. We then share a summary of those
annual reviews with our sponsor bank. E.g., “We performed an annual review of [Foreign Fintech Ltd.],
confirming they remain licensed in their country, had no regulatory penalties this year, their transaction
volumes matched expected ranges, and their AML audit report (attached) showed no material deficiencies.”
Providing such reports preempts the bank asking. It demonstrates we are continuously vetting our sub-
MSBs, not just at onboarding. This aligns with the expectation that banks do periodic reviews of high-risk
customers (we are doing it for them at the granular level, and giving them the high-level results).
By addressing these international and institutional considerations thoroughly, we reassure our sponsor
bank that even the complexities of foreign agents and cross-border flows are well-controlled under our
program. We essentially function as a “mini-bank” for those foreign partners, implementing all the
necessary controls that the sponsor bank would require if it banked them directly. This approach converts
what would normally be a highly risky indirect relationship (U.S. bank -> foreign MSB) into a manageable
one (U.S. bank -> U.S. MSB (us) strong program -> foreign MSB under our program). In effect, we absorb
much of the risk at our level and present the U.S. bank with a relatively clean interface. As a result, the bank
can extend services to our international clients with confidence, knowing we have one foot in each side –
understanding U.S. compliance expectations and our foreign clients’ context – and bridging the gap
effectively.
Recommended Partnership Structure for Our Model: In conclusion, after extensive research and aligning
with regulatory guidance, the optimal partnership structure for our business is a hybrid sponsor bank
program manager arrangement where: - The parent series LLC (master MSB) is the sole contracting
party with the sponsor bank, registered and licensed as required, and takes full responsibility for BSA/
AML compliance across all sub-units. - Each client series operates under the parent’s license as an
authorized delegate/agent, with no independent FinCEN registration or state license needed (except
those covered by the parent), and no further sub-delegation beyond them. - The sponsor bank treats the
parent MSB as its customer, but via the BaaS model provides segregated accounts or sub-accounts for each
series (for fund flows tracking) and BIN sponsorship for any card programs. The bank thereby has visibility
into aggregate flows per sub-unit without having to onboard each as a separate customer. - A
comprehensive services agreement is in place where the bank delegates front-end compliance tasks to
the parent MSB (and by extension to agents under the parent’s program) but retains ultimate control and
audit rights. The agreement includes clear provisions for agent oversight, data sharing, and termination
assistance (as described in Section 1.5). - The parent MSB operates a unified compliance program that
covers all series agents and their end-users, meeting FinCEN, state, and network requirements. This
program is reviewed and approved by the sponsor bank during onboarding, and updated in consultation
109
with the bank for any new products or risk changes. - Regular oversight meetings are held (e.g., quarterly
business risk reviews) between the bank and our MSB’s compliance management to review performance,
discuss any emerging risks, and plan for growth in a controlled manner. This keeps the partnership aligned
and allows adjustments proactively. - The parent MSB maintains robust agent management: thorough due
diligence at onboarding, ongoing transaction and compliance monitoring, and the ability to terminate or
discipline agents swiftly if needed – all actions reported to the bank. This creates a “compliance cascade”
from bank to parent to agents that regulators find acceptable . - The structure leverages multi-layer
communication: e.g., if the bank’s examiner has a question about an end-user transaction at an agent, the
bank asks us, we get details from the agent instantly and relay it. This responsiveness shows the structure
works – no information dead-ends. - A secondary sponsor bank is identified for contingency, and data
portability arrangements are in place (without breaching any exclusivity clauses) so that if the primary bank
exits the business or faces issues, the program can migrate with minimal disruption. (In practice, we keep
the secondary relationship warm by perhaps using them for a small subset of flows or at least conducting
periodic tests of data transfer, etc.) - All parties – our MSB, the sponsor bank, sub-agents, and even
regulators as needed – maintain open lines of communication, facilitated by our MSB. We essentially act
as the central hub to ensure everyone has the information they need. This transparency is the cornerstone
of a well-regarded partnership.
By implementing this structure, we address the key concerns identified in our research: - We satisfy
FinCEN’s and states’ requirements on MSB agent arrangements through licensing, registration, and
program control . - We meet sponsor banks’ expectations by taking on compliance heavy-lifting
while keeping them in the loop at all times . - We mitigate risk to an acceptable level such that the
bank can comfortably support our business without fear of examiner criticism or unexpected losses. In fact,
our goal is to make the partnership a positive example (so much so that if a regulator asked our sponsor
bank about MSB partnerships, they could point to us as a model case).
In summary, the recommended partnership model is one of close integration and oversight: the bank
provides the regulated infrastructure (accounts, payment network access) and top-level supervision, while
our MSB operates within that framework, extending the bank’s compliance culture through our agents to
the end-users. This structure leverages the strengths of each party – the bank’s stability and regulatory
standing, and our agility and focused expertise in the MSB sector – to deliver services in a compliant,
efficient manner.
By adhering to this model, we position our company for sustainable operation with minimal regulatory
friction, fulfilling our business objectives (serving international and institutional clients with U.S. payment
services) while maintaining the trust and support of our banking partner and regulators. The extensive
research and measures detailed in this memo will serve as our roadmap to execute this partnership
successfully, ensuring we continue to operate securely and profitably in the complex MSB-bank ecosystem
for the long term.
omni
https://www.omniwire.com/news/bin-sponsors-processors-and-compliance
GUIDANCE TO MONEY SERVICES BUSINESSES
ON OBTAINING AND MAINTAINING BANKING SERVICES | FinCEN.gov
https://www.fincen.gov/resources/statutes-regulations/guidance/guidance-money-services-businesses-obtaining-and
58
10 58
2 8
1 2 8 9 43 44 71 72 87 88 105
3 4 5 10 14 32 33 40 54 55 56 58 61 84 89 90 97
110
Banking as a Service: A Comprehensive Risk Management Framework for Banks, MSBs,
and Crypto Firms - Bates Group
https://www.batesgroup.com/news/baas-risk-management-strategies
FinCEN Advisory – FIN-2012-A001 | FinCEN.gov
https://www.fincen.gov/resources/advisories/fincen-advisory-fin-2012-a001
Microsoft Word - Part 4 Managing BSA Relationships BSA Grad School 2018 FINAL
https://indiana.bank/sites/default/files/events_files/
Part%204%20Managing%20BSA%20Relationships%20BSA%20Grad%20School%202018%20FINAL.pdf
Money Services Business (MSBs) and Money Transmitters | Fintech | Lithic
https://www.lithic.com/blog/money-services-business
The Essential Guide to Payment Card Program Management
https://www.galileo-ft.com/blog/the-essential-guide-to-payment-card-program-management/
Summary Gift Cards and Gift Certificates Statutes and Legislation
https://www.ncsl.org/financial-services/gift-cards-and-gift-certificates-statutes-and-legislation
[PDF] Unclaimed Property Frequently Asked Questions – FAQ | Pathward
https://www.pathward.com/content/dam/pathward/us/en/documents/pdfs/Unclaimed-Property-FAQ.pdf
10 Tips for Fintechs in Navigating Sponsor Bank Relationships through
this Banking Crisis
https://www.mofo.com/resources/insights/230316-navigating-sponsor-bank-relationships
Regulators’ Consent Orders Signal Increased Focus on Bank-Fintech
Partnerships
https://www.neach.org/Solutions/Trends-Research/regulators-consent-orders-signal-increased-focus-on-bank-fintech-
partnerships
Leveraging Puerto Rico's IFE and Multistate MSB: A Hybrid Model for Optimized Financial
Operations in 2025 - Premier Banking Consultancy
https://banklicense.pro/leveraging-puerto-ricos-ife-and-multistate-msb-a-hybrid-model-for-optimized-financial-operations-
in-2025/
MSB Friendly Banks - Faisal Khan
https://faisalkhan.com/solutions/banking/msb-friendly-banks/
Essentials of AML Compliance For Banking as a Service (BaaS ...
https://amlwatcher.com/blog/essentials-of-aml-compliance-for-banking-as-a-service-baas-model/
Mastering Compliance for BaaS Companies and Their Affiliates
https://www.sedric.ai/blog/mastering-compliance-for-baas-companies-and-their-affiliates-a-growth-driven-approach
Alloy provides new tool to improve the audit process for sponsor banks
https://www.alloy.com/blog/embedded-finance-sponsor-bank-audit
31 CFR Part 1022 -- Rules for Money Services Businesses - eCFR
https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X/part-1022
Whether an Authorized Agent for the Receipt of Utility Payments is a Money Transmitter |
FinCEN.gov
https://www.fincen.gov/resources/statutes-regulations/administrative-rulings/whether-authorized-agent-receipt-utility
6 7 23 24 78
11 13 30 31 52 53 59 60 63 98
12 41
15 16 35 36 37 67 86 104
17 18 75 76
19 77
20 21 73
22 25 26 27 29 42 49 95 96 99
28 47 50 51 79 82 83 91 107 110
34 66 92 93
38 39 85
45
46
48
57 62
64 65 68 100
111
Whether a Company that Provides Online Real-Time Deposit, Settlement, and Payment Services for
Banks, Businesses and Consumers is a Money Transmitter rather | FinCEN.gov
https://www.fincen.gov/resources/statutes-regulations/administrative-rulings/whether-company-provides-online-real-time
U.S. Supreme Court Re-routes Escheatment of Payment Products
https://www.jdsupra.com/legalnews/u-s-supreme-court-re-routes-escheatment-6138964/
Department of Treasury Issues Strategy on De-Risking
https://www.moneylaunderingnews.com/2023/05/department-of-treasury-issues-strategy-on-de-risking/
Faisal Khan's Post - LinkedIn
https://www.linkedin.com/posts/faisalkhan99_msbfriendlybanks-banking-msb-activity-7183215253579587584-E0xi
[PDF] What's the Deal with Gift Cards Today?
https://www.venable.com/-/media/files/events/2012/05/sweepstakes-promotions-and-marketing-laws-comprehe/files/whats-the-
deal-with-gift-cards-today-presentation/fileattachment/nyc_bar_gift_card_presentation.pdf
Prepaid Card Programs that Disburse State Funds Must Comply with ...
https://www.paymentsjournal.com/prepaid-card-programs-that-disburse-state-funds-must-comply-with-state-escheatment-laws/
FACT SHEET: Treasury Department Announces 2023 De-Risking ...
https://home.treasury.gov/news/press-releases/jy1439
Treasury calls for response to de-risking - ICBA.org
https://www.icba.org/w/treasury-calls-for-response-to-de-risking
69 70
74 106
80 81
94
101 103
102
108
109
112
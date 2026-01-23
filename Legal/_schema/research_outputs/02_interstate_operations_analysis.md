Operational Legality for a Montana-Based MSB
Context: A money services business (MSB) based in Montana faces unique compliance challenges. Montana
is the only U.S. state that does not require a state money transmitter license . However, once a Montana
MSB serves customers beyond Montana’s borders, it must navigate federal MSB regulations and other
states’ money transmitter laws. Below, we break down the legal considerations into federal requirements,
Montana-specific rules, and triggers for other states’ licensing. We then provide a detailed Answer Table
mapping various activity patterns to their likely legal characterization, federal obligations, and state
licensing triggers (with key sources). We also examine relationship models (bank partnerships vs. non-
bank operations and third-party processors), practical compliance controls, and include a download pack
of key laws/guidance. Finally, we list questions to ask legal counsel or regulators for fact-specific
guidance.
Federal MSB Requirements (FinCEN/BSA)
At the federal level, MSBs (including money transmitters) are regulated under the Bank Secrecy Act (BSA) by
the Financial Crimes Enforcement Network (FinCEN). FinCEN Definition: A “money transmitter” is any person
that accepts currency, funds, or value from one person and transmits it to another person or location
by any means . This broad definition covers traditional remittances and also digital or crypto value
transfers (FinCEN treats “convertible virtual currency” as “other value that substitutes for currency” for BSA
purposes ).
Federal MSB Registration & Program: A Montana MSB that engages in money transmission must register
with FinCEN as an MSB (via FinCEN Form 107) within 180 days of starting operations . It must
implement an Anti-Money Laundering (AML) program (including written policies, a compliance officer,
training, and independent review) , conduct know-your-customer (KYC) due diligence, file Suspicious
Activity Reports (SARs) for suspect transactions (≥ $2,000) , file Currency Transaction Reports (CTRs)
for cash transactions > $10,000 , and comply with the “Travel Rule” recordkeeping for transfers ≥
$3,000 . These obligations apply regardless of client location (in-state, out-of-state, or international). If
the MSB transmits funds out of the country, additional rules kick in, such as the CFPB’s Remittance
Transfer Rule (for consumer remittances >100 transfers/year, requiring pre-send disclosures and error
resolution). The MSB must also comply with OFAC sanctions screening for international transactions.
Federal Enforcement: Operating without complying can lead to severe penalties. 18 U.S.C. § 1960 makes it
a federal crime to operate an unlicensed money transmitting business – defined as one operating without
a required state license or without registering with FinCEN . In other words, if a Montana MSB
transmits funds involving another state where a license is required, failing to obtain that state license (or
failing to register federally) can violate federal law . Thus, even though Montana itself imposes no
license, a Montana MSB must be mindful of other states’ laws to avoid running afoul of §1960.
Agent of an MSB: FinCEN does provide one notable exception – an entity acting solely as an agent of
another MSB (e.g. a sub-agent or delegate) doesn’t have to register independently . The principal MSB
covers the regulatory responsibilities (the agent still must follow the principal’s BSA program). This becomes
1
2
2
3
4
4
5
6
7
7
8
1
relevant if our Montana MSB chooses to operate as an agent of a larger licensed MSB in other states, or if
it appoints its own agents (discussed later under relationship models).
Payment Processor vs Money Transmitter: FinCEN also recognizes a limited exemption for payment
processors. If the MSB’s activity is solely processing payments for goods/services on behalf of merchants –
and it meets four strict criteria – FinCEN may not classify it as a money transmitter . These criteria are:
(1) the service is for payment of goods or services (other than money transfer itself), (2) all payments flow
through regulated banks or similar clearing systems, (3) there is a formal agreement with the merchant (or
creditor) receiving the funds, and (4) the processor is working directly for the merchant (the payee) . In
short, if our Montana company only facilitates payments as an agent of the payee (merchant) through
bank networks, it might avoid MSB status federally (see Agent-of-Payee discussion below). However, FinCEN
has no general “agent-of-payee” exemption by name – it relies on this payment processor carve-out .
Thus, the federal MSB obligations apply broadly unless the business model squarely falls into an exempt
category.
Montana-Specific Rules (State Level)
Montana is unique in that it does not regulate or license money transmitters at the state level . A
company engaging only in “money transmission” (which Montana law doesn’t even define) does not need a
Montana license . This means a Montana-based MSB can legally operate intrastate (serving Montana
customers) without a state money transmitter license. However, Montana’s lack of licensing does NOT
shield the company from other states’ requirements or federal law. The Montana Division of Banking
explicitly warns that just because Montana doesn’t license MSBs, your company may still need licenses
elsewhere if you do more than pure in-state money transmission .
Additionally, Montana does license certain related activities. Notably, escrow companies are licensed in
Montana . If the MSB’s model involves holding customer funds in a manner resembling an escrow (e.g.
holding payments on behalf of parties until conditions are met), it might inadvertently trigger Montana’s
escrow licensing requirement. Montana also licenses consumer lenders, debt collectors, mortgage finance
companies, etc. – which may be outside our MSB’s scope, but worth noting if the business diversifies.
Crypto Consideration: Montana’s non-regulation covers money transmission generally, and Montana has
no special crypto-specific license (unlike New York’s “BitLicense”). Crypto exchanges or transmitters in
Montana benefit from the no-license environment, but must still follow federal MSB rules (FinCEN in 2013
confirmed that administrators or exchangers of convertible virtual currency are MSBs under federal law)
. And if serving customers in states that regulate crypto transmissions, those state laws may apply (e.g.
a Montana crypto MSB serving New York residents could trigger NY BitLicense requirements). Montana’s
stance makes it a friendly home base, but the moment money (fiat or crypto) crosses state lines, other
jurisdictions come into play.
Other States’ Money Transmitter Licensing Triggers
Nearly every other state requires a license to engage in money transmission involving that state’s
residents. Even if the MSB has no physical presence in a state, doing business with customers in that state or
transmitting funds to or from that state usually triggers that state’s licensing laws . In regulatory terms,
9
9
10
1
11
12
13
14
2
15
2
state laws have “long-arm” jurisdiction over out-of-state transmitters to protect their residents . Below
are general principles and specific examples from major states:
No “Physical Presence” Required: Most states explicitly do not require the transmitter to be
located in-state for the law to apply . If a Montana MSB transmits money on behalf of a person
residing in State X or to a recipient in State X, State X likely deems that as engaging in money
transmission “in” State X. Example: New York’s Department of Financial Services clarified that any
transmitter doing business with NY residents must be licensed in NY, even if operating via the
internet with no NY offices . The NY statute has no physical presence loophole, and NY reversed
older guidance to make this crystal clear . Similarly, Colorado, Michigan, Vermont, and others
have statutes reaching out-of-state transmitters serving their residents .
Representative State Laws:
California: California’s Money Transmission Act prohibits any person from engaging in money
transmission in California or advertising/soliciting such services unless licensed or exempt .
California defines “in California” broadly to include not only entities physically located in CA but also
transactions “with, to, or from persons located in California.” . So a Montana MSB receiving
money from a California user or sending money to a California beneficiary is viewed as doing
business “in California” and must obtain a CA license (or fit an exemption). California also explicitly
includes issuing stored value and receiving money for transmission as licensable activities .
(California recently adopted portions of the CSBS Model Law, including an agent-of-payee exemption
discussed later, via AB 1116 in 2023).
New York: Requires a license for transmitting money from or to NY residents (no physical presence
needed) . NY’s long-arm approach is backed by case law upholding state jurisdiction over out-of-
state financial services targeting in-state residents . A Montana MSB serving NY customers must
obtain a NY money transmitter license (or a specialized BitLicense if dealing in virtual currency
with NY consumers, under NY’s separate regime).
Texas: Texas law mandates a license to conduct money transmission under Tex. Finance Code
§152.101, with no person allowed to “engage in the business of money transmission” (or even
advertise as such) in Texas unless licensed . Practically, this means if either the sender or receiver
is in Texas, a license is required. Texas does allow an “authorized delegate” arrangement: a licensed
MSB can appoint agents who are not individually licensed, to transmit on its behalf under a written
contract . (This is analogous to Western Union’s agent network – more on this in Relationship
Models.) Texas has also adopted the Model Money Transmission Modernization Act (MTMA),
which among other things includes an agent-of-payee exemption and clarified virtual currency
coverage (Texas historically has been crypto-friendly by interpreting decentralized virtual currencies
as not “money,” but under the MTMA, certain stablecoin activities are now regulated ). For our
purposes, a Montana MSB with Texas clients should plan on a Texas license or partnering with a
Texas licensee.
Florida: Florida’s Money Transmitters’ Code is known for strict enforcement. It applies to “all money
transmitters transacting business in [Florida]” . Florida law requires a license for anyone
engaging in funds transmission or payment instrument sales with Florida consumers (Fla. Stat.
§560.204). Even an out-of-state business must be licensed if it offers services to Floridians. Florida
aggressively pursues unlicensed activity (often through undercover transactions), so a Montana MSB
should not serve Florida residents without a Florida license.
15
•
15
15
16
17
•
•
18
18
18
•
19
20
•
21
22
23
•
24
3
Illinois: Under Illinois’ Transmitters of Money Act, any business transmitting money in Illinois or
to an Illinois resident must obtain an Illinois money transmitter license . Illinois regulators
(IDFPR) explicitly state that a company outside Illinois needs a license if it offers remittances to
Illinois customers or pays out to people in Illinois . Illinois also treats certain payment processors
as exempt since 2015 (it issued guidance that third-party payment processors for merchants do not
require a license in IL) – effectively an agent-of-payee concept administratively adopted. But a
direct consumer-facing transmitter must license.
Others: The pattern is consistent: virtually all states except Montana require a license to send or
receive money for residents of their state. Some states extend coverage to receiving money in the
state for transmission outside or receiving outside for transmission into the state. In practice, if a
customer or transaction “touches” a state, assume that state’s license is needed unless an exemption
applies.
Multi-State Licensing: Because of these laws, a Montana MSB aiming to have nationwide clients must
secure licenses in 49 states (plus DC and territories as applicable). This is a significant undertaking,
typically handled via the NMLS (Nationwide Multistate Licensing System) which streamlines applications.
Many states have adopted the Uniform MTL standards under the CSBS Model Law to harmonize
requirements (net worth, bonding, etc.) .
Exemptions – “Agent of Payee” and Others: Some business models can avoid licensing in certain states by
fitting within statutory exemptions. A key exemption trending across states is the “Agent of the Payee”
exemption. In states that recognize it (over 20 states explicitly by statute, and a few by policy ), if an
entity is collecting money on behalf of a payee (e.g. a merchant) for goods or services – and the
arrangement meets specific criteria – then that activity is not “money transmission” under state law. For
example, Arizona’s law exempts an entity “appointed as an agent of a payee to collect and process a
payment from a payor to the payee for goods or services” provided that: (a) there is a written agreement
between payee and agent, (b) the payee is represented as accepting payment via that agent, and (c)
payment to the agent satisfies the payor’s obligation (no risk of loss to the payor if the agent fails to remit)
. When those conditions are met, the law deems the payment as made to the payee at the moment the
agent receives it, thus no money transmission by the agent (it’s an extension of the merchant). This
exemption is hugely relevant for marketplace payouts and bill payment models (discussed further in the
table and Relationship Models below). States like California, Illinois, Texas, Pennsylvania, Ohio, etc. now
have agent-of-payee exemptions either by statute or interpretation . Importantly, not all states have
this exemption, and the conditions vary. Where available, it can spare a Montana MSB from needing a
transmitter license if its service is structured as collecting payments for merchants (payees) under proper
contracts. But if the MSB’s activities include person-to-person remittances or holding consumer funds
outside an immediate payment for goods/services, agent-of-payee likely won’t apply.
Other common state exemptions include: banks (banks are exempt but our MSB is not a bank), payment
processors acting on behalf of licensed entities (some states mirror FinCEN’s payment processor
exemption), closed-loop stored value (certain gift card programs), and peer-to-peer currency exchanges
(state treatment of crypto varies—some states exempt purely decentralized crypto transactions or mining).
We will highlight relevant exemptions per activity in the table.
With this background, the Answer Table below lays out various activity patterns and analyzes their
regulatory characterization, federal requirements, and state licensing triggers. Each cell includes citations to
statutes or regulatory guidance that underpin the statements.
•
25
25
26
•
27 28
29
30
31
4
A. Activity Patterns and Legal Implications (Answer Table)
5
Serving Out-
of-State
Clients
(Montana
MSB with
customers in
other U.S.
states)
Likely money
transmission in
each client’s state.
No exemption
just for out-of-
state service –
transmitting
funds to or from
another state’s
resident =
engaging in that
state’s money
transmission
business. The
MSB is viewed as
a money
transmitter in
those states. (Not
merely incidental
– core business.)
Agent-of-payee
doesn’t apply to
generic P2P
remittances.
Must register
with FinCEN as
an MSB (if not
already) .
Implement full
AML program
(KYC,
recordkeeping,
SAR/CTR filings)
covering
interstate
transactions
. No federal
prohibition on
serving out-of-
state customers
– FinCEN defines
an MSB as doing
business “wholly
or in substantial
part within the
U.S.” regardless
of state lines
, so one
federal
registration
covers multi-
state
operations. The
MSB should also
be aware of
Travel Rule
obligations for
transfers >= $3k
(include sender/
recipient info)
.
License
required in
each state
where
customers are
senders or
recipients.
Nearly all
states assert
jurisdiction if a
transaction
involves their
resident
. For
example, a
Montana MSB
transmitting
funds on
behalf of a
New York
resident must
be licensed by
NYDFS ;
serving a
California user
requires a CA
MTL (California
defines money
transmission
“in this state”
to include
transactions
with or from
CA persons)
. If
unlicensed,
transactions
could violate
state law and
trigger 18 USC
1960 penalties
. No
physical
presence
exception: an
out-of-state
MSB is treated
NY DFS Industry Letter
(2011) – out-of-state
MSBs must license if
doing business with NY
residents ; IL
Regulator FAQ – license
needed to transmit $$ to
IL resident ; CA Fin.
Code §2030 – unlicensed
money transmission “in
this state” prohibited
; 18 USC §1960 –
federal crime for
operating without
required state license
.
15
3
4
32
33
15
25
15
18
7
15
25
18
7
6
Activity
Pattern
Legal
Characterization
(Money
Transmission or
Exempt?)
Federal MSB
Obligations
(FinCEN/BSA)
State
Licensing
Triggers
(Where/when
license
needed)
Key Citations
like a local one
(NYDFS: no
“physical
presence”
loophole) .
The MSB
should plan a
multi-state
licensing
strategy via
NMLS if
expanding
nationally.
19
7
Serving Out-
of-Country
Clients
(clients
located
outside the
U.S.)
Usually still “money
transmission”
under U.S. law if
the MSB is in the
U.S. The MSB’s
activities are
domestic (from
FinCEN’s view) if it
is “doing
business…within
the United
States” . The
client’s foreign
status doesn’t
exempt the MSB.
However, purely
foreign
transactions (no
U.S. sender/
receiver) might be
outside state
scopes. E.g.
sending funds
from a person in
Canada to a
person in Europe
using a Montana
MSB – U.S. state
laws may not
claim jurisdiction
(no in-state user).
But if any part of
the transfer
touches a U.S.
state (funds pass
through or go to
a state), that
state’s law could
apply. In sum,
serving foreign
clients is not itself
illegal, but check
if you’re
incidentally
triggering a
state’s law. No
state license covers
FinCEN MSB
registration
and BSA
compliance still
required. Being
based in
Montana (U.S.)
means the
business is a
U.S. MSB subject
to BSA, even if
some customers
are abroad .
FinCEN expects
the MSB to
apply its AML
program to
foreign clients
(verify identity,
monitor for
suspicious
activity).
Additional
federal
considerations:
If transmitting
funds into or out
of the U.S.,
comply with the
BSA’s funds
transfer
recordkeeping
(Travel Rule) and
OFAC sanctions
screening (e.g.
cannot do
business with
sanctioned
individuals/
countries).
Large
remittances
abroad may
trigger CMIR
filings if
physically
moving
No U.S. state
license purely
for having
foreign
clients. State
licenses are
required by
states to
protect their
own residents.
If neither party
to a transfer is
in State X, that
state’s money
transmitter law
typically
doesn’t apply.
(E.g., California
only cares
about
transmission
“with, to, or
from persons
located in
California” ;
Illinois cares
about in-state
or resident
users .)
Thus, for a
Montana MSB
transmitting
between
foreign parties
with no U.S.
resident
involved, no
other state
license is
triggered (and
Montana has
none).
However, if a
foreign client is
sending
money to a
beneficiary in a
FinCEN definition of MSB
– includes a person
“wherever located doing
business…wholly or in
substantial part within
the United States” ;
CA Money Transmission
Act defines “receiving
money for transmission”
as receiving money in
the U.S. for transmission
within or outside the U.S.
(state laws cover
outbound international
remittances if customer
is in-state); IL FAQ –
license needed to
transmit money in IL or
to IL residents .
32
32
34
25
32
18
25
8
Activity
Pattern
Legal
Characterization
(Money
Transmission or
Exempt?)
Federal MSB
Obligations
(FinCEN/BSA)
State
Licensing
Triggers
(Where/when
license
needed)
Key Citations
“global” scope; it’s
state-by-state.
currency, but
electronic
transfers just
fall under SAR/
CTR rules. Also,
if the MSB does
consumer
international
remittances
>100/year,
comply with
CFPB’s
Remittance
Rule (give pre-
sending
disclosures of
fees/exchange
rates and error
resolution
rights).
U.S. state, that
state will
require a
license for
receiving/
transmitting to
its resident.
Likewise, if a
foreign
customer uses
the MSB to
send from
abroad to, say,
a Texas
resident, a
Texas license is
needed (TX
covers
transmissions
to persons in
TX) . The
MSB should
also consider
foreign
regulations:
serving
customers in
their country
might require
that country’s
license
(outside the
scope of U.S.
law but a
compliance
consideration).
35
9
Interstate
Fund
Transfers
(sending
funds from
one state to
another)
By definition,
money
transmission.
Accepting money
in State A for the
purpose of
transmitting to
State B is the
classic regulated
activity. No
special
exemption; this is
what money
transmitter
licenses and
FinCEN
registration are
designed for.
Whether done via
own system or
through
networks, if the
MSB is the entity
receiving funds
and guaranteeing
delivery to a
recipient in
another state, it’s
acting as a money
transmitter. (If
using a bank
partner to
actually move the
funds, the
characterization
might shift – see
third-party and
bank partner
scenarios below.)
FinCEN/BSA:
The MSB must
incorporate
interstate
transmissions
into its AML
controls. The
federal
registration
covers multi-
state
operations, but
FinCEN expects
compliance
across all
jurisdictions. For
each transfer ≥
$3,000, the MSB
must record
and transmit
required
sender/
recipient
information to
the next
financial
institution in the
chain (Travel
Rule) . If the
transfer is ≥
$10k in cash, file
a CTR. FinCEN
doesn’t require
separate
registrations per
state, but the
MSB should list
all trade names
and agent
locations on its
FinCEN
registration and
maintain an
updated agent
list if using
agents .
Cross-border
Multi-state
licensing: A
transfer from
State A to State
B potentially
involves two
states’ laws –
the state
where the
sender is
located and
the state of the
recipient. Most
states consider
either end
sufficient to
require the
transmitter to
be licensed.
For example, if
a Montana
MSB enables a
user in Florida
to send money
to a person in
Georgia, both
Florida and
Georgia law
are implicated.
Generally, the
transmitter
should be
licensed in the
sender’s state
at minimum,
and often in
the recipient’s
state too
unless the
transaction is
handled by a
licensed
counterpart
there. Many
states’ statutes
define money
transmission
NY Banking Law Art. XIII-
B – License required if
receiving money for
transmission “from
persons residing or
located in New York” or
transmitting money on
behalf of persons in
New York ; California
Fin Code §2030 – covers
receiving money in CA or
transmitting money to
persons in CA (via
definition of “in this
state”) ; Illinois TOMA
205 ILCS 657 – license
required to transmit
money in IL or to IL
residents .
33
36
37
18
25
10
Activity
Pattern
Legal
Characterization
(Money
Transmission or
Exempt?)
Federal MSB
Obligations
(FinCEN/BSA)
State
Licensing
Triggers
(Where/when
license
needed)
Key Citations
aspects (if any)
as noted above
(OFAC, etc.).
as receiving
money from a
person in their
state or
transmitting
to someone in
their state
. In
practice,
licensing is
usually
focused on
where the
customer
(sender) is
located, but
prudence is to
license in any
state where
either end is
located.
(Notably, New
York requires a
license to
transmit from
or on behalf of
NY persons, or
to transmit
money “to any
location in the
state”, covering
both directions
.) Failure to
license in all
required states
can lead to
cease-and-
desist orders
or
enforcement
fines.
34
16
11
Using Third-
Party Payout
Providers
(MSB sends
funds to a
partner in the
recipient’s
state who
then pays out
to the
beneficiary)
Still money
transmission by
the MSB, unless
structured as an
agency
relationship with
the partner. If the
Montana MSB
takes the
customer’s funds
and then uses a
separate licensed
transmitter or
payment
company in the
destination state
to deliver the
money, there are
two
transmissions:
one from the
customer to the
MSB, and one
from the MSB to
the end recipient
(via the partner).
The Montana
MSB remains the
transmitter on the
first leg, and
possibly the
entire transaction
in regulators’
eyes, unless the
partner is
actually the one
serving the
customer under
its license. To
avoid both
needing a license,
one common
approach is to
use the partner as
an “authorized
delegate” of the
Montana MSB, or
No change in
FinCEN
obligations –
the Montana
MSB is still the
entity receiving
and
transmitting
customer
funds, so it
remains the
MSB for BSA
purposes. It
must conduct
KYC on the
customer,
monitor the
transaction, and
(if the payout
partner is not a
bank) the
partner might
be considered
an agent of the
MSB under
FinCEN rules.
FinCEN requires
an MSB to
maintain a list
of agents and
oversee their
BSA compliance
. The MSB
should have an
AML agreement
with the payout
partner if the
partner is acting
on its behalf. If
instead the MSB
is acting as
agent for the
partner (who is
the licensed
MSB principal),
then the partner
is the registered
If not
structured
carefully, both
entities might
need
licensing. The
cleanest
approach: treat
the payout
provider as an
authorized
delegate of
the Montana
MSB or vice
versa. Many
state laws
allow licensed
transmitters to
appoint
delegates/
agents under
contract .
But if the
Montana MSB
is not licensed
in the payout
state, it
technically
cannot appoint
an agent there
(no license to
cover them).
Instead, the
Montana MSB
could sign on
as an agent of
a larger
licensed
network. For
instance, some
startups
operate under
another
company’s
license
network
(common in
Texas Finance Code
§152.101(c)(1) –
authorized delegate of a
licensee is exempt if
under written contract
; Arizona Revised
Stat. §6-1202(A)(3) –
intermediary processor
exemption when
transmitting on behalf of
a licensed entity that
remains solely liable ;
FinCEN MSB agent
exemption – agent of
another MSB need not
register (but
principal must list agents
).36
22
22
38
8
36
12
vice versa. If, for
example, the
Montana MSB
becomes an
agent of a
licensed money
transmitter in the
other state, then
the partner is the
licensed principal
and our MSB is
just an agent.
Alternatively, if
our MSB is
licensed in that
state, it can
appoint the local
payout provider
as its agent.
Simply
outsourcing
payout does not
by itself transfer
the regulatory
burden.
MSB responsible
for BSA
compliance; our
MSB, as an
“MSB agent,” is
exempt from
FinCEN
registration
but still must
adhere to the
principal’s AML
program. In
either case,
FinCEN wants
clarity on who is
the principal
MSB to ensure
one party is
fulfilling BSA
duties.
fintech
“license-as-a-
service”
models). If our
MSB does that,
the partner’s
license covers
the activity in
that state (the
partner is the
transmitter of
record, and
our MSB is
disclosed as an
agent). Absent
that, a
transaction
where MSB A
hands off to
MSB B for
payout may
require both A
and B to be
licensed in the
recipient’s
state. Some
states have
tried to
accommodate
“intermediate
transmitters”:
e.g., Arizona
exempts an
intermediary
that only
receives funds
from a
licensed
transmitter
and forwards
to the
ultimate
recipient’s
provider .
But such
nuances vary.
Bottom line:
8
38
13
Activity
Pattern
Legal
Characterization
(Money
Transmission or
Exempt?)
Federal MSB
Obligations
(FinCEN/BSA)
State
Licensing
Triggers
(Where/when
license
needed)
Key Citations
using a third-
party payout
service does
not eliminate
licensing
requirements; it
only works if
you piggyback
on the third
party’s license
via a formal
agency/
outsourcing
arrangement.
14
Agent
Network
(MSB uses
agents or
franchisees to
offer services
in multiple
states)
Money
transmission by
the principal
(licensee) via
agents. If our
Montana MSB
expands by
appointing agents
(e.g. stores or
individuals who
take cash and
handle
transactions on
its behalf), the
agents
themselves might
avoid needing
individual licenses
provided our
MSB is licensed
in those states
and assumes
responsibility.
This is the
Authorized
Delegate model:
the agent’s
activity is covered
under the
principal MSB’s
license. The agent
is not a separate
transmitter
legally; they act as
an extension of
the principal. If
Montana MSB
lacks a license
where the agent
is, this model
cannot be used
there. Absent a
license,
independent
agents would
each be viewed as
unlicensed
The principal
MSB (our
company)
retains all
federal BSA
obligations for
transactions
conducted
through agents.
It must
incorporate
agents into its
AML program –
e.g. provide
training,
monitor for
compliance, and
file SARs/CTRs
for agents’
transactions as
if its own.
FinCEN explicitly
requires an MSB
to maintain a
list of its
agents and
make it
available to
regulators .
The principal
should collect
required
customer
information
from agents and
ensure agents
follow CIP
(customer
identification)
procedures.
Agents
themselves do
not register
separately with
FinCEN (if
they truly act
only as agents
Licensing: A
licensee can
appoint
agents
(authorized
delegates) in
states where
it holds a
license,
pursuant to
that state’s
rules. Most
states require
a formal agent
contract and
often that the
agent be
reported to the
regulator. For
example,
California
defines “agent”
as an entity
not licensed
itself that
provides
money
transmission in
CA on behalf of
a licensee,
provided the
licensee
assumes
liability for the
transmission
from the
moment the
agent receives
funds . That
is key: the
licensed MSB is
liable for its
agents’
actions and
for customer
funds collected
by the agent
CA Fin Code §2003(b) –
licensee’s liability for
agent: agent can
provide money
transmission on behalf
of a licensee if the
licensee “becomes liable
for the money
transmission” when
agent receives money
; TX Fin Code
§152.101(b),(c) –
engaging in money
transmission requires a
license, but authorized
delegates of a licensee
are exempt when acting
per contract ;
FinCEN MSB Guidance –
MSB must maintain
agent list and make
available to regulators
.
36
8
39
39
21 22
36
15
transmitters
themselves. So
the concept of an
“agent network”
inherently ties to
having a principal
licensee in each
jurisdiction.
(Montana doesn’t
license, but if
agents operate in
other states, we’d
need licenses
there to appoint
them.)
of our MSB).
FinCEN’s
guidance makes
clear that a
person who is
an MSB solely as
an agent of a
registered MSB
is not an
independent
MSB . This
facilitates
networks like
Western
Union’s, where
thousands of
agent locations
are covered by
one central
registration.
However, the
principal MSB’s
compliance
burden
increases with
an agent
network (need
robust agent
oversight
program).
. Texas
similarly allows
agents under
contract and
does not
separately
license them
. When
using agents,
our MSB must
ensure each
state’s agent-
related
requirements
are met (some
states require
agent
reporting or
background
checks). If our
MSB is not
licensed in a
state, it cannot
legally have an
agent conduct
transmission
there – doing
so would be
unlicensed
activity by the
principal (and
possibly by the
agent as aiding
and abetting).
So an agent
network
strategy
requires first
obtaining the
state licenses.
One
alternative:
partner with
an existing
licensed MSB
to leverage
their agent
8
39
22
16
Activity
Pattern
Legal
Characterization
(Money
Transmission or
Exempt?)
Federal MSB
Obligations
(FinCEN/BSA)
State
Licensing
Triggers
(Where/when
license
needed)
Key Citations
network (as
discussed
above). In sum,
agents extend
the reach of a
licensee but
do not
eliminate
licensing
obligations –
they actually
depend on
them.
17
Marketplace
Payouts
(Platform
holding funds
from buyers
to pay sellers;
e.g. gig
platforms, e-
commerce
marketplaces)
Potential money
transmission,
but often fits
“Agent-of-Payee”
exemption if
structured
properly. In a
marketplace
model, the
platform (our
MSB) receives
funds from a
buyer (payor) for
goods/services
provided by a
seller (payee), and
later forwards
those funds
(minus fees
perhaps) to the
seller. Absent any
exemption, this is
receiving money
from one person
for delivery to
another = money
transmission.
However, many
states now
exempt this
scenario if the
platform is an
authorized
agent of the
seller (payee). If
by contract the
seller appoints
the platform as its
agent to accept
customer
payments on its
behalf, and
critically the
payment to the
platform
extinguishes the
buyer’s payment
Federal/BSA:
FinCEN does not
explicitly exempt
agent-of-payee
arrangements in
its MSB
definitions.
Nonetheless,
FinCEN’s
payment
processor
exemption
(discussed
above) closely
aligns with this
model. If our
platform only
facilitates
payments for
goods/services,
uses clearing
through banks,
and has
agreements
with the sellers
(payees), FinCEN
may not treat it
as a money
transmitter .
The platform
should ensure
all four criteria
of FIN-2014-
R009 are met
(especially that
disbursements
to sellers also
occur via bank/
ACH networks)
. If met,
the platform is
not an MSB
federally,
meaning no
FinCEN
registration
required.
Licensing: In
states with an
Agent-of-
Payee
exemption, no
money
transmitter
license is
required for
qualifying
marketplace
payments
. For
example,
Illinois added
an agent-of-
payee
exemption: a
merchant
payment
processor
meeting
conditions is
exempt from
the
Transmitters of
Money Act .
California
(effective Jan
2024 via new
regulations)
clarified that
receiving
money as an
agent of the
payee is not
“receiving
money for
transmission”
under its MTA
. Texas
explicitly
added agent-
of-payee in its
2021 updates
(Tex. Fin. Code
§151.003(6)
Arizona Revised Stat.
§6-1202(A)(2) – Agent-of-
Payee exemption (no
license if agent collects
payment for payee for
goods/services and (a)-
(c) conditions are met)
; Modern Treasury
report – 22 states have
agent-of-payee laws ;
FinCEN Ruling FIN-2014-
R009 – payment
processor meeting 4
criteria not an MSB .
California DFPI (2023) –
confirmed agent-of-
payee not “money
transmission” (amending
Cal. Code Regs) .
9
40 41
42
30
26
43 44
30
29
9
45
18
obligation to the
seller, then the
transfer is
considered
complete at the
time the
platform
receives the
funds . The
platform isn’t
seen as
transmitting
money for the
buyer; it’s seen as
simply collecting
money as the
seller’s agent. This
is the Agent-of-
Payee
exemption,
which would
mean the
platform’s
activities are not
“money
transmission”
under those
states’ laws. So, a
Montana
marketplace MSB
can leverage this
in states that
recognize it. Care
must be taken to
meet all
conditions
(written agency
agreement with
sellers, proper
disclosures, and
ensuring the
seller treats a
customer’s
payment to the
platform as final).
If any condition
fails or in states
However, if any
criterion is not
met (say the
platform pays
some sellers in
crypto or cash,
or holds funds
outside of
regulated
clearing systems
for a time),
FinCEN could
deem it a money
transmitter with
full MSB
obligations.
Many large
payment
processors
(Stripe, PayPal,
etc.) rely on this
exemption
federally. So the
Montana MSB
should design
payouts to go
through BSA-
regulated
institutions and
clearly be in
service of
sellers. The
platform still
needs robust
AML controls
(marketplaces
can be used for
fraud/money
laundering via
fake
transactions).
Even if not an
MSB, suspicious
activity should
be monitored
and possibly
reported (some
under the
MTMA).
Florida does
not yet have a
statutory
agent-of-payee
safe harbor, so
the platform
would need a
license in FL to
do this. Thus,
the MSB might
be able to
operate
without
licenses in
states X, Y, Z
that have the
exemption (so
long as
conditions are
met), but still
need licenses
in states A, B, C
that lack it. A
prudent
approach is to
get licensed
wherever
required, but
leverage
exemptions
where possible
to reduce the
licensing
footprint. Still,
since Montana
has no license,
for those other
states without
AoP
exemptions,
operating
without a
license is
legally risky.
Each state’s
30
19
Activity
Pattern
Legal
Characterization
(Money
Transmission or
Exempt?)
Federal MSB
Obligations
(FinCEN/BSA)
State
Licensing
Triggers
(Where/when
license
needed)
Key Citations
without this
exemption, the
activity is money
transmission
requiring a
license.
choose to file
SARs
voluntarily).
exact
exemption
language
should be
reviewed to
ensure
compliance
(e.g. some only
exempt
payments to
business
payees, not
individuals).
20
Escrow-Like
Holding of
Funds (MSB
holds
customer
funds
pending
some
condition or
time delay,
e.g. holding
money in an
account/
wallet for
later use or
release)
Generally money
transmission
(holding funds for
others = “stored
value” or an
obligation) and
possibly escrow
business in some
states. If the MSB
receives funds
from a customer
and does not
immediately
transmit them to
a recipient, but
rather holds them
(in a ledger or
pooled account)
until a condition
is met (like
delivery of a
product, or user’s
decision to
withdraw), it is
taking on an
obligation to
make those funds
available or
transmit them in
the future. This
fits the definition
of issuing “stored
value” or
receiving money
for transmission
at a later time –
both are usually
covered under
money
transmitter laws
. Additionally,
maintaining an
escrow (third-
party holding) for
transactions
could trigger
escrow agent
Federal:
Holding funds
for a customer
still makes the
business a
money
transmitter
under FinCEN’s
definition
(transmission
can be
immediate or
later; providing
stored value to
customers is an
MSB activity). In
fact, FinCEN has
specific rules for
“prepaid
access” (stored
value): providers
of prepaid
programs over
certain
thresholds must
register as MSBs
and implement
AML controls
. Our MSB
would need to
treat stored
funds like any
other
transmittal –
collecting KYC at
account
opening,
monitoring for
suspicious use
of the wallet,
and when
transmitting
out, comply with
Travel Rule, etc.
If the MSB
qualifies as a
“provider of
State: Almost
all state money
transmitter
laws cover
stored value
issuance and
receiving
money for
later
transmission.
For example,
California
expressly
includes
issuing stored
value in the
definition of
money
transmission
and even
says “Only a
licensee may
issue stored
value or
payment
instruments” .
So offering an
e-wallet or
account where
customers load
funds would
require a
license in CA
(or a qualifying
exemption like
being an agent
of a bank – see
next section).
Some states
had exclusions
for closed-loop
gift cards (e.g.
usable with
one issuer or
franchise), but
for general
stored value, a
CA Fin Code §2003(q) –
“Money transmission”
includes issuing stored
value and receiving
money for transmission
; CA Fin Code §2030 –
must be licensed to
engage in those
activities ; “Only a
licensee may issue
stored value” – CA Fin
Code §2003(x) (as
amended) . Montana
licenses escrow
companies (MT Code
Ann. §32-7-101 et seq.)
(not excerpted, but
Montana official
guidance notes escrow
companies need license
even though money
transmitters per se do
not). FinCEN Prepaid
Access Rule – 31 CFR
1010.100(ff)(4), 1022.210
etc., requiring MSB
compliance for stored
value programs .
18
46
18
47
18
18
47
48
46
21
licensing in
certain states
(often for real
estate or legal
escrows; general
online escrow
might or might
not fall under
those). Montana
notably licenses
escrow
companies , so
if our MSB offers
an escrow service
(say, holding
buyer’s funds and
releasing to seller
upon
confirmation), we
should check if
that requires a
Montana Escrow
Company license.
Other states (e.g.
California Escrow
Law) define
escrow narrowly
(usually real
estate closing),
but some might
consider online
escrow as money
transmission
anyway. In
summary,
holding funds =
money
transmission
unless a specific
exemption. One
possible
exemption angle:
if the funds are
stored without the
ability to transfer
to others (closed-
loop stored value
prepaid access”
(e.g. offering
general spend
prepaid cards or
wallet where
funds can be
used broadly), it
must retain
records of
customers and
transactions
under 31 CFR
§1022.420
and
§1022.210(d).
Essentially, the
federal MSB
obligations
apply fully.
There’s no
escrow
exemption
federally; even
escrow accounts
are subject to
BSA if the
intermediary is
engaged in
funds transfer.
The MSB should
also segregate
and safeguard
customer funds
(though that’s
more a state
requirement,
federal law
expects SARs if
funds seem to
be misused).
license is
needed.
Additionally, if
the service is
marketed as
an escrow
(holding funds
on behalf of
parties in a
transaction),
certain states
might require
an escrow
license.
Montana: as
noted, licenses
escrow
businesses, so
if our MSB’s
holding of
funds fits
Montana’s
definition of
escrow (likely if
acting as
neutral agent
in a sale), that
could be an
issue .
California: has
a separate
Escrow Law
(Financial Code
§17000+), but
typical online
payment
intermediaries
have not been
treated as
escrow agents
under that law
unless they
formally
advertise
escrow
services.
Generally, we’d
13
46
48
22
Activity
Pattern
Legal
Characterization
(Money
Transmission or
Exempt?)
Federal MSB
Obligations
(FinCEN/BSA)
State
Licensing
Triggers
(Where/when
license
needed)
Key Citations
for one
merchant), some
states exempt
that. But open-
loop stored value
or generic
customer
balances are
regulated.
treat it as
money
transmission
licensing is
needed, and if
doing any
specialized
escrow (like
real estate),
consult those
laws too. Thus,
a Montana
MSB that holds
customer
funds in
wallets or for
P2P escrow will
trigger
licensing in all
states where
users are
located. There
are often
additional
bonding/net
worth
requirements
for stored
value
businesses due
to the float
they hold.
Table Summary: In general, a Montana MSB can have out-of-state and international clients and can
send/receive funds across state lines, but doing so will almost certainly require obtaining money
transmitter licenses in those other states. Using third-party service providers or novel models does not
eliminate the need; at best it shifts who must be licensed (e.g., using a bank partner or acting under
another’s license). Federal MSB requirements apply uniformly at the company level (one FinCEN
registration, one AML program) but the MSB must adapt its program to cover the complexities of interstate
and agent operations.
23
Next, we delve into relationship models and how the choice of partners (banks vs non-banks) and
structuring can affect the regulatory posture.
B. Relationship Models: Bank Partnerships vs. Non-Bank Rails, and
Third-Party Processors
1. Bank Partner Model: One strategy for an MSB to operate nationally without 50 state licenses is to
partner with a bank. Banks are generally exempt from state money transmitter licensing – they can
transmit money under federal banking laws and their charter authority. Crucially, banks can preempt state
licensing for agents acting on their behalf. If our Montana MSB can structure itself as an agent of a bank,
with the bank being the entity that actually receives and transmits customer funds, then state money
transmission laws would not apply to the bank or its agent (states can’t require a national or state-chartered
bank to get a transmitter license). This model is common in fintech: e.g., prepaid card programs where a
bank is the issuer of the accounts and the fintech program manager is an agent of the bank.
For this to work, the bank must truly be in control of the monetary transaction. Typically, customer
funds are held in bank accounts (FBO accounts or individual accounts at the bank), and all payments are
executed by the bank. The fintech (our MSB) acts under a service agreement/agent agreement with the
bank. Many states explicitly exempt an agent of a bank. For instance, Arizona’s law exempts any person
appointed as a third-party service provider or agent of an exempt entity (like a bank) to conduct money
transmission, as long as there is a written agreement and the bank assumes full responsibility for the
transmission obligations . This means if our Montana MSB is an agent of (say) ABC Bank for a payments
program, and ABC Bank “owns” the funds flow and is liable to customers, then Montana MSB doesn’t need
individual state licenses – the bank’s regulated status covers it .
Benefits: Leveraging a bank partner can drastically simplify multi-state operations (no state licenses
needed for the MSB itself), and banks come with customer trust and direct Fed payment system access.
Also, banks are examined by federal regulators for BSA, so they have robust compliance programs; the
fintech can piggyback on that.
Challenges: The bank must be willing to assume responsibility for the MSB’s transactions. From a
compliance perspective, the bank will impose stringent requirements. The bank remains fully liable to
regulators for BSA/AML compliance of the program. In practice, the bank will require the fintech to perform
KYC and transaction monitoring to the bank’s standards under a contract. The MSB effectively operates as a
program manager/agent, while the bank has veto power over products, customers (often the bank must
approve the onboarding standards), and can terminate the relationship if risk issues arise.
Additionally, not all activities can be neatly done by a bank. Banks cannot directly engage in certain crypto
activities without regulatory permission, for example. So if the business involves crypto, a bank partnership
covers the fiat movements, but the crypto part might still need an MSB license in some states (or a separate
approach like a trust charter).
2. Non-Bank Rails Model: This is the classic licensed MSB route – the company itself gets licensed in states
and uses non-bank payment processors or networks to move money (e.g., using ACH via an Originating
Depository Financial Institution, using another licensed money transmitter’s API, etc., but not having a
sponsor bank as the transmitter). In this model, the Montana MSB is the primary licensee in each
49
49
24
jurisdiction and directly holds customer funds (often in a pooled account) and instructs payments. It
may integrate with third-party processors for technical connectivity (for example, integrating with Stripe
or Modern Treasury for ACH processing, or with the FedNow service via a correspondent bank), but these
processors are just vendors – the MSB remains the “money transmitter” on record.
Who is the Transmitter? A critical regulatory question in complex money flows is “who is the actual
money transmitter?” If multiple parties are involved (fintech, bank, processor, licensed partner), regulators
will apply a substance-over-form test. They’ll ask: which party has the relationship with the sender/receiver?
who receives the customer’s money and is responsible for delivering it to the end recipient? There can be
joint liability – for instance, if a fintech without a license uses a licensed processor to execute payments,
the state might still view the fintech as engaging in unlicensed transmission, unless the licensed entity is in
the foreground as the service provider.
Third-Party Payment Processors: A common example is a fintech that uses a payment processor (like a
payment facilitator or an ACH payment API provider). If that processor is a licensed money transmitter,
sometimes the arrangement is that the processor is actually operating under its license and the fintech is
just its customer or agent. If that’s explicit (and the end user is a customer of the licensed entity in terms of
terms of service), then the licensed entity is the transmitter. But if the fintech is seen as the one providing
the service to the user and merely using the processor as a backend, regulators may say the fintech needs
licenses too.
Delegation Boundaries: Essentially, you can delegate technology and operations to third parties, but you
cannot delegate legal liability without a proper agency/license framework. If our Montana MSB hires a
company in New York to pay out cash to recipients for us, that NY company becomes our agent in NY (if
we’re licensed there, fine; if not, that’s problematic). Conversely, if we sign on as an agent of that NY
licensed transmitter, then that company is the one sending money (legally) and we’re just front-end.
Regulators often scrutinize contracts and customer agreements to determine the roles. They will look at
who the customer believes is providing the service and who is “on the hook” if something goes wrong. For
example, if the terms of service say “MontanaMSB Inc. will transfer your funds,” then MontanaMSB is
holding itself out as the transmitter (needs license). If instead it says “Service provided by BigTransmit Co.
(licensed in NY) and MontanaMSB is assisting,” that indicates BigTransmit is the transmitter of record.
Agent-of-Payee vs. Authorized Delegate vs. Bank Agent: These are three different legal constructs that
can prevent needing a license: (a) Agent-of-Payee – where the transmitter is deemed the agent of the
recipient (payee) so no third-party transmission is occurring (already discussed above); (b) Authorized
Delegate of a Licensee – where the company operates under another company’s license by contract; (c)
Agent of a Bank – where the company operates under a bank’s authority. Each requires specific contracts
and risk allocations: - Authorized Delegate Model: The delegate must operate under the principal’s
compliance program. The principal licensee usually requires regular reporting and may require the
delegate to register on NMLS as an authorized agent. The contract should specify that the principal is liable
for the money (this is required by law in many states) . - Bank Agency Model: The agreement must make
clear that all customer funds are handled as bank deposits or payments, the bank has ultimate control, and
the agent (fintech) only acts at the bank’s direction. Often the bank will insist that the agent’s marketing
clearly disclose the bank’s role (some require “funds held by XYZ Bank, Member FDIC” in the app or website).
39
25
In all cases, the MSB must not inadvertently stray outside the boundaries. For instance, if acting as an
agent-of-payee, the MSB should not also start offering P2P transfers between users – that wouldn’t be
covered by the payee exemption and could trigger licensing.
C. Practical Compliance Controls for Each Model
To implement these models while staying compliant, a Montana MSB should establish certain contracts,
policies, and internal controls. Key controls include:
Agency/Service Agreements: For any third-party relationship (bank partnership, authorized
delegate, processor), have a robust written contract defining roles and compliance duties. For
example, a Bank Sponsorship Agreement should specify that the fintech is an agent of the bank for
money transmission, that the bank is responsible for BSA/AML compliance, and outline how the
fintech will perform customer onboarding, monitoring, reporting of suspicious activity to the bank,
etc. Similarly, an Authorized Delegate Agreement with a licensed MSB should include the
delegate’s obligation to comply with the principal’s policies, the scope of authority (e.g. can only sell
or pay out transfers on behalf of principal), and indemnification clauses. If using an agent-of-payee
model, have an Agent of Payee clause in the merchant’s terms of service: the merchant (payee)
appoints the MSB as its agent to accept customer payments, and importantly that payment to the
MSB fulfills the customer’s obligation to the merchant .
Funds Flow & Settlement Controls: Create funds flow diagrams and narratives that document
how money moves from sender to receiver, including which entity holds the funds at each point.
Regulators will ask for this. For a bank partner model, the diagram should show funds go into an
FDIC-insured account at the partner bank (often an FBO – “for benefit of” – account holding
customer funds) and that payments out of that account are made by the bank. For an agent-of-
payee, the funds flow should show that the payee is deemed paid at the moment the platform
receives the money (per contract). Maintaining clear settlement procedures (how often funds are
remitted to payees, what happens with refunds) is important. Also, implement controls to segregate
customer funds from the MSB’s operational funds, as most state laws require safeguarding
customer money (often via permissible investments or surety bond).
KYC and CIP Allocation: Determine how KYC (Customer Identification Program) responsibilities are
divided. In a direct-licensed model, the MSB does all KYC. In a bank model, either the bank performs
CIP on end customers or the bank can rely on the fintech’s CIP under the USA PATRIOT Act reliance
provision if conditions are met (the fintech would be subject to examination or an agent of the bank)
. The policy should be explicit: who verifies customer identity, who checks watchlists (OFAC),
and how that information is shared. With multiple parties, consider a consolidated BSA/AML policy
or at least a BSA responsibilities matrix. For example, the contract might state the fintech will
conduct initial KYC and monitoring, but will escalate suspicious activity to the bank for SAR filing –
then internal procedures must support that (e.g., a documented process for sending suspicious
activity reports to the bank’s BSA officer within X days).
Transaction Monitoring & Reporting: Ensure there are tools to monitor transactions across all
channels. If using agents, you need to monitor agent locations for unusual activity (spikes in volume,
unusual patterns concentrated at one agent – this has been an issue in Western Union/MoneyGram
consent orders). If using a processor API, make sure you receive sufficient data to detect anomalies.
•
30
•
•
50 51
•
26
SAR filing responsibility needs to be clear: if not in a bank program (where the bank files), the MSB
must file SARs itself. Policies should require investigation of alerts and a SAR decision within the 30-
day window per FinCEN rules.
Recordkeeping and Information Sharing: Maintain the required records for each transaction
(sender/recipient name, amount, date, payment instrument, etc.) for the mandated retention period
(5 years under BSA) . If the model involves multiple entities (say, our MSB and a partner), include
provisions that the partner will provide any records needed for compliance and examinations. Also,
consider signing a 314(b) information sharing agreement if applicable, to facilitate sharing of
customer activity between bank and fintech for AML purposes .
Reporting to Regulators: In a multi-state setup, track each state’s reporting requirements – e.g.,
many states require quarterly or annual reports of transmission volume, agent lists, etc. If using
authorized delegates, states often require you to maintain an updated list of agents and
sometimes notify the state of new agents. This should be built into compliance procedures
(perhaps managed via NMLS, which has an “Authorized Agent” section for many states).
Consumer Protection Policies: Ensure clarity in customer-facing disclosures about who holds
their funds and who to contact for complaints. For instance, if using a bank partner, the terms should
disclose that funds are held by XYZ Bank, member FDIC (if applicable), and the bank’s name may
need to appear on customer statements. If licensed in multiple states, you’ll need to post license
information and consumer complaint notices as required by each state (often on the website/app
and in user agreements). This is a tedious but essential compliance task.
Internal Audit and Training: Because operations are spread across models, implement an audit
function to periodically check that, e.g., agents are following procedures (mystery shopping agents
is a known practice), or that the fintech’s program with the bank is meeting all the bank’s conditions.
Conduct training for any agents or partners about AML/CFT responsibilities and how to identify
suspicious activity or fraud (some states require specific training for authorized delegates).
Contingency and Liability Management: In agent relationships, state laws typically hold the
licensee liable for the agent’s conduct . Thus, the MSB should have indemnification clauses in
contracts and adequate insurance (e.g., fidelity bond, cyber insurance if online) to cover losses
caused by an agent or service provider. Also, if using a bank sponsor, be prepared for enhanced
regulatory scrutiny – bank regulators (OCC/FDIC) have guidance on third-party risk management;
our MSB might be required to provide information or even be examined as a third-party service
provider.
By establishing these controls, a Montana MSB can create a compliant operational framework whether it
chooses direct licensing or partnership routes.
•
52
53
•
•
•
•
39
27
D. Key Laws, Regulations, and Guidance (Download Pack)
Below is a selection of key primary sources referenced above, with full URLs, which can be downloaded or
consulted for detailed requirements and guidance:
FinCEN Regulations and Guidance:
31 C.F.R. § 1010.100(ff) – Definition of Money Transmitter and MSB (via eCFR) – https://www.ecfr.gov/
current/title-31/chapter-X/part-1010#1010.100
31 C.F.R. § 1022.210 – Requirement of AML Program for Money Services Businesses – https://
www.ecfr.gov/current/title-31/chapter-X/part-1022#1022.210
FinCEN Ruling FIN-2014-R009 (Aug. 27, 2014) – Payment Processor exemption conditions – https://
www.fincen.gov/sites/default/files/shared/FIN-2014-R009.pdf
FinCEN Guidance – MSB Agent List (maintenance and requirements) – https://www.fincen.gov/money-
services-business-msb-agent-list
FinCEN MSB Registration – FinCEN Form 107 and Instructions – https://www.fincen.gov/sites/default/
files/shared/FinCEN107.pdf (for reference on registration info)
FinCEN “Am I an MSB?” FAQ – https://www.fincen.gov/am-i-msb (helps determine MSB status including
examples)
FinCEN Guidance FIN-2013-G001 (Mar. 2013) – Application of FinCEN regs to cryptocurrency
transmitters – https://www.fincen.gov/sites/default/files/shared/FIN-2013-G001.pdf
Federal Law:
18 U.S.C. § 1960 – Federal criminal statute: Prohibition of Unlicensed Money Transmitting
Businesses – https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title18-section1960
(see subsection (b)(1)(A)–(B))
Bank Secrecy Act/USA PATRIOT Act – 31 U.S.C. § 5318(l) and 31 C.F.R. § 1020.220 (Customer Identification
Program rules, relevant for bank partnerships) – https://www.ecfr.gov/current/title-31/chapter-X/
part-1020#1020.220
Montana and Multi-State Resources:
Montana Division of Banking – Money Transmitters Page (Montana’s stance of not licensing MSBs) –
https://banking.mt.gov/moneytransmitters
Montana Division – “The Challenge of Being the Only State Not Regulating Money Transmitters” (article) –
https://banking.mt.gov/Portals/58/MT%20Not%20Regulating%20Money%20Transmitters.pdf (may
provide context on operating from MT)
CSBS Model Money Transmission Modernization Act (MTMA) (2021) – https://www.csbs.org/csbs-money-
transmission-modernization-act-mtma (download PDF for the model law adopted by many states,
which includes agent-of-payee and crypto provisions)
CSBS “Agent of the Payee Exemption” Map & Summaries – https://www.csbs.org/agent-payee-
exemption-map (state-by-state info on which states have agent-of-payee laws)
NMLS Industry Resources for MSB Licensing – https://nationwidelicensingsystem.org/slr/Pages/
MoneyServicesBusinesses.aspx (checklists and state licensing info via NMLS)
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
28
State Laws & Guidance (selected states):
New York: NY Banking Law Article 13-B (Money Transmitters); NYDFS Industry Letter, 3/31/2011 – “No
Physical Presence Required” – https://www.dfs.ny.gov/industry_guidance/industry_letters/
il20110331_money_transmitters_with_no_physical_presence_ny
California: California Financial Code, Division 1.2 – Money Transmission Act (Cal. Fin. Code § 2000 et
seq.) – https://dfpi.ca.gov/regulated-industries/money-transmitters/ (DFPI page with links to code
sections); DFPI Opinion Letter (2016) – “Money Transmission in this State” (defines in-state, and discusses
when license is needed) – https://dfpi.ca.gov/wp-content/uploads/sites/337/2019/03/Opinion-Letter-
Money-Transmission-in-this-State-08-23-16.pdf
Texas: Texas Finance Code Chapter 151 (old) / 152 (new) – Texas Money Services Act; Texas Dept. of
Banking – Money Services Businesses FAQ – https://www.dob.texas.gov/money-services-businesses
(general info and links to statutes, and the Supervisory Memorandum 1035 on when out-of-state
entities need a TX license)
Florida: Florida Statutes Chapter 560 – Money Services Businesses (Part II for money transmitters);
Florida OFR – Money Transmitters Overview – https://flofr.gov/sitePages/MoneyTransmitters.htm
(includes guidance on activities and licensing)
Illinois: Illinois Compiled Statutes, 205 ILCS 657/ Transmitters of Money Act; IDFPR Currency Exchange
Section FAQ (includes MSB info) – https://idfpr.illinois.gov/DFI/CCD/ccd_main.asp (the PDF we cited with
Q&A on needing IL license for out-of-state companies)
Escrow and Others:
Montana Escrow Companies Licensing Info – https://banking.mt.gov/Consumer-Finance/Escrow-
Companies (if our MSB contemplates escrow services)
FFIEC BSA/AML Examination Manual – MSB Section – https://bsaaml.ffiec.gov/manual/MSBs (for
detailed regulatory expectations on MSBs, agents, compliance programs)
(The above sources provide full legal text or official guidance to support the analysis. They can be downloaded for
reference.)
Questions to Ask Counsel / Regulators
Finally, given the complexity and fact-specific nature of MSB compliance, here are critical questions our
Montana MSB should discuss with legal counsel or even pose to regulators (informally or via advisory
opinions):
Customer Locale: Where are my customers located and where do they receive funds? – This drives which
state licenses are needed. (E.g., “If we have a user in State X sending to State Y, do we need both
licenses?” – likely yes, but confirm specifics for edge cases.)
Business Model Specifics: Is our planned activity considered “money transmission” under State X’s law,
or do any exemptions apply? – For each major state, review the definitions. For instance, if the MSB
will only facilitate payments to merchants, ask counsel if the Agent-of-Payee exemption in those
states is applicable and what evidence is needed (e.g., ensuring contracts with merchants have
•
•
•
•
•
•
•
•
•
•
•
29
proper language). If the business involves crypto, ask how states treat that (some might not require
a license for crypto-to-crypto only transactions, others do if fiat is involved).
Licensing Thresholds: Are there any de minimis thresholds or limited scope scenarios that avoid
licensing? – Generally not for money transmission (no transaction volume exemption in most states),
but worth asking. For example, FinCEN has an exemption for MSBs with transactions under $1,000
that don’t charge a fee in certain situations, but it’s narrow. Confirm no state offers a “small
business” exception that could apply.
Agent Strategy: If we use an existing licensee’s services (or become an agent of a licensee), will
regulators deem us compliant or still expect our own license? – Get legal advice on structuring a “rent-a-
license” partnership. Some states require even agents to be individually licensed if they do more
than the principal’s scope, etc. Seeking a regulator’s informal input (through a no-action request) on
a proposed agent-of-licensee setup can provide comfort.
Bank Partnership Feasibility: Will a bank sponsorship fully cover our activities, and what will regulators
expect from us as a bank’s third-party service provider? – Discuss with counsel the OCC/FDIC guidance
on third-party relationships (e.g., OCC Bulletin 2020-10). Also, which bank? (Not all banks will work
with MSBs, and those that do will heavily diligence the program). Engaging early with a bank’s
compliance team or an experienced consultant can surface potential issues (like, if any part of the
service falls outside what the bank can do).
Montana and Other License Types: Beyond money transmission, are there other licenses we need for
our model? – For instance, if holding customer funds with interest, is that a banking/deposit activity?
(Probably not if no interest and just transmission.) If offering stored value, any consumer protections
(like escheatment of unclaimed funds) to plan for? If operating a marketplace escrow, do we
inadvertently need an escrow license in some state? These are nuances counsel can check.
Corporate Structure and Regulatory Footprint: Would it be beneficial to set up separate entities for
different activities (e.g., a licensed entity for transmission vs. a tech entity), or even obtain a charter (like a
trust charter) instead of 50 state licenses? – This is strategic: some fintechs opt for a New York trust
charter or other banking charter to preempt state-by-state licensing. Is that viable for our scale? It’s
a heavy lift but worth exploring with counsel if the business is national and handling crypto (for
example, Paxos and others went the NY trust route).
Engaging Regulators: Should we approach certain state regulators for clarification or a no-action letter
on our business plan? – In some cases, seeking an opinion from a regulator (with counsel’s help) can
clarify if you need a license. For example, California’s DFPI has an inquiry process for whether an
activity constitutes “money transmission.” If our model is novel, a proactive request could provide a
green light or reveal concerns.
Compliance Program Build-out: What aspects of compliance will regulators scrutinize most given our
model? – For instance, if using agents: agent monitoring and anti-fraud controls. If crypto: blockchain
analytics and OFAC controls. Knowing this can help allocate resources (perhaps hire a BSA officer
experienced in MSBs, implement a transaction monitoring system early, etc.). Counsel can share
insights from enforcement cases (like past consent orders against transmitters for compliance
failures) so we can avoid those mistakes.
•
•
•
•
•
•
•
30
Each of these questions will help tailor the legal and compliance strategy to the MSB’s specific facts. Given
the ever-evolving regulatory landscape (e.g., new states adopting the Model Law, federal proposals for
fintech charters), maintaining open dialogue with knowledgeable counsel and regulators is essential.
Disclaimer: This analysis is based on authoritative sources and current laws as of 2025 , but it is not
legal advice. MSB regulations are complex and fact-dependent; consultation with legal counsel is
recommended before operating nationwide. All citations above provide the legal grounding for the
statements made.
Money Transmitters
https://banking.mt.gov/moneytransmitters
Application of Money Services Business Regulations to a Company Acting as an
Independent Sales Organization and Payment Processor | FinCEN.gov
https://www.fincen.gov/resources/statutes-regulations/administrative-rulings/application-money-services-business
18 USC 1960: Prohibition of illegal money transmitting businesses
https://uscode.house.gov/view.xhtml?req=granuleid:USC-1999-title18-section1960&num=0&edition=1999
BSA Requirements for MSBs | FinCEN.gov
https://www.fincen.gov/bsa-requirements-msbs
MSB Exceptions | FinCEN.gov
https://www.fincen.gov/msb-exceptions
[PDF] NOTICE OF RULEMAKING ACTION TITLE 10. California ... - DFPI
https://dfpi.ca.gov/wp-content/uploads/sites/337/2020/03/PRO07-17-MTA-Agent-of-Payee-Regulations-Notice-of-Rulemaking-
Action-2.19.2020.pdf
Industry Letter - March 31, 2011: Money Transmitters with No Physical Presence in
New York | Department of Financial Services
https://www.dfs.ny.gov/industry_guidance/industry_letters/il20110331_money_transmitters_with_no_physical_presence_ny
Money Transmission in this State - DFPI
https://dfpi.ca.gov/rules-enforcement/laws-and-regulations/opinion-letters-by-law-subject/money-transmission-in-this-state-2/
Texas Finance Code Section 152.101 (2024) - Money Transmission License Required :: 2024 Texas
Statutes :: U.S. Codes and Statutes :: U.S. Law :: Justia
https://law.justia.com/codes/texas/finance-code/title-3/subtitle-e/chapter-152/subchapter-c/section-152-101/
Money Services Businesses | Texas Department of Banking
https://www.dob.texas.gov/money-services-businesses
Chapter 560 - MONEY TRANSMITTERS\' CODE :: Florida REGULATION OF TRADE, COMMERCE,
INVESTMENTS, AND SOLICITATIONS :: 2005 Florida Code :: Florida Code :: U.S. Codes and Statutes :: U.S.
Law :: Justia
https://law.justia.com/codes/florida/2005/TitleXXXIII/ch0560.html
idfprapps.illinois.gov
https://idfprapps.illinois.gov/Forms/Brochures/DFI%20Currency%20Exchange%20Section.pdf
15 18
1 11 12 13 14 48
2 9 32 40 41 50 51
3 7
4 5 6 46 53
8
10
15 16 17 19 20 37
18 34
21 22
23 35
24 28
25
31
Third-Party Payment Processors No Longer Require Money ...
https://idfpr.illinois.gov/news/2015/thirdpartyprocessornotice07292015.html
[PDF] CSBS Money Transmission Modernization Act (MTMA)
https://www.csbs.org/print/pdf/node/231461
What is an Agent of the Payee Exemption? - Modern Treasury
https://www.moderntreasury.com/learn/what-is-an-agent-of-the-payee-exemption
6-1202 - Exemptions
https://www.azleg.gov/ars/6/01202.htm
Funds Transfers Recordkeeping - BSA/AML Manual
https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/09
Money Services Business (MSB) Agent List | FinCEN.gov
https://www.fincen.gov/money-services-business-msb-agent-list
Codes Display Text
http://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=FIN&division=1.2.&title=&part=&chapter=1.&article=
California Finalizes Rulemaking for Agent-of-a-Payee Exemption in ...
https://www.cooley.com/news/insight/2021/2021-06-28-california-rulemaking-agent-of-a-payee-exemption-money-transmission-
licensing
26
27
29 31
30 38 42 49
33
36 52
39 47
43 44 45
32
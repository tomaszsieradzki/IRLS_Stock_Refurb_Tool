IRLS MASTER RULES — COMPLETE SYSTEM SPECIFICATION (UNIFIED VERSION)



====================================================

0\. PURPOSE OF THE SYSTEM

========================



IRLS is a workflow‑driven refurbishment management system controlling the full lifecycle of used machines:

Inbound → Verification → Offers → Decision → Repair → Sale → Shipment → Closure



System replaces Excel + email communication and focuses on:



\* deadline control

\* responsibility tracking

\* cost \& margin control



THIS IS NOT A WAREHOUSE SYSTEM.

This is a PROCESS CONTROL SYSTEM.



Every action:



\* has an owner

\* changes status

\* generates notification



====================================================



1\. MACHINE LIFECYCLE (GLOBAL FLOW)

&nbsp;  ====================================================

&nbsp;  INBOUND

2\. Machine added

3\. Transport in progress

4\. Pending Verification

5\. Verification in progress

6\. Waiting for offer

7\. Offer prepared

8\. Waiting for manager decision



REFURBISHMENT

8\. Approved for repair

9\. In repair

10\. Waiting for parts

11\. Repair finished

12\. Ready



OUTBOUND

13\. Sold / Ready for sale

14\. Preparing shipment

15\. In transport

16\. Delivered

17\. Closed



System reminder:

Pending Verification → every 5 days (summary notification)



====================================================

2\. VERIFICATION (CHECK‑IN)

==========================



Technician workflow:



1\. photos first (40+ allowed)

2\. checklist

3\. description



Verification may end WITHOUT offer → status READY

Offers created later on desktop using photos



====================================================

3\. OFFERS

=========



Two independent types:

INTERNAL — technicians

OTHER — external partner (e.g. paint shop)



External offer contains 3 ranges:

LOW / MEDIUM / HIGH

(not alternatives — levels of refurbishment)



Parallel offers allowed (internal + external)

Manager chooses one or rejects both



Manager permissions:



\* accept

\* reject

\* remove items before accept

&nbsp; Manager DOES NOT build offers



====================================================

4\. OFFER VERSIONING

===================



Each modification = new version

History stored: who / when / what changed

Old version status: BEFORE AMENDMENTS



Price change rules:

≤ 500 PLN → auto approved



> 500 PLN → requires manager approval again



Statuses:

Draft

Waiting decision

Approved

Before amendments

Closed not selected



====================================================

5\. MACHINE CYCLES

=================



Machine may return multiple times

Each return = NEW CYCLE



STRICT RULE:

Costs, invoices and profits CANNOT mix between cycles



====================================================

6\. FINANCE (CORE LOGIC)

=======================



Purchase:

trade‑in price



Sale prices:

transfer price

list price

final customer price



Costs included in profit:



\* parts

\* labor

\* external services

\* inbound transport

\* outbound transport

\* internal transports

\* cranes / loading / washing / operations

\* all invoices



System calculates:

profit value

profit %



Red Flags:

Green ≥ 30%

Orange 15‑29.9%

Red < 15%

Dashboard shows colors without details



====================================================

7\. INVOICES

===========



One invoice may be split between machines:

Example:

Invoice 123

→ IRLS‑001 Cycle 2 (40%)

→ IRLS‑005 Cycle 1 (60%)



FORBIDDEN:

Assign same invoice to two cycles of the same machine



====================================================

8\. LOCATIONS \& TRANSPORT HISTORY

================================



Manual location list

Machine stores:



\* current location

\* transport history



Location change may be:

physical transport

manual correction



====================================================

9\. INBOUND \& OUTBOUND LOGISTIC FIELDS

=====================================



Inbound:



\* incoterms

\* carrier

\* arrival date

\* comments

\* invoice paid (yes/no)

\* invoice booked (yes/no)



Outbound:



\* incoterms

\* customs agency

\* customs procedure number

\* invoice number

\* invoice paid (yes/no)

\* invoice booked (yes/no)



====================================================

10\. INCOTERMS

=============



Stored for each transport (inbound \& outbound)

Examples: EXW, FCA, FOB, CIF, DAP, DDP



====================================================

11\. NOTIFICATIONS (EVENT DRIVEN)

================================



Push PWA notifications for:



\* machine arrived

\* verification required

\* offer required

\* offer accepted/rejected

\* repair finished

\* shipment planned

\* customs deadline approaching

\* status change

\* pending > 5 days summary



Mobile first — no app store required



====================================================

12\. MOBILE VS DESKTOP RESPONSIBILITIES

======================================



Phone:

photos

checklists

quick updates



Desktop:

offers

decisions

analysis

management



====================================================

13\. USER ROLES \& PERMISSIONS (LEVELS)

=====================================



Level 1 – External Company (e.g. paint shop)



\* prepare offer only

\* notification: machine waiting for offer

\* notification: offer accepted



Level 2 – Technician



\* verification

\* notification: verification required

\* notification: offer accepted



Level 3 – Logistics



\* manage transports

\* add machines

\* edit stock

\* comments

\* incoterms

\* customs

\* invoices paid/booked

\* deadlines control



Level 4 – Manager



\* full operational edit

\* no system settings



Level 5 – Administrator



\* system settings

\* user management

\* roles



Global system roles (database enum lowercase):

admin / ops / finance / viewer



====================================================

14\. SAP NUMBER

==============



Optional field: SAP Machine Number

Entered manually in dashboard



====================================================

15\. CURRENCIES

==============



PLN / EUR / USD



====================================================

16\. BACKEND TECHNICAL RULES

===========================



\* roles enum lowercase only

\* bcrypt via passlib

\* password max 72 bytes

\* scripts run as module: python -m app.scripts.create\_admin

\* sessionmaker SessionLocal

\* Swagger always available



====================================================

17\. DEVELOPMENT PRINCIPLES

==========================



No feature without process stage mapping

Each feature must answer: which workflow stage does it control?



Priorities:

1 deadlines control

2 responsibility control

3 cost control

4 UI convenience



====================================================

18\. MAIN IDEA

=============



Not CRM

Not ERP

Not warehouse



System controlling machine flow and business decisions




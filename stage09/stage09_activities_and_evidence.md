# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: Group 1 / Thursday at 2.30 pm
Members and responsibilities: Rylan - Pengi376, Tomas - Tom-uc3, Barry - BarrytheLegoMan;
Stage 8 integrated SHA, command, working directory and actual result: Stage 8 SHA= a3feb86 


## A. Tutorial activities

### A1 Session state classification

| Information            | Required session/domain or transient state? | Requirement or reason                                            |
|------------------------|---------------------------------------------|------------------------------------------------------------------|
| Patient identity       | domain state                                | as it is a permanent database record                             |
| Appointment history    | domain state                                | as it has to stay in the database                                |
| Temporary menu choice  | transient state                             | UI only logic                                                    |
| Practitioner specialty | domain state                                | as it is stored with the other practitioner data in the database |
| Debug print output     | transient state                             | it vanishes the moment the terminal window closes                |
| Appointment status     | domain state                                | as the state of the appointment is stored in database            |

What is intentionally lost on exit?: anything in the transient state which is effectively everything not stored in the database.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types                                                  | Outputs                                                                                                                                                                | Responsibility and validation           | Domain source / existing constraint |
|-----------------------|----------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------|-------------------------------------|
| appointment_sort_key  | appointment ID = str, appointment_date_time = datetime                     | appointment list based on key                                                                                                                                          | Sorts appoinments based on entered key. |                                     |
| select_appointments   | appointment ID = str                                                       | appointment with same ID entered                                                                                                                                       | finds appointment based on ID           |                                     |
| Service listing       | Menu option = str                                                          | register patient, find patient, register practitioner, find practitioner, book appointment, cancel appointment, find appointment, list practitioner appointments, EXIT | to be able to pick a service on menu.   |                                     |
| Console               | service required = str, patient data, practitioner data, appointment data. | it outputs the desired menu task.                                                                                                                                      | to be able to use the services          |                                     |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: <!-- response -->

### A3 Responsibility violations

| Conceptual case                 | Violation                                              | Correct boundary and reason                                                                 |
|---------------------------------|--------------------------------------------------------|---------------------------------------------------------------------------------------------| 
| Appointment.cancel reads input  | it should just cancel appointment                      | console should be the only one reading inputs and controlling functions based off of inputs |
| Service prints/reads the menu   | service shouldn't do that.                             | service should just provide services                                                        |
| Query sorts its source in place | not having appointmens sorted alread                   | the appointments should already be sorted prior to selecting them.                          |
| Store prints Appointment saved  | appointment saved being printed does not help the user | Store appointment should return appointment                                                 |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)` 
, predict source order, return value and result identity. Give a meaningful mutation check: The source order for '.sort()' will order this list from lowest number to higher based on app ID, the return value will be none.
Where as 'sorted()' will leave the original list unchanged, instead the sorted list is stored as result thus also being the return value. And the result identity is not in appointments as it is a new list.
using the (.sort) method it mutates the original list so here is a mutation check for the sorted method.

before = appointments.copy()

result = sorted(appointments, key=appointment_sort_key)

assert appointments == before
assert result is not appointments


Score-example prediction and explanation of passing the named key: score example prediction is that it scores and sorts appointments from lowest id number to highest.
Passing the named key key=appointment_sort_key passes the function itself to sorted(), so Python can call that function on each item and use the returned value as the sorting key.

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion:
Cancel an appointment by changing its status from `SCHEDULED` to `CANCELLED`; do not delete the record, because SmartCare needs the appointment history for reports. To verify retention in the current session, cancel a booked appointment and look it up by ID through a service using the same data store; assert the returned object is the original appointment and its status is `CANCELLED`. Then verify the default practitioner listing (no status filter) still includes that appointment and includes appointments of other statuses. Finally, request the `SCHEDULED` filter and assert it contains only scheduled appointments, excluding the cancelled one (and any completed appointments). These checks demonstrate lookup and listing behavior; they do not imply the data persists after the in-memory session ends.


## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: <!-- response -->

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|-------------|----------------------|-------------------------------------|--------------------------|-----------------|
|             |                      |                                     |                          |                 |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: <!-- response -->

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| | | | | |

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: <!-- response -->
What the tests do and do not establish: <!-- response -->

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | | | | |
| UI-02 invalid-input recovery | | | | |
| Automated service workflow | | | | |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: <!-- reference -->
Actual prompt/context supplied: <!-- paste or accessible reference -->
Actual response: <!-- accessible reference -->

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| | | | | | |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: <!-- response -->

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? <!-- response -->
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->
3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- response -->

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? <!-- response -->
2. Which explicit inputs are needed, and why avoid a global store? <!-- response -->
3. How can a new list reuse Appointment objects safely? <!-- response -->
4. Why use a named key, and what breaks equal-time ties? <!-- response -->
5. How do default and explicit status filters differ? <!-- response -->
6. How do empty, unknown practitioner and invalid filter cases differ? <!-- response -->
7. Which console errors recover, and how is unchanged state checked? <!-- response -->
8. What is data integrity for registered participants, conflicts and history? <!-- response -->
9. What is Copilot's review role, and who verifies findings? <!-- response -->
10. How do pure functions and OOP responsibilities work together? <!-- response -->

## H. Review, completion and common handover

Issues and bounded branches: <!-- links -->
PR/diff and another-member human reviewer: <!-- actual links/name -->
Review responses and Copilot comparison: <!-- links -->
Integrated common Stage 9 SHA: <!-- complete -->
Full regression command, working directory, actual count/result and evidence: <!-- complete -->
README run instructions and scope/limitations: <!-- link -->
Unresolved issues and support/action: <!-- complete -->
UG common candidate / PG future branch plan: <!-- complete -->

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.

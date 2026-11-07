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

The query takes the appointment collection, requested practitioner ID and optional `AppointmentStatus` as explicit inputs. `None` means include every status; an explicit enum filters by that exact status. It returns a newly allocated list of the original appointment objects, ordered by the named `(date_time, appointment_id)` key.

| Requirement                                                                                              | Input / session data                                                         | Operation and responsible component                                                          | Expected result or error                                                                                                    | Test / evidence                                                    |
|----------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| Only the requested practitioner's appointments, with another practitioner as a control                   | Appointment list containing `D1` and `D2` records; query `D1`                | `select_appointments` filters by practitioner ID                                             | Only `D1` appointments are returned                                                                                         | `test_select_appointments_filters_practitioner_and_status`         |
| Default all statuses; each explicit enum status; no-match status produces an empty result                | Records in `SCHEDULED`, `CANCELLED` and `COMPLETED`; explicit enum or `None` | `select_appointments` includes all when status is `None`, otherwise filters by enum identity | Default includes all statuses; each explicit filter includes only its status; a status with no match returns `[]`           | `test_select_appointments_filters_practitioner_and_status`         |
| Date/time ordering and equal-time appointment-ID tie-break, with source order and fields unchanged       | Unsorted appointments, including equal times                                 | Query filters then sorts with `appointment_sort_key`; sorting is non-mutating                | Result is ordered by time then ID; source order and appointment fields are unchanged                                        | `test_select_appointments_orders_without_mutating_source`          |
| Repeat unchanged inputs; inspect code for hidden state, input/output and side effects                    | Same explicit list and query arguments used repeatedly                       | Pure `select_appointments` function                                                          | Repeated calls give equivalent results in distinct lists; inspection confirms no hidden state or I/O and no source mutation | `test_select_appointments_returns_fresh_lists_and_repeats_cleanly` |
| Distinct returned list for empty, already-sorted and unsorted inputs; contained objects remain unchanged | Empty, sorted and unsorted appointment lists                                 | `select_appointments` creates and sorts a filtered list                                      | Each call returns a distinct list; existing appointment objects are retained by identity and source remains unchanged       | `test_select_appointments_returns_fresh_lists_and_repeats_cleanly` |
| Test the named key directly and check sorting actually uses it                                           | Appointment and query input                                                  | `appointment_sort_key` defines the ordering tuple and is passed as the sort key              | Direct call returns `(date_time, appointment_id)`; query invokes the named key                                              | `test_appointment_sort_key_and_query_use_named_key`                |


An empty result is valid when a registered practitioner has no matching appointments; an unknown practitioner raises `LookupError`, while a blank ID or non-`AppointmentStatus` filter raises `ValueError`. The service API requires an enum value and does not convert strings; the interactive menu is not implemented, so UI enum conversion and UI-01–02 are not claimed as verified here. Query results contain the original appointment objects in a new list. Expected errors propagate, and tests verify rejected requests do not add records; cancellation changes status but preserves the retrievable appointment history.

## C. Implementation and query verification

| Requirement / test ID                                                        | Code location                                                     | Case and meaningful assertion                                                                                                                                                    | Actual result                                                                     | Evidence link                                                                                                           |
|------------------------------------------------------------------------------|-------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| QRY-01/02: practitioner isolation, default all statuses and each enum status | `project/smartcare/queries.py`; `project/tests/test_queries.py`   | D1 results exclude D2; `None` includes SCHEDULED, CANCELLED and COMPLETED; each enum returns only its status; unmatched status returns `[]`                                      | Passed                                                                            | `test_select_appointments_filters_practitioner_and_status`                                                              |
| QRY-03: date/time order, equal-time ID tie-break, non-mutation               | `project/smartcare/queries.py`; `project/tests/test_queries.py`   | Earlier time sorts first; equal times sort by ID; assert source order and appointment fields are unchanged and returned elements are the original objects                        | Passed                                                                            | `test_select_appointments_orders_without_mutating_source`                                                               |
| QRY-04 / FP-01–03: named key, repeat calls, fresh lists and purity           | `project/smartcare/queries.py`; `project/tests/test_queries.py`   | Direct key tuple check; instrument the named key to prove query reuse; repeated calls on empty, sorted and unsorted inputs return distinct lists and preserve source/objects     | Passed; code inspection confirms no hidden state, input/output or source mutation | `test_appointment_sort_key_and_query_use_named_key`; `test_select_appointments_returns_fresh_lists_and_repeats_cleanly` |
| Service lookup/filter errors and known-empty result                          | `project/smartcare/services.py`; `project/tests/test_services.py` | Registered practitioner with no appointments returns `[]`; unknown ID raises `LookupError`; blank ID and non-enum status raise `ValueError`; invalid requests do not add records | Passed                                                                            | `test_list_practitioner_appointments_known_empty_and_invalid_inputs`                                                    |
| FR-08: cancelled history retained and scheduled-only exclusion               | `project/smartcare/services.py`; `project/tests/test_services.py` | Cancellation returns the same appointment; ID lookup and default listing retain it; SCHEDULED listing excludes it; store still contains the record                               | Passed                                                                            | `test_list_practitioner_appointments_retains_cancelled_history`                                                         |


Purity explanation from code inspection, including absence of hidden state and I/O: `appointment_sort_key` only reads an appointment's `date_time` and `appointment_id` and returns them as a tuple. `select_appointments` uses only its explicit arguments to build a filtered list and passes the named key to `sorted()`, which produces a separate list. Neither function changes the source list or appointment objects, stores state, reads input, writes output, or accesses the data store.
What the tests do and do not establish: The query tests verify representative practitioner/status filters, sorting including equal-time ID tie-breaks, source and field preservation, object identity, a distinct result for empty/sorted/unsorted inputs, repeated calls, and named-key reuse. Service tests verify known-empty, unknown and invalid requests and that cancelled history remains retrievable/listable but is excluded from SCHEDULED results. A scripted menu test exercises all menu choices, session-store reuse and selected recovery cases. These tests establish the asserted behavior for their cases; they do not prove all possible inputs or runtime conditions, nor replace a manual interactive demonstration.

## D. Integrated console and workflow evidence

| Scenario / acceptance ID               | Reproducible inputs / artefact                                                                                                                        | Expected result                                                                                     | Observed result and state check                                                                                                                                                 | Evidence link                                                                                   |
|----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| UI-01 menu workflow across all choices | `project/tests/test_console.py::test_menu_reuses_session_store_and_recovers_from_invalid_commands` scripted inputs                                    | Register/find patient and practitioner; book, cancel, find and list an appointment; exit            | Choices 1-8 and 0 exercised. One store retained one patient, practitioner and cancelled appointment across commands; lookup and all-status listing showed retained cancellation | `PYTHONPATH=. ../../.venv/bin/python -m pytest -q tests/test_console.py`                        |
| UI-02 invalid-input recovery           | Same scripted menu test: duplicate patient/practitioner/appointment IDs, malformed date, unknown patient/practitioner, invalid status, unknown choice | Display expected errors and continue; rejected registration/booking does not replace or add records | Menu continued to exit; original participant names remained and only the valid appointment was stored                                                                           | `test_menu_reuses_session_store_and_recovers_from_invalid_commands`                             |
| Automated service workflow             | `project/tests/test_queries.py`; `project/tests/test_services.py`                                                                                     | Query filtering/order/purity and service listing, errors and cancellation history                   | Focused query/service run: 17 passed                                                                                                                                            | `PYTHONPATH=. ../../.venv/bin/python -m pytest -q tests/test_queries.py tests/test_services.py` |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: <!-- reference -->
Actual prompt/context supplied: Act as a query and console integration reviewer for SmartCare.
Review the supplied code and tests for:
1. explicit inputs, purity and source non-mutation;
2. domain, service, data-store and console responsibilities;
3. validation and recovery without partial state changes;
4. correct object identity, enum filtering and ordering;
5. retained history and integrity risks;
6. missing query, workflow and console tests.
Do not redesign the domain or add storage/frameworks.
Do not invent fields or requirements or delete cancelled history.
Separate observed evidence from optional improvements.
Rank findings as Critical, Important or Optional.
For each finding, identify the code/test evidence to check
Actual response: 
Review result: No Critical findings. The query is pure for valid inputs, returns a fresh sorted list containing the original appointment objects, and filters statuses by enum identity. The service validates practitioner and status inputs; the console delegates workflows to services and catches expected ValueError/LookupError without broad exception handling. The full suite passes: 43 passed.
Important — integration-test coverage is incomplete. The console test test_menu_reuses_session_store_and_recovers_from_invalid_commands in project/tests/test_console.py covers session reuse, valid workflows, malformed date format, duplicates, unknown participants, invalid status, and unknown choice. It does not cover impossible calendar dates, blank menu inputs, unknown appointment lookup/cancellation, repeated cancellation, or menu recovery after a booking conflict. Service tests cover some of these separately, but not the complete menu recovery path. Also missing from that menu scenario: rejecting a conflicting booking, successfully booking the freed slot after cancellation, and booking at the same time with another practitioner. Check project/smartcare/console.py:132-183 and the relevant service tests in project/tests/test_services.py.
Optional — direct-query invalid-filter behavior. select_appointments in project/smartcare/queries.py:16-33 assumes status is AppointmentStatus | None; a string passed directly will silently produce no matches. The service rejects non-enum values at project/smartcare/services.py:149-169, so normal service/menu use is guarded. If the query itself is intended to reject invalid runtime arguments, add a direct-query test for that contract.
Integrity and responsibility evidence: The store checks that appointments use the actual registered participant objects (project/smartcare/data_store.py:66-87); the service handles booking conflicts and cancellation transitions (project/smartcare/services.py:88-147); cancellation updates status without removing the stored appointment (project/smartcare/domain.py:129-137). The query tests verify filtering, ordering, object identity, and source non-mutation (project/tests/test_queries.py). No deletion or storage/framework changes are indicated.

| AI finding                                                                                                                                                                                                                      | Code/test evidence                                                                                                                                                                  | Severity  | Accept/Modify/Reject and reason                                                                 | Change or no change                                                     | Actual verification                                                                                                    |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|-------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| Query implementation is pure for valid inputs, returns a fresh ordered list of original objects, and filters statuses by enum identity.                                                                                         | `project/smartcare/queries.py:9-33`; `project/tests/test_queries.py`                                                                                                                | Optional  | reject: no need at the moment                                                                   | No change.                                                              | Full suite: `PYTHONPATH=. ../../.venv/bin/python -m pytest -q` from `project/` — 43 passed.                            |
| Console delegates to services, catches expected validation/lookup errors, and preserves cancellation history.                                                                                                                   | `project/smartcare/console.py:72-183`; `project/smartcare/services.py`; `project/smartcare/domain.py:129-137`; `project/tests/test_console.py`; `project/tests/test_services.py`    | Optional  | reject : no need at the moment                                                                  | No change.                                                              | Full suite: 43 passed; scripted menu test confirms one store is reused and cancelled record remains findable/listable. |
| Menu recovery coverage missed impossible dates, blank inputs, unknown appointment lookup/cancellation, repeated cancellation, and conflict recovery; workflow coverage omitted freed-slot and different-practitioner booking.   | `project/tests/test_console.py::test_menu_recovers_from_blank_unknown_and_impossible_date_inputs`; `test_menu_handles_conflicts_freed_slots_and_repeated_cancellation`              | Important | Accept; these cases needed scripted menu-level coverage to verify recovery and unchanged state. | Added two scripted menu tests; no production-code change was needed.    | Focused menu tests: `PYTHONPATH=. ../../.venv/bin/python -m pytest -q tests/test_console.py` — 3 passed.               |
| Direct `select_appointments` calls with a non-enum status silently return no matches; service listing rejects such values.                                                                                                      | `project/smartcare/queries.py:16-33`; `project/smartcare/services.py:149-169`; `project/tests/test_services.py::test_list_practitioner_appointments_known_empty_and_invalid_inputs` | Optional  | reject                                                                                          | None`; no requirement for direct invalid-query handling is established. | No change.                                                                                                             | 

Responsibility check:
Domain objects enforce local validity and guarded appointment status transitions. `SmartCareDataStore` owns the session's collections and checks uniqueness and that appointments reference the registered participant objects. Services coordinate lookups, bookings, conflict checks, cancellation and listing through that shared store without duplicating domain rules. Query functions take explicit collections and filters, return sorted fresh lists, and do not perform I/O or mutate source data. The console owns prompts, status-string conversion, formatting and user-facing error recovery; it creates one store and one set of services for the menu session, and calls the service APIs rather than changing records directly.

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail?
The architectural concern was ensuring that the console, all services and the appointment query work through the same session-scoped data store. This preserves shared records and participant object identity across commands, while keeping state transitions and conflict rules in the domain/service layers.
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->
3. How did you prove cancelled appointments remain retrievable and listable in the same session? In the service test, I booked and cancelled an appointment, then asserted cancellation returned the original object, lookup by its ID returned that same object, and the default practitioner listing still included it. I also checked that the `SCHEDULED` filter excluded it while the store still contained it. The scripted menu test additionally verifies that one shared store is used across commands and that cancelled history remains available before exit.

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? It depends only on its explicit appointment list, practitioner ID and optional status, then returns a new sorted list without changing the source list or appointments or doing I/O. Mutating the input list (for example, sorting it in place) or an appointment would break purity; so would reading input, printing, or accessing hidden global/store state.
2. Which explicit inputs are needed, and why avoid a global store? Pass the appointment list, requested practitioner ID and optional `AppointmentStatus` (`None` means all statuses). Explicit inputs make the query's dependencies clear, allow it to be tested with different collections and filters, and prevent hidden coupling to shared mutable state or another session's data.
3. How can a new list reuse Appointment objects safely? Build a new list containing references to the matching stored appointments, then sort that list rather than the source. Callers can reorder or clear the result without affecting the source collection, while the shared appointment identities and status/history remain intact.
4. Why use a named key, and what breaks equal-time ties? A named `appointment_sort_key` keeps the ordering rule in one reusable, directly testable function and lets the query sort consistently with `key=appointment_sort_key`. It returns `(date_time, appointment_id)`: the appointment ID provides a deterministic tie-break when two appointments have the same date and time.
5. How do default and explicit status filters differ? With `status=None` (the default), the query includes all matching appointments regardless of whether they are `SCHEDULED`, `CANCELLED` or `COMPLETED`. An explicit `AppointmentStatus` returns only appointments whose status is that enum member; for example, `SCHEDULED` excludes cancelled and completed history.
6. How do empty, unknown practitioner and invalid filter cases differ? A registered practitioner with no appointments matching the filter is a valid request and returns `[]`. An unregistered practitioner ID raises `LookupError`; a blank ID or a filter that is not `None` or an `AppointmentStatus` raises `ValueError` through the service. The console converts recognized status text to the enum and reports invalid status text as a `ValueError` without leaving the menu.
7. Which console errors recover, and how is unchanged state checked? The menu reports `ValueError` for blank or duplicate IDs, invalid fields/statuses, malformed or impossible date/time, conflicts and illegal repeated cancellation, and `LookupError` for unknown records; it reports unknown menu choices and returns to the menu. Scripted console tests inspect the shared store after rejected actions to confirm original registrations and appointments remain, no rejected booking was added, and later valid commands still work.
8. What is data integrity for registered participants, conflicts and history? Booked appointments must reference the actual patient and practitioner objects registered in the shared store, and duplicate IDs or a same-practitioner/time conflict with another `SCHEDULED` appointment are rejected without adding a record. Cancellation changes the appointment status rather than deleting it, preserving the original appointment and participant links for retrieval and all-status history listing; only a `SCHEDULED` appointment can be cancelled.
9. What is Copilot's review role, and who verifies findings? Copilot can offer a second-pass review by identifying potential behavior, responsibility and test-coverage issues with code/test evidence. Its findings are suggestions, not proof: I check them against the requirements and implementation, decides whether to accept or reject them, makes any changes, and verifies those changes with focused tests and regression checks.
10. How do pure functions and OOP responsibilities work together? OOP keeps appointment invariants and guarded state transitions in domain objects, collections and participant identity in the shared store, and workflows in services. Pure query functions complement these objects by taking explicit data and returning ordered results without changing stored state; the console coordinates user interaction and calls services and queries through their contracts.

## H. Review, completion and common handover

Issues and bounded branches: N/a
PR/diff and another-member human reviewer: <!-- actual links/name -->
Review responses and Copilot comparison: <!-- links -->
Integrated common Stage 9 SHA: f5f8c2c
Full regression command, working directory, actual count/result and evidence: Working directory: `st1-assignment-3/project/`. Command: `PYTHONPATH=. ../../.venv/bin/python -m pytest -q`. Actual result: `45 passed`. Evidence: pytest output from the full regression run; tests include domain, service, query and scripted console coverage.
README run instructions and scope/limitations: See [`project/README.md`](../project/README.md) for `python main.py`, `python main.py --interactive`, and `python -m pytest` commands (run from `project/`). Stage 9 supports in-memory registration, lookup, booking, cancellation and practitioner appointment listing; the interactive session discards data on exit. Use synthetic data only. Persistence, rescheduling, assurance, past-date checks, duration rules checks are out of scope.
Unresolved issues and support/action: N/A
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

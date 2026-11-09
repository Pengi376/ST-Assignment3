# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: Group 1 / Thursday at 2.30 pm
Members and UG/PG cohorts: Rylan - Pengi376, Tomas - Tom-uc3, Barry - BarrytheLegoMan;

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

| Statement                                                         | Classification   | Reason                                                                                                                                                                                           |
|-------------------------------------------------------------------|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Appointment disappears after cancellation.                        | Symptom          | It describes what is seen when the system is used and does not say why it happens. It goes against FR-07, which says cancelled history must be retained.                                         |
| The data-store removal path is probably being called.             | Hypothesis       | The word "probably" shows it is a guess about the cause that has not been tested. It can be tested by checking data_store.py and services.py, as SmartCareDataStore has no public delete method. |
| The failing test shows store.find_appointment('A1') returns None. | Evidence         | It is an observed result from running a test and can be repeated. It supports the symptom but does not explain the cause.                                                                        |
| The service layer is badly designed.                              | Opinion          | It is a general judgement with nothing observed or testable behind it, and it doesn't explain this failure.                                                                                      |
| Traceback points to smartcare/services.py line 42 in the example. | Evidence         | A traceback is recorded output showing where the failure appeared. It shows the location, not the cause, and the line number must be checked in the actual run.                                  |

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Scenario chosen: cancelled history.
- Requirement used: FR-06 and FR-07 (AC-05.1 and AC-05.2). A SCHEDULED appointment changes to CANCELLED and the cancelled appointment must remain retrievable in the current session.
- Expected behaviour: after cancel_appointment('A1'), find_appointment('A1') returns the same appointment with status AppointmentStatus.CANCELLED.
- Observed behaviour: after cancellation, find_appointment('A1') raises LookupError('Appointment not found') or the store returns None.
- Minimal reproduction: create a new SmartCareDataStore, register patient P1 and practitioner D1, book A1 at 2027-04-23 11:00, cancel A1, then look up A1.
- Hypothesis: the cancel path removes the appointment from the stored appointments, or a lookup hides appointments that are not SCHEDULED.
- Evidence to inspect: cancel_appointment in services.py and cancel in domain.py; any del, pop or filtering of _appointments in data_store.py; the exact failing assertion and traceback; whether list_appointments() still contains A1 (this separates deleted from hidden).

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

- Cancelled appointment test: the test should be changed. FR-07 says history must be retained, so the test is expecting behaviour that is not required. The product code should not be changed to match it. The test should check that the appointment can still be found after cancellation and that its status is CANCELLED.
- Different practitioners at the same time: this test does not reflect AC-04.2. The conflict rule only applies to the same practitioner at the same time (has_practitioner_conflict compares practitioner_id, date_time and SCHEDULED status), and AC-04.2 allows different practitioners at the same time. This test is also a test defect.
- Not every failing test is correct. The requirement decides whether the test or the code is wrong.

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Smells and proposed refactorings:

| Smell | Why it is a problem | Small refactoring |
|-------|---------------------|-------------------|
| Duplicate status strings | A typing mistake would fail silently and any change has to be made in many places | Replace with the existing AppointmentStatus enum |
| Direct collection manipulation | Bypasses the SmartCareDataStore checks for types and duplicate IDs | Use add_appointment, find_appointment and list_appointments |
| Printing inside the service | Mixes user output with business logic and makes testing harder | Return a value or raise an error and leave printing to console.py |
| Validation mixed with workflow | The method does several jobs so it is hard to read and test | Rely on the domain and store validation or extract a small helper |
| Four nested conditionals | Hard to follow and easy to break | Use early raises (guard clauses) and extract a conflict helper |

Classification of the proposed changes:

| Proposed change | Classification | Reason |
|-----------------|----------------|--------|
| Rename appt to appointment | Refactoring | Only the name changes, behaviour stays the same |
| Extract a repeated conflict helper | Refactoring | Same logic in one place with the same results and errors |
| Add rescheduling | Feature | It is new behaviour that is not in the current requirements |
| Restore retained cancellation lookup | Repair | It fixes behaviour that breaks FR-07 so the observable behaviour is changed back to what is required |
| Replace a magic status string with the existing enum | Refactoring | Same value and meaning using the existing type |

Behaviour that must remain unchanged: the same return values, the same exception types and messages (ValueError and LookupError), cancelled appointments still retained, the same conflict rule (same practitioner, same time, SCHEDULED only), state left unchanged when an operation fails, and the full test suite still passing before and after each step.

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: Changing code straight away means the fix is only a guess. It may hide the symptom while the cause is still there, or break something that worked. Without an expected behaviour from a requirement, a reproduction and a hypothesis there is no way to know if the fix worked or why. It also risks changing correct code when the test or the expectation was the real problem. Working out the cause first and then making the smallest change is safer.

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: f5ee9ce (tested Stage 7 main SHA from the Stage 7 record). Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
- Baseline test command / working directory / observed result / evidence: python -m pytest, project/, 
collected 36 items                                                                                                                                                             

tests\test_domain.py ....                                                                                                                                                [ 11%]
tests\test_services.py ...........                                                                                                                                       [ 41%]
tests\test_starter.py .....................                                                                                                                              [100%]

============================================================================= 36 passed in 0.16s ==============================================================================
- Clean preparation SHA if a record-only commit followed Stage 7: a3feb86b918ce7b967a45fdbd12fa8e378150449 (the baseline Git SHA reported by the tool). Two record-only commits followed f5ee9ce: 14b5887 changed only stage07/stage07_activities_and_evidence.md and a3feb86 changed only stage08/stage08_activities_and_evidence.md (checked with git diff --stat), so the code is the same as f5ee9ce.
- Branch and preparer / how teammates obtained this branch: debug/stage08, created from main with git checkout -b debug/stage08 and pushed to origin (https://github.com/Pengi376/ST-Assignment3). Preparer: Rylan (Pengi376). Teammates obtain it with git fetch and git checkout debug/stage08.
- Downloaded tool version, source SHA256 and --check outcome: prepare_debugging.py, Stage 8 tool 1.1, kept outside the repository (C:\Users\rylan\Downloads\challenge). Baseline project SHA256 986c5445532ffd1d85e88639b6b6f34b84e15b2bbfc1882511a96938c3b641f6. python prepare_debugging.py project --check: preflight PASS, project unchanged, both proposed fault signatures verified in a temporary copy.
- --apply and --verify output summaries / artefact references: --apply: PREPARED F8-01 practitioner conflict; F8-02 retained-history lookup; verified expected failures test_f8_01_conflict and test_f8_02_history (2 failed); backup and hash recorded in .stage8_faults. --verify: VERIFIED exactly 2 expected failures, both approved symptom signatures present.
- Bounded diff inspected and recovery location (not committed): git diff showed only project/smartcare/data_store.py changed (11 insertions, 18 deletions), in find_appointment and has_practitioner_conflict. Recovery backup is in project/.stage8_faults, which is listed in .gitignore and was not committed. It is for setup recovery only and was not used to repair the code.
- Prepared faulty-state commit SHA: c549c68 ("Prepare Stage 08 Debug") on debug/stage08.
- Preparation or recovery issues and resolution, if any: The first run of the tool omitted the project argument and gave a usage error. It was re-run with project and --check, --apply and --verify. No recovery was needed. Git warned that LF would be replaced by CRLF in data_store.py; this did not affect the commit.
- Initial prepared full-suite command / result / key failures: python -m pytest -q, project/, 4 failed, 32 passed in 0.41s. Failures: tests/test_starter.py::test_conflict_rule_and_different_practitioner (DID NOT RAISE ValueError); tests/test_starter.py::test_cancelled_appointment_remains_retrievable, tests/test_services.py::test_cancel_appointment_twice_raises_value_error and tests/test_starter.py::test_cancel_appointment_twice_raises_value_error (all LookupError: Appointment not found).

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: A second appointment for the same practitioner at the same date and time is accepted, so book_appointment does not raise ValueError.
- Expected behaviour and requirement: A practitioner cannot have two SCHEDULED appointments at the same date/time (AC-04.1), while a different practitioner may be booked at the same time (AC-04.2). A conflict is rejected with ValueError.
- Minimal synthetic reproduction steps: new SmartCareDataStore; register patient P1 and practitioners D1 and D2; book A1 for P1 with D1 at 2026-10-01 09:00; book A2 for P1 with D1 at the same time (expected ValueError, none raised); book A3 with D2 at the same time (expected to succeed).
- Meaningful failing test path/name and exact relevant failure: tests/test_starter.py::test_conflict_rule_and_different_practitioner, line 127, `Failed: DID NOT RAISE ValueError` at the pytest.raises(ValueError) around the A2 booking.
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: In SmartCareDataStore.has_practitioner_conflict (data_store.py) the practitioner comparison was inverted, `appointment.practitioner.practitioner_id != practitioner_id`. The method therefore reported a conflict only for a different practitioner at that time and never for the same one. Evidence: book_appointment calls has_practitioner_conflict with the requested practitioner ID (services.py), the other conditions (exclude ID, date_time, SCHEDULED) match the original contract, and the test passed D1 twice and so got False.
- Smallest justified fix / diff / why other behaviour is preserved: change `!=` to `==` in the practitioner_id comparison (one line in data_store.py). The exclude ID, date_time and status conditions are untouched, so different practitioners can still book the same time and a cancelled appointment still does not block a slot.

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: After cancel_appointment('A001'), find_appointment('A001') raises LookupError: Appointment not found, and cancelling the same appointment a second time also raises LookupError instead of ValueError.
- Expected behaviour and requirement: A cancelled appointment stays stored with status CANCELLED and can be retrieved in the same session (FR-07, AC-05.1 and AC-05.2). Cancelling it again raises ValueError.
- Minimal synthetic reproduction steps: new SmartCareDataStore; register patient P001 and practitioner PR001; book A001 at 2026-01-01 10:00; cancel A001; find A001 (expected the same object with status CANCELLED).
- Meaningful failing test path/name and exact relevant failure: tests/test_starter.py::test_cancelled_appointment_remains_retrievable, `LookupError: Appointment not found` raised from services.py find_appointment. The twice-cancel tests (tests/test_services.py and tests/test_starter.py, test_cancel_appointment_twice_raises_value_error) fail with the same LookupError.
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: SmartCareDataStore.find_appointment (data_store.py) scanned the appointments but skipped any whose status was cancelled, so it returned None for them. AppointmentService.find_appointment turns None into LookupError. The appointment was not deleted: list_appointments() still returns it (the domain-cancellation test checks this), so the record was hidden by the lookup filter. cancel_appointment calls find_appointment, which explains why the second cancel gave LookupError instead of reaching the ValueError guard in Appointment.cancel.
- Smallest justified fix / diff / why other behaviour is preserved: remove the `and appointment.status.value != "cancelled"` condition from find_appointment. The blank-ID ValueError, the trimmed ID match and the None result for unknown IDs are unchanged, and the conflict rule still only considers SCHEDULED appointments.

## E. Human-first hypotheses



### F8-01 human entry
Likely cause and why plausible: The booking check does not recognise an existing SCHEDULED appointment for the same practitioner at the same time, so `has_practitioner_conflict` returns False and no ValueError is raised (the test shows DID NOT RAISE ValueError). The practitioner comparison inside `SmartCareDataStore.has_practitioner_conflict` is the most plausible place, for example `!=` written instead of `==`. That would still let the different-practitioner part of the test behave as expected.
Evidence intended to inspect / competing explanation / discriminating check: Inspect has_practitioner_conflict in data_store.py and the arguments passed to it in book_appointment (services.py). Competing explanations: book_appointment passes the wrong arguments, or the two times do not compare equal. Discriminating check: after booking A1 with D1, call `store.has_practitioner_conflict('D1', when)` directly. It should be True, and False for D2.

### F8-02 human entry
Likely cause and why plausible: After cancellation, the appointment can no longer be found: the data store's `find_appointment` returns None, which the service turns into LookupError. Plausible causes are that the lookup ignores cancelled appointments, or that cancelling removes the appointment from the store. The first fits the rest of the code better, because cancellation is meant to change the status only (FR-07).
Evidence intended to inspect / competing explanation / discriminating check: Inspect find_appointment in data_store.py and cancel/cancel_appointment. Competing explanation: cancellation deletes the record. Discriminating check: cancel an appointment and then call `store.list_appointments()`. If the cancelled appointment is still listed while `store.find_appointment` returns None, the lookup is hiding it. If it is not listed, it was deleted.

## F. GitHub Copilot prompts, findings and human decisions



### F8-01 Copilot review
Actual prompt / output reference and member: Assistant used: Claude. Prompt: "Act as a debugging reviewer for SmartCare (Python). Do not rewrite the code and do not invent requirements. Use only the information below. DEFECT: F8-01 practitioner conflict. OBSERVED: a second booking for the same practitioner at the same time is accepted (DID NOT RAISE ValueError). EXPECTED: same practitioner and time rejected with ValueError, a different practitioner allowed (AC-04.1, AC-04.2). REPRODUCTION: register P1, D1, D2; book A1 with D1 at 2026-10-01 09:00; book another appointment with D1 at the same time. FAILING TEST: tests/test_starter.py::test_conflict_rule_and_different_practitioner. OUR HYPOTHESIS: the practitioner comparison in has_practitioner_conflict is wrong. RELEVANT CODE: SmartCareDataStore.has_practitioner_conflict and AppointmentService.book_appointment. Give three ranked possible causes, and for each a discriminating check that would confirm or rule it out."
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: The practitioner comparison in has_practitioner_conflict is inverted (`!=` where `==` is needed). Check: read the method and call it directly. Observed: the code line is `appointment.practitioner.practitioner_id != practitioner_id`; with A1 booked for D1, `has_practitioner_conflict('D1', when)` returned False and for D2 returned True, the opposite of the rule. Correct. Accept: it matches the failing test and AC-04.1/AC-04.2.
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: book_appointment passes the wrong values to the conflict check. Check: read the call in services.py and the direct call above. Observed: it passes the requested practitioner ID and date/time as the method expects, and the method itself gives the wrong answer when called directly. Wrong as the cause. Reject.
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: The two times are not equal (for example seconds or a timezone difference), so no conflict is found. Check: compare the datetimes used by the test. Observed: the test uses identical `datetime` values and `w == datetime(2026, 10, 1, 9)` is True. Wrong. Reject. This was the least supported suggestion, as nothing in the failure pointed to time handling.
Final human conclusion and comparison with initial hypothesis: The root cause is the inverted practitioner comparison in has_practitioner_conflict, which matches our hypothesis. Competing explanations were ruled out by the direct call and the argument check.

### F8-02 Copilot review
Actual prompt / output reference and member: Assistant used: Claude. Prompt: "Act as a debugging reviewer for SmartCare (Python). Do not rewrite the code and do not invent requirements. Use only the information below. DEFECT: F8-02 retained-history lookup. OBSERVED: after cancelling A001, finding A001 raises LookupError: Appointment not found; cancelling it again also gives LookupError. EXPECTED: the cancelled appointment stays retrievable with status CANCELLED, and cancelling twice raises ValueError (FR-07, AC-05.2). REPRODUCTION: register P001 and PR001; book A001; cancel A001; find A001. FAILING TEST: tests/test_starter.py::test_cancelled_appointment_remains_retrievable. OUR HYPOTHESIS: the data store lookup hides cancelled appointments. RELEVANT CODE: SmartCareDataStore.find_appointment, AppointmentService.find_appointment and cancel_appointment. Give three ranked possible causes, and for each a discriminating check that would confirm or rule it out."
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: The store's find_appointment skips cancelled appointments, so a cancelled one looks missing. Check: cancel an appointment and compare `list_appointments()` with `find_appointment`. Observed: the list still shows ('A1', 'cancelled') while `store.find_appointment('A1')` returns None; the code has `and appointment.status.value != "cancelled"` in the lookup. Correct. Accept.
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: cancel_appointment removes the record from the store. Check: list the stored appointments after cancellation. Observed: the record is still stored with status cancelled. Wrong. Reject: the record is hidden, not deleted.
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: AppointmentService.find_appointment raises LookupError incorrectly. Check: read the service method. Observed: it correctly raises LookupError when the store returns None, so it only reports the symptom; the fault is one layer below. Partly correct (explains where the error comes from and why the second cancel also gives LookupError, as cancel_appointment calls find_appointment first). Modify: the fix belongs in the store, not the service.
Final human conclusion and comparison with initial hypothesis: The root cause is the cancelled-status filter in SmartCareDataStore.find_appointment. This matches our first hypothesis and rules out deletion.

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | c549c68 | python -m pytest -q tests/test_starter.py::test_conflict_rule_and_different_practitioner, project/ | 1 failed: DID NOT RAISE ValueError |
| F8-01 after repair | same command | 1 passed; full suite 3 failed, 33 passed (remaining failures are F8-02) |
| F8-02 before repair | python -m pytest -q tests/test_starter.py::test_cancelled_appointment_remains_retrievable, project/ | 1 failed: LookupError: Appointment not found |
| F8-02 after repair | same command | 1 passed |
| Full suite after both repairs, before refactor | python -m pytest -q, project/ | 36 passed |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: The F8-01 test books the same practitioner at the same time and expects ValueError, so an inverted comparison (no error raised) fails it. It then books a different practitioner at the same time and expects success, so a fix that blocked every booking at that time would also fail. The F8-02 test cancels an appointment and asserts that find_appointment returns the same object (`is`) with status CANCELLED, so a lookup that hides or deletes cancelled history fails. The twice-cancel tests assert ValueError, which protects the guard in Appointment.cancel. The rest of the 36 tests were kept unchanged and still pass.
Unrelated failures investigated / resolution: None. The two twice-cancel failures looked separate but have the F8-02 cause, because cancel_appointment looks the appointment up first. They passed after the F8-02 repair with no other change.

## H. Refactoring decision and before/after verification

Smell and exact location: Magic string in SmartCareDataStore.has_practitioner_conflict (data_store.py): `appointment.status.value == "scheduled"` compares against a literal when the AppointmentStatus enum already exists.
Small proposed structural change / why justified: Replace the string comparison with `appointment.status is AppointmentStatus.SCHEDULED`, which is how the original code compared status. A misspelt literal would fail silently, and the enum is the single source of the value.
External behaviour to preserve / relevant tests: has_practitioner_conflict returns True only for another SCHEDULED appointment for the same practitioner at the same time, ignoring the excluded ID and cancelled appointments. Relevant tests: test_conflict_rule_and_different_practitioner and the full suite (36 passed before).
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: one line in data_store.py, `and appointment.status.value == "scheduled"):` changed to `and appointment.status is AppointmentStatus.SCHEDULED):`.
Focused and full after-refactor commands / working directory / results / evidence: python -m pytest -q tests/test_starter.py::test_conflict_rule_and_different_practitioner, then python -m pytest -q, both from project/: focused 1 passed, full 36 passed. 
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: Accepted. The same tests pass before and after (36 passed), and the change only replaces how the status is compared, so external behaviour is preserved.

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? The least-supported suggestion was the F8-01 idea that the two datetimes did not compare equal because of seconds or a timezone. It sounded reasonable because date handling often causes bugs, but nothing in the failure pointed to it, and a quick comparison showed the times were equal. The F8-02 idea that cancellation deletes the record was also plausible, but listing the stored appointments showed it was still there.
2. What evidence changed your group's view? Three things. First, a direct call to `has_practitioner_conflict` returned the opposite of what the rule needs, which located F8-01 in the data store. Second, `list_appointments()` still showed the cancelled appointment while `find_appointment` returned None, so it was hidden rather than deleted. Third, the two twice-cancel tests failing with LookupError showed they shared the F8-02 cause, because cancel_appointment looks the appointment up first.
3. How did regression tests protect the refactoring? The full suite (36 tests) passed before the change, and the refactor replaced only how the status is compared. Running the suite after it showed the same 36 passed, and the F8-01 test would fail if the enum comparison changed the conflict rule. The F8-02 test would also catch a change that hid cancelled history again. So the tests showed that behaviour was unchanged.

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: Stop and work out the cause first. Record the symptom, decide the expected behaviour from a requirement, find a minimal reproduction and form a hypothesis with evidence to check, then make the smallest justified change.

2. Where should expected behaviour come from during debugging?

Response: From the requirements and acceptance criteria (e.g. FR-07 or AC-04.2) and the documented contracts in the code, not from what the current code happens to do or from a test that may be wrong.

3. What is a debugging hypothesis?

Response: A testable explanation of why a failure happens, written before the fix, with the evidence that would confirm or disprove it.

4. What is a regression test and why is it retained?

Response: A test that checks behaviour that already worked still works after a change. It is retained so that later repairs or refactors that break old behaviour are detected.

5. What is meant by root cause?

Response: The underlying fault that causes the failure, which when corrected removes the failure. It is not the symptom or the line where the failure showed up and it needs evidence to support it.

6. What is refactoring?

Response: Changing the internal structure of code to make it clearer or easier to maintain without changing its external behaviour, checked by tests passing before and after.

7. What is a swallowed exception?

Response: An exception that is caught and ignored or hidden (e.g. an empty except block) so the failure is not reported and the program carries on in a wrong state.

8. What is a code smell?

Response: A sign in the code (e.g. duplicate strings, a very long method or deep nesting) that suggests a deeper design problem. It is not a bug by itself but it is a prompt to consider refactoring.

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: As hypotheses and not facts. Each suggestion should be checked against the actual code, tests and requirements, judged correct, partly correct or wrong, then accepted, modified or rejected with a reason. The human is responsible for the conclusion.

10. What is the Stage 8 engineering rule?

Response: Diagnose before changing code: find evidence for the cause, make the smallest justified fix, protect it with regression tests, and only refactor when the full suite passes and re-run the tests afterwards.

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: Group 1 / Thursday at 2.30 pm
Members and UG/PG cohorts: Rylan - Pengi376, Tomas - Tom-uc3, Barry - BarrytheLegoMan; [complete: UG/PG cohort for each member]
Record owner / contribution links for each member: [complete]

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

| Statement | Classification | Reason |
|-----------|----------------|--------|
| Appointment disappears after cancellation. | Symptom | It describes what is seen when the system is used and does not say why it happens. It goes against FR-07, which says cancelled history must be retained. |
| The data-store removal path is probably being called. | Hypothesis | The word "probably" shows it is a guess about the cause that has not been tested. It can be tested by checking data_store.py and services.py, as SmartCareDataStore has no public delete method. |
| The failing test shows store.find_appointment('A1') returns None. | Evidence | It is an observed result from running a test and can be repeated. It supports the symptom but does not explain the cause. |
| The service layer is badly designed. | Opinion | It is a general judgement with nothing observed or testable behind it, and it doesn't explain this failure. |
| Traceback points to smartcare/services.py line 42 in the example. | Evidence | A traceback is recorded output showing where the failure appeared. It shows the location, not the cause, and the line number must be checked in the actual run. |

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

Response and reason: [complete after the prepared Stage 8 project has a real failing test]

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: Changing code straight away means the fix is only a guess. It may hide the symptom while the cause is still there, or break something that worked. Without an expected behaviour from a requirement, a reproduction and a hypothesis there is no way to know if the fix worked or why. It also risks changing correct code when the test or the expectation was the real problem. Working out the cause first and then making the smallest change is safer.


Classification responses (1–5, each with reason): see A.1
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: see A.2
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: [complete after the prepared Stage 8 project has a real failing test]

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: f5ee9ce (tested Stage 7 main SHA from the Stage 7 record). Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
- Baseline test command / working directory / observed result / evidence: python -m pytest, project/, 
collected 36 items                                                                                                                                                             

tests\test_domain.py ....                                                                                                                                                [ 11%]
tests\test_services.py ...........                                                                                                                                       [ 41%]
tests\test_starter.py .....................                                                                                                                              [100%]

============================================================================= 36 passed in 0.16s ==============================================================================
- Clean preparation SHA if a record-only commit followed Stage 7: 14b5887 (stage 7 wrong SHA removed correct one added). [complete: confirm only records changed using git diff f5ee9ce 14b5887 --stat]
- Branch and preparer / how teammates obtained this branch: [complete]
- Downloaded tool version, source SHA256 and --check outcome: [complete]
- --apply and --verify output summaries / artefact references: [complete]
- Bounded diff inspected and recovery location (not committed): [complete]
- Prepared faulty-state commit SHA: [complete]
- Preparation or recovery issues and resolution, if any: [complete]
- Initial prepared full-suite command / result / key failures: [complete]

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: [complete]
- Expected behaviour and requirement: [complete]
- Minimal synthetic reproduction steps: [complete]
- Meaningful failing test path/name and exact relevant failure: [complete]
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: [complete]
- Expected behaviour and requirement: [complete]
- Minimal synthetic reproduction steps: [complete]
- Meaningful failing test path/name and exact relevant failure: [complete]
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: [complete]
Evidence intended to inspect / competing explanation / discriminating check: [complete]
Member and saved sequence/time or commit showing this preceded consultation: [complete]

### F8-02 human entry
Likely cause and why plausible: [complete]
Evidence intended to inspect / competing explanation / discriminating check: [complete]
Member and saved sequence/time or commit showing this preceded consultation: [complete]

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

### F8-02 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-02 before repair | [complete] | [complete] | [complete] |
| F8-02 after repair | [complete] | [complete] | [complete] |
| Full suite after both repairs, before refactor | [complete] | [complete] | [complete] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [complete]
Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

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

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]

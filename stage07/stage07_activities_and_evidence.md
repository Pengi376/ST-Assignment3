# Stage 7 Testing and Verification Record

Group/tutorial: Group 1 / Thursday at 2.30 pm  Members/cohorts: Rylan - Pengi376, Tomas - Tom-uc3, Barry - BarrytheLegoMan;
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement                         | Positive test                                                                                         | Negative test                                                                                | Key assertion                                                     |
|-------------------------------------|-------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|-------------------------------------------------------------------|
| FR-01 Register patient              | Test that a patient can be registered with correct data types                                         | Test that a patient cannot be registered with incorrect data types                           | check if patient information has been stored                      |
| FR-05 Prevent practitioner conflict | Test that an appointment can be booked when there is no other appointments with the same practitioner | test that an appointment cannot be booked when a practitioner is already busy                | check if that code behaves as expected                            |
| FR-06 Cancel appointment            | test that an appointment can be canceled                                                              | test that the wrong appointment will not be cancelled and only the one meant to be cancelled | check that once cancelled the appointment becomes available again |
| FR-07 Retain cancelled history      | test the appointment history to see if oppointments state has changed to cancelled                    | test that the system wont remove it from history.                                            | check if appointment remains in history once cancelled            |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: [Weak/unclear]  Why: assert True doesn't verify that the code works as expected, it only checks if the output is true.

`assert appointment is not None`
Judgement: [Weak/unclear]  Why: It isn't clear on what it is doing, as there could just be no appointments created yet hence there is none.

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: [Strong for stated behaviour]  Why: It is testing that appointment status can be cancelled very clear.

`assert len(results) > 0`
Judgement: [Strong for stated behaviour / Weak/unclear]  Why: it is both unclear but also strong as I'm unsure what results it is testing, however if it needed to test that the results are greater then zero it is clear.

`assert data_store.find_appointment('A1') is appointment`
Judgement: [Strong for stated behaviour]  Why: As it is clear that it is ensuring appointment A1 is apart of the class appointment in the data

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract: 

1. Blank Identifiers 
PatientID = "", PractitionerID = ""
Expected result = ValueError PatientID cannot be blank or ValueError PractionerID cannot be blank.
Contract supporting that expectation = as per the Required text function in the domain file, anything utilising it cannot be left blank.
2. Whitespace-only names
first name = "  ", last name = "   "
expected result = ValueError Patient name cannot be blank or ValueError Practioner name cannot be blank.
Contract supporting that expectation = as per the Required text function in the domain file, anything utilising it cannot be left blank or have only whitespace.
3. same-time practitioner bookings
 Appointment = appointment_id: 5, patient_id: 23, practitioner_id: 60, date_time: 23/4/27 11:00, status: SCHEDULED
 Appointment = appointment_id: 6, patient_id: 26, practitioner_id: 60, date_time: 23/4/27 11:00
expected result = Practitioner already has a SCHEDULED appointment at this time
Contract supporting that expectation = Function has_practitioner_Conflict in data_store and the book_appointment function in services stop this from happening.
4. cancelled appointments
Cancel appointment in 2014, cancel an already canceled appointment
expected result = ValueError Only SCHEDULED appointments may be canceled
Contract supporting that expectation = function cancel in domain only allows appointments with a status of SCHEDULED to be cancelled.
5. invalid status transitions
completed too canceled, canceled to completed
expected result = ValueError Only SCHEDULED appointments may be canceled
Contract supporting that expectation = Function cancel in domain won't allow status changes unless it is scheduled to canceled
### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate| What is wrong                                                                                            | Rewritten test intention                                                                                              |
|---|----------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| 1 | If an assert is only testing an object is not equal to none it is only really testing if it exist or not | Rewrite test to be more specific on what it doesn't want to be none                                                   |
| 2 | If an assert is only testing an object is not equal to none it is only really testing if it exist or not | Rewrite test to be more specific on what it doesn't want to be none or change it so that a feild cannot be left empty |
| 3 | Assert True only tests wether or not a statement is True nothing specific, it effectively does nothing   | Rewrite test to test something more specific that a specific input/output returns True                                |
| 4 | assuming sms notifications exist doesn't test if they are there or not.                                  | rewrite test to check if sms notifications exist                                                                      |
| 5 | assuming sms notifications exist doesn't test anything to actually do with sms notifications             | Rewrite test to check if sms notifications work as intended.                                                          |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
As code coverage just ensures it has been tested, it does not check if the tests are verifying correct outcomes.

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement                                                                                        | Acceptance criterion                                                                                              | Test ID   | Test type  | Test name / location                                                            | Expected behaviour                                                                 | Result / observed status                | Supplied or student-authored |
|----------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|-----------|------------|---------------------------------------------------------------------------------|------------------------------------------------------------------------------------|-----------------------------------------|------------------------------|
| valid required patient data with an unused id is stored                                            | a patient can be added aslong as the patient ID is an unused one                                                  | AC-01.1   | unit test  | Patient_registration_with_unused_id /test_domain.py                             | Tests wether or not a patient can be registered with an unused id                  | the result should be that is is allowed | supplied                     |
| Registration with an existing patient ID is rejected                                               | a patient cannot be registered if they have the same patient id as another patient                                | AC-01.2   | unit test  | patient_registration_with_same_id / test_domain.py                              | test wether or not a patient can be registered with the same id as another patient | the result should be it is not allowed  | supplied                     |
| unknown patient lookup reports absence                                                             | a patient that doesnt exist cannot be looked up and reports that the patient doesn't exist                        | AC-02.2   | unit test  | patient_search_does_not_exist / test_domain.py                                  | LookupError                                                                        | passed                                  | supplied                     |
| registered participants, a unique ID and a free time produce a stored scheduled appointment        | If all the appointment information is factual it produces and stores it as a scheduled appointment                | AC-03.1   | unit test  | test_registration_and_booking / test_starter.py                                 | ValueError                                                                         | passed                                  | supplied                     |
| booking an unkown patient or practitioner is rejected                                              | cannot double book the same practioner for the same time but can book 2 different practitioners for the same time | AC-04.1-2 | unit test  | test_conflict_rule_and_different_practitioner / test_starter.py                 | ValueError                                                                         | passed                                  | supplied                     |
| cancelling a scheduled appointment changes it to cancelled                                         | a cancelled appointments status changes from scheduled to cancelled                                               | AC-05.1   | unit test  | test_cancel_appointment_changes_status_and_returns_same_object/ test_starter.py | Status changes to cancelled                                                        | passed                                  | supplied                     |
| cancelled history remains retreivable in the current session                                       | A cancelled appointment remains in the stored appointment history                                                 | AC-05.2   | unit test  | test_cancelled_appointment_remains_retrievable/ test_starter.py                 | Cancelled appointment information is still stored                                  | passed                                  | supplie d                    |
| repeated cancellation is rejected                                                                  | that an already cancelled appointment cannot be cancelled again.                                                  | AC-05.3   | unit test  | test_cancel_appointment_twice_raises_value_error/test_starter.py                | an appointment cannot be cancelled more then once                                  | passed                                  | supplied                     |
| a known appointment ID returns that appointment                                                    | when searching for an appointment if the ID is known and used, it returns the correct appointment                 | AC-06.1   | unit test  | test_find_appointment_with_id / test_domain.py                                  | appointment found                                                                  | passed                                  | supplied                     |
## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID                                         | Requirement                                                                   | Acceptance criterion                                                | Positive / Negative / Boundary                                                                                                  | Test intention                                                             | Observable result expected          | Added evidence beyond supplied tests            |
|-------------------------------------------------|-------------------------------------------------------------------------------|---------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|-------------------------------------|-------------------------------------------------|
| test_patient_registeration_with_unused_ID       | Thats a patient can be register with a unique id                              | that the patient is registered                                      | different Id = registered, differentId but wrong type = not registered                                                          | to test if a patient can be registered with a different id                 | patient gets registered             | a patient needs to be able to be registered     |
| test_patient_registeration_with_same_patient_ID | that a patient is not registered if trying to use the same id                 | that the patient is not registered                                  | same id = not register                                                                                                          | to test if a patient can be registered with the same id as another patient | Patient does not get registered     | a patient should not be registered with same id |
| unknown_patient_lookup_reports_absence          | finding a patient without a known id should report an absence                 | unknown patient ID reports absence                                  | known id = found, unknown id = report absence                                                                                   | to test wether or not an unknown id reports absence                        | software reports absence of patient | the sytem needs to report unknown patient       |
| known_appointment_lookup                        | to be able to find an appointment with a known ID                             | if the appointment is found                                         | appointment found, unknown id appointment not found                                                                             | to test if an appointment can be found with a known id                     | appointment is found                | smartcare needs to be able to find appointments |
| test_appointment_feilds_not_empty               | appointment feilds are not allowed to be left empty.                          | if appointment only books appointments with fully filled out feilds | appointment not able to be booked, if only missing to things = still not booked.                                                | to test if an appointment is rejected is it is missing feilds              | appointment unable to be booked     | smartcare needs all appointment information     |
| test_required_fields                            | appointment feilds have to be completly filled out + patient and practitioner | if an appointment cannot be booked if it is missing information     | appointment has full info and books, appointment missing all info and is not booked, appointment missing 1 thing and not booked | to ensure if an appointment is missing anything software throws an error   | appointment unable to be booked     | smartcare needs all information to be enterered |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID                                                          | Arrange | Act        | Assert                                                          | Why meaningful / why assertion proves criterion |
|------------------------------------------------------------------|---------|------------|-----------------------------------------------------------------|-------------------------------------------------|
| test_required_fields                                             | pass    | [complete] | all feilds need to be filled                                    | as it does what it is suppose to                |
| test_appointment_feilds_not_empty                                | pass    | [complete] | no appointment feild can be empty                               | as it does what it is suppose to                |
| test_registration_and_booking                                    | pass    | [complete] | registration and booking function                               | as it does what it is suppose to                |
| test_cancel_appointment_changes_status_and_returns_same_object   | pass    | [complete] | cancelled appointment returns same object with cancelled status | as it does what it is suppose to                |
| [complete]                                                       | pass    | [complete] | [complete]                                                      | [complete]                                      |
## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID                                                        | Behaviour                                        | Requirement / criterion                                                  | Test file/function | Result     |
|----------------------------------------------------------------|--------------------------------------------------|--------------------------------------------------------------------------|--------------------|------------|
| test_required_fields                                           | all feilds need to be filled out                 | only accepts registration for things completly filled out                | test_domain.py     | pass       |
| test_appointment_feilds_not_empty                              | no appointment feild can be empty                | only lets an appointment be booked if all info is in there               | test_domain.py     | pass       |
| test_registration_and_booking                                  | registration and booking need to function        | patient and practitioner can be registered and appointment can be booked | test_domain.py     | pass       |
| test_cancel_appointment_changes_status_and_returns_same_object | appointment needs status to change to cancelled  | cancelled appointment status changes to cancelled                        | test_domain.py     | pass       |
|                                                                | [complete]                                       | [complete]                                                               | [complete]         | [complete] |
|                                                                | [complete]                                       | [complete]                                                               | [complete]         | [complete] |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

|  Test ID                                                              | Behaviour                                                                               | Test file/function | Result    |
|-----------------------------------------------------------------------|-----------------------------------------------------------------------------------------|--------------------|-----------|
| test_known_patient_lookup                                             | searches known patient                                                                  | test_services      | passed    |
| test_known_practitioner_lookup                                        | searches known practitioner                                                             | test_services      | passed    |
| test_unknown_practitioner_lookup                                      | searches unknown practitioner                                                           | test_services      | passed    |
| test_unknown_appointment_lookup                                       | searches unknow appointment                                                             | test_services      | passed    |
| test_practitioner_registration                                        | tests if practitioner can be registered                                                 | test_services      | passed    |
| test_practitioner_registration_with_same_id                           | tests if practitioner can be registered with same id                                    | test_services      | passed    |
| test_cancelled_appointment_does_not_stop_new_appointment_at_same_time | test if cancelled appointment stops new appointment at same time with same practitioner | test_services      | passed    |
| test_cannot_duplicate_appointments                                    | tests if an appointment can be booked twice                                             | test_services      | passed    |


## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour                | Boundary/invalid input                     | Expected result | Test ID                             |
|--------------------------|--------------------------------------------|-----------------|-------------------------------------|
| patient id lookup        | unknown id, or incorrect id form           | lookup error    | test_unknown_patient_lookup         |
| practitioner lookup      | unknown practitioner id, or incorrect form | lookup error    | test_unknown_practitioner_lookup    |
| appointment duplication  | same appointment booked twice              | ValueError      | test_cannot_duplicate_appointments  |


## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: cancelled history remains retreivable in the current session.
Acceptance criterion: A cancelled appointment remains in the stored appointment history.
Behaviour to test: appointment remains stored after cancelled
Human-first test idea/categories: test_services
Prompt and purpose: [complete or link]

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: test_history_retrieval_without_cancellation_is_not_a_valid_verification()
- What it claims to verify: that a cancelled appointment can be found after cancellation
- Requirement trace: none
- Assertion quality: Very poor
- Human critique: Copilot just made a function with nothing inside the function
- Decision: reject
- Reason: copilot failed to actually create a real function
- Final test reference if accepted/modified: [not retained]
- Actual verification result: did not pass

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? all of them
Why was it weak? although i used suggested prompt copilot failed to created anything usefull or that worked
How did you strengthen it? by creating my own tests

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command          | Working directory | Code SHA | Passed      | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|------------------|-------------------|----------|-------------|--------|-----------------|-------------------------------------------|-----------------------------|
| python -m pytest | tests/            | 02fe9ff  | all of them | none   | nonw            | none                                      | everything worked           |

Individual test runs and changed-order independence evidence: [commands, results, links]
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove? that the code will function all together when every stage is completed
Coverage if used: not used
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? it doesn't know how it will be used in the final software
Optional fixtures/parametrisation used and why, if any: [ not used]

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch     | PR         | Reviewer   | Key feedback | Outcome    |
|------------|------------|------------|------------|--------------|------------|
| [complete] | [complete] | [complete] | [complete] | [complete]   | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member   | Actual contribution                 | Evidence link |
|----------|-------------------------------------|---------------|
| u3304415 | test_domain.py and test_services.py |               |

## N Formative Questions

1. What question does verification answer?
that a specific peice of code is coded correctly.

2. What question does validation answer?
it ensures the code works how it should

3. What is a unit test?
a test on a specific function requirement

4. What is a pytest fixture?
a fixed baseline for a test to run reliably

5. What is parametrisation in pytest?
a feature that allows a single test function to run multiple times with different sets of inmput data.

6. What is regression testing?
when you re run functional and non function tests after software updates to ensure the code still runs as it should.

7. What does code coverage tell us, and what does it not prove?
it tells us which parts of the code ran and which parts didn't, it does not prove if the code actually works.

8. What makes an assertion weak?
when it lacks supporting evidence or logical reasoning

9. What is the appropriate role of GitHub Copilot as a test assistant?
to speed up repetitive tasks and help with technical implementation.

10. What is the Stage 7 engineering rule?
that code needs to be tested, verified and validated properly and it needs to be repeatable for future implementations of the software.

## O Stage Completion

Tested Stage 7 main SHA: f5ee9ce
Full-suite result: passed
Unresolved defects and effect on baseline: [none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: complete
All tutorial/formative responses and traceability/Copilot decisions complete: yes

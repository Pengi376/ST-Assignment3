# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Group 1 / Thursday at 2.30 pm
- Members, GitHub usernames and cohorts: Rylan - Pengi376, Tomas - Tom-uc3, Barry - BarrytheLegoMan;   
- Repository URL: https://github.com/Pengi376/ST-Assignment3
- Starting SHA: [ea582f1]

## A Requirement to issue activities

### FR-02 Patient Search

- Title: Find a patient by patient ID
- Context: SmartCare staff need to retrieve an already registered patient using a unique patient ID so that patient details can be used in SmartCare booking process.
- Requirement: The system shall allow retrieval of a registered patient by their patient ID. A valid unknown ID must report that the patient does not exist. Invalid or blank IDs must be rejected.
- Acceptance criteria: The patient search feature correctly retrieves registered patients and handles invalid lookup requests.

Scenario 1: Successful lookup

Given a patient is registered with a valid patient ID\
When the user searches using that patient ID\
Then the stored patient object is returned

Scenario 2: Unknown patient

Given a valid patient ID that is not registered\
When the user searches for that patient\
Then a LookupError is raised

Scenario 3: Invalid input

Given a blank or invalid patient ID\
When the user searches for a patient\
Then a ValueError is raised

Scenario 4: State preservation

Given a patient exists in the data store\
When a search is performed\
Then no patient data is modified
- Scope: Implement patient lookup functionality only. Do not add name searching, partial matching, authentication, or patient record modification.
- Definition of Done: 
  - Patient lookup implementation completed.
  - Tests cover successful lookup, unknown ID, and invalid ID cases.
  - All existing and new tests pass.
  - Code reviewed and merged through PR.
- Owner: Barry
- Actual issue link: https://github.com/Pengi376/ST-Assignment3/issues

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: Cancel only a SCHEDULED appointment and retain appointment history
- Context: SmartCare staff need to cancel appointments when required while preserving appointment records for the current SmartCare session.
- Requirement: The system shall allow cancellation of a SCHEDULED appointment. The appointment must remain stored with status CANCELLED and continue to be retrievable after cancellation.
- Acceptance criteria: The appointment cancellation feature correctly cancels scheduled appointments, retains appointment history, and rejects invalid cancellation requests.

Scenario 1: Successful cancellation

Given an appointment has status SCHEDULED\
When cancellation is requested using its appointment ID\
Then the appointment status becomes CANCELLED\
And the same appointment object is returned

Scenario 2: Retained history

Given an appointment has been cancelled\
When the appointment is retrieved by its appointment ID\
Then the appointment is still available\
And its status remains CANCELLED

Scenario 3: Repeated cancellation

Given an appointment already has status CANCELLED\
When cancellation is requested again\
Then a ValueError is raised\
And the appointment state remains unchanged

Scenario 4: Invalid appointment state

Given an appointment has status COMPLETED\
When cancellation is requested\
Then a ValueError is raised\
And the appointment state remains unchanged

Scenario 5: Invalid appointment ID

Given a valid but unknown appointment ID, or a blank/invalid appointment ID\
When cancellation is requested\
Then a LookupError or ValueError is raised as appropriate\
And no appointment data is modified
- Scope: Implement appointment cancellation and retained history only. Do not delete appointments, modify booking logic, add persistence, or introduce new appointment states.
- Definition of Done: 
  - Cancellation functionality implemented according to the service contract.
  - Tests cover successful cancellation, retained history, unknown IDs, invalid IDs, and illegal transitions.
  - Existing booking and lookup behaviour remains unchanged.
  - All tests pass.
  - Code reviewed and merged through PR.
- Owner: Barry
- Actual issue link: https://github.com/Pengi376/ST-Assignment3/issues

## B Commit quality

| Original example                               | Strong or Weak | Reason                                                                                                                                                                                     |
|------------------------------------------------|----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| changes                                        | Weak           | The message is too vague and does not describe what was changed or which requirement was addressed. It would be difficult for another team member to understand the purpose of the commit. |
| final version                                  | Weak           | The message gives no information about the functionality or bug fix included in the commit. "Final" is subjective and may not remain true as the project evolves.                          |
| Add patient search by ID                       | Strong         | The message clearly describes the feature that was implemented and can be traced back to FR-02 Patient Search. Another developer can quickly understand the purpose of the commit.         |
| fix stuff                                      | Weak           | The message does not identify what was fixed, why it was fixed, or what requirement it relates to. It provides little value when reviewing project history.                                |
| Prevent cancellation of completed appointments | Strong         | The message clearly communicates a specific behaviour change and relates directly to the appointment cancellation rules. It helps reviewers understand the intent of the change.           |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: The PR is over-scoped because it combines appointment cancellation with unrelated patient field renaming, code restructuring, and a new dependency. In a mature team with strong release management, clear feature ownership, well-maintained user stories, and comprehensive testing, multiple changes can sometimes be coordinated and released together. However, for this Stage 6 feature, the changes are unrelated to the cancellation requirement, making the PR harder to review and increasing the risk of unintended side effects.
- Responsibility and architecture concerns: Appointment cancellation should focus on appointment workflow responsibilities. Renaming patient fields affects a different area of the application, while restructuring code and introducing dependencies may have architectural impacts beyond the feature being delivered. These changes should have their own justification and review process. Combining them into a cancellation PR makes it more difficult to verify that responsibilities remain properly separated.
- Testing and review concerns: Although experienced teams can manage larger releases through disciplined testing and release processes, combining unrelated changes increases review complexity and makes defect isolation more difficult. If a test fails or a bug is discovered, it becomes harder to determine whether the cause is the cancellation implementation, the field renaming, the refactoring, or the new dependency. Smaller, focused PRs provide clearer traceability and make reviews more effective.
- Changes to remove or separate, with reasons: 
  - Appointment cancellation changes should remain in the current PR because they directly address FR-06 and FR-07.
  - Patient field renaming should be moved to a separate PR because it affects a different feature area and requires independent review.
  - Code restructuring or refactoring should be submitted separately so behaviour can be verified independently of functional changes.
  - New dependency additions should be reviewed in a dedicated PR unless they are essential to the cancellation feature, as dependencies affect the entire project and introduce additional risk.

    Keeping the cancellation PR focused makes it easier to verify requirements, write meaningful tests, review the changed behaviour, and trace the implementation back to the linked issue and acceptance criteria.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

AI can provide analysis, suggestions, and alternative viewpoints, but accountability for decisions remains with the human reviewer, developer, or manager.

- Missing evidence: The review provides no evidence that the requirements, acceptance criteria, edge cases, or design responsibilities were checked. "Tests pass" is not enough to approve a change.
- Follow-up review question 1: How does this change satisfy the linked requirement and acceptance criteria?
- Follow-up review question 2: What tests were run, and which behaviours do they verify?
- Follow-up review question 3: How are invalid inputs and error conditions handled?
- Follow-up review question 4: Were any unrelated changes included that should be reviewed separately?
- Follow-up review question 5: What evidence supports approving this change beyond passing tests?
- Additional questions if useful:
  - Has a human reviewer independently checked the code and requirements?
  - Are there any risks or assumptions that need verification?
  - Does the implementation follow SmartCare responsibilities?

## E Team workflow agreement

| Practice                            | Team agreement                                                                                                                         |
|-------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| Branch naming                       | Use descriptive names based on the feature or requirement, e.g. feature/stage-6_FR02-FR06and07                                         |
| Commit message convention           | Use clear messages that describe the change or behaviour implemented, e.g. "Add patient search by ID and updated testing plan"         |
| PR size                             | Keep PRs focused on a single requirement or related set of changes so they are easier to review and test.                              |
| Another-member review requirement   | At least one other team member reviews the change before it is considered complete.                                                    |
| Merge rule                          | Changes should be tested and reviewed before being merged into the main codebase.                                                      |
| Significant Copilot disclosure rule | Record significant Copilot use, including the task, purpose, output summary, human review, decision taken, and verification performed. |

An early pull request was used to learn the recommended workflow. After experiencing difficulties and disruption while learning GitHub and the project structure, the team agreed to work sequentially and review changes in main rather than maintaining separate feature branches. We recognise this increases risk compared with isolated feature branches, but it was considered the most practical approach for our team's current level of experience.

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.


| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|------------|------------|-------|------------|------------|
| Issue #1: FR-02 Patient Search | FR-02 Find a patient by patient ID | Barry | Registered patient returns the stored object; unknown ID raises `LookupError`; invalid ID raises `ValueError`. | Completed |
| Issue #2: FR-06/FR-07 Appointment Cancellation and History | FR-06 Cancel only a SCHEDULED appointment; FR-07 Retain cancelled appointment history | Barry | SCHEDULED appointment changes to `CANCELLED`; appointment remains retrievable; repeated cancellation raises `ValueError`; unknown ID raises `LookupError`. | Completed |
| Issue #3: Practitioner Lookup Service | Practitioner lookup supporting FR-03 | Barry | Registered practitioner returns the stored object; unknown ID raises `LookupError`; invalid ID raises `ValueError`. | Completed |


## G Pull request evidence

1. PR link and title: No formal PR used for this Stage 6 change.
2. Linked issue and requirement: FR-02 Patient Search, FR-06/FR-07 Appointment Cancellation.
3. Feature branch: N/A.
4. Changed behaviour: Implemented patient lookup, practitioner lookup and appointment cancellation services.
5. Meaningful commits: [commit links]
6. Test command, directory and observed result: python -m pytest, project/, Observed result: 21 tests collected and all 21 passed successfully in 0.05 seconds. Exit code 0.
7. Another-member reviewer: [name if code was reviewed].
8. Human observations recorded before Copilot: Recorded in Stage 6 evidence document.
9. Requirement, responsibilities, test assertions and unrelated-scope checks: Checked service contracts, exception handling and Stage 6 requirements.
10. Key feedback: [actual feedback received or "None"].
11. Author response/change and verification: Author Barry [name of verification] .
12. Reviewer recheck and approval: [if applicable].
13. Merge outcome and SHA: Changes committed directly to main, SHA [actual SHA].
14. Significant Copilot assistance: Used for implementation discussion and test design. All suggestions independently reviewed and verified. Use of Co-pilot as assistance technology and part of RAP.
15. Linked issue closure: [issue reference or completion note].
16. Each member updated main: [member names and confirmations].
17. Integrated verification after merge: python -m pytest, project/, [actual result], SHA [actual SHA].


## H Copilot collaboration record

- Member and task: Barry - Stage 6 service implementation and test design for patient lookup, practitioner lookup, and appointment cancellation.

- Prompt/purpose and relevant issue/diff: Used Copilot to discuss the service contracts, understand the responsibilities of the data store, service layer and domain layer, and develop tests for FR-02 Patient Search and FR-06/FR-07 Appointment Cancellation.

- Summary of output: Copilot suggested test cases as no experience with pytest,  for successful lookups, invalid IDs, unknown IDs, cancellation, retained history, repeated cancellation and completed appointments. Also has been used as assistance technology alongside requirements of RAP. 

- Human check against actual code, requirements and tests: Reviewed the Stage 6 handout, service contracts, `data_store.py`, `domain.py`, and test results. Verified that suggestions matched the documented requirements and existing application structure.

- Decision — Accept / Modify / Reject: Modify

- Reason: Copilot suggestions were useful but were reviewed against the assignment requirements and adjusted where necessary. Final implementation and test selection were based on independent analysis and verification rather than direct acceptance.

- Verification/evidence: Compared suggestions against Stage 6 requirements, implementation code and pytest results. Verification result: 21 tests passed, 0 failed.


## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: The service methods should follow the documented contracts, use existing data store validation, preserve responsibility boundaries, and include tests for successful and error scenarios.

- Copilot noticed: The lookup services should convert `None` results into `LookupError`, cancellation should use the domain `cancel()` method, and additional tests were required for error conditions and retained history.

- Overlap: Both identified the importance of following the service contracts, validating error handling, and testing both successful and failure scenarios.

- What did the human reviewer notice that Copilot did not: The importance of keeping the implementation aligned with team workflow decisions, code-review practices, and ensuring human accountability for approval decisions.

- What did Copilot identify that the human reviewer initially missed: Additional edge-case tests, including repeated cancellation, completed appointment cancellation, and retained history verification.

- Unsupported or incorrect Copilot suggestion: None identified. Suggestions were checked against the requirements, existing code, and test results before use.

- Human judgement accepted, modified or rejected, and why: Modified. Copilot suggestions were treated as recommendations and reviewed against the Stage 6 requirements, codebase structure, and actual test outcomes before implementation.

- Which evidence justified merge approval: Service implementations matched the documented contracts, test cases covered required behaviours and error conditions, and pytest verification showed 21 tests passed with 0 failures.

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]


- Member: Barry Dobson

- Implementation: Implemented `PatientService.find_patient()`, `PractitionerService.find_practitioner()`, and `AppointmentService.cancel_appointment()`. Verified use of data store lookups and domain-based appointment cancellation.

- Testing: Added and executed tests for patient lookup, practitioner lookup, successful appointment cancellation, retained history, repeated cancellation, completed appointment rejection, unknown appointment IDs, and invalid appointment IDs. Verified 21 tests passed (building on the provided 8 tests).

- Review: Reviewed service contracts, data store behaviour, domain responsibilities, and Stage 6 requirements before implementation. Evaluated whether code changes remained within the intended feature scope.

- Issue refinement: Created and refined issue descriptions for FR-02 Patient Search, FR-06 Appointment Cancellation, FR-07 Retained History, and practitioner lookup support. Defined acceptance criteria using Given/When/Then scenarios.

- Design and responsibility discussion: Discussed separation of responsibilities between the data store, service layer, and domain objects. Ensured lookup validation remained in the data store and appointment state transitions remained in the domain model.

- Debugging or integration: Investigated service and data store interactions to determine how `LookupError` and `ValueError` should be handled. Verified integrated behaviour through pytest execution.

- Documentation or team support: Completed Stage 6 evidence documentation, contributed workflow discussions, reviewed team processes, and documented testing and AI-assisted development activities.

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

A high commit count only shows how often changes were recorded, not the quality or impact of the work. A small number of well-planned commits may contribute more value than many minor commits. Contributions such as design discussions, testing, code review, debugging, documentation, and mentoring are also important and may not result in many commits.

---

## L Stage 6 formative questions

### 1. What is version control?

Version control is a system that tracks changes to files over time, allowing a team to collaborate, review history, and recover previous versions if needed.

### 2. Why is a feature branch useful?

A feature branch allows changes to be developed and tested separately from the main codebase, reducing the risk of affecting stable work before review and integration.

### 3. What makes a commit a good engineering commit?

A good engineering commit is focused, meaningful, and clearly describes the behaviour, feature, or fix being implemented.

### 4. What is a pull request?

A pull request is a request to merge changes into another branch. It provides an opportunity for review, discussion, testing, and approval before integration.

### 5. What is the purpose of code review?

The purpose of code review is to verify requirements, identify defects, improve code quality, share knowledge, and ensure changes are appropriate before integration. A seccond human in the loop.

### 6. What does a Git diff show?

A Git diff shows the differences between versions of files, including added, removed, and modified lines of code.

### 7. What is a Definition of Done?

A Definition of Done is an agreed set of criteria that must be satisfied before work is considered complete, such as implementation, testing, review, and documentation.

### 8. What is the appropriate role of GitHub Copilot in pull-request review?

GitHub Copilot can help identify risks, suggest improvements, and support analysis, but a human reviewer must verify the evidence and make the final approval decision.

### 9. Why should individual contribution not be judged only by commit count?

Commit count does not measure the quality of work or other valuable contributions such as testing, review, issue refinement, design discussions, debugging, documentation, and team support.

### 10. What is the Stage 6 engineering rule?

The Stage 6 engineering rule is to follow the complete development cycle: understand the requirement, create a focused change, implement and test the solution, review the work, verify the results, and record evidence before integration.


## M Completion and handover

1. Starting SHA: [starting commit SHA]

2. Final Stage 6 code SHA: [tested commit SHA]

3. Test command: `python -m pytest`

4. Working directory: `C:\Users\barry\PycharmProjects\st1-assignment-3\project`

5. Observed result: 21 tests collected, 21 tests passed, 0 failed. Exit code 0.

6. PR and another-member reviewer: No formal PR used. Team reviewed changes directly on the shared repository. Reviewer: [team member name].

7. Unresolved issue or none: None identified for Stage 6.

8. Stage 7 handover status: Ready for tutor checkpoint.

9. Final submitted SHA if later than tested SHA: Same as tested SHA, or [new SHA] if documentation-only updates were made after testing.

10. Three Stage 6 service targets completed and checked: Yes.

11. Original supplied tests retained and passing: Yes.

12. At least two focused issues link requirements and acceptance criteria: Yes.

13. Feature work reviewed by another member using the actual diff: Yes.

14. Human-first review and required Copilot comparison recorded: Yes.

15. Feedback resolved and approval recorded before merge: Yes, where applicable to team workflow.

16. Everyone pulled main and integrated checks passed: [Not yet]

17. Required activities, quiz responses and contribution notes completed: Yes.

18. Only synthetic data included; confidential peer material kept out: Yes.

19. Tutor can trace a requirement through issue, code, tests, PR and checkpoint: Requirement → implementation → tests → review evidence documented in Stage 6 record.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.

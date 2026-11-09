# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Group 1 / Thursday at 2.30 pm
Members and UG/PG applicability: Rylan - Pengi376, Tomas - Tom-uc3, Barry - BarrytheLegoMan. All three members are undergraduates (UG). Written for the UG common scope (Stages 6, 7, 8, 9, 12); there is no Stage 10 or 11 PG work.


## A Release scope and starting SHA

Release label/version and requirements baseline: SmartCare 1.0 (common UG release). Requirements baseline: SmartCare A3 2026, revision 2.
Common starting SHA / branch / applicable members: 9170455c418e92ca245918e789a4ae417103587c (main after merging PR #2, which brought the Stage 8 repairs 6979b6c onto the Stage 9 commit 3c1d8ac), main, all three members.
PG starting SHA / branch / applicable members or not applicable: Not applicable (UG common release).
Working-state review and approved integration: The Stage 8 branch was merged by Rylan through PR #2 (merge commit 9170455) without an independent reviewer. Stage 9 and Stage 12 work was committed directly to main by group agreement. No independent review is recorded.
Protected common candidate and PG differences: The common candidate is 9170455c418e92ca245918e789a4ae417103587c; there are no PG differences.
Feature freeze / owner / verifier: No new features after 9170455; later commits change only documentation and repository hygiene.


## B Requirements and release readiness matrix

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | FR-06 to FR-08: cancelled appointment stays stored with status CANCELLED and can be found and listed | tests/test_starter.py::test_cancelled_appointment_remains_retrievable; tests/test_services.py::test_list_practitioner_appointments_retains_cancelled_history; 9170455 | No independent reviewer (self-assessed by Rylan) | Yes (not independently reviewed) | Repair is in 6979b6c, merged in 9170455 |
| Architecture responsibilities are appropriate | Domain cancels, store holds collections, services coordinate, queries are pure, console is the only I/O | project/smartcare/ (see project/README.md structure); code inspection; 9170455 | No independent reviewer (self-assessed by Rylan) | Yes (not independently reviewed) | run_menu in console.py is long (see E, H) |
| Rescheduling is safe — PG only | Not applicable (UG common scope) | Not applicable | Not applicable | Not applicable | Not applicable |
| AI use is responsible — common recheck / PG assurance | Copilot prompt, findings and human decisions recorded for Stage 9 (section E of that record); Stage 8 Copilot entries | stage08/ and stage09/ records | No independent reviewer (self-assessed by Rylan) | Partly | No independent human review at Stages 8, 9 and 12; Claude was used at Stage 8 without asking the tutor, and the hypotheses were not saved separately |
| System is maintainable | Four-layer structure, type hints and docstrings, 45 passing tests, 90% statement coverage (console 83%) | project/tests/; pytest-cov run, 9170455 | No independent reviewer (self-assessed by Rylan) | Yes (not independently reviewed) | Style items in E and H (line length, blank lines, test duplication) |
| FR-01–03 register/find and validation | Duplicate and unregistered cases preserve the original; blank, whitespace and unknown IDs rejected; lookup case-sensitive | tests/test_starter.py (duplicate_*, find_*), tests/test_services.py (registration, lookup); 9170455 | No independent reviewer (self-assessed by Rylan) | Yes | None |
| FR-04–05 booking/conflict rules | Same practitioner/time rejected, different practitioner allowed, cancelled slot reusable, duplicate ID rejected | tests/test_starter.py::test_conflict_rule_and_different_practitioner; tests/test_services.py::test_cancelled_appointment_does_not_stop_new_appointment_at_same_time, test_cannot_duplicate_appointments; 9170455 | No independent reviewer (self-assessed by Rylan) | Yes | Repair is in 6979b6c, merged in 9170455 |
| FR-06–08 cancellation/history/find | Cancel changes status and returns the same object; repeat, unknown, completed and blank IDs rejected | tests/test_starter.py (cancel_*), tests/test_services.py (cancel twice, unknown appointment); 9170455 | No independent reviewer (self-assessed by Rylan) | Yes | None |
| FR-09 and QRY/FP listing/filter/order/purity | Practitioner isolation, every status and default all, time then ID order, source unchanged, new lists, named key, known-empty/unknown/invalid | tests/test_queries.py (4 tests); tests/test_services.py::test_list_practitioner_appointments_*; 9170455 | No independent reviewer (self-assessed by Rylan) | Yes | Tests cover representative cases, not all inputs |
| UI full console sequence and error recovery | Scripted menu covers choices 1 to 8 and 0, bad date, unknown choice, duplicate IDs, conflicts, freed slot, repeat cancel | tests/test_console.py (3 tests); scripted run in D; 9170455 | No independent reviewer (self-assessed by Rylan) | Yes | Evidence is a scripted run (D); no live team demonstration is recorded |
| Session-only scope / FR-10 retired | Menu and README state data is discarded on exit; no persistence code exists | project/README.md; console.py exit messages; 9170455 | No independent reviewer (self-assessed by Rylan) | Yes | None |
| PG RES and assurance integration | Not applicable (UG common scope) | Not applicable | Not applicable | Not applicable | Not applicable |


## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | Python 3.12.2, pytest 9.1.1, Windows (run by Rylan) | python -m pytest, project/ | 9170455 | 45 passed in 0.25s | Terminal output from Rylan's run; not saved as a file |
| Complete PG if applicable | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Affected focused checks after correction | Not applicable | Not applicable | Not applicable | No code changed after the tested SHA | Not applicable |
| Full integrated recheck | Python 3.12.2, pytest 9.1.1, Windows (run by Rylan) | python -m pytest, project/ | 9170455 | 45 passed in 0.25s | Terminal output from Rylan's run; not saved as a file |
Prior assertions preserved / reviewed test diff: The Stage 6 to 9 tests are all still present (4 domain, 13 service, 21 starter, 4 query, 3 console = 45). No assertions were removed, and no code or tests were changed in Stage 12. 
Remaining failure / limitation: No failing test. Statement coverage is 90% (console.py 83%, data_store.py 89%, domain.py 92%), measured by Claude with pytest-cov on Python 3.12.3 against the Stage 9 code; coverage is not proof of correctness.


## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders | Small clinic booking problem; stakeholders: patients, practitioners, reception staff | FR-01 to FR-09 overview | SmartCare is a session-only console system for booking and cancelling appointments | README purpose |
| Register and find Patient and two Practitioners | Patient P1 Alex Example; practitioners D1 and D2 (GP) | FR-01 to FR-03 | Patient registered: P1; Practitioner registered: D1, D2; find P1 and D2 returned the right records (scripted run of python main.py --interactive with piped input, by Claude on the Stage 9 code) | Scripted console run on the Stage 9 code (Claude); tests/test_console.py |
| Valid booking | A1, P1, D1, 2027-04-23 11:00 | FR-04 | Appointment booked: A1: P1 with D1, 2027-04-23 11:00, scheduled | Scripted console run on the Stage 9 code (Claude); tests/test_console.py |
| Same practitioner exact-time conflict rejected | A2, P1, D1, same time | FR-05, AC-04.1 | Error: Practitioner already has a SCHEDULED appointment at this time | Scripted console run on the Stage 9 code (Claude); tests/test_console.py |
| Different practitioner same time allowed | A3, P1, D2, same time | AC-04.2 | Appointment booked: A3: P1 with D2, 2027-04-23 11:00, scheduled | Scripted console run on the Stage 9 code (Claude); tests/test_console.py |
| Cancel SCHEDULED and retain/find CANCELLED object | Cancel A1, then find A1 | FR-06, FR-07 | Appointment cancelled: A1 ... cancelled; find A1 shows the same record with status cancelled | Scripted console run on the Stage 9 code (Claude); tests/test_console.py |
| Invalid/repeated cancellation rejected | Cancel A1 again | FR-06 | Error: Only SCHEDULED appointments may be cancelled | Scripted console run on the Stage 9 code (Claude); tests/test_console.py |
| Default all-status listing | List D1, blank status | FR-09 | A1 (cancelled) is listed | Scripted console run on the Stage 9 code (Claude); tests/test_console.py |
| Explicit filtering / empty vs unknown / deterministic order | D1 scheduled; D2 all; D9; ordering from test_queries | FR-09, QRY-01 to QRY-04 | D1 scheduled: No matching appointments found; D2: A3; D9: Error: Practitioner not found; order verified by tests/test_queries.py | Scripted console run on the Stage 9 code (Claude); tests/test_console.py |
| Invalid date/status/menu/lookup recovery and continued operation | Status bogus; date 2027-02-30; menu choice 9; blank choice | UI-02 | Errors: Status must be scheduled, cancelled or completed; Invalid calendar date/time; Unknown menu choice; the next valid booking (A5, same slot as the cancelled A1) succeeded | Scripted console run on the Stage 9 code (Claude); tests/test_console.py |
| Session-only limitation and normal exit | Choice 0 | FR-10 retired | Session ended; in-memory data discarded. | Scripted console run on the Stage 9 code (Claude); tests/test_console.py |
| One meaningful requirement-linked pytest test explained | test_cancelled_appointment_remains_retrievable | FR-07 | It cancels a booked appointment then asserts find_appointment returns the same object (`is`) with status CANCELLED, so deletion or hiding fails it. It does not prove history after the session ends. | Scripted console run on the Stage 9 code (Claude); tests/test_console.py |
| Architecture and one actual AI decision / known limitation | Layers: domain, store, services, queries, console | Architecture requirement | AI decision: rejected suggestions in Stage 8 (stage08 section F); limitation: session-only data | Scripted console run on the Stage 9 code (Claude); tests/test_console.py |
| PG reschedule identity/participants/time and no-op | Not applicable (UG) | Not applicable | Not applicable | Not applicable |
| PG conflict/invalid status/failure non-mutation | Not applicable (UG) | Not applicable | Not applicable | Not applicable |
| PG old slot / current lookup/list ordering / assurance risks | Not applicable (UG) | Not applicable | Not applicable | Not applicable |
Stable demo owner / fresh process / command: Rylan (Stage 12 owner); fresh process with `python main.py --interactive` from project/.
PG demonstrations through service/tests or not applicable: Not applicable (UG common scope).


## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | services.py, queries.py, console.py | No finding: queries.py has no I/O or hidden state and returns new lists; services coordinate; only console.py reads and prints | No change |
| PascalCase and snake_case naming | All smartcare/*.py | No finding in source. Test names contain two misspellings (test_patient_registeration_*, test_appointment_feilds_not_empty) | Rename the tests if time allows; re-run pytest |
| Useful type hints and meaningful docstrings | smartcare/*.py | No finding: public functions are typed and documented. services.py still has a docstring beginning `Stage 9:` | Optional wording change in list_practitioner_appointments |
| Four-space indentation and imports/layout | pycodestyle and pyflakes over project/ | Findings: lines over 79 characters (console.py lines 123 and 150, services.py 123, some tests); missing blank lines (E302) in services.py, main.py and tests; unused import `data_store` in services.py (and unused imports in two test files) | No change, so the tested code stays as it was; recorded as a limitation in H |
| Focused methods / duplication / dead or commented code | console.py run_menu | Finding: run_menu is about 100 lines with eight branches; no commented-out code found | Accepted as a known maintainability limit, or split into helper functions in a separate verified refactor |
| Globals / leakage / unnecessary inheritance or frameworks | smartcare/*.py | No finding: no globals, inheritance or frameworks; the console creates one store per session | No change |
| No SQLite/persistence/repository ABCs/speculative features | imports and project tree | No finding: standard library only, no persistence, no rescheduling code | No change |
| Synthetic data / secrets / dependencies / provenance | grep and tree inspection | No secrets found by searching for password, secret, token and API key; only synthetic names; one dev dependency, pytest 8.3.5. `.idea/` IDE folder was in the repository | `.idea/` added to .gitignore; remove it from Git with `git rm -r --cached .idea` |
| Significant common Copilot contributions and human verification | stage08/ and stage09/ records | The AI assistant diagnosed the two Stage 8 defects (F8-01 inverted practitioner comparison, F8-02 cancelled-status filter in find_appointment) and later helped draft the Stage 12 review. Each claim was checked with direct calls, tests and code inspection (stage08 sections E to F) | The AI-assisted Stage 8 and Stage 12 sections were not independently reviewed; no reviewer is recorded. |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | Not applicable | Not applicable (UG) | Not applicable |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| F8-02: find_appointment hides cancelled appointments | FR-07 retained history; data_store.py find_appointment | `list_appointments()` still held the cancelled record while `find_appointment` returned None; the failing test and code line were read | Accept: it matched the evidence and the test | Cancelled-status filter removed; full suite 36 passed after both Stage 8 repairs |
| F8-01 (3rd suggestion): the times were unequal, causing no conflict | AC-04.1; has_practitioner_conflict | Compared the datetimes used by the test; they are equal | Reject: nothing in the failure pointed to date handling | No change; the real cause was the inverted practitioner comparison |
| Stage 12 review: the unused `data_store` import in services.py is harmless | Code quality; services.py | pyflakes reported it; nothing in the file uses it | Modify: true, but left unchanged | No change: services.py stays as tested so that 9170455 is the final code; recorded as a minor limitation in H |
Access route or approved equivalent / limitations: Rylan used Claude as an equivalent to GitHub Copilot for the Stage 8 diagnosis (sections E to F) Limits: it could not see the team's private environment, its own test runs used Python 3.12.3, and its output was treated as hypotheses to be checked.


## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | project/README.md, Purpose and scope | Rylan (self-check; no independent verifier) | Added; states common UG scope only |
| Out-of-scope capabilities and known limitations | project/README.md | Rylan (self-check; no independent verifier) | Added |
| Confirmed teaching Python version and dependency installation | project/README.md, Setup and commands | Rylan (self-check; no independent verifier) | Added; states Python 3.13 and pytest 8.3.5 as the verified teaching versions (the final test run used Python 3.12.2 and pytest 9.1.1; the README says so) |
| Working directory / demo / interactive / test commands | project/README.md | Rylan (self-check; no independent verifier) | Added: python main.py, python main.py --interactive, python -m pytest from project/ |
| Repository structure and architecture responsibilities | project/README.md, Structure | Rylan (self-check; no independent verifier) | Added |
| Responsible AI summary / synthetic-data rule | project/README.md | Rylan (self-check; no independent verifier) | Added |
| Release label/version and SHA links | root README.md and project/README.md | Rylan (self-check; no independent verifier) | Root README updated: verified code SHA 9170455, latest completed stage 12 |
Root README index and project/README verified: Root README updated with all-UG cohorts, the observed test result and SHA 9170455; project/README title corrected from `Stage 6 starter` to `SmartCare`, with scope, structure and setup added. Checked by Rylan; not independently verified.
Fresh clone or extracted ZIP / candidate identity: Not done: no clean-clone check was carried out. Rylan ran the tests in his working repository on main (9170455).
Verifier and clean environment / actual version: None. Rylan's environment: Python 3.12.2, pytest 9.1.1, Windows.
Setup/run/test commands and observed results: Rylan: python -m pytest from project/ on main (9170455): 45 passed in 0.25s. Claude (separate sandbox, Python 3.12.3): pip install -r requirements-dev.txt, python main.py and python -m pytest all ran, with 45 passed.
Missing local file or setup gap / remedy and recheck: None found; no clean-clone recheck was done.


## G Known limitations debt and release notes

Delivered features: Registration and lookup of patients and practitioners; booking with the practitioner conflict rule; cancellation with retained history; pure appointment queries (filter by practitioner and status, ordered by time then ID); practitioner appointment listing; an interactive console with error recovery.
Important fixes: Stage 8 repairs of F8-01 (practitioner conflict comparison) and F8-02 (retained-history lookup), committed in 6979b6c and merged in 9170455.
Architecture/quality improvements: Status comparison uses the AppointmentStatus enum rather than a string; pure query layer separated from the services and console; README completed.
Known limitations: Data is lost on exit; no rescheduling; local minute-precision times only; some style findings remain (E, H).
AI-assisted development note: AI assistants were used (GitHub Copilot at Stage 9, Claude at Stages 8 and 12), and their output was checked against code, tests and requirements; decisions are recorded in the stage records.

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| Session-only data is lost on exit | Records vanish when the program ends | Medium | Add persistence in future work | Accepted: FR-10 is retired for this course |
| Long run_menu function | Harder to maintain and test | Low | Split into helpers with tests | Accepted for the release |
| Style findings (line length, blank lines) | Readability only | Low | Reformat and re-run tests | Accepted for the release |
Session-only synthetic data and minute-precision local time: Records exist only in memory for one run, only synthetic data is used, and times are local to the minute with no timezone rules.
Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: None of these are implemented and none are claimed; they would be needed before any real clinical use.
Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: Single user, single process, no monitoring, plain text console only.
Difference between accepted scope limit and unresolved required behaviour: The items above are outside the required scope. A required behaviour that fails (for example a lost cancellation history) would be a defect and a release blocker; none is open in the tests.
PG assurance residual risks / owner / status or not applicable: Not applicable (UG common scope).


## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| Maintainability: unused import | pyflakes: `smartcare.data_store` imported but unused in services.py | Low | Rylan; left unchanged | None | Not applicable (no code change) | Unused import remains in services.py (and two test files); tested code left as it was |
| Repository hygiene: IDE metadata | `.idea/` was tracked in the repository | Low | Rylan; ignored and untracked | `.idea/` added to .gitignore; removed from tracking with `git rm -r --cached .idea` | Not a code change | None |
| Reproducibility: README | project/README.md title said Stage 6 starter and lacked scope, structure and setup | Medium | Rylan; rewritten | Updated project/README.md and the root README index | README commands run by Rylan (python -m pytest, 45 passed) | None |
| Style: line length and blank lines | pycodestyle: E501 in console.py (2), services.py (1), tests; E302 in services.py, main.py, tests | Low | Rylan; not changed | Not changed | Not applicable | Accepted limitation (readability only) |
Justified no-change conclusion if no defect found: No functional defect was found: all 45 tests pass and the scripted console run matched the requirements. The items above are quality, hygiene and documentation findings.
Release blockers still open / status: None. Known gaps recorded honestly: no independent human review at Stages 8, 9 and 12; the Stage 8 hypotheses were not saved separately before the consultation; tutor approval for Claude was not asked; tests were run on Python 3.12.2 rather than 3.13; no clean-clone check.


## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA: Stage 8: PR #2 https://github.com/Pengi376/ST-Assignment3/pull/2 (branch debug/stage08, commit 6979b6c, merged 2026-11-09 21:45 +1100 as 9170455). Stage 9: no PR, commits made directly to main. Stage 12: no PR, committed directly to main by group agreement. Reviewed SHA: none (no review). No GitHub issues were opened.
Independent reviewer / feedback / response: None. No independent reviewer or feedback exists at any stage. Rylan approved and merged the Stage 8 PR himself, and the group agreed to commit directly to main.
Integration commit / full recheck: Merge commit 9170455 (PR #2). Full recheck by Rylan on main: python -m pytest from project/, 45 passed in 0.25s (Python 3.12.2, pytest 9.1.1).
Tracked and untracked file inspection / cleanliness: Tracked tree contains project/ (source and 5 test files), stage06 to stage12 records, README.md, .gitignore, .gitattributes and `.idea/`; `.idea/` is to be untracked with `git rm -r --cached .idea` and ignored. No __pycache__, .venv, .env, .pytest_cache or Stage 8 tool files are tracked. Commit 6979b6c accidentally deleted stage12/stage12_activities_and_evidence.md; the record is restored in the final records commit.
Secrets/staff material/caches/tool-metadata exclusion check: Search for password, secret, token and API key found nothing in code or README. .gitignore excludes .stage8_faults/, the check/verify folders and `.idea/`; the Stage 8 tool is kept outside the repository.
Candidate recovery plan / known-good SHA: Known-good SHA 9170455c418e92ca245918e789a4ae417103587c. Recover with `git checkout 9170455` or `git revert` of any later commit.
Named substantive contributions: Rylan: Stages 8 and 12 (preparation tool, repairs, PR #2, Stage 12 record). Tomas: Stages 7 and 9 (Stage 7 testing and verification; Stage 9 queries, console, tests and records). Barry: Stage 6 (FR-02, FR-06, FR-07 and tests; PR #1 from feature/patient-lookup).


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: READY WITH DOCUMENTED LIMITATIONS (proposed; not approved by a named person, and subject to the conditions below).
Approver / date / rationale and evidence: Approved by Rylan (Pengi376), 2026-11-09. Rationale: all 45 tests pass on 9170455 (Python 3.12.2, pytest 9.1.1); both Stage 8 repairs are covered by tests; the scripted console run and invalid paths behaved as required; the known limitations (session-only data, no rescheduling, style findings) are documented in G and are outside the required scope.
What risks remain / conditions / owners: Conditions: none outstanding. Residual risks (owner Rylan): no independent review; style findings and the long run_menu function (low); no persistence (accepted); tests run on Python 3.12.2 rather than the README's 3.13.
Can the team explain the system: Each member explains their own stage using section N (Rylan: Stages 8 and 12; Tomas: Stages 7 and 9; Barry: Stage 6). No joint practice session is recorded.
Can a change be recovered: Yes. Every stage is a commit in Git history. Known-good SHA 9170455c418e92ca245918e789a4ae417103587c; a faulty change can be undone with `git revert` or by checking out that commit.
Common decision / PG decision where different: Common decision as above. PG: not applicable (UG common scope).


## K Final tested release SHA

Exact common tested SHA: 9170455c418e92ca245918e789a4ae417103587c, tested by Rylan: 45 passed in 0.25s (Python 3.12.2, pytest 9.1.1).
Exact PG tested SHA or not applicable: Not applicable (UG common scope).
Final submitted SHA / repository URL: The head of main after the final records commit (`git rev-parse HEAD`); it contains this record, so its SHA cannot be written into it. Repository https://github.com/Pengi376/ST-Assignment3
Evidence-only later commit and difference explanation: The final records commit changes only documentation and repository hygiene (README.md, project/README.md, .gitignore, the stage records and removal of `.idea/` from tracking). `git diff 9170455 HEAD --stat` lists no .py files.
Executable changes after testing and re-verification: None.
Source ZIP name / SHA correspondence / extracted comparison: SmartCare_Group1.zip, made with `git archive --format=zip -o SmartCare_Group1.zip HEAD` from the submitted commit, so its contents correspond exactly to that commit.


## L Submission package verification

- [ ] Feature freeze and scoped requirements traced.
- [ ] Applicable full regressions, integrated demo and invalid paths verified.
- [ ] Architecture/code quality and final AI/dependency checks complete.
- [ ] Root README and project/README reproduced by another verifier.
- [ ] Release notes, technical debt and limitations visible.
- [ ] Independent human review, integration and release decision recorded.
- [ ] Repository URL accessible to marker and exact candidate SHA identified.
- [ ] One source ZIP from submitted commit with root README.md and .gitignore.
- [ ] project/ source and all accumulated applicable tests included.
- [ ] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [ ] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [ ] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [ ] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, confidential individual peer forms and common team viva routed separately.


## M Formative questions

1. What is a release candidate? A version of the software that is believed ready to release and is tested as if it were final. Only fixes for found problems are allowed afterwards.

2. What is feature freeze and why is it used? Stopping new features at a set point so the code stays stable. It lets the team test, fix and document the exact version being released.

3. What is regression testing in a release context? Re-running the full set of tests on the release candidate to show that new changes did not break behaviour that previously worked.

4. What is a known limitation? A known gap or restriction in the delivered system that is documented and accepted (for example data lost on exit), as opposed to an unfixed defect in required behaviour.

5. What is technical debt? The extra future work created by shortcuts or unfinished quality work (for example a long function or style issues). It has a cost that should be recorded and prioritised.

6. What are release notes? A short document for users and maintainers describing what the release delivers, important fixes, known limitations and any changes in behaviour.

7. What is software maintenance? Changing software after release to fix faults, adapt it, improve it or keep it understandable, which depends on clear structure, tests and documentation.

8. What is the purpose of the individual demonstration/viva? To confirm that each member understands the system and can explain and justify their own contribution, rather than relying on others' or an AI's work.

9. What should the final responsible-AI check establish before release? That AI-assisted work was verified by humans against requirements and tests, that no real data or secrets were used, that dependencies and provenance are acceptable, and that the team can explain it.

10. What is the main course conclusion about AI and the role of the software engineer? AI can speed up writing code, but the engineer is responsible for requirements, design, verification, safety and decisions, so human judgement and accountability remain essential.


## N Reflection viva and handover

Strongest evidence SmartCare is ready: All 45 tests pass, including regression tests for both Stage 8 defects (F8-01 conflict rule, F8-02 retained history), and the scripted console run showed registration, booking, conflict rejection, cancellation, filtered listing and error recovery behaving as required.
Weakest area: Maintainability polish and records: the 100-line run_menu function, style findings, and the records that still needed completing. Data is also lost on exit by design.
How AI use changed from Stage 1 to Stage 12: Not provided by the team. Recorded use: Claude at Stage 8 for diagnosis after the team had formed its own hypotheses, GitHub Copilot at Stage 9 as a reviewer after the team's own design, and Claude to help draft the Stage 12 record, with each output checked against code, tests or the commit history.
Start doing — engineering and AI use: Write the hypothesis and expected behaviour before asking an AI; save prompts as we go; run the linter and a clean-environment check earlier.
Stop doing — engineering and AI use: Leaving records until the end; accepting an AI explanation because it sounds plausible.
Continue doing — engineering and AI use: Small commits with focused tests and regression runs after each change.
What worked / caused rework / future delivery improvement: Worked: tests that failed for a clear reason made diagnosis quick. Rework: an SHA in the root README that did not match the tested commit. Improvement: keep the README and evidence updated at each stage.
One paragraph — If AI can write code why do we still need software engineers: AI can produce code quickly, but it does not know the real requirements, and it can be confidently wrong. In Stage 8 an assistant offered plausible causes, such as a datetime mismatch, that the evidence ruled out. Engineers decide what the system must do, check that the code does it with tests and review, take responsibility for safety, privacy and maintainability, and can explain and change the system when it fails. AI is a useful tool, but the accountability stays with people.

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | A small clinic needs to register patients and practitioners and book and cancel appointments without clashes. Stakeholders: patients, practitioners, reception staff. |
| Two requirements and acceptance criteria | FR-05 / AC-04.1 and AC-04.2: the same practitioner cannot have two SCHEDULED appointments at the same time, but a different practitioner can. FR-07 / AC-05.2: a cancelled appointment stays retrievable with status CANCELLED. |
| Domain model and architecture | Patient, Practitioner and Appointment (with a status enum) in domain.py; one SmartCareDataStore holding three dictionaries; services that coordinate workflows; pure query functions; a console as the only input/output layer. See project/README.md. |
| Design trade-off | In-memory dictionaries are simple and fast to test but lose data on exit (FR-10 retired); a database would persist but add complexity outside the scope. Keeping queries pure makes them easy to test but adds a layer. |
| Meaningful test and its limits / 100 percent coverage | test_conflict_rule_and_different_practitioner fails if the conflict rule is inverted. Its limits: it checks one scenario and not all possible inputs. Coverage was 90% in Claude's pytest-cov run, and even 100% would only show lines ran, not that every behaviour is right. |
| Diagnosed defect and verification | F8-02: the lookup hid cancelled appointments (found because list_appointments still held the record); verified by the retention test and the full suite passing. See stage08 sections C, D and G. |
| Shared store and session-state/query responsibilities | All three services share one store object so a patient registered by one service is visible to booking. The store holds the session state, and the query functions only read lists passed to them and return new ones. |
| What would break if session-state lookup/query responsibilities changed? | If each service created its own store, booking would not find registered patients. If a query sorted its source in place, callers' lists and stored order would change unexpectedly. |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | Cancellation is a rule about one appointment's own status (only SCHEDULED can be cancelled), so it belongs in the Appointment. Checking a clash needs all appointments for a practitioner, so a service coordinates it with the store. |
| FR-07 retained history test | test_cancelled_appointment_remains_retrievable cancels a booking then asserts the same object is found with status CANCELLED. It would fail if cancelled records were deleted or hidden. |
| Actual AI change rejected/modified or honestly accepted with verification | Rejected: the suggestion that unequal datetimes caused F8-01 (the times were equal) and that cancellation deletes the record in F8-02 (the record was still stored). See stage08 section F. |
| Unresolved limitation / future production work | No persistence, authentication, concurrency or timezone handling; these would be needed for production. |
| Personal implementation contribution | Rylan: Stage 8 repairs (6979b6c) and the Stage 12 record. Tomas: Stage 9 queries, console and tests. Barry: Stage 6 services and tests (FR-02, FR-06, FR-07). |
| Personal test/review/design/integration contribution | Rylan: PR #2 and integration to main, Stage 8 regression tests. Tomas: Stage 7 testing and verification, Stage 9 tests. Barry: Stage 6 testing. |
| PG agentic change and rescheduling verification | Not applicable (UG) |
| PG responsible-AI risk/remediation or supported no finding | Not applicable (UG) |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: Not undertaken.
Separate reflection / peer / common team viva evidence links and routing: Routed separately as set out in the published assessment instructions; not restated here.
No further coding stage. Later corrections use the published assessment process.

# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Group 1 / Thursday at 2.30 pm; repository https://github.com/Pengi376/ST-Assignment3
Members and UG/PG applicability: Rylan (Pengi376), Tomas (Tom-uc3), Barry (BarrytheLegoMan). All three are UG. This is a UG-only release of the common scope; PG Stages 10 and 11 do not apply, and their templates are left unchanged.

Code SHA used for all Stage 12 testing below: `9170455c418e92ca245918e789a4ae417103587c` (`main` after PR #2 merged the Stage 8 repairs onto the Stage 9 code), shortened to `9170455`. Stage ownership: Barry Stage 6, Tomas Stages 7 and 9, Rylan Stages 8 and 12. Evidence below is attributed to whoever made it.


## A Release scope and starting SHA

Release label/version and requirements baseline: SmartCare A3 UG common release v1.0. Requirements baseline: SmartCare A3 2026 revision 2 (FR-01 to FR-09, QRY-01 to QRY-04, FP-01 to FP-03, UI-01 and UI-02; FR-10 retired).
Common starting SHA / branch / applicable members: `9170455` on `main`. It contains the Stage 6 work (Barry, PR #1 and `02fe9ff`), Stage 7 (Tomas, `f5ee9ce`, `14b5887`), Stage 9 (Tomas, final commit `3c1d8ac`) and the Stage 8 repairs (Rylan, `6979b6c`, PR #2). Applies to Rylan, Tomas and Barry.
PG starting SHA / branch / applicable members or not applicable: Not applicable (UG common release).
Working-state review and approved integration: Stage 6 was integrated by PR #1 (Barry, `feature/patient-lookup`). Stage 8 was integrated by PR #2 (Rylan, `debug/stage08`, merge `9170455`). Stages 7 and 9 were committed directly to `main` by group agreement, so they have no PR. No independent reviewer is recorded for any stage, which is disclosed in H and I. Commit `6979b6c` also deleted `stage12/stage12_activities_and_evidence.md`; the file is restored in the final records commit.
Protected common candidate and PG differences: The common candidate is the code at `9170455`. There is no PG extension, so there are no PG differences. After this SHA only documentation and repository-hygiene files change (`README.md`, `project/README.md`, `.gitignore`, `stage08/`, `stage09/`, `stage12/`); `project/smartcare/`, `project/main.py` and `project/tests/` stay as they are.
Feature freeze / owner / verifier: Feature freeze is at `9170455`: no new features and no code changes. Owner: Rylan, as Stage 12 owner. The group agreed to work directly on `main`; no separate verifier is recorded.


## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: **Release with conditions.** Passing tests only show that the behaviour we tested works. Another person cannot reproduce the build if the README setup is incomplete, an unreviewed dependency is an unknown licence and supply-chain risk, and an undocumented limitation lets users rely on behaviour that is not there. All three gaps are cheap to close (finish the README, review or remove the dependency, write the limitation down), and the core behaviour works, so "Do not release" is too strong. The conditions are that those three items are done and the full suite is rerun on the final commit before release. Releasing unconditionally would ignore the gaps.

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | `test_cancelled_appointment_remains_retrievable`, `test_cancel_appointment_changes_status_and_returns_same_object`, `test_cancel_completed_appointment_raises_value_error`, `test_cancel_unknown_appointment_raises_lookup_error`, `test_cancel_appointment_twice_raises_value_error`, `test_list_practitioner_appointments_retains_cancelled_history`; console steps 6 to 8 in D | `project/tests/test_starter.py`, `test_services.py`; `project/smartcare/domain.py`, `data_store.py` @ `9170455`; FR-06 to FR-08 written by Barry (`02fe9ff`), lookup repaired by Rylan (`6979b6c`) | Rylan (Stage 12 check); original author Barry; repair author Rylan | Yes | No independent review of the repair (disclosed in H) |
| Architecture responsibilities are appropriate | Code inspection (section E): domain validates and changes state, the store holds three collections, services coordinate, `queries.py` is pure, only `console.py` reads input and prints | `project/smartcare/*.py` @ `9170455`; `project/README.md` "Structure and responsibilities" | Rylan (inspection); Stage 9 author Tomas | Yes | Style findings only (E, H) |
| Rescheduling is safe — PG only | Not applicable (UG common scope) | Not applicable | Not applicable | Not applicable | Not applicable |
| AI use is responsible — common recheck / PG assurance | Stage 8 Claude diagnosis with ranked causes and decisions (Rylan); Stage 9 Copilot review table (Tomas); Stage 12 disclosure (E) | `stage08/` section F, `stage09/` section E | Rylan | Partly | Stage 8 tutor approval for Claude was not asked; Stage 8 hypotheses were not saved before the consultation (E, H) |
| System is maintainable | 45 tests in 5 files (domain 4, services 13, starter 21, queries 4, console 3); docstrings and type hints on the public functions read; five small modules | `project/tests/`, `project/smartcare/` @ `9170455` | Rylan | Yes | Debt items in G |
| FR-01–03 register/find and validation | `test_required_fields`, `test_registration_and_booking`, `test_duplicate_patient_preserves_original`, `test_duplicate_practitioner_preserves_original`, `test_find_patient_returns_registered_patient`, `test_find_practitioner_*` (5 tests: found, unknown, blank, whitespace, case-sensitive) | `project/tests/test_starter.py`, `test_services.py`, `test_domain.py`; Barry's `feature/patient-lookup` (PR #1) and Stage 6 work | Rylan (Stage 12 check); author Barry | Yes | None |
| FR-04–05 booking/conflict rules | `test_conflict_rule_and_different_practitioner` (same practitioner rejected, different practitioner allowed), `test_cancelled_appointment_does_not_stop_new_appointment_at_same_time`, `test_cannot_duplicate_appointments`, `test_duplicate_appointment_preserves_original`, `test_unregistered_participants_rejected` | `project/tests/test_starter.py`, `test_services.py`; F8-01 repaired in `6979b6c` (Rylan) | Rylan (repair author and Stage 12 check) | Yes | Exact-time rule only, by design (G); no independent review of the repair |
| FR-06–08 cancellation/history/find | Cancel returns the same object with status CANCELLED; repeat cancel `ValueError`; unknown ID `LookupError`; blank and whitespace IDs `ValueError`; completed appointments cannot be cancelled | `project/tests/test_starter.py` (`test_cancel_*`), `test_services.py` @ `9170455` | Rylan (Stage 12 check); author Barry | Yes | None |
| FR-09 and QRY/FP listing/filter/order/purity | `test_select_appointments_filters_practitioner_and_status`, `test_select_appointments_orders_without_mutating_source`, `test_select_appointments_returns_fresh_lists_and_repeats_cleanly`, `test_appointment_sort_key_and_query_use_named_key`; `test_list_practitioner_appointments_known_empty_and_invalid_inputs` | `project/tests/test_queries.py`, `test_services.py`; written by Tomas (Stage 9, `3c1d8ac`) | Rylan (Stage 12 check); author Tomas | Yes | Tests cover representative cases, not all inputs |
| UI full console sequence and error recovery | `test_menu_reuses_session_store_and_recovers_from_invalid_commands`, `test_menu_recovers_from_blank_unknown_and_impossible_date_inputs`, `test_menu_handles_conflicts_freed_slots_and_repeated_cancellation`; D | `project/tests/test_console.py`; `project/smartcare/console.py` (Tomas, Stage 9) | Rylan (Stage 12 check); author Tomas | Yes | No manual console run is recorded; evidence is the tests (D) |
| Session-only scope / FR-10 retired | No file or database code; exit message `Session ended; in-memory data discarded.`; README limitation | `project/smartcare/data_store.py`, `console.py`, `project/README.md` | Rylan | Yes | None |
| PG RES and assurance integration | Not applicable (UG common scope) | Not applicable | Not applicable | Not applicable | Not applicable |


## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | Windows, Python 3.12.2, pytest 9.1.1 (Rylan's machine; the README's Python 3.13 and pytest 8.3.5 baseline was not available) | `project/`: `python -m pytest` | `9170455` | 45 passed, 0 failed in 0.25s | Rylan's terminal output (not saved as a file); per file: test_console 3, test_domain 4, test_queries 4, test_services 13, test_starter 21 |
| Complete PG if applicable | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Affected focused checks after correction | No code correction was made in Stage 12 (H) | – | – | Not run: nothing to recheck | – |
| Full integrated recheck | Windows, Python 3.12.2, pytest 9.1.1 (Rylan) | `project/`: `python -m pytest` | `9170455` | 45 passed, 0 failed in 0.25s | Rylan's terminal output (not saved as a file) |
Prior assertions preserved / reviewed test diff: The suite is 36 tests at Stage 8 (after both repairs) and 45 at Stage 9; the Stage 6 starter tests in `test_starter.py` (21) are still there. The F8-01 and F8-02 failures were fixed in product code (`data_store.py`), not by changing assertions. No tests were added, deleted or weakened in Stage 12, and Stage 12 does not touch `project/tests/`.
Remaining failure / limitation: None failing. Python note: the README states Python 3.13 and pytest 8.3.5 as the teaching baseline, but the final run used Python 3.12.2 and pytest 9.1.1; no run on 3.13 exists. No coverage measurement was made, so no coverage claim is made.


## D Console and end to end demonstration
Evidence for this section is the automated tests in `project/tests/test_console.py`, `test_services.py` and `test_starter.py`, which pass in Rylan's 45-passed run on `9170455`; no separate manual console run is recorded. For the live demonstration, run `python main.py --interactive` in `project/` in one fresh process with these inputs, one per prompt: `1 P1 "Alex Example"`, `3 D1 "Dr One" GP`, `3 D2 "Dr Two" GP`, `2 P1`, `4 D2`, `5 A1 P1 D1 2027-04-23 11:00`, `5 A2 P1 D1 2027-04-23 11:00`, `5 A3 P1 D2 2027-04-23 11:00`, `6 A1`, `6 A1`, `7 A1`, `8 D1 (blank)`, `8 D1 scheduled`, `8 D2 (blank)`, `8 D9 (blank)`, `8 D1 bogus`, `5 A4 P1 D1 2027-02-30 10:00`, `5 A5 P1 D1 2027-04-23 11:00`, `9`, `(blank)`, `0`. "Demo input n" below refers to its order.


| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders | A small clinic needs to register patients and practitioners and book and cancel appointments without clashes, and to keep cancelled history; stakeholders are reception staff, practitioners and patients | Overview problem statement | Explained from the requirements baseline | Overview handout; `project/README.md` |
| Register and find Patient and two Practitioners | 1 P1 "Alex Example"; 3 D1 "Dr One" GP; 3 D2 "Dr Two" GP; 2 P1; 4 D2 | FR-01 to FR-03 | Covered by the registration and lookup tests, which pass in the 45-passed run | Demo inputs 1 to 5; `test_find_patient_returns_registered_patient`, `test_find_practitioner_returns_registered_practitioner` |
| Valid booking | 5 A1 P1 D1 `2027-04-23 11:00` | FR-04 | Covered by `test_registration_and_booking` and the console menu test, which pass | Demo input 6 |
| Same practitioner exact-time conflict rejected | 5 A2 P1 D1 `2027-04-23 11:00` | FR-05, AC-04.1 | Covered by `test_conflict_rule_and_different_practitioner`, which failed with `DID NOT RAISE ValueError` before the Stage 8 repair and passes now | Demo input 7; `test_menu_handles_conflicts_freed_slots_and_repeated_cancellation` |
| Different practitioner same time allowed | 5 A3 P1 D2 `2027-04-23 11:00` | AC-04.2 | Covered by the second half of `test_conflict_rule_and_different_practitioner`, which passes | Demo input 8 |
| Cancel SCHEDULED and retain/find CANCELLED object | 6 A1; 7 A1 | FR-06 to FR-08, AC-05.1, AC-05.2 | Covered by `test_cancelled_appointment_remains_retrievable`, which failed with `LookupError: Appointment not found` before the Stage 8 repair and passes now | Demo inputs 9 and 11 |
| Invalid/repeated cancellation rejected | 6 A1 again | FR-06 | Covered by `test_cancel_appointment_twice_raises_value_error` (two copies), which failed with the same `LookupError` before the repair and pass now | Demo input 10 |
| Default all-status listing | 8 D1 with a blank status | FR-09, QRY-02 | Covered by `test_list_practitioner_appointments_retains_cancelled_history`, which passes | Demo input 12 |
| Explicit filtering / empty vs unknown / deterministic order | 8 D1 `scheduled`; 8 D2 blank; 8 D9 blank | QRY-01 to QRY-04 | Covered by the four query tests and `test_list_practitioner_appointments_known_empty_and_invalid_inputs`, which pass | Demo inputs 13 to 15; `project/tests/test_queries.py` |
| Invalid date/status/menu/lookup recovery and continued operation | 8 D1 `bogus`; 5 A4 `2027-02-30 10:00`; menu `9`; blank choice; then 5 A5 P1 D1 at the freed slot | UI-02 | Covered by `test_menu_recovers_from_blank_unknown_and_impossible_date_inputs` and `test_menu_handles_conflicts_freed_slots_and_repeated_cancellation`, which pass | Demo inputs 16 to 21 |
| Session-only limitation and normal exit | `0` | FR-10 retired | Covered by the console menu tests, which end each session with `0`; the README states data is lost on exit | Demo input 22 |
| One meaningful requirement-linked pytest test explained | `tests/test_starter.py::test_cancelled_appointment_remains_retrievable` | FR-07, AC-05.2 | It books and cancels A001, then finds A001 through the service. It fails if cancelled records are hidden or deleted (the Stage 8 F8-02 fault: `LookupError: Appointment not found`). It does not show that history survives after the session ends. | `project/tests/test_starter.py`; Stage 8 record C, D and G |
| Architecture and one actual AI decision / known limitation | Domain / store / services / queries / console split. AI decision (Stage 8, Rylan with Claude): the suggestion that unequal datetimes caused F8-01 was rejected because the test books both appointments at the same `datetime` value. Limitation: exact-time conflicts only | Architecture, responsible AI | Explained from the code and `stage08/` section F | `stage08/` section F; `project/README.md` |
| PG reschedule identity/participants/time and no-op | Not applicable (UG) | Not applicable | Not applicable | Not applicable |
| PG conflict/invalid status/failure non-mutation | Not applicable (UG) | Not applicable | Not applicable | Not applicable |
| PG old slot / current lookup/list ordering / assurance risks | Not applicable (UG) | Not applicable | Not applicable | Not applicable |
Stable demo owner / fresh process / command: Stage 12 owner Rylan runs the live demo; the console and tests it demonstrates were written by Tomas (Stage 9). Use a fresh process with `python main.py --interactive` from `project/`, following the input sequence above.
PG demonstrations through service/tests or not applicable: Not applicable (UG common scope).


## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | `domain.py`, `data_store.py`, `services.py`, `queries.py`, `console.py` | No finding. Only `console.py` calls `input` and `print`. `select_appointments` takes explicit inputs and returns `sorted(...)` of a new list. Cancellation is `Appointment.cancel`; conflict coordination is in the service and store | No change |
| PascalCase and snake_case naming | All modules and tests | No finding in source: classes are PascalCase and functions snake_case. Minor: two test names are misspelt (`test_patient_registeration_*`, `test_appointment_feilds_not_empty`) | Accepted as debt (G); no change after the freeze |
| Useful type hints and meaningful docstrings | smartcare/*.py | No finding: public functions are typed and documented. services.py still has a docstring beginning `Stage 9:` | Optional wording change in list_practitioner_appointments |
| Four-space indentation and imports/layout | Files read in `project/smartcare/` | No linter was run. The files read use four-space indentation and grouped imports. | No change |
| Focused methods / duplication / dead or commented code | `console.py` `run_menu` | Finding: `run_menu` is long (about 100 lines) with one branch per menu choice; no commented-out code seen | Accepted as a maintainability limit (G); splitting it would be a code change after the freeze |
| Globals / leakage / unnecessary inheritance or frameworks | smartcare/*.py | No finding: no globals, inheritance or frameworks; the console creates one store per session | No change |
| No SQLite/persistence/repository ABCs/speculative features | imports and project tree | No finding: standard library only, no persistence, no rescheduling code | No change |
| Synthetic data / secrets / dependencies / provenance | grep and tree inspection | No secrets found by searching for password, secret, token and API key; only synthetic names; one dev dependency, pytest 8.3.5. `.idea/` IDE folder was in the repository | `.idea/` added to .gitignore; remove it from Git with `git rm -r --cached .idea` |
| Significant common Copilot contributions and human verification | `stage08/` section F; `stage09/` section E | Stage 8: Claude (run by Rylan) gave three ranked causes for each defect; two were rejected on evidence and one was accepted as the root cause for each. Stage 9: Copilot's review (Tomas) produced one Important finding, accepted and covered by two added console tests, and Optional findings that were rejected | The Stage 8 and Stage 12 AI-assisted text was not independently reviewed |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | Not applicable | Not applicable (UG) | Not applicable |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| Claude (Rylan, Stage 8): F8-01 root cause is the inverted practitioner comparison (`!=` instead of `==`) in `has_practitioner_conflict` | FR-05, AC-04.1, AC-04.2; `data_store.py` | The failing test showed `DID NOT RAISE ValueError`; Rylan read the practitioner condition in the method and changed it, after which the test passed | Accept: it matched the failing test and the requirement | Repaired in `6979b6c`, merged in `9170455` |
| Claude (Rylan, Stage 8): F8-01 might be caused by unequal datetimes (seconds or timezone) | AC-04.1; the test's `when` value | Read the test: both bookings use the same `datetime` value | Reject: nothing in the failure pointed to time handling | No change |
| Claude (Rylan, Stage 8): F8-02 root cause is the cancelled-status filter in `SmartCareDataStore.find_appointment` | FR-07, AC-05.2 | The failing tests showed `LookupError: Appointment not found` from the lookup; the repair touched only the lookup condition and the retention tests then passed | Accept: the record was hidden, not deleted | Condition removed in `6979b6c` |
| Claude (Rylan, Stage 8): F8-02 might be caused by cancellation deleting the record | FR-07 | The repair did not touch the cancel logic and the retention tests passed, so the record was never deleted | Reject: wrong cause | No change |
| Copilot (Tomas, Stage 9): console tests miss impossible dates, blank input, repeated cancellation and conflict recovery | UI-02; `project/tests/test_console.py` | Read the existing menu test against the list of cases | Accept: these cases needed menu-level coverage | Two console tests added (3 console tests now) |
| Copilot (Tomas, Stage 9): direct `select_appointments` calls with a non-enum status silently return no matches | `queries.py`; `services.py` | The service already rejects non-enum values; the requirements do not ask the query to validate | Reject: over-engineering | No change |
| Claude (Rylan, Stage 12): drafted this record from the repository, Rylan's git history and Rylan's test output | Release documentation only | Rylan checked the results against his own test run and the git log | Accept after review; every result comes from a command that was run | No code changed |
Access route or approved equivalent / limitations: GitHub Copilot (the course-nominated assistant) was used for the Stage 9 review (Tomas). Rylan used Claude as an equivalent route at Stages 8 and 12; tutor approval for Claude was not asked. Limit: Claude could not see the team's own machines, and its output was treated as hypotheses to be checked.
Available AI evidence and missing evidence honestly disclosed: Available: the Stage 8 prompts, ranked suggestions and decisions (`stage08/` section F) and the Stage 9 Copilot prompt, response and decision table (`stage09/` section E). Missing: no exported transcripts; Rylan says the Stage 8 hypotheses came before the Claude consultation, but they were not saved or committed separately and the section E text was written up with Claude's help; the Stage 12 record was also drafted with Claude.


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
Setup/run/test commands and observed results: Rylan: `python -m pytest` from `project/` on `main` (`9170455`): 45 passed in 0.25s. No other setup or run result is recorded.
Missing local file or setup gap / remedy and recheck: None found; no clean-clone recheck was done.


## G Known limitations debt and release notes

Delivered features: Register and find patients and practitioners with validation. Book appointments with same-practitioner exact-time conflict rejection. Cancel while keeping history, and find cancelled appointments. List a practitioner's appointments (all statuses or one), ordered by date/time then ID, through a pure query. An interactive menu that recovers from invalid input. A runnable demo.
Important fixes: F8-01: the conflict check compared practitioners with `!=` instead of `==`, so a second booking for the same practitioner was accepted (Rylan, `6979b6c`). F8-02: lookup skipped cancelled appointments, so history could not be found and a repeat cancel raised `LookupError` instead of `ValueError` (Rylan, `6979b6c`). Both are guarded by existing tests, and `PR #2` merged them as `9170455`.
Architecture/quality improvements: The status comparison uses the `AppointmentStatus` enum instead of a string; pure query layer (`queries.py`) separated from the services and console (Tomas, Stage 9); `project/README.md` rewritten with scope, limitations, structure and setup; the suite grew from the Stage 6 starter tests to 45 across domain, services, queries and console.
Known limitations: Session-only data. Local, minute-precision time. Only exact-time conflicts for the same practitioner. No duration or overlap checks and no patient double-booking check. Case-sensitive IDs. No rescheduling, editing or deleting. Not production software.
AI-assisted development note: AI assistants were used (GitHub Copilot at Stage 9, Claude at Stages 8 and 12), and their output was checked against code, tests and requirements; decisions are recorded in the stage records.

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| Misspelt test names (`registeration`, `feilds`) | Harder to search | Low | Rename the tests | Accepted |
| `run_menu` is about 100 lines with eight branches | Harder to read and test in pieces | Low | Split into helper functions with tests | Accepted for this release |
| Only exact-time conflicts (no durations) | Overlapping appointments of different lengths are possible | Medium (for real use) | Add durations and an overlap rule if requirements change | Accepted: this is the specified rule (AC-04.1), so it is a scope limit, not a defect |
| Session-only data | Records vanish when the program ends | Medium (for real use) | Add persistence in future work | Accepted: FR-10 is retired |
| No independent review at Stages 8, 9 and 12; tests not run on Python 3.13 | Evidence is weaker than the process asks for | Medium (assessment) | Another member reviews and reruns on 3.13 if time allows | Accepted and disclosed here, not hidden |
Session-only synthetic data and minute-precision local time: All data is held in memory for one session and lost on exit (FR-10 retired). Only synthetic records are used. Times are naive local `datetime` values entered as `YYYY-MM-DD HH:MM`, so seconds and time zones are not represented.
Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: None of these exist and none are in scope. There is no login or role check, no patient portal, no reminders, no billing or insurance, and no clinical decision support or AI features in the app.
Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: Single user, single process, in-memory and not tested with large data. Listing is a linear scan. No time zone or daylight-saving policy, no logging, monitoring or deployment, and a text-only console with no accessibility review.
Difference between accepted scope limit and unresolved required behaviour: An accepted scope limit is something the requirements deliberately leave out, such as persistence (FR-10 retired) or duration-based conflicts; it is documented and needs no fix. Unresolved required behaviour would be an in-scope requirement that does not work, for example if a cancelled appointment could not be found (FR-07); that would block release. None was found: every in-scope requirement has passing tests (B).
PG assurance residual risks / owner / status or not applicable: Not applicable (UG common scope).


## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| Reproducibility: `project/README.md` | It still carried the Stage 6 starter title and lacked scope, limitations, structure and setup | Medium: misleading for a marker or new developer | Rylan (Stage 12) | `project/README.md` rewritten; root `README.md` group index filled in | Commands in the README run by Rylan (`python -m pytest`, 45 passed) | None |
| Submission package: Stage 12 record missing on `main` | `git show --stat 6979b6c` showed it deleted `stage12/stage12_activities_and_evidence.md` | Medium: a required record was gone | Rylan: restore it | Record restored in the final records commit | Present in the final commit and ZIP | None |
| Repository hygiene: IDE metadata | `.idea/` was tracked | Low | Rylan | `.idea/` added to `.gitignore` and removed from tracking (`git rm -r --cached .idea`) | Not a code change | None |
| Responsible-AI evidence (Stage 8) | Hypotheses were not saved before the Claude consultation; tutor approval was not asked | Medium: assessment evidence, not code | Rylan: disclose | Disclosure in E and in `stage08/` | Re-read the records | Cannot be recreated afterwards, so it is disclosed |
| Independent review | No other member reviewed the Stage 8 PR, Stage 9 or Stage 12; Stages 7 and 9 went straight to `main` | Medium: process evidence | Group: disclose | Disclosure in I and J | – | Accepted and disclosed |
| Code quality findings (E) | Long `run_menu` function; misspelt test names; no linter run | Low | Group decision: accept as debt | None in Stage 12 | – | Listed in G |
Justified no-change conclusion if no defect found: No functional defect was found. All 45 tests pass on `9170455`; the console and invalid-input paths are covered by passing tests (D); the code inspection found only cosmetic issues (E). No code was changed after the feature freeze, so the tested code SHA stays `9170455`.
Release blockers still open / status: None for the software. The review, Python 3.13 and clean-clone gaps listed in G and I are disclosed limitations of the evidence, not defects in the code.


## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA: Stage 6: PR #1 (`feature/patient-lookup`, Barry). Stage 7: direct commits `f5ee9ce` and `14b5887` (Tomas). Stage 8: PR #2 https://github.com/Pengi376/ST-Assignment3/pull/2 (`debug/stage08`, `6979b6c`, merged 2026-11-09 21:45 +1100 as `9170455`; Rylan). Stage 9: direct commits `5e218c2`, `4629b3d`, `f5f8c2c`, `3c1d8ac` (Tomas). Stage 12: direct commit to `main` by group agreement. No GitHub issues were opened. Code reviewed and tested: `9170455`.
Independent reviewer / feedback / response: None at any stage. PR #1 was merged by BarrytheLegoMan, PR #2 by Pengi376, and the group agreed to commit the remaining stages directly to `main`. No review feedback exists to respond to.
Integration commit / full recheck: Merge commit `9170455` (PR #2). Recheck by Rylan on `main`: `python -m pytest` from `project/`, 45 passed in 0.25s (Python 3.12.2, pytest 9.1.1).
Tracked and untracked file inspection / cleanliness: The tracked tree has `project/` (source and 5 test files), the stage records, `README.md`, `.gitignore`, `.gitattributes` and `.idea/`, which is removed from tracking in the final commit. No `__pycache__`, `.venv`, `.env`, `.pytest_cache` or Stage 8 tool files are tracked. The Stage 8 recovery backup (`project/.stage8_faults`) is listed in `.gitignore`.
Secrets/staff material/caches/tool-metadata exclusion check: Search for password, secret, token and API key found nothing in code or README. .gitignore excludes .stage8_faults/, the check/verify folders and `.idea/`; the Stage 8 tool is kept outside the repository.
Candidate recovery plan / known-good SHA: Known-good SHA `9170455c418e92ca245918e789a4ae417103587c`. If a later commit breaks anything, `git revert` it; alternatively build the ZIP from `9170455` with `git archive`, since later commits are documentation only.
Named substantive contributions: Barry (BarrytheLegoMan): Stage 6 foundation and FR-02, FR-06 and FR-07 with tests (`02fe9ff`), the `feature/patient-lookup` branch and PR #1 (`e0bf952`, `f3303e7`), repository layout fix (`ea582f1`). Tomas (Tom-uc3): Stage 6 starting SHA and review (`e8fbb21`, `aae6611`), Stage 7 testing and verification (`f5ee9ce`, `14b5887`), Stage 9 queries, practitioner listing, interactive console, tests and record (`5e218c2`, `4629b3d`, `f5f8c2c`, `3c1d8ac`). Rylan (Pengi376): repository and starter pack (`de31dc9`, `583bb64`, `15c87c0`), Stage 8 preparation and record (`a3feb86`, `c549c68`), the F8-01 and F8-02 repairs and PR #2 (`6979b6c`, `9170455`), and Stage 12.


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: READY WITH DOCUMENTED LIMITATIONS. The evidence supports release of the common scope, and the limitations in G and the evidence gaps in H and I are written down.
Approver / date / rationale and evidence: Group 1 (Rylan, Tomas, Barry), recorded by Rylan as Stage 12 owner, 2026-11-09. Rationale: all 45 tests pass on `9170455`; both Stage 8 repairs are covered by tests; the console and invalid-input paths are covered by passing tests; the known limitations are documented and outside the required scope.
What risks remain / conditions / owners: (1) No independent review at any stage (group); (2) tests run on Python 3.12.2 rather than the README's 3.13 (whoever has 3.13 can rerun); (3) cosmetic debt items in G (accepted); (4) Stage 8 hypotheses not saved before the consultation (Rylan, disclosed). No condition blocks release.
Can the team explain the system: Each member explains the stages they built, using section N: Barry Stage 6 (domain, validation, cancellation), Tomas Stages 7 and 9 (testing, queries, console), Rylan Stages 8 and 12 (diagnosis, repairs, release record). No joint rehearsal is recorded.
Can a change be recovered: Yes. Every change is in Git history, with the known-good SHA `9170455` recorded. A faulty change is undone with `git revert`, or the candidate is rebuilt from `9170455` with `git archive` (I).
Common decision / PG decision where different: Common decision as above. PG: not applicable (UG common scope).


## K Final tested release SHA

Exact common tested SHA: `9170455c418e92ca245918e789a4ae417103587c` (45 passed, C).
Exact PG tested SHA or not applicable: Not applicable (UG common scope).
Final submitted SHA / repository URL: The head of `main` after the final records commit (`git rev-parse HEAD`); a record cannot contain the SHA of the commit that contains it. Repository https://github.com/Pengi376/ST-Assignment3
Evidence-only later commit and difference explanation: The final records commit changes only documentation and hygiene files (`README.md`, `project/README.md`, `.gitignore`, `stage08/`, `stage09/`, `stage12/`, and untracking `.idea/`). `git diff --stat 9170455 HEAD -- project/smartcare project/main.py project/tests` should print nothing.
Executable changes after testing and re-verification: None.
Source ZIP name / SHA correspondence / extracted comparison: SmartCare_Group1.zip, made with `git archive --format=zip -o SmartCare_Group1.zip HEAD` from the submitted commit, so its contents correspond exactly to that commit.


## L Submission package verification

- [x] Feature freeze and scoped requirements traced.
- [x] Applicable full regressions, integrated demo and invalid paths verified.
- [x] Architecture/code quality and final AI/dependency checks complete.
- [ ] Root README and project/README reproduced by another verifier.
- [x] Release notes, technical debt and limitations visible.
- [ ] Independent human review, integration and release decision recorded.
- [ ] Repository URL accessible to marker and exact candidate SHA identified.
- [ ] One source ZIP from submitted commit with root README.md and .gitignore.
- [ ] project/ source and all accumulated applicable tests included.
- [x] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [ ] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [ ] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [ ] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: As set out in the published assessment instructions; not restated here.
Deadline/timezone: As set out in the published assessment instructions; not restated here.
Repository access arrangement: The repository is https://github.com/Pengi376/ST-Assignment3; the source ZIP is the submitted copy.
Mixed-candidate upload arrangement: Not applicable if all members are UG
Oral/video recording/accessibility arrangements: As set out in the published assessment instructions; not restated here.
Remaining administration or release dependency: Open items are listed in H.


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

Strongest evidence SmartCare is ready: All 45 tests pass on `9170455`, including the tests that guard both Stage 8 faults (conflict rule and retained history). The console tests, including every invalid input, pass, and the code has no persistence, globals or speculative features.
Weakest area: Process evidence: no independent review at any stage, no clean-clone check, tests run on Python 3.12.2 instead of 3.13, and Stage 8 hypotheses not saved before the AI consultation. The code itself is well tested.
How AI use changed from Stage 1 to Stage 12: The team's own record shows AI used later as a checker rather than a source: at Stage 9 Tomas wrote the design first and used Copilot only as a reviewer, and at Stage 8 Rylan used Claude after reproducing the failures, then tested each suggested cause. Some suggestions were rejected on evidence.
Start doing — engineering and AI use: Save the hypothesis or design before asking an AI; open a PR for every stage and have another member review it; run a linter and a clean-clone check before release.
Stop doing — engineering and AI use: Committing straight to `main` without review; leaving records until the end; accepting an AI explanation because it sounds plausible.
Continue doing — engineering and AI use: Small commits with focused tests, rerunning the full suite after each change, and recording the evidence for each AI suggestion.
What worked / caused rework / future delivery improvement: Worked: tests that failed for a clear reason made the Stage 8 diagnosis quick. Rework: a Stage 8 commit deleted the Stage 12 record, and the root README showed an out-of-date SHA. Improvement: review every merge, and keep the README and records updated at each stage.
One paragraph — If AI can write code why do we still need software engineers: AI can produce plausible code quickly, but plausible is not the same as correct. In Stage 8 the AI's suggested causes were only useful because the failures had already been reproduced and tests could tell the causes apart; some suggestions, such as a datetime mismatch or deletion on cancel, were wrong and were rejected on evidence. Engineers decide what the system must do, keep it inside its requirements, check each change with tests and review, and are accountable for what is released. AI changes how fast we write things, not who is responsible.

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | A small clinic registers patients and practitioners and books and cancels appointments without clashes and with kept history; stakeholders are reception staff, practitioners and patients. Overview handout |
| Two requirements and acceptance criteria | FR-05 / AC-04.1 and AC-04.2: the same practitioner cannot have two SCHEDULED appointments at the same time, a different practitioner can. FR-07 / AC-05.2: a cancelled appointment stays retrievable with status CANCELLED. `stage06/` and the requirements baseline |
| Domain model and architecture | Patient, Practitioner and Appointment (with `AppointmentStatus`) in `domain.py`; one `SmartCareDataStore`; services; pure queries; console. `project/README.md` |
| Design trade-off | In-memory dictionaries are simple and fast to test but lose data on exit (FR-10 retired); a database would persist but add complexity outside the scope. Keeping queries pure makes them easy to test but adds a layer. |
| Meaningful test and its limits / 100 percent coverage | `test_conflict_rule_and_different_practitioner` fails if the practitioner comparison is inverted (F8-01). It checks one scenario, not all inputs or large data. No coverage was measured, and even 100% coverage would only show lines ran, not that every behaviour is right |
| Diagnosed defect and verification | F8-02: the lookup hid cancelled records (the list still held them); verified by `test_cancelled_appointment_remains_retrievable` and the full suite. `stage08/` C, D, G |
| Shared store and session-state/query responsibilities | All three services share one store object so a patient registered by one service is visible to booking. The store holds the session state, and the query functions only read lists passed to them and return new ones. |
| What would break if session-state lookup/query responsibilities changed? | If each service created its own store, booking would not find registered patients. If a query sorted its source in place, callers' lists and stored order would change unexpectedly. |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | Cancellation is a rule about one appointment's own status (only SCHEDULED can be cancelled), so it belongs in the Appointment. Checking a clash needs all appointments for a practitioner, so a service coordinates it with the store. |
| FR-07 retained history test | `test_cancelled_appointment_remains_retrievable` and `test_list_practitioner_appointments_retains_cancelled_history` in `project/tests/` |
| Actual AI change rejected/modified or honestly accepted with verification | Rejected: the unequal-datetime cause for F8-01, and deletion-on-cancel for F8-02. Accepted with checks: the inverted comparison and the status filter. `stage08/` F |
| Unresolved limitation / future production work | Session-only data and exact-time conflicts; production would need persistence, durations, authentication and time zones (G) |
| Personal implementation contribution | Barry: Stage 6 services and tests (FR-02, FR-06, FR-07), `02fe9ff`. Tomas: Stage 9 queries, practitioner listing and console, `3c1d8ac`. Rylan: Stage 8 repairs, `6979b6c`. See I. |
| Personal test/review/design/integration contribution | Barry: Stage 6 testing and PR #1. Tomas: Stage 7 testing and verification (`f5ee9ce`) and Stage 9 tests and Copilot review. Rylan: Stage 8 preparation, regression runs, PR #2 and integration to `main`, and Stage 12. |
| PG agentic change and rescheduling verification | Not applicable (UG) |
| PG responsible-AI risk/remediation or supported no finding | Not applicable (UG) |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: Not undertaken.
Separate reflection / peer / common team viva evidence links and routing: Routed separately as set out in the published assessment instructions; not restated here.
No further coding stage. Later corrections use the published assessment process.

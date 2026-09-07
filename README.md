# Feedback Theme Board

Classifies participant feedback into a facilitator-defined frozen theme set, then lets the participants themselves vote on the board priority.

## Why it is an Intelligent Contract

Validators independently score every frozen theme `0`, `1`, or `2` for each feedback entry. The contract stores the complete ordered score vector and deterministically selects the unique highest positive theme; ties and all-zero vectors become OTHER. Participants—not the model—then vote on priority through the board lifecycle.

## Reusable deployment model

Deploy once per feedback question or event. A deployment supports six named themes and twenty one-entry-per-address participants; reuse the source for a new board.

One completed deployment is an auditable record and is not reset or silently repurposed. Reuse means deploying the same reviewed source with new constructor data.

## Roles and workflow

A facilitator defines themes and controls phase changes; each participant submits once and receives one priority vote after all feedback is classified. Priority voting can be finalized after a strict-majority quorum, so one nonvoting participant cannot stall a three-person board.

State path: `DEFINING_THEMES → COLLECTING_FEEDBACK → CLASSIFYING → PRIORITY_VOTING → COMPLETE`

## Evidence boundary

Feedback question, classification standard, frozen theme descriptions, and participant-submitted feedback text.

The contract uses only the stored question, standard, frozen theme descriptions, and feedback. It does not enrich entries from profiles, sentiment services, or outside records.

## Core invariants

- The theme taxonomy freezes before feedback collection.
- Consensus binds the complete per-theme score vector; the model never supplies the selected theme ID.
- Priority quorum is deterministic: `floor(eligible participants / 2) + 1`.
- After quorum, the facilitator may finalize using the complete recorded tally; nonvoters remain counted and cannot block completion.
- A unique highest tally wins, while tied highest tallies are recorded as `NO_PRIORITY`.

## Public interface

Write methods: `add_theme, classify_feedback, finalize_board, lock_feedback, open_feedback, submit_feedback, vote_priority`

View methods: `get_feedback, get_policy, get_state, get_theme`

`get_policy` exposes the machine-readable operating boundary and confirms that this contract never custodies funds.

## Verification

Pinned GenVM runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

```powershell
python -m pip install -r requirements.txt
genvm-lint check contracts/feedback_theme_board.py
genvm-lint typecheck contracts/feedback_theme_board.py
pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
gltest tests/integration/test_glsim_consensus.py --network localnet -q
```

The StudioNet smoke test is opt-in and requires three disposable owner-specific test accounts. It reads state using `LATEST_FINAL` and asserts successful finalized execution.

## Current StudioNet deployment

The deployment below contains the strict-majority quorum source and a completed three-participant demonstration with one nonvoter.

- Contract: https://explorer-studio.genlayer.com/address/0xDA680f355dfDC1178357844AB70cc197D5b910a8
- Studio import: https://studio.genlayer.com/?import-contract=0xDA680f355dfDC1178357844AB70cc197D5b910a8
- Deployment transaction: https://explorer-studio.genlayer.com/tx/0x44dc5684cfc2c42eb0f6569332a6506ffd82c9307398cc204129e5804776c7da
- Intelligent classification transaction: https://explorer-studio.genlayer.com/tx/0xf9403f3a2adb9a71332063e0f2013190dbc572e376ab0f97c01fba830d5d66fe
- Quorum finalization transaction: https://explorer-studio.genlayer.com/tx/0xfce029cef108fb6b4f12ccb242f713afdd386b95f7b57de6e1df1443905e1b0a
- Observed final state: `{"board_phase":"COMPLETE","feedback_count":3,"vote_count":2,"priority_quorum":2,"nonvoter_count":1,"priority_theme":"ACCESS"}`
- Audited source SHA-256: `7c231f53a40551898d23ecfe4baa46af7a9d81c79048545355cf3bed90ac0dff`

## Limitations

- The facilitator chooses the taxonomy and may omit a useful theme.
- The facilitator must call `finalize_board` after quorum is reached; later eligible votes are not accepted once the board is complete.
- Feedback text is public and should not include private or medical information.

## Repository map

- `contracts/feedback_theme_board.py` — Intelligent Contract source
- `tests/direct` — fast leader/validator and lifecycle tests
- `tests/integration/test_glsim_consensus.py` — five-validator simulator flow
- `tests/integration/test_studionet_smoke.py` — live opt-in proof
- `deployments/studionet.json` — source-bound public deployment evidence
- `ARCHITECTURE.md`, `SOURCE_POLICY.md`, `SECURITY.md`, `AUDIT.md` — review material

License: MIT.

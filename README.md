# Feedback Theme Board

Classifies participant feedback into a facilitator-defined frozen theme set, then lets the participants themselves vote on the board priority.

## Why it is an Intelligent Contract

Validators independently score every frozen theme `0`, `1`, or `2` for each feedback entry. The contract stores the complete ordered score vector and deterministically selects the unique highest positive theme; ties and all-zero vectors become OTHER. Participants—not the model—then vote on priority through the board lifecycle.

## Reusable deployment model

Deploy once per feedback question or event. A deployment supports six named themes and twenty one-entry-per-address participants; reuse the source for a new board.

One completed deployment is an auditable record and is not reset or silently repurposed. Reuse means deploying the same reviewed source with new constructor data.

## Roles and workflow

A facilitator defines themes and controls phase changes; each participant submits once and receives one priority vote after all feedback is classified.

State path: `DEFINING_THEMES → COLLECTING_FEEDBACK → CLASSIFYING → PRIORITY_VOTING → COMPLETE`

## Evidence boundary

Feedback question, classification standard, frozen theme descriptions, and participant-submitted feedback text.

The contract uses only the stored question, standard, frozen theme descriptions, and feedback. It does not enrich entries from profiles, sentiment services, or outside records.

## Core invariants

- The theme taxonomy freezes before feedback collection.
- Consensus binds the complete per-theme score vector; the model never supplies the selected theme ID.
- The final priority comes from authenticated participant votes, with ties recorded as NO_PRIORITY.

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

## Previous StudioNet deployment (superseded)

These links and the recorded source hash refer to the earlier single-theme implementation. Redeploy the score-vector version and replace this section before submission.

- Contract: https://explorer-studio.genlayer.com/address/0x936D5aA5570bFE30AfBF5334144d2368A6aE31b5
- Studio import: https://studio.genlayer.com/?import-contract=0x936D5aA5570bFE30AfBF5334144d2368A6aE31b5
- Deployment transaction: https://explorer-studio.genlayer.com/tx/0x6111c206b69b1b49f201c9914b60c3a464986bab040ed4749bd27675d4cae0cd
- Intelligent transaction: https://explorer-studio.genlayer.com/tx/0x6ca322f6975435a7b9c78b2482e0476783ddead0bfc3ff32cbe322097d1c23f6
- Observed legacy final-state sample: `{"theme": "ACCESS"}`
- Audited source SHA-256: `274e48028f03b0ddeab7782f68acfccd706129438cf11a1ddc9081e9e994bf99`

## Limitations

- The facilitator chooses the taxonomy and may omit a useful theme.
- Every participant must vote before finalization.
- Feedback text is public and should not include private or medical information.

## Repository map

- `contracts/feedback_theme_board.py` — Intelligent Contract source
- `tests/direct` — fast leader/validator and lifecycle tests
- `tests/integration/test_glsim_consensus.py` — five-validator simulator flow
- `tests/integration/test_studionet_smoke.py` — live opt-in proof
- `deployments/studionet.json` — source-bound public deployment evidence
- `ARCHITECTURE.md`, `SOURCE_POLICY.md`, `SECURITY.md`, `AUDIT.md` — review material

License: MIT.

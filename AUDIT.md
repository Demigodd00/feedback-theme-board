# Structured Judgment Update Audit

Audit date: 2026-08-31

Audited source: `contracts/feedback_theme_board.py`

Source SHA-256: `2f0de13f5163f437e83afa6b9b7bf033add7def405ebac602cf339b81cbd8151`

## Outcome

The category-only judgment identified in the prior review has been removed. Validators bind a complete ordered 0/1/2 relevance-score vector across every frozen theme. The contract stores that vector and deterministically selects a unique positive maximum, with ties and all-zero vectors mapped to OTHER before participant priority voting.

The current source passed local and GitHub verification. It is not ready to submit with the previous StudioNet links: that deployment is bound to the superseded source and must be replaced by a deployment of the current hash.

## Verification matrix

| Check | Result |
| --- | --- |
| Concrete GenVM runner pin | Pass |
| `genvm-lint check` | Pass |
| `genvm-lint typecheck` | Pass in GitHub CI |
| Hardened direct tests | Pass — 3 tests |
| Independent validator replay over intermediate results | Pass |
| Five-validator GLSim integration | Pass |
| Deterministic final-outcome derivation | Pass |
| Structured intermediate result stored on-chain | Pass |
| Meaningful reusable lifecycle after judgment | Pass |
| Current-source StudioNet deployment and intelligent write | Pending redeployment |
| Previous deployment | Superseded; do not submit as current proof |
| Fund custody and cross-contract calls | None |

## Rejection issue addressed

The model no longer returns a final category for one equality check. Consensus binds independently replayed intermediate findings, the contract derives the final outcome by explicit rules, and that outcome controls later contract-specific state transitions.

## Required before submission

1. Deploy the current `contracts/feedback_theme_board.py` source.
2. Execute and finalize a representative intelligent write.
3. Record the new contract address, transaction hashes, observed intermediate fields, and source hash.
4. Replace the pending fields in `SUBMISSION.md`, `README.md`, and `deployments/studionet.json`.

Legacy deployment address: `0x936D5aA5570bFE30AfBF5334144d2368A6aE31b5`.

# Security

## Scope

This repository is a bounded Intelligent Contract, its direct and five-validator tests, and an opt-in StudioNet smoke test. It has no frontend, backend, database, token, payout, upgrade proxy, or privileged secret.

## Trust model

The one-field consensus schema avoids disagreement over decorative prose or subjective urgency, and participant voting determines the outcome that matters.

A facilitator defines themes and controls phase changes; each participant submits once and receives one priority vote after all feedback is classified.

## Implemented controls

- Concrete immutable GenVM runner hash; no floating `latest` dependency.
- Address normalization, explicit role separation, one-time actions, collection caps, and lifecycle locks.
- Bounded text and strict model-response schemas with `[EXPECTED]` versus `[LLM_ERROR]` failure classes.
- Sorted, delimited untrusted evidence packets and independent validator replay.
- All storage is read before entering nondeterministic callbacks; the final static audit found zero `self`/storage reads inside consensus callbacks.
- No cross-contract calls, fund custody, transfer, automatic purchase, deletion, or off-chain webhook.
- `.env`, caches, artifacts, wallet files, and local deployment material are ignored. Live wallets are encrypted and stored outside the workspace.

## Contract-specific safety properties

- The theme taxonomy freezes before feedback collection.
- Consensus is limited to one stable theme field; subjective urgency was deliberately removed.
- The final priority comes from authenticated participant votes, with ties recorded as NO_PRIORITY.

## Residual risks

- The facilitator chooses the taxonomy and may omit a useful theme.
- Every participant must vote before finalization.
- Feedback text is public and should not include private or medical information.

This contract should not be used to make legal, medical, financial, employment, admission, or physical-safety decisions unless its own policy explicitly supports that domain and an independent professional review is added. This version does not.

## Reporting

Report a vulnerability privately to the repository owner with the contract name, affected method, reproduction, expected invariant, and impact. Do not include private keys or personal data. The owner should reproduce it in a fresh disposable deployment before publishing details.

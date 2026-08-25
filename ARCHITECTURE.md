# Architecture

## Deployment boundary

Deploy once per feedback question or event. A deployment supports six named themes and twenty one-entry-per-address participants; reuse the source for a new board.

The constructor establishes the deployment's subject and policy. Later calls add only the bounded records allowed by the state machine; a completed instance cannot be reopened.

## Participants

A facilitator defines themes and controls phase changes; each participant submits once and receives one priority vote after all feedback is classified.

Addresses are normalized before authorization comparisons. Role checks and phase gates execute before any semantic assessment.

## State machine

`DEFINING_THEMES → COLLECTING_FEEDBACK → CLASSIFYING → PRIORITY_VOTING → COMPLETE`

The phase value is the primary lifecycle lock. Every write either advances that path, performs a documented single-use loop, or fails with an `[EXPECTED]` user error.

## Evidence assembly

Feedback question, classification standard, frozen theme descriptions, and participant-submitted feedback text.

Before consensus, the contract normalizes bounded text, reads all required storage, constructs a sorted JSON packet, and places it between explicit data delimiters. The nested nondeterministic callbacks use captured plain values and do not read contract storage.

## Consensus boundary

Return only the closest supplied theme ID or OTHER. The AI does not assign urgency or decide the priority.

The leader callback validates JSON shape, field types, closed categories, masks, and length bounds. A validator reruns the same semantic operation and rejects disagreement. Where an explanatory label can vary harmlessly, consensus binds the stable decision field while still checking that the leader's advisory text is well formed.

## Deterministic boundary

One submission/vote per address, theme counts, all-entry classification, vote tallying, and NO_PRIORITY tie handling are deterministic.

Important invariants:

- The theme taxonomy freezes before feedback collection.
- Consensus is limited to one stable theme field; subjective urgency was deliberately removed.
- The final priority comes from authenticated participant votes, with ties recorded as NO_PRIORITY.

No method sends value, pays rewards, escrows assets, deletes external data, or calls another contract.

## Failure model

- Invalid caller input or lifecycle use raises `[EXPECTED]` and leaves state unchanged.
- Malformed or out-of-policy model output raises `[LLM_ERROR]` and leaves the record assessable.
- Validator disagreement cannot commit an assessment.
- StudioNet proof reads explicitly target `LATEST_FINAL`, avoiding stale pre-final state.

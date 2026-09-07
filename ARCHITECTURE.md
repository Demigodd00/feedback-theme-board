# Architecture

## Deployment boundary

Deploy once per feedback question or event. A deployment supports six named themes and twenty one-entry-per-address participants; reuse the source for a new board.

The constructor establishes the deployment's subject and policy. Later calls add only the bounded records allowed by the state machine; a completed instance cannot be reopened.

## Participants

A facilitator defines themes and controls phase changes; each participant submits once and receives one priority vote after all feedback is classified. A strict-majority quorum prevents an absent participant from indefinitely blocking completion.

Addresses are normalized before authorization comparisons. Role checks and phase gates execute before any semantic assessment.

## State machine

`DEFINING_THEMES → COLLECTING_FEEDBACK → CLASSIFYING → PRIORITY_VOTING → COMPLETE`

The phase value is the primary lifecycle lock. Every write either advances that path, performs a documented single-use loop, or fails with an `[EXPECTED]` user error.

## Evidence assembly

Feedback question, classification standard, frozen theme descriptions, and participant-submitted feedback text.

Before consensus, the contract normalizes bounded text, reads all required storage, constructs a sorted JSON packet, and places it between explicit data delimiters. The nested nondeterministic callbacks use captured plain values and do not read contract storage.

## Consensus boundary

Validators independently return one `0/1/2` relevance score for every frozen theme in its stored order. Consensus binds the complete vector, not a preselected theme ID, and does not assess urgency.

The leader callback validates exact vector length and the closed score alphabet. A validator reruns the same per-theme analysis and rejects disagreement in any score. The contract deterministically selects a unique positive maximum and falls back to OTHER for ties or all-zero vectors.

## Deterministic boundary

Theme selection, one submission/vote per address, theme counts, all-entry classification, strict-majority quorum calculation, vote tallying, and NO_PRIORITY tie handling are deterministic.

Important invariants:

- The theme taxonomy freezes before feedback collection.
- Consensus binds every stored per-theme score; subjective urgency was deliberately removed.
- Priority quorum is `floor(eligible participants / 2) + 1`; after quorum the facilitator can finalize without every participant voting.
- The unique highest recorded tally wins; tied highest tallies become `NO_PRIORITY`.
- `get_state` exposes quorum, votes still needed, and nonvoter count.

No method sends value, pays rewards, escrows assets, deletes external data, or calls another contract.

## Failure model

- Invalid caller input or lifecycle use raises `[EXPECTED]` and leaves state unchanged.
- Malformed or out-of-policy model output raises `[LLM_ERROR]` and leaves the record assessable.
- Validator disagreement cannot commit an assessment.
- StudioNet proof reads explicitly target `LATEST_FINAL`, avoiding stale pre-final state.

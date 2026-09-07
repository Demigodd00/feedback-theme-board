# Source Policy

## Authoritative source collection

The contract uses only the stored question, standard, frozen theme descriptions, and feedback. It does not enrich entries from profiles, sentiment services, or outside records.

Concretely, the validator evidence consists of: feedback question, classification standard, frozen theme descriptions, and participant-submitted feedback text.

## No autonomous retrieval

This contract performs no HTTP request, web search, URL rendering, oracle lookup, or hidden enrichment. A URL or source label inside user text remains untrusted text; validators are not asked to open it. This prevents mutable pages, blocked domains, and different search results from changing consensus.

## Collection responsibility

The deployer and participants must provide complete, lawfully usable, non-secret material. On-chain storage proves which bytes were considered after normalization; it does not prove authorship, completeness, ownership, or real-world truth.

## Normalization and limits

Text inputs normalize CRLF/CR to LF, trim surrounding whitespace, and enforce field-specific minimum and maximum lengths. Collection sizes are capped. Structured model output uses closed categories or fixed-order binary masks and fails closed on extra, missing, malformed, or out-of-range values.

## Prompt-injection boundary

Every evidence packet is serialized as sorted JSON and surrounded by named START/END delimiters. The prompt states that the packet is data, never instructions. A validator independently replays the assessment before any result is stored.

## Interpretation boundary

The facilitator chooses the taxonomy and may omit a useful theme. Priority voting may be finalized after a strict-majority quorum (`floor(eligible participants / 2) + 1`); the unique highest recorded tally wins and a tied highest tally becomes `NO_PRIORITY`. Applications must display the quorum, recorded tally, and nonvoter count next to results and use a fresh deployment when the underlying source set or policy changes.

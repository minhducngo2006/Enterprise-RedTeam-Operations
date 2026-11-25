# ADR 0001 — Offline synthetic evidence

Status: implemented and published to public `main` under the owner's limited publication authorization dated 2026-11-25; no tagged/versioned release.

## Context

The project must demonstrate reproducible defensive software without claiming real assessment results or handling real identity-bearing evidence. The legacy dataset analyzer is retired. A scalar educational decoder remains useful but must not become a data-analysis or attack platform.

## Decision

Use two independent Python standard-library CLI flows: a scalar UAC decoder and a bounded-reader/pure-model/renderer scorecard. Keep exactly five catalog definitions, strict versioned synthetic input, deterministic reports and exclusive new-file output. Supplied statuses are not measurements and labels are not artifacts. No live integrations, external catalog, web service, database or new operational capabilities.

## Consequences

Small dependency surface and repeatable offline tests; deliberate rejection of free text and external evidence. Coverage over submitted controls can differ from whole-catalog coverage. An empty denominator produces null/N/A. File operations assume trusted stable paths; write failure may leave a partial file, which the owner inspects manually. Neither clean local files nor tests prove historical exposure has been remediated. Release requires separate incident, provenance, final-SHA CI and owner approval.

Rejected alternatives: retain/extend the legacy dataset ingestion; implement a live integration or service; infer outcomes from real artifacts. All are outside the approved scope.

See [architecture](../architecture.md) and [limitations](../limitations.md).

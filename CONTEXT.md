# Project glossary

Canonical project name: **Security Assessment & Defensive Evidence Toolkit**.

The project is an offline educational portfolio with two independent command-line flows: a scalar Active Directory UserAccountControl decoder and a synthetic defensive evidence scorecard. It does not connect to or assess live systems.

## Canonical terms

| Term | Meaning |
|---|---|
| UAC decoder | The scalar CLI that decodes one unsigned 32-bit UserAccountControl mask. It does not ingest users or directory exports. |
| Evidence scorecard | The CLI and model that validate supplied synthetic control records and render a summary. |
| Control catalog | The fixed five-control tuple LAB-C001 through LAB-C005. |
| Submitted control | A catalog control represented by one record in the input `controls` array. |
| Omitted control | A catalog control absent from the input array. Omission is not a status. |
| Evaluated control | A submitted control with status `met` or `not_met`. |
| Inconclusive | A submitted control whose supplied information does not support a pass/fail outcome. It is not evaluated. |
| Not tested | A submitted control for which no test outcome is supplied. It is not evaluated. |
| Evidence ID | A synthetic `LAB-E###` reference label. It is not a file, hash, link, artifact or independent attestation. |
| Synthetic source | Fictional input data. The `source_kind: synthetic` field is a schema assertion, not independent proof of provenance. |

## Language rules

- Describe the UAC command as a **decoder**, not a live Active Directory audit or dataset analyzer.
- Describe the evidence output as a **report of supplied synthetic statuses**, not a measurement, verification, risk score or compliance result.
- Use **toolkit** for the project as a whole; avoid calling it a live platform or operational framework.
- Keep the two CLI flows independent in documentation and code.
- Do not imply that a blank Rules of Engagement template grants permission.
- Do not describe synthetic case studies as real engagements, customer outcomes or validated security findings.

# Migration from V1 to V2.1

The legacy `analyze` command, its dataset ingestion, report generator and embedded demo have been retired with explicit owner approval. The analyzer-specific tests were retired with that functionality; both original scalar decoder tests remain. No live or dataset analyzer replaces it.

The scalar interface remains `python3 tools/ad_audit.py uac 512 --json`. Valid masks are ASCII decimal strings of 1–10 digits in the unsigned 32-bit range. Successful JSON preserves the existing scalar keys. Invalid arguments (including `analyze` and its flags) exit 2 with a fixed diagnostic and no stdout. The scalar risk labels are educational heuristics, not verified risk assessments.

The independent synthetic evidence scorecard is not a migration target for real AD exports. Do not submit real records. Local retirement does not erase Git history. The owner separately attests that the F-01 credential-like value and F-10 placeholder were fictional and never used or reused in any real system; live credential rotation is not applicable on those attestations. Historical public text/copies remain to be reviewed, and original-report provenance remains UNKNOWN. See [security disposition](security-disposition.md).

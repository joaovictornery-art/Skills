# Diagnosis Reference

Diagnose a blocking finding against its exact reported symptom.

1. Define the smallest deterministic pass/fail signal available at the real
   call-site seam.
2. Reproduce the reported symptom, not a nearby failure.
3. Rank up to three falsifiable root-cause hypotheses.
4. Run one targeted, non-mutating probe per hypothesis, cheapest first.
5. Record the confirmed cause, falsified causes, or the missing access or test
   seam that blocks a conclusion.

Prefer existing tests, direct function or CLI calls, HTTP requests, captured
payload replay, and read-only inspection. In review-only mode, recommend any
new regression test or instrumentation instead of adding it.

A diagnosis is sufficient when another implementer can reproduce the signal
and tell what correction would close the defect class. If no correct seam
exists, the absence of that seam is part of the finding.

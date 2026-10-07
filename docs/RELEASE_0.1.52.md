# K.I.T.T. AI Workers 0.1.52 — Agent CLI 0.84.6 alignment

Evals and Evolution now resolve Agent CLI 0.84.6 at `0f14d68b5fbdd6848660f68707230d7d6c3db584`.

Agent 0.84.6 completes the durable Goals/TaskPlan ownership fix by omitting TaskPlan host-verification context, as well as its completion gate, for GOAL-owned turns that have no nested TaskPlan. Real TaskPlans remain unchanged.

This release is immutable-consumer alignment only. AI Workers behavior and KITT Protocol are unchanged. All three package/editable-lock versions move together to 0.1.52.

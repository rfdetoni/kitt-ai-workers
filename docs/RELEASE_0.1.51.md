# K.I.T.T. AI Workers 0.1.51 — Agent CLI 0.84.5 alignment

AI Workers itself has no behavioral dependency on the Goals loop. The Evals and Evolution packages do consume Agent CLI directly, so their immutable locks now point to Agent CLI 0.84.5 at `fc4646c98b2b55af8a992798440e079f8d3da124`.

Agent 0.84.5 fixes completion ownership for GOAL-owned durable contract items that do not have a nested TaskPlan. This release only aligns consumers; it does not add a scheduler, change worker behavior, or modify KITT Protocol.

All three package/editable-lock versions move together to 0.1.51.

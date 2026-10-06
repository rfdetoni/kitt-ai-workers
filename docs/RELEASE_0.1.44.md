# AI Workers 0.1.44

Evolution and Evals locks now resolve Agent CLI 0.83.18 at b9e8949367a69eac7fa39e09fd6ec627aa228de8, retaining the same dependencies and Protocol revision. This prevents frozen worker environments from holding the previous Agent endpoint binding behavior. No worker, evaluation or promotion semantics change.

Worker, Evolution and Evals package metadata and editable locks agree at 0.1.44. Existing worker/STT, evolution security/atomic promotion and evaluation contract suites remain required in CI.

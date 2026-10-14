# AI Workers 0.1.61 — KAP/2 safe Python dependency alignment

Worker root 0.1.61, Evals 0.1.58, and Evolution 0.1.58 align their `uv.lock`
files to Protocol 0.13.2 at `0b9300e418557b00e371eeb2c70ef91fbf50855d`.
Evals and Evolution additionally resolve Agent CLI 0.87.10 at
`6a76c27f4e71962a644d174e9187f4d386f794f7`.

The feature is owned by Agent CLI; no worker-specific execution paths,
permissions, APIs or KAP grammar are added.

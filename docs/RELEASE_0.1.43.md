# kitt-ai-workers 0.1.43

Make retrieval ablations exercise graph-disabled, graph-enabled and lexical feature reranking stages before selection. Add a real indexed dependency-neighbor case, per-case latency/token costs and stage diagnostics. Replace misleading small-model/large-direct labels with `hybrid_graph_lexical_rerank` and `single_lexical_hit`. Synthetic lexical embeddings do not represent model quality. The fixture shows 5/6 structural versus 6/6 graph recall@5; lexical reranking remains optional and is not promoted.

Validation uses Python 3.14, Node 24 and Rust checks where applicable. Cross-repository CI covers supported deployment environments.

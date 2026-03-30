- **Tree-sitter**: Incremental parser generator for languages; builds concrete syntax trees in O(n) time per document change. **Math/Logic:** uses LR(0) automata and editorial closures for efficient parse; complexity linear in input size. **Steps:** generate grammar, attach node creation actions, parse incrementally on edits; visit nodes for each hunk surface. **Surfaces:** structural/grammatical; **Depth:** 1.

- **Ohm**: Parser/generator using PEG grammars and semantic actions. **Math:** packrat parsing (O(n) worst-case) with backtracking; context-free grammar with custom attribute evaluation. **Steps:** define grammar rules, write semantic actions to annotate parse tree; on parse attach 5-face metadata. **Surfaces:** grammatical/structural; **Depth:** 1.

- **ANTLR**: LL(*) parser generator with listener/visitor API. **Math:** predictive parsing using adaptive LL(*) lookahead (polynomial) and parse tree production. **Steps:** write grammar, auto-generate parser, traverse tree with visitor to fill surfaces. **Surfaces:** structural/grammatical; **Depth:** 1.

- **Difftastic**: Structured diff tool using syntax-aware AST diff. **Math:** tree differencing via matching of unchanged subtrees; runs in O(n) often. **Steps:** parse two versions with Tree-sitter, align similar subtrees, output edit mapping; use to merge new relations. **Surfaces:** structural/statistical (edits); **Depth:** 2.

- **GumTree**: AST-based diff (Tree matching algorithm). **Math:** computes tree edit distance via Zhang-Shasha or AS-UR matching (O(n^3) worst, heuristics). **Steps:** parse ASTs, find optimal mapping between trees, list node-level edits. **Surfaces:** structural; **Depth:** 2.

- **ColBERTv2/Late Interaction**: Retrieval model that matches query and document tokens via learned vectors. **Math:** each token → d-dim vector; score = sum over token dot-products. **Steps:** encode each hunk token, keep dense token vectors, compare query and hunk via matrix multiply (no pooling). **Surfaces:** semantic; **Depth:** 2.

- **SPLADE/SPLATE**: Sparse lexical expansion models. **Math:** text → sparse high-dimensional vector via learned weights; inner product for retrieval. **Steps:** run transformer, project to large vocab-weight vector with ReLU (or product of query/doc); index using sparse codes. **Surfaces:** semantic/statistical; **Depth:** 2.

- **ByT5**: Byte-level transformer. **Math:** same multi-head attention as BERT, but over raw bytes (256-token alphabet). Complexity similar to standard Transformers (O(n^2)). **Steps:** tokenize bytes, feed through BPE-free Transformer, use output to fill semantic surface. **Surfaces:** verbatim/semantic; **Depth:** 3.

- **CANINE**: Char-level model with downsampling. **Math:** FFT or convolution for pooling chars to word-size tokens, then Transformer. **Steps:** break text into characters, do local pooling, run Transformer on pooled spans, back-project to chars. **Surfaces:** verbatim/semantic; **Depth:** 3.

- **Git/IPFS/IPLD (CAS/Merkle DAG)**: Content-addressed storage (hash = data ID). **Math:** hash functions (SHA) give unique CID; Merkle DAG: node = (data, link list). **Steps:** chunk hunk data, compute hash, store unique content only; retrieve by hash ID. **Surfaces:** verbatim/structural (identity); **Depth:** 2.

- **Faiss/PQ/HNSW**: Vector index. **Math:** PQ splits d-dim vector into m subvectors, quantizes each to k centroids; distance ~ sum of subspace distances. IVF clusters vectors (k-means), HNSW builds navigable small-world graph; polysemous filtering uses precomputed sign bits for quick filtering. **Steps:** train PQ codebooks, encode all hunk embeddings, build HNSW; query by computing quantized codes or distance heuristics. **Surfaces:** semantic; **Depth:** 2.

- **Vector Symbolic Architectures (HDC)**: High-dim binary/continuous vectors with bind/unbind. **Math:** Binding (⊗) often XOR or circular convolution; bundling (⊕) is vector addition or majority. **Steps:** encode each face as random vector, bind with role vectors, aggregate with bundling. Unbind by inverse binding to test relation. **Surfaces:** all (if faces encoded); **Depth:** 3.

- **Byte-Pair Encoding (BPE) + CAS Hybrid**: Tokenize binary data into frequent byte sequences, then dedupe via CAS. **Math:** greedily merge most common byte pairs (simple frequency count) into tokens. **Steps:** run BPE on raw bytes to get token IDs; store each unique token’s data via CAS; represent hunk as sequence of CAS IDs. **Surfaces:** verbatim; **Depth:** 2.

- **Content-Hashed Buffer / Memmap Header Design**: Store CAS addresses in a memory-mapped structure. **Math:** map file offsets to content IDs; header = table of CID → offset. **Steps:** allocate memmap file for flattened tokens, maintain index mapping, lookup by hash. **Surfaces:** verbatim/structural; **Depth:** 2.

- **Polysemous Binary Filters**: Fast binary codes for initial filtering. **Math:** compute short binary hash (e.g. locality-sensitive bit vectors) where similar items share bits; filter by Hamming distance. **Steps:** precompute binary code for each hunk embedding, during search do bitwise XOR and threshold. **Surfaces:** semantic; **Depth:** 2.

- **Sparse + Late-Interaction Pipelines**: Combine sparse lexical hits with late dense matching. **Math:** final score = f(sparse_score, dense_score). **Steps:** first filter neighbors by TF-IDF or LSH, then run dense attention among top candidates. **Surfaces:** semantic; **Depth:** 2.

- **Spectral Clustering**: Graph clustering via Laplacian eigenvectors. **Math:** compute affinity matrix A, Laplacian L=D-A, take k smallest eigenvectors of L, cluster via k-means. **Steps:** build similarity graph of hunks, compute eigenvectors (O(n^3) naive), run k-means on projected space. **Surfaces:** structural/semantic; **Depth:** 3.

- **Louvain/Infomap Community Detection**: Network clustering by optimizing modularity (Louvain) or compressing flow (Infomap). **Math:** modularity Q = sum[(w_in/community)/(2m) - (deg_sum/2m)^2] to maximize. **Steps:** greedily merge nodes to increase Q, iterate on super-nodes. **Surfaces:** structural/semantic; **Depth:** 3.

- **HMM / CRF Segmentation**: Probabilistic sequence models. **Math:** HMM: P(states,observations)=π_s1 ∏ a_{s_i,s_{i+1}} * b_{s_i}(obs_i); CRF: P(y|x)=exp(∑λ_k f_k(x,y))/Z. **Steps:** define state = segment type, train transition/emission; run Viterbi or forward-backward (O(N*S^2)). For CRF, define features (e.g. topic, cue words) and train via gradient. **Surfaces:** structural (HMM), structural/grammatical (CRF); **Depth:** 2.

- **Hierarchical Clustering (linkage variants)**: Agglomerative clustering of hunks. **Math:** distance(s,t)=e.g. single = min, complete = max, average = mean over pairwise distances. **Steps:** start each hunk as cluster, iteratively merge nearest clusters by linkage criterion until threshold. Complexity ~O(n^3) naive, use priority queue O(n^2). **Surfaces:** semantic/structural; **Depth:** 2.

- **Transformer Attention Modifications**: Sparse/global attention. **Math:** scaled dot-product attention A=softmax((QK^T)/√d + mask). **Steps:** implement sparse masks (block or KNN), global tokens; adjust temperature by scaling logits or add λ to softmax denominator. **Surfaces:** semantic/structural; **Depth:** 3.

- **LDA/HDP Topic Models**: Generative bag-of-words model. **Math:** each document has topic vector θ∼Dir(α), each word w_i∼Cat(β_{z_i}) with z_i∼Cat(θ). Inference via Gibbs sampling or variational EM. **Steps:** preprocess hunks to bag of words, initialize topics, iterate word-topic assignments, estimate θ per hunk. **Surfaces:** semantic; **Depth:** 3.

- **TimeML/TimeBank (Temporal Relations)**: Annotation schema for events/times. **Math:** no formula. **Steps:** use rule-based or ML to tag EVENT, TIMEX3, LINK tags, compute Allen relations. **Surfaces:** temporal/statistical; **Depth:** 3.

- **Coreference Resolution**: Link mentions of same entity. **Math:** pairwise binary classifier or clustering (mention embedding cosine > threshold). **Steps:** extract mentions, compute pair features (string match, distance, syntax), train CRF or neural model, cluster mentions by entity. **Surfaces:** semantic/grammatical; **Depth:** 3.

- **RST Discourse Relations**: Hierarchical labeling of spans (nucleus/satellite). **Math:** no closed formula. **Steps:** detect elementary discourse units, classify relation type (e.g. “Cause”), attach into binary tree. **Surfaces:** rhetorical/structural; **Depth:** 3.

- **WindowDiff/Pk Metrics**: Segmentation evaluation. **Math (WindowDiff):** from 【50†L557-L564】: WD= (1/(N−k))∑_{i=1}^{N−k} [|b_ref(i,i+k)−b_hyp(i,i+k)|>0]. **Pk:** probability two random points k apart are mis-segmented. **Steps:** slide window, compare boundary counts; compute Pk similarly. **Surfaces:** statistical evaluation; **Depth:** 2.

- **NMI/Purity/Silhouette**: Clustering quality. **Math:** NMI from scikit (normalized MI), purity = (1/N)∑_clusters max_{label}count, silhouette s(i)=(b−a)/max(a,b). **Steps:** given true labels or cluster labels, compute MI, counts. **Surfaces:** statistical evaluation; **Depth:** 2.

- **Graph Neural Networks (GCN/GAT/GraphSAGE)**: Node embedding from graph. **Math:** GCN layer: H'=σ(D^−1/2 A D^−1/2 H W); GAT: use self-attention a_{ij}=softmax((h_iW_i)(h_jW_j)^T); GraphSAGE: H'=σ( concat(h,mean(neighbors))). **Steps:** construct graph of hunks, initialize node features (embedding), apply message-passing layers to propagate; use for link prediction or clustering. **Surfaces:** structural/semantic; **Depth:** 3.

- **Dynamic Graphs / Streaming Community Detection**: Update graph incrementally. **Math:** time-decay: w_new = α w_old + (1−α)w_obs. **Steps:** as new hunks arrive, attach edges, run incremental Louvain or label-prop; decay old links. **Surfaces:** temporal/structural; **Depth:** 3.

- **PQ/IVF Indexing**: Product Quantization + Inverted File. **Math:** PQ as above; IVF clusters (k-means) index vectors, search in nearest clusters. **Steps:** cluster all embeddings, assign hunk to cell, train PQ in each cell; at query, find top cells then PQ distance. **Surfaces:** semantic; **Depth:** 2.

- **Mermaid/Visualization Hooks**: Diagramming syntax. **Math:** N/A. **Steps:** write flowcharts or class diagrams in Markdown (```mermaid) to visualize pipelines or hierarchies. **Surfaces:** visualization; **Depth:** 1.
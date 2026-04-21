---
type: index
updated: 2026-04-22
note_count: 58
---

# AI / Deep Learning — Wiki Index

Catalog of all notes in this knowledge base. Grouped by topic cluster. Read this first when answering queries.

Legend: **[stub]** = < 500 B, **[empty]** = 0 B, **[VN]** = written in Vietnamese.

---

## 1. Search Algorithms (11)

- [[A-star search]] — informed search with heuristic + path cost
- [[Basic Search Algorithms in Artificial Intelligence]] — overview of uninformed/informed search
- [[Best-first search]] — greedy heuristic-driven search
- [[Bread-first search]] — BFS: level-order exploration
- [[Depth-first search]] — DFS: stack-based exploration
- [[Depth-Limited Search]] — DFS with depth cap
- [[Graph Search]] — visited-set variant to avoid cycles
- [[Iterative-deepening search]] — repeated DLS with increasing depth
- [[Local Search Algorithm]] — hill climbing, simulated annealing family
- [[Uniformed-cost search]] — Dijkstra-like optimal uninformed search
- [[Về các thuật toán tìm kiếm]] **[VN]** — Vietnamese overview of search algorithms

## 2. Gradient & Optimization (6)

- [[Gradient Descent]] — definition, update formula, applications
- [[Gradient Descent Variants]] — Batch vs SGD vs Mini-batch
- [[Gradient Descent in Linear Regression]] — worked example
- [[Adamw and Adam (optimizer)]] — adaptive learning rate optimizers
- [[Vanishing and Exploding Gradient]] — training instability and mitigations
- [[Normalizing Inputs]] — input scaling for stable training

## 3. Deep Learning Fundamentals (6)

- [[Backpropagation]] — forward/backward pass, chain rule, weight updates
- [[Neural Network]] — basic NN anatomy
- [[Neural Networks Foundation]] — deeper intro to NN components
- [[Common Activation Function In Neural Networks]] — sigmoid, ReLU, tanh, etc.
- [[Model Generalization]] — bias/variance, overfitting, train/val/test
- [[double descent]] — test-error non-monotonicity with capacity **[stub-ish]**

## 4. Attention / Sequence Models (3)

- [[Attention Mechanism]] — Seq2Seq + BiGRU attention pipeline (detailed)
- [[Recurrent Neural Networks (RNN)]] — sequence modeling basics
- [[transformer]] **[empty]** — critical gap, needs full page

## 5. NLP / Embeddings (6)

- [[Foundations of NLP - Machine Learning, Deep Learning, and Representation]] — NLP + ML/DL overview
- [[Word embedding and Word Representation]] — embedding concepts
- [[Word embedding and Word2Vec]] — Word2Vec specifics
- [[SkipGram and CBOW]] — two Word2Vec training objectives
- [[SubWord Models]] — BPE, WordPiece, SentencePiece
- [[Compositional Semantics]] — meaning from composition

## 6. Computer Vision (4)

- [[CNN review]] — conv/pool/FC pipeline summary
- [[Convolutional Neural Networks]] — deeper CNN treatment
- [[Faster R-CNN]] — object detection with RPN
- [[FGSM]] — Fast Gradient Sign Method adversarial attack

## 7. Contrastive / Self-Supervised (3)

- [[Contrastive Learning]] — instance discrimination, SSL motivation
- [[10 Contrastive Learning Frameworks]] — SimCLR, MoCo, BYOL, etc.
- [[Contrastive Learning Loss Functions]] **[stub]**

## 8. Classical ML (7)

- [[Linear Regression]] — OLS fundamentals
- [[Linear Regression for more complex models]] — polynomial/basis expansion
- [[Logistic Regression]] — binary classification
- [[Logistic Regression review 1]] — *probable duplicate*
- [[Logistic Regression review 2]] — *probable duplicate*
- [[SVM Classification Model]] — max-margin classifier
- [[Decision Tree]] **[stub]**

## 9. Dimensionality Reduction (3)

- [[SVD for denoising]] — SVD in practice
- [[So Sánh Giữa PCA, SVD và LSA]] **[VN]** — PCA/SVD/LSA comparison
- [[ISOMAP]] — nonlinear manifold learning

## 10. Clustering (1)

- [[So sánh sự khác nhau giữa Kmeans, K_medoids, Kernel K-Means]] **[VN]**

## 11. Generative / Modern (1)

- [[VAE và các Diffusion Models]] **[VN]** — VAEs and diffusion models

## 12. Training Techniques (1)

- [[regularization]] **[stub]**

## 13. AI Process / Meta (4)

- [[AI Engineering]] — practitioner workflow
- [[Creating ML pipeline from scratch]] — end-to-end pipeline
- [[Introduction to Data Mining]] — DM overview
- [[The Basics Data Types and Major Building Blocks]] — data type primer

## 14. Other (2)

- [[Fuzzy Logic]] — fuzzy set theory basics
- [[Generic Algorithm]] — (likely "Genetic Algorithm" — rename candidate)

---

## Sources (ingested)

*(none yet — clip papers into `raw/` to populate)*

## Health snapshot (2026-04-22)

- **58 concept notes**, **0 ingested sources**
- **1 empty**, **3 stubs**, **5 probable duplicate groups** — see `CLAUDE.md` lint section
- Suggested first ingests to kick off compounding: attention/transformer papers (to fill [[transformer]] empty page)

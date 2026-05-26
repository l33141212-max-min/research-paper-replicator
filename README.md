
# AI/ML Research Paper Replicator

An end-to-end NLP pipeline that ingests academic research papers (PDF) and automatically extracts structured technical intelligence — model architecture, training methodology, benchmark results, and step-by-step replication guides.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-UI-red) ![Mistral](https://img.shields.io/badge/Mistral--7B-4bit-orange) ![Kaggle](https://img.shields.io/badge/Kaggle-T4%20GPU-20BEFF)

---

## What It Does

Upload any AI/ML research paper in PDF format. The system processes it through a multi-stage pipeline and returns three structured outputs across dedicated tabs:

| Tab | Contents |
|---|---|
|  Architecture & Methodology | Model architecture, layer dimensions, training procedure, datasets, hardware |
|  Results & Metrics | Benchmark scores, baseline comparisons, ablation studies, efficiency metrics |
| Implementation Guide | Step-by-step replication guide with exact hyperparameters and library calls |

---

## How It Works

```
PDF Upload
    │
    ▼
pymupdf4llm         ← extracts and converts paper to clean markdown
    │
    ▼
SciBERT Embedder    ← encodes chunks using scientific domain embeddings
    │               ← runs 4 targeted semantic queries (arch / method / metrics / impl)
    ▼
Mistral-7B (4-bit)  ← 3 focused generation passes, one per output tab
    │
    ▼
Streamlit UI        ← displays results across 3 tabs with live progress logging
```

---

## Tech Stack

- **PDF Extraction** — `pymupdf4llm` for clean markdown output preserving multi-column layouts
- **Semantic Search** — `SciBERT` (`allenai/scibert_scivocab_uncased`) — 110M parameter encoder pre-trained on 1.14M scientific papers
- **Text Generation** — `Mistral-7B-Instruct-v0.3` with 4-bit NF4 quantization via `bitsandbytes`
- **Frontend** — `Streamlit` with live progress logging, session caching, and manual cache controls
- **Infrastructure** — Kaggle T4 GPU (16GB VRAM); automatic CPU fallback for local development
- **AI Development Tools** — Claude (Anthropic) and Gemini (Google) used for code generation and debugging throughout

---

## Running on Kaggle (Recommended)

1. Create a new Kaggle notebook and enable GPU (Settings → Accelerator → GPU T4)
2. Upload `engine_1.py` and `app_1.py` to the notebook
3. Install dependencies:
```bash
pip install streamlit pymupdf4llm transformers sentence-transformers torch bitsandbytes numpy accelerate
```
4. Run the app:
```bash
streamlit run app_1.py
```
5. Use the Kaggle public URL to access the interface

---

## Running Locally (CPU)

>  Local CPU runs use TinyLlama-1.1B as an automatic fallback. Output quality is reduced compared to GPU inference with Mistral-7B.

```bash
# Clone the repo
git clone https://github.com/yourusername/research-paper-replicator
cd research-paper-replicator

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app_1.py
```

---

## Project Structure

```
research-paper-replicator/
├── app_1.py            # Streamlit frontend — UI, tabs, caching, progress log
├── engine_1.py         # Core pipeline — PDF extraction, SciBERT retrieval, Mistral generation
├── requirements.txt    # Dependencies
└── README.md
```

---

## Key Engineering Decisions

- **SciBERT over MiniLM** — domain-specific embeddings for scientific vocabulary significantly improve chunk retrieval accuracy at negligible speed cost (~0.5s vs ~0.1s for 35 chunks)
- **4-bit quantization** — fits Mistral-7B within T4 VRAM constraints with minimal quality tradeoff
- **3 independent generation passes** — one per output tab, each with a focused prompt; single-pass approaches with small models reliably fail to populate all sections
- **MD5 file hash caching** — re-uploading the same paper returns instantly without re-running inference
- **Full chunk pool per query** — all 4 SciBERT queries search the complete chunk pool independently, preventing context starvation on short papers

---

## Built With AI-Assisted Development

This project was built using Claude (Anthropic) and Gemini (Google) as development tools — generating code, diagnosing errors, and working through debugging iteratively. Failure modes resolved during development included transformer API version incompatibilities, model degeneration loops, chat template mismatches, and GPU memory constraints.

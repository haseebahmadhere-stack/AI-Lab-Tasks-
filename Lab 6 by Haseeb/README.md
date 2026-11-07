# Lab 6 - NLP Fundamentals: Tokenization, Embeddings & Text Chunking

Name: Haseeb Ahmad  , Roll No: 057 , Semester: 3A , Instructor: Rasikh Ali
Course: CAI601400 , Artificial Intelligence Lab ,- Lab 6 (CLO3, C3: Apply)

All documents are "synthetic teaching data" (not real university policies), written for this lab.

## Setup
```
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows PowerShell   (macOS/Linux: source .venv/bin/activate)
python -m pip install numpy scikit-learn sentence-transformers
python -m pip freeze > requirements.txt   # overwrite with exact versions after installing
```
The first embedding run downloads `sentence-transformers/all-MiniLM-L6-v2` (internet needed once). CPU only.

## Run order
| Step | Command |
|---|---|
| Dataset (once) | `python create_dataset.py` (corpus.json + queries.json already included) |
| Helper self-test | `python lab6_search.py` |
| Scenarios 1-5 | `python scenario1_handbook.py` ... `python scenario5_equipment.py` |
| Guided examples | `guided_tokens.py`, `guided_embeddings.py`, `guided_limits.py`, `guided_metrics.py`, `guided_chatbot.py [--backend embedding]`, `guided_suggestions.py [tfidf\|embedding] "query"` |
| Task 1 | `python task1_tokens.py` then `python task1_chatbot_check.py` and `python guided_chatbot.py` |
| Task 2 | `python task2_chunks.py` (tests + chunk comparison) then `python task2_semantic_check.py` |
| Task 3 | `python task3_retrieval.py [--verbose]` (writes retrieval_log.csv, results_summary.csv) then `python document_chatbot.py` |

## Files
`lab6_search.py` shared retriever | `task1_tokens.py` | `task2_chunks.py` | `task2_semantic_check.py` | `task3_retrieval.py` | `document_chatbot.py` | `corpus.json` (5 docs, 205-232 words) | `queries.json` (8 answerable + 2 unanswerable; 4 dev / 4 test answerable) | `retrieval_log.csv` | `Lab6_Report.docx`

## Notes / honesty
- Chunk units: "whitespace words" (40-word windows, overlap 0 and 10; sentence-aware budget 40 words). Offsets are character positions, `text == source[start:end]`.
- Embedding configurations require `sentence-transformers`. If it is missing, `task3_retrieval.py` runs TF-IDF only and says so. Re-run it after installing to regenerate `retrieval_log.csv` with all six configurations.
- Code adapted from the Lab 6 manual (reference solutions); expanded corpus, extra FAQs, tests, summary output and fallbacks are my own additions.
- No credentials, personal data, model weights or virtual environment are included.

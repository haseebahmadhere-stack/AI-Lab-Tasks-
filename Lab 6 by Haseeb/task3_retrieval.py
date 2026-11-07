# Name: Haseeb Ahmad | Roll No: 057 | Semester: 3A | Instructor: Rasikh Ali | AI Lab 6 (CAI601400)
"""Task 3 (Advanced): evaluate TF-IDF vs sentence embeddings over 3 chunking strategies.
Run create_dataset.py first. Writes retrieval_log.csv and results_summary.csv."""
import csv
import json
import sys
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from task2_chunks import make_chunks

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def evaluate(scores, chunks, items):
    """Hit@3 and MRR@3 on answerable queries only. Also returns failed queries."""
    hits, reciprocal, failures = [], [], []
    for row, q in zip(scores, items):
        if q["doc"] is None:
            continue
        top = np.argsort(-row, kind="stable")[:3]
        good = [rank for rank, i in enumerate(top, 1)
                if chunks[i]["doc"] == q["doc"]
                and q["evidence"] in chunks[i]["text"]]
        hits.append(bool(good))
        reciprocal.append(1/good[0] if good else 0)
        if not good:
            failures.append(q["query"])
    if not hits:
        return None, None, failures
    return float(np.mean(hits)), float(np.mean(reciprocal)), failures


def fmt(x):
    return "n/a" if x is None else f"{x:.3f}"


def main():
    with open("corpus.json", encoding="utf-8") as f:
        docs = json.load(f)
    with open("queries.json", encoding="utf-8") as f:
        items = json.load(f)
    assert docs and items
    for q in items:
        assert q["split"] in {"dev", "test"}
        if q["doc"] is not None:
            assert q["evidence"] and q["evidence"] in docs[q["doc"]]

    # model load is measured separately from encoding/search
    model, methods = None, ["tfidf"]
    try:
        from sentence_transformers import SentenceTransformer
        t = time.perf_counter()
        model = SentenceTransformer(MODEL_NAME, device="cpu")
        print(f"Model load seconds: {time.perf_counter()-t:.2f}")
        methods.append("embedding")
    except Exception as exc:
        print("WARNING: embedding model unavailable ->", type(exc).__name__)
        print("Running TF-IDF only. Install sentence-transformers and rerun "
              "to complete the embedding configurations.\n")

    query_texts = [q["query"] for q in items]
    logs, summary = [], []
    for strategy in ["0", "10", "sentence"]:
        chunks = make_chunks(docs, strategy)
        texts = [c["text"] for c in chunks]
        if model is not None:          # token-length audit
            lengths = [len(model.tokenizer(t, truncation=False)["input_ids"])
                       for t in texts + query_texts]
            print(f"[audit] strategy={strategy}: max tokens {max(lengths)} "
                  f"(limit {model.max_seq_length})")
            if max(lengths) > model.max_seq_length:
                raise ValueError("Model limit exceeded; rechunk or shorten query")

        for method in methods:
            t = time.perf_counter()
            if method == "tfidf":
                vectorizer = TfidfVectorizer()
                C = vectorizer.fit_transform(texts)
                Q = vectorizer.transform(query_texts)
            else:
                C = model.encode(texts, normalize_embeddings=True)
                Q = model.encode(query_texts, normalize_embeddings=True)
            encode_seconds = time.perf_counter()-t
            t = time.perf_counter()
            scores = (Q @ C.T).toarray() if method == "tfidf" else Q @ C.T
            search_seconds = time.perf_counter()-t

            res = {}
            for split in ["dev", "test"]:
                idx = [i for i, q in enumerate(items) if q["split"] == split]
                res[split] = evaluate(scores[idx], chunks, [items[i] for i in idx])
                print(f"{strategy:8} {method:9} {split:4} Hit@3={fmt(res[split][0])} "
                      f"MRR@3={fmt(res[split][1])} chunks={len(chunks)} "
                      f"encode={encode_seconds:.4f}s search={search_seconds:.4f}s")
                for qq in res[split][2]:
                    print("    FAILED:", qq)
            summary.append(dict(
                strategy=strategy, method=method, chunks=len(chunks),
                dev_hit3=res["dev"][0], dev_mrr3=res["dev"][1],
                test_hit3=res["test"][0], test_mrr3=res["test"][1],
                encode_seconds=round(encode_seconds, 5),
                search_seconds=round(search_seconds, 5)))

            for row, q in zip(scores, items):
                for rank, i in enumerate(np.argsort(-row, kind="stable")[:3], 1):
                    c = chunks[i]
                    logs.append(dict(
                        strategy=strategy, method=method, query=q["query"],
                        split=q["split"], answerable=q["doc"] is not None,
                        rank=rank, score=round(float(row[i]), 4),
                        chunk_id=c["id"], doc=c["doc"], start=c["start"],
                        end=c["end"], relevant=(q["doc"] is not None
                            and c["doc"] == q["doc"] and q["evidence"] in c["text"]),
                        text=c["text"]))
            # top-3 display for every query in this configuration
            if "--verbose" in sys.argv:
                for row, q in zip(scores, items):
                    print(f"\n[{strategy}/{method}] {q['query']}")
                    for rank, i in enumerate(np.argsort(-row, kind="stable")[:3], 1):
                        c = chunks[i]
                        print(f"  {rank}. {c['id']} score={row[i]:.3f} "
                              f"chars {c['start']}-{c['end']} | {c['text'][:70]}...")

    with open("retrieval_log.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(logs[0]))
        w.writeheader()
        w.writerows(logs)
    with open("results_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0]))
        w.writeheader()
        w.writerows(summary)

    # unanswerable queries: highest-score retrieval still returns text
    print("\nUnanswerable queries (no relevant evidence exists):")
    for r in logs:
        if not r["answerable"] and r["rank"] == 1:
            print(f"  [{r['strategy']}/{r['method']}] {r['query']!r} -> "
                  f"top1 {r['chunk_id']} score={r['score']}")
    print("\nSaved retrieval_log.csv and results_summary.csv")


if __name__ == "__main__":
    main()

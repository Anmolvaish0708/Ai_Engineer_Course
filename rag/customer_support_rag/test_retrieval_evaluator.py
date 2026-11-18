
from app.evaluation.retrieval_evaluator import RetrievalEvaluator


# Example 1: Test individual metrics

retrieved_ids = ["A", "X", "B"]
relevant_ids = ["A", "B", "C", "D"]

precision = RetrievalEvaluator.precision_at_k(
    retrieved_ids, relevant_ids, k=3
)

recall = RetrievalEvaluator.recall_at_k(
    retrieved_ids, relevant_ids, k=3
)

rr = RetrievalEvaluator.reciprocal_rank(
    retrieved_ids, relevant_ids
)

print("Individual Metrics")
print("Precision@3:", precision)
print("Recall@3:", recall)
print("Reciprocal Rank:", rr)


# Example 2: Evaluate multiple queries

retrieved_results = [
    ["faq_001", "faq_008", "faq_002"],
    ["faq_005", "faq_003", "faq_010"],
    ["faq_007", "faq_011", "faq_012"]
]

relevant_results = [
    ["faq_001", "faq_002", "faq_006"],
    ["faq_003", "faq_004"],
    ["faq_020"]
]

evaluation = RetrievalEvaluator.evaluate_retrieval(
    retrieved_results=retrieved_results,
    relevant_results=relevant_results,
    k=3
)

print("\nOverall Evaluation")
for metric, score in evaluation.items():
    print(f"{metric}: {score:.4f}")

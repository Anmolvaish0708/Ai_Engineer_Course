
from app.embeddings.embedding_generator import EmbeddingGenerator
from app.vector_store.chroma_store import ChromaStore
from app.evaluation.retrieval_evaluator import RetrievalEvaluator

from tests.evaluation_dataset import evaluation_dataset


def run_evaluation():
    """Compare retrieval quality across different thresholds."""

    embedding_generator = EmbeddingGenerator()
    store = ChromaStore()

    store.get_or_create_collection("customer_support")

    # Prepare evaluation queries and ground truth
    queries = [item["query"] for item in evaluation_dataset]

    relevant_results = [
        item["relevant_ids"] for item in evaluation_dataset
    ]

    # Generate query embeddings once
    query_embeddings = [
        embedding_generator.generate_query_embedding(query)
        for query in queries
    ]

    thresholds = [None, 0.40, 0.60, 0.80]

    comparison_report = {}

    for threshold in thresholds:

        print(f"\n{'=' * 55}")
        print(f"Evaluating threshold: {threshold}")
        print("=" * 55)

        retrieved_results = []

        # Run retrieval for every query
        for query, query_embedding in zip(queries, query_embeddings):

            results = store.search(
                query_embedding=query_embedding,
                n_results=3,
                max_distance=threshold
            )

            retrieved_ids = results["ids"][0]
            distances = results["distances"][0]

            retrieved_results.append(retrieved_ids)

            print("\nQuery:", query)
            print("Retrieved IDs:", retrieved_ids)
            print("Distances:", distances)

        # Calculate metrics
        evaluation = RetrievalEvaluator.evaluate_retrieval(
            retrieved_results=retrieved_results,
            relevant_results=relevant_results,
            k=3,
            queries=queries
        )

        comparison_report[threshold] = evaluation

        print("\nPer-query evaluation:")

        for item in evaluation["per_query"]:
            print(
                f"Query {item['query_index']}: "
                f"Precision={item['precision']:.4f}, "
                f"Recall={item['recall']:.4f}, "
                f"RR={item['reciprocal_rank']:.4f}"
            )

        print("\nAggregate evaluation:")

        for metric, score in evaluation["aggregate"].items():
            print(f"{metric}: {score:.4f}")

    # Final threshold comparison
    print("\n========== THRESHOLD COMPARISON ==========")

    for threshold, evaluation in comparison_report.items():

        aggregate = evaluation["aggregate"]

        print(
            f"Threshold={threshold} | "
            f"Precision@3={aggregate['precision@3']:.4f} | "
            f"Recall@3={aggregate['recall@3']:.4f} | "
            f"MRR={aggregate['mrr']:.4f}"
        )


if __name__ == "__main__":
    run_evaluation()

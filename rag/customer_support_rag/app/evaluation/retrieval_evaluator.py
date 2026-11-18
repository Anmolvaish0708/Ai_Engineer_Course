
class RetrievalEvaluator:
    """Evaluate the quality of document retrieval in a RAG system."""

    @staticmethod
    def _validate_ids(ids, name, allow_empty=False):
        """Validate a list of document IDs."""

        if not isinstance(ids, list):
            raise TypeError(f"{name} must be a list.")

        if not allow_empty and not ids:
            raise ValueError(f"{name} cannot be empty.")

        if any(not isinstance(item, str) or not item.strip() for item in ids):
            raise ValueError(f"Every item in {name} must be a non-empty string.")

        normalized_ids = [item.strip() for item in ids]

        if len(normalized_ids) != len(set(normalized_ids)):
            raise ValueError(f"{name} must not contain duplicate IDs.")

        return normalized_ids

    @staticmethod
    def _validate_k(k):
        """Validate the number of retrieved documents to evaluate."""

        if isinstance(k, bool) or not isinstance(k, int):
            raise TypeError("k must be an integer.")

        if k <= 0:
            raise ValueError("k must be greater than zero.")

    @classmethod
    def precision_at_k(cls, retrieved_ids, relevant_ids, k=3):
        """Calculate Precision@K."""

        cls._validate_k(k)

        retrieved_ids = cls._validate_ids(
            retrieved_ids, "retrieved_ids", allow_empty=True
        )
        relevant_ids = cls._validate_ids(
            relevant_ids, "relevant_ids"
        )

        top_k_ids = retrieved_ids[:k]

        relevant_set = set(relevant_ids)

        relevant_retrieved = sum(
            1 for doc_id in top_k_ids if doc_id in relevant_set
        )

        return relevant_retrieved / k

    @classmethod
    def recall_at_k(cls, retrieved_ids, relevant_ids, k=3):
        """Calculate Recall@K."""

        cls._validate_k(k)

        retrieved_ids = cls._validate_ids(
            retrieved_ids, "retrieved_ids", allow_empty=True
        )
        relevant_ids = cls._validate_ids(
            relevant_ids, "relevant_ids"
        )

        top_k_ids = retrieved_ids[:k]

        relevant_set = set(relevant_ids)

        relevant_retrieved = sum(
            1 for doc_id in top_k_ids if doc_id in set(relevant_ids)
        )

        return relevant_retrieved / len(relevant_ids)

    @classmethod
    def reciprocal_rank(cls, retrieved_ids, relevant_ids):
        """Calculate Reciprocal Rank for a single query."""

        retrieved_ids = cls._validate_ids(
            retrieved_ids, "retrieved_ids", allow_empty=True
        )
        relevant_ids = cls._validate_ids(
            relevant_ids, "relevant_ids"
        )

        relevant_set = set(relevant_ids)

        for rank, doc_id in enumerate(retrieved_ids, start=1):
            if doc_id in relevant_set:
                return 1 / rank

        return 0.0

    @classmethod
    def mean_reciprocal_rank(cls, retrieved_results, relevant_results):
        """Calculate Mean Reciprocal Rank across multiple queries."""

        if not isinstance(retrieved_results, list) or not retrieved_results:
            raise ValueError("retrieved_results must be a non-empty list.")

        if not isinstance(relevant_results, list) or not relevant_results:
            raise ValueError("relevant_results must be a non-empty list.")

        if len(retrieved_results) != len(relevant_results):
            raise ValueError(
                "Retrieved and relevant results must contain the same number of queries."
            )

        reciprocal_ranks = []

        for retrieved_ids, relevant_ids in zip(
            retrieved_results, relevant_results
        ):
            score = cls.reciprocal_rank(retrieved_ids, relevant_ids)
            reciprocal_ranks.append(score)

        return sum(reciprocal_ranks) / len(reciprocal_ranks)

    
    @classmethod
    def evaluate_retrieval(
        cls,
        retrieved_results,
        relevant_results,
        k=3,
        queries=None
    ):
        """Calculate per-query and aggregate retrieval metrics."""

        cls._validate_k(k)

        if not isinstance(retrieved_results, list) or not retrieved_results:
            raise ValueError("retrieved_results must be a non-empty list.")

        if not isinstance(relevant_results, list) or not relevant_results:
            raise ValueError("relevant_results must be a non-empty list.")

        if len(retrieved_results) != len(relevant_results):
            raise ValueError(
                "Retrieved and relevant results must contain "
                "the same number of queries."
            )

        if queries is not None:
            if not isinstance(queries, list):
                raise TypeError("queries must be a list.")

            if len(queries) != len(retrieved_results):
                raise ValueError(
                    "Number of queries must match the number of results."
                )

            if any(not isinstance(q, str) or not q.strip() for q in queries):
                raise ValueError("Every query must be a non-empty string.")

        per_query_results = []

        precision_scores = []
        recall_scores = []
        reciprocal_ranks = []

        for index, (retrieved_ids, relevant_ids) in enumerate(
            zip(retrieved_results, relevant_results)
        ):

            precision = cls.precision_at_k(
                retrieved_ids, relevant_ids, k
            )

            recall = cls.recall_at_k(
                retrieved_ids, relevant_ids, k
            )

            rr = cls.reciprocal_rank(
                retrieved_ids, relevant_ids
            )

            precision_scores.append(precision)
            recall_scores.append(recall)
            reciprocal_ranks.append(rr)

            query_result = {
                "query_index": index + 1,
                "precision": precision,
                "recall": recall,
                "reciprocal_rank": rr
            }

            if queries is not None:
                query_result["query"] = queries[index]

            per_query_results.append(query_result)

        aggregate_results = {
            f"precision@{k}": sum(precision_scores) / len(precision_scores),
            f"recall@{k}": sum(recall_scores) / len(recall_scores),
            "mrr": sum(reciprocal_ranks) / len(reciprocal_ranks)
        }

        return {
            "per_query": per_query_results,
            "aggregate": aggregate_results
        }

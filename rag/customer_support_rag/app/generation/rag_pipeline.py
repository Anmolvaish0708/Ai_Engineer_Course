
from app.exceptions import RAGApplicationError


class RAGPipeline:
    """Orchestrates the complete Retrieval-Augmented Generation workflow."""

    def __init__(
        self,
        retriever,
        context_builder,
        prompt_builder,
        llm_client
    ):
        self.retriever = retriever
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client

    def ask(self, query, top_k=3, max_distance=0.6):
        """Answer a user question using retrieved knowledge."""

        if not isinstance(query, str):
            raise TypeError("Query must be a string.")

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if isinstance(top_k, bool) or not isinstance(top_k, int):
            raise TypeError("top_k must be an integer.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        try:
            # Step 1: Retrieve relevant documents
            retrieved_documents = self.retriever.retrieve(
                query=query.strip(),
                top_k=top_k,
                max_distance=max_distance
            )

            # Step 2: Build context and extract source information
            context_data = self.context_builder.build_context(
                retrieved_documents
            )

            context = context_data["context"]
            sources = context_data["sources"]

            # Step 3: Handle cases where no context was retrieved
            if not context.strip():
                return {
                    "query": query.strip(),
                    "answer": (
                        "I couldn't find relevant information "
                        "in the available knowledge base."
                    ),
                    "sources": [],
                    "retrieved_count": 0
                }

            # Step 4: Construct the grounded prompt
            prompt = self.prompt_builder.build_prompt(
                query=query.strip(),
                context=context,
                sources=sources
            )

            # Step 5: Generate the answer using the selected LLM
            answer = self.llm_client.generate(prompt)

            # Step 6: Return answer and source information
            return {
                "query": query.strip(),
                "answer": answer,
                "sources": sources,
                "retrieved_count": len(retrieved_documents)
            }

        except RAGApplicationError:
            raise

        except Exception as exc:
            raise RAGApplicationError(
                "An unexpected error occurred in the RAG pipeline."
            ) from exc



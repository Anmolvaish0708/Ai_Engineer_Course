
from app.config import CHROMA_DB_PATH
from app.embeddings.embedding_generator import EmbeddingGenerator
from app.vector_store.chroma_store import ChromaStore
from app.retrieval.retriever import Retriever
from app.retrieval.context_builder import ContextBuilder
from app.generation.prompt_builder import PromptBuilder
from app.generation.llm_client import LLMClient
from app.generation.rag_pipeline import RAGPipeline
from app.exceptions import RAGApplicationError


def initialize_rag_pipeline():
    """
    Initialize all components required by the RAG pipeline
    and connect them together.
    """

    print("Initializing RAG application...")

    # 1. Initialize embedding generator
    embedding_generator = EmbeddingGenerator()

    # 2. Initialize vector store
    vector_store = ChromaStore(
        db_path=CHROMA_DB_PATH
    )

    # 3. Initialize retriever
    retriever = Retriever(
        embedding_generator=embedding_generator,
        vector_store=vector_store,
        collection_name="customer_support"
    )

    # 4. Initialize context builder
    context_builder = ContextBuilder()

    # 5. Initialize prompt builder
    prompt_builder = PromptBuilder()

    # 6. Initialize LLM client
    llm_client = LLMClient()

    # 7. Connect everything through RAGPipeline
    rag_pipeline = RAGPipeline(
        retriever=retriever,
        context_builder=context_builder,
        prompt_builder=prompt_builder,
        llm_client=llm_client
    )

    print("RAG application initialized successfully!")

    return rag_pipeline


def run_application():
    """
    Run the interactive command-line RAG application.
    """

    try:
        # Initialize pipeline once when application starts
        rag_pipeline = initialize_rag_pipeline()

        print("\n" + "=" * 50)
        print("CUSTOMER SUPPORT RAG ASSISTANT")
        print("=" * 50)
        print("Ask questions about customer support.")
        print("Type 'exit' or 'quit' to stop.\n")

        while True:

            query = input("You: ").strip()

            if query.lower() in ["exit", "quit"]:
                print("Closing RAG application. Goodbye!")
                break

            if not query:
                print("Please enter a valid question.\n")
                continue

            try:
                response = rag_pipeline.ask(
                    query=query,
                    top_k=3,
                    max_distance=0.6
                )

                print("\nAssistant:")
                print(response["answer"])

                if response["sources"]:
                    print("\nSupporting Sources:")

                    for source in response["sources"]:
                        print(f"- {source['id']}")

                print(
                    f"\nRetrieved Documents: "
                    f"{response['retrieved_count']}"
                )

                print("-" * 50 + "\n")

            except RAGApplicationError as exc:
                print(f"\nUnable to process your question: {exc}\n")

    except RAGApplicationError as exc:
        print(f"Failed to initialize RAG application: {exc}")

    except KeyboardInterrupt:
        print("\nApplication interrupted. Goodbye!")


if __name__ == "__main__":
    run_application()

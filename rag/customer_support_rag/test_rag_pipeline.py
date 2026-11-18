from app.embeddings.embedding_generator import EmbeddingGenerator
from app.vector_store.chroma_store import ChromaStore
from app.retrieval.retriever import Retriever
from app.retrieval.context_builder import ContextBuilder
from app.generation.prompt_builder import PromptBuilder
from app.generation.llm_client import LLMClient
from app.generation.rag_pipeline import RAGPipeline


# Initialize dependencies
embedding_generator = EmbeddingGenerator()
vector_store = ChromaStore()

retriever = Retriever(
    embedding_generator=embedding_generator,
    vector_store=vector_store,
    collection_name="customer_support"
)

context_builder = ContextBuilder()
prompt_builder = PromptBuilder()
llm_client = LLMClient()


# Initialize RAG pipeline
rag_pipeline = RAGPipeline(
    retriever=retriever,
    context_builder=context_builder,
    prompt_builder=prompt_builder,
    llm_client=llm_client
)


# Ask a question
# response = rag_pipeline.ask(
#     query="I forgot my password. How can I access my account?",
#     top_k=3
# )
response = rag_pipeline.ask(
    query="What is the process for applying for a home loan?",
    top_k=3
)

print(response)

print("\nQuestion:", response["query"])
print("\nAnswer:", response["answer"])
print("\nRetrieved count:", response["retrieved_count"])
print("\nSources:")

for source in response["sources"]:
    print(source)

  
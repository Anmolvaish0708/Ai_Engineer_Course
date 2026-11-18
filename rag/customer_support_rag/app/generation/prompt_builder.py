
class PromptBuilder:
    """Builds prompts for grounded RAG generation."""

    def build_prompt(self, query, context, sources):
        """
        Build a prompt using the user question,
        retrieved context and source references.
        """

        # 1. Validate query
        if not isinstance(query, str):
            raise TypeError("Query must be a string.")

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        query = query.strip()

        # 2. Validate context
        if not isinstance(context, str):
            raise TypeError("Context must be a string.")

        context = context.strip()

        # 3. Validate sources
        if not isinstance(sources, list):
            raise TypeError("Sources must be a list.")

        valid_source_ids = []

        for source in sources:

            if not isinstance(source, dict):
                raise TypeError(
                    "Each source must be a dictionary."
                )

            source_id = source.get("id")

            if not isinstance(source_id, str) or not source_id.strip():
                raise ValueError(
                    "Each source must contain a valid document ID."
                )

            valid_source_ids.append(source_id.strip())

        if len(valid_source_ids) != len(set(valid_source_ids)):
            raise ValueError("Duplicate source IDs are not allowed.")

        # 4. Handle empty context
        if not context or not valid_source_ids:
            raise ValueError(
                "Cannot build a generation prompt without "
                "retrieved context and source references."
            )

        # 5. Define system instructions
        system_instructions = """
        You are a helpful customer-support assistant.

        Your task is to answer customer questions using
        the supplied knowledge base context.

        Follow these rules:

        1. Answer using only the supplied context.
        2. Do not invent facts or make unsupported assumptions.
        3. If the context does not contain enough information,
        clearly state that you do not have enough information.
        4. Provide the IDs of documents supporting your answer.
        5. Only reference document IDs supplied in the source list.
        6. Be clear, concise and helpful.
        """

        # 6. Construct source information
        source_information = "\n".join(
            f"- {source_id}"
            for source_id in valid_source_ids
        )

        # 7. Construct final prompt
        prompt = f"""
        {system_instructions}

        AVAILABLE SOURCE IDs:

        {source_information}

        RETRIEVED CONTEXT:

        {context}

        USER QUESTION:

        {query}

        INSTRUCTIONS FOR YOUR RESPONSE:

        Answer the user's question using the retrieved context.
        Include the IDs of the documents supporting your answer.

        ANSWER:
        """

        return prompt.strip()

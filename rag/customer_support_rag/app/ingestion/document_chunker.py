class DocumentChunker:
    """Splits documents into smaller chunks for a RAG ingestion pipeline."""

    def __init__(self, chunk_size, chunk_overlap, separators=None):
        """Initialize and validate the chunking configuration."""

        if not isinstance(chunk_size, int):
            raise TypeError("chunk_size must be an integer.")

        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero.")

        if not isinstance(chunk_overlap, int):
            raise TypeError("chunk_overlap must be an integer.")

        if chunk_overlap < 0:
            raise ValueError(
                "chunk_overlap must be greater than or equal to zero."
            )

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap cannot be greater than or equal to chunk_size."
            )

        if separators is None:
            separators = ["\n\n", "\n", ". ", " ", ""]
        else:
            if not isinstance(separators, list):
                raise TypeError("separators must be a list.")

            if not separators:
                raise ValueError("separators cannot be empty.")

            for separator in separators:
                if not isinstance(separator, str):
                    raise TypeError(
                        "Each separator must be a string."
                    )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators

    def chunk_documents(self, documents):
        """Split a list of documents into smaller chunks."""

        if not isinstance(documents, list):
            raise TypeError("documents must be a list.")

        if not documents:
            raise ValueError("documents cannot be empty.")

        chunks = []

        for document in documents:
            if not isinstance(document, str):
                raise TypeError(
                    "Each document must be a string."
                )

            document = document.strip()

            if not document:
                continue

            chunks.extend(self._split_text(document))

        if not chunks:
            raise ValueError(
                "No valid chunks could be created from the documents."
            )

        return chunks

    def _split_text(self, text, separators=None):
        """Recursively split text using increasingly smaller separators."""

        if separators is None:
            separators = self.separators

        for index, separator in enumerate(separators):

            # Final fallback: split by characters.
            if separator == "":
                return self._split_by_characters(text)

            # Use the first separator available in the text.
            if separator in text:
                parts = text.split(separator)
                processed_parts = []

                for part in parts:
                    part = part.strip()

                    if not part:
                        continue

                    if len(part) <= self.chunk_size:
                        processed_parts.append(part)
                    else:
                        remaining_separators = separators[index + 1:]

                        processed_parts.extend(
                            self._split_text(
                                part,
                                remaining_separators
                            )
                        )

                return self._merge_splits(
                    processed_parts,
                    separator
                )

        # Defensive fallback.
        return [text]

    def _split_by_characters(self, text):
        """Split text by characters when no other separator is available."""

        chunks = []
        step_size = self.chunk_size - self.chunk_overlap
        start = 0

        while start < len(text):
            chunk = text[start:start + self.chunk_size]

            if chunk:
                chunks.append(chunk)

            start += step_size

        return chunks

    def _merge_splits(self, parts, separator):
        """Merge text parts into chunks while preserving overlap."""

        results = []
        current_parts = []

        for part in parts:
            part = part.strip()

            if not part:
                continue

            candidate_parts = current_parts + [part]
            candidate_chunk = separator.join(candidate_parts)

            # The new part fits inside the current chunk.
            if len(candidate_chunk) <= self.chunk_size:
                current_parts.append(part)
                continue

            # Save the completed chunk.
            if current_parts:
                results.append(separator.join(current_parts))

            # Build overlap from the end of the previous chunk.
            overlap_parts = []
            overlap_length = 0

            for previous_part in reversed(current_parts):
                if overlap_parts:
                    new_length = (
                        len(previous_part)
                        + len(separator)
                        + overlap_length
                    )
                else:
                    new_length = len(previous_part)

                # Keep complete parts instead of cutting words.
                overlap_parts.insert(0, previous_part)
                overlap_length = new_length

                if overlap_length >= self.chunk_overlap:
                    break

            # Start the next chunk with the overlap.
            current_parts = overlap_parts

            # Check whether the new part fits with the overlap.
            candidate_parts = current_parts + [part]
            candidate_chunk = separator.join(candidate_parts)

            if len(candidate_chunk) <= self.chunk_size:
                current_parts.append(part)
            else:
                # The overlap plus the new part is too large.
                # Start a new chunk with the new part.
                if current_parts:
                    current_parts = [part]
                else:
                    current_parts = [part]

        # Add the final chunk.
        if current_parts:
            results.append(separator.join(current_parts))

        return results


chunker = DocumentChunker(
    chunk_size=50,
    chunk_overlap=10
)

chunks = chunker.chunk_documents(
    [
        "Hi I am anmol pandey. Currently working as a software engineer"
        "at Accenture. \n\n I am from IT background and my focus is currently upskilling myself."
        "Also i'm learning DSA side by side to crack high paying job at mncs."
    ]
)

print(chunks)
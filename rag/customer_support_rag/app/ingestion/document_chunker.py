
class DocumentChunker:
    """Splits documents into smaller chunks for RAG ingestion."""

    def __init__(self, chunk_size, chunk_overlap, separators=None):  #A default list can potentially be shared between instances of the class if we directly use a mutable default argument like a list. This can lead to unexpected behavior if the list is modified in one instance, as it will affect all other instances that use the default value. To avoid this, we can set the default value to None and then initialize the list inside the constructor if it's not provided.
        # Validate and store configuration
        if chunk_size <=0:
            raise ValueError("chunk size should be greate than zero")
        
        if chunk_overlap < 0:
            raise ValueError("chunk overlap should be greater than equal to zero")

        if chunk_overlap >= chunk_size:
            raise ValueError("chunk overlap cannot be greater than or equal to chunk size.")

        if separators is None:
            separators = ["\n\n", "\n", ". ", " ", ""]
        else:
            if not isinstance(separators, list):
                        raise TypeError("separators must be a list")
            
            if not separators:
                        raise ValueError("Separators cannot be empty.")
            
            for sep in separators:
                if not isinstance(sep,str):
                    raise TypeError("each element inside separator must be a string.")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap    
        self.separators = separators   


    def chunk_documents(self, documents):

        # Validate input
        if not isinstance(documents,list):
            raise TypeError("documents must be a list")

        chunks = []

        for doc in documents:
           chunks.extend(self._split_text(doc)) 

        # Chunk the documents
        # chunks = []
        # step_size = self.chunk_size - self.chunk_overlap

        # for doc in documents:
        #     start = 0
        #     while start < len(doc):
        #         chunk = doc[start:start + self.chunk_size]
        #         chunks.append(chunk)
        #         start += step_size
            

        # # Return the chunks
        return chunks

    def _split_text(self, text, separators=None):
        """Splits the text recursively using the configured separators."""

        if separators is None:
            separators = self.separators

        # Find the first suitable separator
        for index, sep in enumerate(separators):

            # Handle the final fallback separately
            if sep == "":
                results = []
                start = 0

                while start < len(text):
                    chunk = text[start:start + self.chunk_size]
                    results.append(chunk)
                    start += self.chunk_size

                return results

            # Use this separator only if it exists in the text
            if sep in text:
                parts = text.split(sep)
                processed_parts = []

                for part in parts:
                    part = part.strip()

                    # Skip empty pieces
                    if not part:
                        continue

                    # Small pieces can be merged at this level
                    if len(part) <= self.chunk_size:
                        processed_parts.append(part)

                    # Large pieces need to be split using the next separators
                    else:
                        processed_parts.extend(
                            self._split_text(
                                part,
                                separators[index + 1:]
                            )
                        )

                return self._merge_splits(processed_parts, sep)

        return [text]

    def _merge_splits(self, parts, separator):
        """Merge small text parts into chunks of the configured size."""

        results = []
        current_chunk = ""

        for part in parts:
            # Remove unnecessary whitespace
            part = part.strip()

            # Skip empty parts
            if not part:
                continue

            # Calculate the length if we add this part
            if current_chunk:
                combined_length = (
                    len(current_chunk) + len(separator) + len(part)
                )
            else:
                combined_length = len(part)

            # Add the part if it fits
            if combined_length <= self.chunk_size:
                if current_chunk:
                    current_chunk += separator + part
                else:
                    current_chunk = part

            # Otherwise, save the current chunk and start a new one
            else:
                if current_chunk:
                    results.append(current_chunk)

                current_chunk = part

        # Add the final chunk because the loop may end with
        # a chunk that has not yet been added to results
        if current_chunk:
            results.append(current_chunk)

        return results        
                        
                
                



chunker = DocumentChunker(10,2)
chunks =  chunker.chunk_documents(
    ["Hi, I am Anmol Pandey.\n\n working as a software engineer at accenture."]
)

print(chunks)
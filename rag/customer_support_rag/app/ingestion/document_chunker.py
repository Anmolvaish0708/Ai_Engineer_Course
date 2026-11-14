
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

    def _split_text(self, text, separators = None):
        """ Splits the text into chunks based on specified separators. """
        if separators is None:
             separators = self.separators

        results = []

        for index, sep in enumerate(separators):
            if sep in text:

                if sep == "":
                    # If the separator is an empty string, we can split the text into individual characters
                    start = 0
                    while start < len(text):
                        chunk = text[start:start + self.chunk_size]
                        results.append(chunk)
                        start += self.chunk_size

                    return results    

                parts = text.split(sep)
                for part in parts:
                     if part.strip():
                        if len(part) <= self.chunk_size:
                            results.append(part)
                        else:
                            # If the part is still too large, we can recursively split it using the next separator
                            results.extend(self._split_text(part,separators[index+1:]))

                return results 
                     
             
             



chunker = DocumentChunker(10,2)
chunks =  chunker.chunk_documents(
    ["Hi, I am Anmol Pandey.\n\n working as a software engineer at accenture."]
)

print(chunks)
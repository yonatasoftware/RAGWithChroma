import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extract_pdf_text(pdf_path):
    """
    Extracts text from a PDF file.
    """

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    return text

#policy = extract_pdf_text("policy.pdf")
#print(policy)





def chunk_text(text, chunk_size=500, chunk_overlap=100):
    """
    Split text into overlapping chunks using LangChain's
    RecursiveCharacterTextSplitter.

    Returns:
        List of dictionaries containing chunk text and metadata.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    # Returns a list of Document objects
    documents = splitter.create_documents([text])

    chunks = []

    current_position = 0

    for chunk_id, document in enumerate(documents):

        # Extract the actual chunk text
        chunk_text = document.page_content

        # Find where this chunk starts in the original text
        start_index = text.find(chunk_text, current_position)

        if start_index == -1:
            # Fallback in case of repeated text
            start_index = current_position

        end_index = start_index + len(chunk_text)

        chunks.append(
            {
                "chunk_id": chunk_id,
                "text": chunk_text,
                "start_index": start_index,
                "end_index": end_index,
                "metadata": document.metadata
            }
        )

        # Move the search window forward
        current_position = start_index

    return chunks



#print(f"Number of chunks: {len(chunks)}")

#for i, chunk in enumerate(chunks):

#    print(chunk)
#    print("-" * 20)  # Visual separator between chunks


# main.py
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader, PyMuPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain

class LangChainProcessor:
    def __init__(self):
        # Initialize components
        self.llm = Ollama(model="mistral")
        self.embeddings_llm = OllamaEmbeddings(model="mistral")
        self.text_splitter = RecursiveCharacterTextSplitter()

        # Define the prompt template
        self.prompt = ChatPromptTemplate.from_template("""
        Answer the following question based on the provided context and your internal knowledge.
        Give priority to context and if you are not sure then say you are not aware of topic:
        
        <context>
        {context}
        </context>
        
        Question: {input}
        """)

        # Initialize the document chain
        self.document_chain = create_stuff_documents_chain(self.llm, self.prompt)

    def load_and_process_docs(self, urls=None, pdf_path=None):
        """Load documents from URLs or PDF and process them."""
        docs = []

        # Load documents from URLs
        if urls:
            for url in urls:
                loader = WebBaseLoader(url)
                docs.extend(loader.load())

        # Load documents from a PDF file
        if pdf_path:
            loader = PyMuPDFLoader(pdf_path)
            docs.extend(loader.load())

        # Split documents into smaller chunks
        documents = self.text_splitter.split_documents(docs)

        # Create a vector index using the document chunks
        vector_index = FAISS.from_documents(documents, self.embeddings_llm)
        retriever = vector_index.as_retriever()

        return retriever

    def get_answer(self, question, retriever):
        """Retrieve documents and generate an answer."""
        relevant_docs = retriever.invoke({"input": question})
        context = "\n".join([doc.page_content for doc in relevant_docs])
        
        response = self.document_chain.invoke({
            "input": question,
            "context": [Document(page_content=context)]
        })
        
        return response

# Example usage:
# This part of the code would be used within FastAPI routes (e.g., in api_gateway.py)

# urls = [
#     "https://www.anthropic.com/news/releasing-claude-instant-1-2",
#     "https://www.anthropic.com/news/claude-pro",
#     # Add more URLs as needed
# ]
# processor = LangChainProcessor()
# retriever = processor.load_and_process_docs(urls=urls)
# answer = processor.get_answer("Do you know about Claude 3?", retriever)
# print(answer)

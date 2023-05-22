import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import ConversationalRetrievalChain
from pdfminer import high_level

os.environ["OPENAI_API_KEY"] = "api-key"

# read file
# pdf_path = "./sample.pdf"

def get_chain(pdf_path):
    # read the pdf text
    text = high_level.extract_text(pdf_path, "")

    # split data into chuncks
    data_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=150, length_function=len)
    chunks = data_splitter.split_text(text)

    # get embeddings
    embeddings = OpenAIEmbeddings()
    vector_embedding = FAISS.from_texts(chunks, embeddings)
    # qa = load_qa_chain(OpenAI(model="gpt-3.5-turbo"), chain_type="stuff")
    doc_retriever = vector_embedding.as_retriever(search_type="similarity")

    chain = ConversationalRetrievalChain.from_llm(OpenAI(model="text-davinci-002", temperature=0.7),
                                                  retriever=doc_retriever,
                                                  chain_type="stuff")
    # chat_history = []
    # query = "what is operations research?"
    # result = qa({"question": query, "chat_history": chat_history})
    # print(result)
    return chain

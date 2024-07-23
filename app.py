import streamlit as st
import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain.text_splitter  import CharacterTextSplitter
from langchzin.enbeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
#Charger les vairables d'environnement
load_dotenv()
genai_api_key = os.getenv('GENAI_API_KEY')

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(texte_brute):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len        
    )
    chunks = text_splitter.split_text(texte_brute)
    return chunks

def get_vector_store(text_chnuks):
    embeddings = OpenAIEmbeddings()
    vectorestore = FAISS.from_texts(texts=text_chnuks, embedding=embeddings)
    return vectorestore

def main():
    #Configuration de la page streamlit
    st.set_page_config(page_title="Chat with multiple PDF's", page_icon=":books:")

    st.header("Welcome to the Multi-PDF :books: Chat Application")
    st.text_input("Ask a question about your documents:")

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDF's here and click on 'Process'", 
            accept_multiple_files=True,
            type='pdf'
            )
      #  st.button("Process")

        if st.button("Process"):
            if pdf_docs:
                with st.spinner("Processing"):
                    
                    #Obtenir le pdf brute
                    texte_brute = get_pdf_text(pdf_docs)

                    #Get the text chunk/Séparer le text en morceaux
                    text_chunks = get_text_chunks(texte_brute)
                    
                    #Créer le store de vecteur
                    vec
            else:
                st.warning("Please upload at least one PDF file.")

if __name__ == '__main__':
    main()
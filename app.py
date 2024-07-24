import streamlit as st
import os

from dotenv import load_dotenv
from pypdf import PdfReader
from langchain.text_splitter  import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI
from htmlTemplates import css, bot_template, user_template


#Charger les vairables d'environnement
load_dotenv()
genai_api_key = st.secrets["general"]["GOOGLE_API_KEY"]


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

def get_vector_store(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5", encode_kwargs={"normalize_embeddings": True})
    vectorestore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorestore

def get_conversation_chain(vectorstore):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro", 
        temperature=0
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever= vectorstore.as_retriever(),
        memory= memory
    )

    if conversation_chain is None:
        print("Conversation chain is None")
    else:
        print("Conversation chain initialized successfully")

    return conversation_chain

def handle_userinput(user_question):
    if st.session_state.conversation:
        response = st.session_state.conversation({"question": user_question})
        if 'answer' in response:
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            st.session_state.chat_history.append({"role": "bot", "content": response['answer']})
        else:
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            st.session_state.chat_history.append({"role": "bot", "content": "Sorry, I couldn't process that request."})
    else:
        st.warning("Conversation is not initialized.")



def main():
    #Configuration de la page streamlit
    st.set_page_config(page_title="Chat with multiple PDF's", page_icon=":books:")
    
    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header("Welcome to the Multi-PDF :books: Chat Application")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(user_template.replace("{{MSG}}", chat["content"]), unsafe_allow_html=True)
        else:
            st.markdown(bot_template.replace("{{MSG}}", chat["content"]), unsafe_allow_html=True)

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
                    vectorstore = get_vector_store(text_chunks)
                    
                    #Créer la haine de conversation
                    st.session_state.conversation = get_conversation_chain(vectorstore)

            else:
                st.warning("Please upload at least one PDF file.")
        

if __name__ == '__main__':
    main()
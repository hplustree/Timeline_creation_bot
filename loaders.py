from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import Docx2txtLoader
from generate_final_timeline import *

from dotenv import load_dotenv
import os

load_dotenv()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=int(os.getenv('CHUNK_SIZE')),
    chunk_overlap=int(os.getenv('CHUNK_OVERLAP'))
)
def load_csv(file_path):
    loader = UnstructuredExcelLoader(file_path=file_path)
    data = loader.load()
    return data

def load_docx(file_path):
    loader = Docx2txtLoader(file_path=file_path)
    data = loader.load()
    return data

def load_html_page(file_path):
    loader = UnstructuredHTMLLoader(file_path=file_path)
    data = loader.load()
    return data

def load_pdf(file_path):
    loader = PyPDFLoader(file_path=file_path)
    pages = loader.load_and_split()
    return pages

def load_text(file_path):
    loader = TextLoader(file_path=file_path)
    data = loader.load()
    return data

def load_file(file_path):
    if file_path.endswith('.xlsx'):
        return load_csv(file_path)
    elif file_path.endswith('.txt'):
        return load_text(file_path)
    elif file_path.endswith('.pdf'):
        return load_pdf(file_path)
    elif file_path.endswith('.docx'):
        return load_docx(file_path)
    elif file_path.endswith('.html'):
        return load_html_page(file_path)
    else:
        return Exception('File format not supported')
    
def split_text(text):
     chunks=text_splitter.split_text(text)
     return chunks

def split_file(file_path):
    pages=load_file(file_path)
    text = "\n".join(page.page_content for page in pages)
    chunks = split_text(text)
    return chunks

# # Example purpose
# file_path=os.getenv('PDF_FILE_PATH')
# chunks=split_file(file_path)
# timeline=refine_timeline(chunks)
# print("Timeline: ", timeline)
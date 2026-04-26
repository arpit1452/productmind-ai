from langchain_community.document_loaders import PyPDFLoader

def load_pdf(path):
    return PyPDFLoader(path).load()
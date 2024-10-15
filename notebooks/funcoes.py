import re
import os
import unicodedata
from PyPDF2 import PdfReader
from langchain_core.documents import Document

def clean_text(self, text):
    text = re.sub(r'[\u2022\u2013]', '', text)

    text = '\n'.join([line.strip() for line in text.split('\n')])

    text = text.lower()

    text = re.sub(r'\s+', ' ', text).strip()

    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

    text = re.sub(r'[“”‘’]', '"', text)
    text = re.sub(r'[–—]', '-', text)

    text = re.sub(r'[^a-z0-9\s.,!?;:()-]', '', text)

    text = re.sub(r'figura\s*\d+[:]?.*', '', text, flags=re.IGNORECASE)

    text = re.sub(r'tabela\s*\d+[:]?.*', '', text, flags=re.IGNORECASE)

    text = re.sub(r'\n+', '\n', text).strip()
    text = re.sub(r'\s+', ' ', text)

    return text


def get_amount_of_pages_of_references(self, reader):
    find_referencias_bibliograficas = True
    index = -1
    amount_of_pages = 1
    while find_referencias_bibliograficas:
        if 'Referências Bibliográficas'.upper() in reader.pages[index].extract_text().upper():
            find_referencias_bibliograficas = False
        else:
            amount_of_pages += 1
            index -= 1

    return amount_of_pages


def get_amount_of_useless_pages_in_start(self, reader):
    for index in range(len(reader.pages)):
        if 'APRESENTAÇÃO' in reader.pages[index].extract_text() and 'SUMÁRIO' not in reader.pages[index].extract_text():
            return index

    def extract_text_from_pdf(self, pdf_path) -> list:
        documents = []
        reader = PdfReader(pdf_path)
        pages_of_references = self.get_amount_of_pages_of_references(reader)
        useless_pages = self.get_amount_of_useless_pages_in_start(reader)
        text = ""
        for page_num in range(len(reader.pages)):
            if page_num > useless_pages and page_num < len(reader.pages) - pages_of_references:
                page = reader.pages[page_num]
                text = page.extract_text()

                if text:
                    documents.append(Document(page_content=text, metadata={'page_number': page_num + 1}))
        
        return documents
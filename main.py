#!/usr/bin/env python
# -*- coding: utf-8 -*-

import concurrent.futures
import os
import shutil
import ssl
from simple_term_menu import TerminalMenu
from datetime import datetime
from urllib import request

import img2pdf
import ocrmypdf
import yaml

BASE_URL = "https://historico.conaliteg.gob.mx/"
WORKSPACE = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
ssl._create_default_https_context = ssl._create_unverified_context


class Book:
    def __init__(self, code, name, year, grade):
        self.id = code
        self.name = '. '.join([x.strip().capitalize() for x in name.split('.')]).strip()
        self.year = year
        self.grade = grade
        self.url = f"{BASE_URL}/{self.id}.htm"
        self._page_count = None

    def get_title(self):
        return f"[{self.grade}º Primaria] {self.name} ({self.year})({self.id})"

    def get_page_count(self):
        if self._page_count is None:
            html_doc = get_html_document(self.url)
            self._page_count = int(html_doc.split("ag_pages = ")[1].split(";")[0])
        return self._page_count

    def get_dir_path(self):
        return os.path.join(WORKSPACE, "output", self.get_title())

    def get_book_file_path(self):
        return os.path.join(self.get_dir_path(), f"{self.get_title()}.pdf")

    @staticmethod
    def fetch_page(url, file_path):
        _, headers = request.urlretrieve(url, file_path)
        if headers.get("Content-Type") == "text/html":
            shutil.copy(os.path.join(WORKSPACE, "assets", "missing_page.jpg"), file_path)

    def fetch_pages(self):
        print("Espera...")
        if not os.path.exists(self.get_dir_path()):
            os.mkdir(self.get_dir_path())
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for page in range(self.get_page_count()):
                page_url = f"{BASE_URL}/c/{self.id}/{page:03}.jpg"
                page_file_path = os.path.join(self.get_dir_path(), f"{page:03}.jpg")
                if not os.path.exists(page_file_path):
                    executor.submit(Book.fetch_page, page_url, page_file_path)

    def fetch(self):
        self.fetch_pages()
        if not os.path.exists(self.get_book_file_path()):
            with open(self.get_book_file_path(), "wb") as f:
                pages = [os.path.join(self.get_dir_path(), f"{page:03}.jpg") for page in range(self.get_page_count())]
                pages.insert(1, os.path.join(WORKSPACE, "assets", "disclaimer.jpg"))
                pages.insert(2, os.path.join(WORKSPACE, "assets", "blank.jpg"))
                f.write(img2pdf.convert(
                    pages,
                    title=self.name,
                    creationdate=datetime(int(self.year), 1, 1),
                    author="Comisión Nacional de Libros de Texto Gratuitos",
                ))
        try:
            ocrmypdf.ocr(
                self.get_book_file_path(),
                self.get_book_file_path(),
                language='spa',
                clean=True,
                jobs=12,
                max_image_mpixels=900
            )
        except ocrmypdf.exceptions.PriorOcrFoundError:
            pass
        except Exception as e:
            return print(f"Error este libro no pudo ser indexado: {e}")
        self.cleanup()
        print(f"Tu libro está listo en: {self.get_book_file_path()}\n")

    def cleanup(self):
        files = [os.path.join(self.get_dir_path(), f"{page:03}.jpg") for page in range(self.get_page_count())]
        for file in files:
            os.remove(file)


def get_html_document(url):
    req = request.urlopen(url)
    return req.read().decode("utf-8")


def get_catalogue():
    html_doc = get_html_document(f"{BASE_URL}/libros.js")
    raw_catalogue = yaml.safe_load(html_doc.split("var libros = ")[1])
    raw_catalogue.sort(key=lambda x: x[3])
    catalogue = {}
    for item in raw_catalogue:
        catalogue.setdefault(item[3], {})
        catalogue[item[3]].update({
            item[1]: Book(item[1], item[0], item[2], item[3])
        })
    return catalogue


def download_books(book_list):
    for book in book_list:
        if not os.path.exists(book.get_book_file_path()):
            print(book.get_title())
            book.fetch()


def prompt_choice(options, prompt):
    print(prompt)
    return TerminalMenu(options).show()


def prompt_grade(catalogue):
    return prompt_choice(list(map(lambda x: f"{x}º Primaria", catalogue.keys())),
                         'Elige el grado escolar del libro a buscar:') + 1


def prompt_book(catalogue, grade):
    book_index = prompt_choice([book.get_title() for book in catalogue[grade].values()],
                               'Elige el libro que deseas:')
    return catalogue[grade][list(catalogue[grade].keys())[book_index]].id


def create_output_dir():
    output_dir_path = os.path.join(WORKSPACE, 'output')
    if not os.path.exists(output_dir_path) or not os.path.isdir(output_dir_path):
        os.mkdir(output_dir_path)


def main():
    create_output_dir()
    catalogue = get_catalogue()
    grade = prompt_grade(catalogue)
    book_code = prompt_book(catalogue, grade)
    download_books([catalogue[grade][book_code]])
    print("¡Listo!")


if __name__ == '__main__':
    main()

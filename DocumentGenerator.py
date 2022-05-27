from imports import *


class DocumentGenerator:
    def __init__(self):
        self.__document_type = None

    def set_document_type(self, doc_type: str):
        self.__document_type = doc_type

    def get_document_type(self):
        return self.__document_type

    def __gen__(self, *args, **kwargs):
        document = documents[self.__document_type](*args, **kwargs)
        return document

    def __save__(self, document):
        term(f'mkdir documents; mkdir documents/{self.__document_type}')

        tree = ET.ElementTree(document)
        tree.write(f"./documents/{self.__document_type}/{dt.now().isoformat()}.xml",
                   xml_declaration=True, encoding='utf-8',
                   method="xml")

    def __send__(self, username, machine, filename):
        document_path = f'./documents/{self.__document_type}/{filename}'
        term(f'mkdir /home/ldapusers/{username}/documents2send/{self.__document_type}')
        status = term(f'scp {document_path} {username}@{machine}: /home/ldapusers/{username}/documents2send/{self.__document_type}/{filename}')
        return status

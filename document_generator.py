import variables
from base_logger import BaseLogger
from imports import *
from uuid import uuid4


class DocumentGenerator:
    def __init__(self):
        self.log = BaseLogger().get_logger('DocumentGenerator')
        self.__document_type = None

    def set_document_type(self, doc_type: str):
        self.__document_type = doc_type

    def get_document_type(self):
        return self.__document_type

    def __gen__(self, *args, **kwargs):
        document = generate_documents[self.__document_type](*args, **kwargs)
        return document

    def __save__(self, document, filename=None):
        self.log.debug("Generating directories")
        term(f'mkdir documents; mkdir documents/{self.__document_type}')

        tree = ET.ElementTree(document)
        if filename is None:
            filename = f'{uuid4()}.xml'
        else:
            filename = f'{filename}.xml'

        filepath = f'./documents/{self.__document_type}/{filename}'
        tree.write(
            filepath,
            encoding='utf-8',
            method="xml")
        return filename, filepath

    def __ssh_send__(self, filename, username='gabko', machine='dockerHub'):
        document_path = f'./documents/{self.__document_type}/{filename}'
        term(f'ssh {username}@{machine} mkdir /home/ldapusers/{username}/documents2send/{self.__document_type}')
        filename_ = filename.replace(":", "_")
        status = term(f'scp {document_path} {username}@{machine}:/home/ldapusers/{username}/documents2send/{self.__document_type}/{filename_}')

        if self.__document_type == 'wbgz':
            variables.send_documents['wbgz'](filename_)
        return status

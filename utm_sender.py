from os import system as term, popen as rterm

from base_logger import BaseLogger


class UtmSender(BaseLogger):

    def __init__(self, utm_ip='localhost', utm_port=8080, doc_type=None):
        self.utm_addr = f'http://{utm_ip}:{utm_port}'
        self.log = BaseLogger().get_logger('UtmSender', 'info')

    def __create_curl(self, filepath, href):
        base = f'curl -F "xml_file=@{filepath[2:]}"'
        self.log.debug(base)

        return f'{base} {href}'

    def send(self, filepath, file_type):
        """curl -F "xml_file=@Che.xml" http://localhost:8080/xml?type=Cheque"""
        if 'cheque' in file_type.lower():
            href = f'{self.utm_addr}/xml?type={file_type}'
        else:
            href = f'{self.utm_addr}/opt/in/{file_type}'
        self.log.debug(href)
        curl = self.__create_curl(filepath, href)
        self.log.info(curl.replace('http', '\nhttp'))
        term(curl)

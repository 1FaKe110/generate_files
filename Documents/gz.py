import copy

from base_logger import BaseLogger
from datetime import datetime as dt
from xml.etree.ElementTree import Element, SubElement, register_namespace, indent


class WayBillGZ(BaseLogger):

    def __init__(self):
        self.logger = self.get_logger(__name__)
        self.ns = {
            "ns": "http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01",
            "gz": "http://fsrar.ru/WEGAIS/goznak"
        }
        [register_namespace("{" + ns + "}", uri) for ns, uri in self.ns.items()]
        self.skeleton = self.__create_base()
        self.document = self.skeleton

    def __create_base(self):
        document = Element('ns:Documents', {'xmlns:' + k: v for k, v in self.ns.items()})
        header = SubElement(document, 'ns:Header')
        SubElement(header, 'gz:DocType').text = 'WayBillGoznak'

        SubElement(header, 'gz:DocId').text = dt.now().isoformat()[:-7]
        SubElement(header, 'gz:DocDate').text = dt.now().date().isoformat()
        SubElement(header, 'gz:doc_iid').text = '1'
        SubElement(header, 'gz:shipperID').text = '020000004400'
        SubElement(header, 'gz:ConsigneeID')

        content = SubElement(header, 'gz:Content')
        pos = SubElement(content, 'gz:Pos')
        SubElement(pos, 'gz:DocPosId').text = '1'
        SubElement(pos, 'gz:Form2').text = '1'
        SubElement(pos, 'gz:bc')

        return document

    def fill(self, fsrarid, mark_list):
        self.document = copy.deepcopy(self.skeleton)
        consignee_id = self.document.find('.//{http://fsrar.ru/WEGAIS/goznak}ConsigneeID', self.ns)
        consignee_id.text = fsrarid
        bc = self.document.find('.//{http://fsrar.ru/WEGAIS/goznak}bc')

        for mark in mark_list:
            SubElement(bc, 'gz:NCode').text = mark

    def build(self):
        return self.document

    def show(self):
        """ pretty print of current document state """
        # self.logger.info(f'{et.tostring(self.base_part, encoding="utf-8").decode()}') # for Python < 3.9
        self.logger.info(indent(self.document, space="\t", level=0))  # works on Python3.9 +


def main():
    wb = WayBillGZ()
    wb.show()
    wb.fill(
        fsrarid='030000504835',
        mark_list=['mark1', 'mark2', 'mark3', 'mark4', 'mark5']
    )
    wb.show()
    wb.build()


if __name__ == '__main__':
    main()

from abc import ABCMeta, abstractmethod
from pprint import pprint

from base_logger import BaseLogger
from datetime import datetime as dt
from xml.etree.ElementTree import Element, SubElement, register_namespace, tostring, indent, ElementTree


class SceletonV4(metaclass=ABCMeta):
    def __init__(self, ns):
        self.ns = ns
        self.reg_namespaces()

    def reg_namespaces(self):
        [register_namespace("{" + ns + "}", uri) for ns, uri in self.ns.items()]

    @abstractmethod
    def show(self):
        """ pretty print of current document state """
        pass

    @abstractmethod
    def build(self):
        pass


class RepProducedProductV4(SceletonV4):
    """
    Create xml document of RepProducedProductV4
    """
    ns = {
        "ns": "http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01",
        "oref": "http://fsrar.ru/WEGAIS/ClientRef_v2",
        "rpp": "http://fsrar.ru/WEGAIS/RepProducedProduct_v4",
        "ce": "http://fsrar.ru/WEGAIS/CommonV3"
    }

    def __init__(self):
        super().__init__(ns=self.ns)
        self.log = BaseLogger().get_logger(__name__, filter=True)
        self.base_part = self.__create_base()

    def __create_base(self):
        documents = Element(f"ns:Documents", {'xmlns:' + k: v for k, v in self.ns.items()})
        owner = SubElement(documents, "ns:Owner")
        SubElement(owner, "ns:FSRAR_ID").text = '030000504835'

        document = SubElement(documents, "ns:Document")
        rpp = SubElement(document, "ns:RepProducedProduct_v4")
        SubElement(rpp, "rpp:Identity")

        header = SubElement(rpp, "rpp:Header")
        SubElement(header, "rpp:Producer")
        SubElement(rpp, "rpp:Content")

        # ----
        SubElement(header, "rpp:Type").text = 'OperProduction'
        SubElement(header, "rpp:NUMBER")
        SubElement(header, "rpp:Date").text = dt.now().isoformat()[:10]
        SubElement(header, "rpp:ProducedDate").text = dt.now().isoformat()[:10]
        SubElement(header, "rpp:Note").text = 'for test only'

        return documents

    @staticmethod
    def __create_position(**kw):
        position = Element('rpp:Position')
        SubElement(position, "rpp:ProductCode").text = '0300005048350000001'
        SubElement(position, "rpp:Quantity").text = str(len(kw.get('mark_list', '')))
        SubElement(position, "rpp:Identity").text = kw.get('identity', '')
        SubElement(position, "rpp:Party").text = '20160201/2'
        mark_info = SubElement(position, "rpp:MarkInfo")

        for mark in kw.get('mark_list', ['None']):
            SubElement(mark_info, "ce:amc").text = mark

        return position

    @staticmethod
    def __create_ul():
        ul = Element("oref:UL")
        SubElement(ul, "oref:ClientRegId").text = '030000504835'
        SubElement(ul, "oref:FullName").text = 'АКЦИОНЕРНОЕ ОБЩЕСТВО "ЦЕНТРИНФОРМ"'
        SubElement(ul, "oref:INN").text = '7841051711'
        SubElement(ul, "oref:KPP").text = '246343001'

        address = SubElement(ul, "oref:address")
        SubElement(address, "oref:Country").text = '643'
        SubElement(address, "oref:RegionCode").text = '24'
        SubElement(address, "oref:description").text = '660028,РОССИЯ,,,КРАСНОЯРСК Г,,ТЕЛЕВИЗОРНАЯ УЛ,ДОМ 1,СТРОЕНИЕ 9,'

        return ul

    def set_org(self):
        """
        Set the organization data
        """
        xml_header = self.base_part.find('ns:Document').find('ns:RepProducedProduct_v4').find('rpp:Header')
        xml_header.find(f'rpp:Producer').append(self.__create_ul())

    def set_header(self, number):
        """
        Configure the header variables
        """
        self.base_part.find('ns:Document').find('ns:RepProducedProduct_v4').find('rpp:Header').find('rpp:NUMBER').text = str(number)
        self.base_part.find('ns:Document').find('ns:RepProducedProduct_v4').find('rpp:Identity').text = str(number)

    def add_position(self, **position):
        """
        Add a position to document.content
        :param position: dict | dict with position for content
        """
        rppv4 = self.base_part.find('ns:Document').find('ns:RepProducedProduct_v4')
        rppv4.find(f'rpp:Content').append(self.__create_position(**position))

    def show(self, elem: Element = None):
        """ pretty print of current document state """
        # indent(self.base_part, space="\t", level=0)  # works on Python3.9 +
        if elem is None:
            elem = self.base_part

        self.log.info(
            tostring(elem,  method='xml', xml_declaration=True, encoding='utf-8').decode()
        )

    def build(self):
        return self.base_part


def main():
    rpp = RepProducedProductV4()

    rpp.set_header("TEST")
    position = {
        "identity": "1",
        "mark_list": [f'mark_list{i}' for i in range(5)]
    }
    rpp.set_org()
    rpp.add_position(**position)
    rpp.show()
    pprint(rpp.build())


if __name__ == "__main__":
    main()

import xml.etree.ElementTree as et
from typing import List
from datetime import datetime as dt, timedelta, date
from rstr import xeger
from random import randrange as rr

# from Documents.v4 import RepProducedProductV4
from base_logger import BaseLogger


class RepProducedProductV4(BaseLogger):
    """
    Create xml document of TTNSRFSM
    """

    def __init__(self):
        self.logger = self.get_logger(__name__)
        self.ns = {
            "ns": "http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01",
            "oref": "http://fsrar.ru/WEGAIS/ClientRef_v2",
            "rpp": "http://fsrar.ru/WEGAIS/RepProducedProduct_v4",
            "ce": "http://fsrar.ru/WEGAIS/CommonV3"
        }
        self.reg_namespaces()
        self.base_part = self.__create_base

    def reg_namespaces(self):
        [et.register_namespace("{" + ns + "}", uri) for ns, uri in self.ns.items()]

    @property
    def __create_base(self):
        documents = et.Element(
            f"ns:Documents", {'xmlns:' + k: v for k, v in self.ns.items()})
        owner = et.SubElement(documents, "ns:Owner")
        et.SubElement(owner, "ns:FSRAR_ID").text = '030000504835'

        document = et.SubElement(documents, "ns:Document")
        rppv4 = et.SubElement(document, "ns:RepProducedProduct_v4")
        et.SubElement(rppv4, "rpp:Identity")

        header = et.SubElement(rppv4, "rpp:Header")
        et.SubElement(header, "rpp:Producer")
        et.SubElement(rppv4, "rpp:Content")

        # ----
        et.SubElement(header, "rpp:Type").text = 'OperProduction'
        et.SubElement(header, "rpp:NUMBER")
        et.SubElement(header, "rpp:Date").text = dt.now().isoformat()[:10]
        et.SubElement(header, "rpp:ProducedDate").text = dt.now().isoformat()[:10]
        et.SubElement(header, "rpp:Note").text = 'for test only'

        return documents

    @staticmethod
    def __create_position(**kw):
        position = et.Element('rpp:Position')
        et.SubElement(position, "rpp:ProductCode").text = '0300005048350000001'
        et.SubElement(position, "rpp:Quantity").text = str(len(kw.get('mark_list', '')))
        et.SubElement(position, "rpp:Identity").text = kw.get('identity', '')
        et.SubElement(position, "rpp:Party").text = '20160201/2'
        mark_info = et.SubElement(position, "rpp:MarkInfo")

        for mark in kw.get('mark_list', ['None']):
            et.SubElement(mark_info, "ce:amc").text = mark

        return position

    @staticmethod
    def __create_ul():
        ul = et.Element("oref:UL")
        et.SubElement(ul, "oref:ClientRegId").text = '030000504835'
        et.SubElement(ul, "oref:FullName").text = 'АКЦИОНЕРНОЕ ОБЩЕСТВО "ЦЕНТРИНФОРМ"'
        et.SubElement(ul, "oref:INN").text = '7841051711'
        et.SubElement(ul, "oref:KPP").text = '246343001'

        address = et.SubElement(ul, "oref:address")
        et.SubElement(address, "oref:Country").text = '643'
        et.SubElement(address, "oref:RegionCode").text = '24'
        et.SubElement(address, "oref:description").text = '660028,РОССИЯ,,,КРАСНОЯРСК Г,,ТЕЛЕВИЗОРНАЯ УЛ,ДОМ 1,СТРОЕНИЕ 9,'

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
        rrpv4 = self.base_part.find('ns:Document').find('ns:RepProducedProduct_v4')
        rrpv4.find(f'rpp:Content').append(self.__create_position(**position))

    def show(self):
        """ pretty print of current document state """
        # et.indent(self.base_part, space="\t", level=0)  # works on Python3.9 +
        self.logger.info(f'{et.tostring(self.base_part, encoding="utf-8").decode()}')
        # self.logger.info(et.indent(self.base_part, space="\t", level=0))

    def build(self):
        return self.base_part


def rpp4(uid: str, mark_list: List):
    rpp = RepProducedProductV4()

    rpp.set_header(uid)
    position = {
        "identity": "1",
        "mark_list": mark_list
    }
    rpp.set_org()
    rpp.add_position(**position)
    rpp.show()
    return rpp.build()


def marks(mark_type, product_code, number, ver, amount=1) -> list:
    """
    ([1-9]\d{2}|\d([1-9]\d|\d[1-9])){2}([1-9]\d{7}|\d([1-9]\d{6}|\d([1-9]\d{5}|\d([1-9]\d{4}|\d([1-9]\d{3}|\d([1-9]\d{2}|\d([1-9]\d|\d[1-9])))))))
    :param mark_type:
    :param product_code:
    :param number:
    :param ver:
    :param amount:
    :return:
    """
    if mark_type == '150':
        return [f'{product_code}' + xeger(r"\d{3}") + f'{number}' +
                xeger('(0[1-9]|1[0-2])(1[8-9]|[2-9][0-9])([1-9]\d{2}|\d([1-9]\d|\d[1-9]))[0-9A-Z]{100}[0-9A-Z]{29}').upper()
                for _ in range(amount)]
    elif mark_type == '68':
        return ['not ready for mark 68']
    elif mark_type == '31':
        return ['not ready for mark 31']
    else:
        raise ValueError(f'wrong mark type, available 150, 68, 31 | yours -> {mark_type}')


def wbgz(fsrarid, mark_list):
    document = et.Element('{http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01}Documents')
    header = et.SubElement(document, '{http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01}Header')
    doctype = et.SubElement(header, '{http://fsrar.ru/WEGAIS/goznak}DocType').text = 'WayBillGoznak'

    docid = et.SubElement(header, '{http://fsrar.ru/WEGAIS/goznak}DocId').text = dt.now().isoformat()[:-7]
    docdate = et.SubElement(header, '{http://fsrar.ru/WEGAIS/goznak}DocDate').text = dt.now().date().isoformat()
    dociid = et.SubElement(header, '{http://fsrar.ru/WEGAIS/goznak}doc_iid').text = '1'
    shipperid = et.SubElement(header, '{http://fsrar.ru/WEGAIS/goznak}shipperID').text = '020000004400'
    consigneeid = et.SubElement(header, '{http://fsrar.ru/WEGAIS/goznak}ConsigneeID').text = fsrarid

    content = et.SubElement(header, '{http://fsrar.ru/WEGAIS/goznak}Content')
    pos = et.SubElement(content, '{http://fsrar.ru/WEGAIS/goznak}Pos')
    docposid = et.SubElement(pos, '{http://fsrar.ru/WEGAIS/goznak}DocPosId').text = '1'
    form2 = et.SubElement(pos, '{http://fsrar.ru/WEGAIS/goznak}Form2').text = '1'
    bc = et.SubElement(pos, '{http://fsrar.ru/WEGAIS/goznak}bc')

    for mark in mark_list:
        ncode = et.SubElement(bc, '{http://fsrar.ru/WEGAIS/goznak}NCode').text = mark

    return document


def cheque(bc_list: list):
    rd = dt.now()
    hour = rr(0, 23)
    minute = rr(0, 59)

    datetime = f"{'0' + str(rd.day) if rd.day < 10 else rd.day}" \
               f"{'0' + str(rd.month) if rd.month < 10 else rd.month}" \
               f"{str(rd.year)[2:4]}" \
               f"{'0' + str(hour) if hour < 10 else hour}" \
               f"{'0' + str(minute) if minute < 10 else minute}"

    cq_data = {
        'inn': "7841051711",
        'kpp': "770101006",
        'address': "Россия,117105,Москва Г, Варшавское ш, д. 37 А, стр. 8",
        'name': "АКЦИОНЕРНОЕ ОБЩЕСТВО \"ЦЕНТРИНФОРМ\"",
        'kassa': str(rr(0, 999)),
        'number': str(rr(0, 999)),
        'shift': str(rr(0, 999)),
        'datetime': datetime
    }

    root = et.Element('Cheque')
    for k, v in cq_data.items():
        root.set(k, v)

    def price():
        return "-" + str(rr(100, 10000) / 100) if rr(0, 1) == 1 else str(rr(100, 10000) / 100)

    for bc in bc_list:
        bttl_data = {
            'price': price(),
            'barcode': bc,
            'volume': f"{rr(1000, 30000) / 10000}"
        }

        bottle = et.Element("Bottle")
        for k, v in bttl_data.items():
            bottle.set(k, v)

        root.append(bottle)

    return root


def chequev3():
    return "not done yet"

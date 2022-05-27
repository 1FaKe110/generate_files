import xml.etree.ElementTree as ET
from pprint import pprint
from datetime import datetime as dt
from rstr import xeger


def marks(mark_type, product_code, number, ver, amount=1) -> list:
    if mark_type == '150':
        return [{xeger(fr'{product_code}\d{{3}}{number}0\d[1-9]22{ver}[a-z0-9]{{100}}[a-z0-9]{{29}}'): 'false'} for _ in range(amount)]
    elif mark_type == '68':
        return ['not ready for mark 68']
    elif mark_type == '31':
        return ['not ready for mark 31']
    else:
        raise ValueError(f'wrong mark type, available 150, 68, 31 | yours -> {mark_type}')


def wbgz(fsrarid, mark_list):
    document = ET.Element('{http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01}Document')
    header = ET.SubElement(document, '{http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01}Header')
    doctype = ET.SubElement(header, '{http://fsrar.ru/WEGAIS/goznak}DocType').text = 'WayBillGoznak'

    docid = ET.SubElement(header, '{http://fsrar.ru/WEGAIS/goznak}DocId').text = dt.now().isoformat()
    docdate = ET.SubElement(header, '{http://fsrar.ru/WEGAIS/goznak}DocDate').text = dt.now().date().isoformat()
    dociid = ET.SubElement(header, '{http://fsrar.ru/WEGAIS/goznak}doc_iid').text = '1'
    shipperid = ET.SubElement(header, '{http://fsrar.ru/WEGAIS/goznak}shipperID').text = '020000004400'
    consigneeid = ET.SubElement(header, '{http://fsrar.ru/WEGAIS/goznak}ConsigneeID').text = fsrarid

    content = ET.SubElement(header, '{http://fsrar.ru/WEGAIS/goznak}Content')
    pos = ET.SubElement(content, '{http://fsrar.ru/WEGAIS/goznak}Pos')
    docposid = ET.SubElement(pos, '{http://fsrar.ru/WEGAIS/goznak}DocPosId').text = '1'
    form2 = ET.SubElement(pos, '{http://fsrar.ru/WEGAIS/goznak}Form2').text = '1'

    bc = ET.SubElement(pos, '{http://fsrar.ru/WEGAIS/goznak}bc')

    for mark in marks:
        ncode = ET.SubElement(bc, '{http://fsrar.ru/WEGAIS/goznak}NCode').text = mark

    return document

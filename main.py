import json
from time import sleep
from uuid import uuid4

import utm_sender
from base_logger import BaseLogger
from document_generator import DocumentGenerator
from utm_sender import UtmSender
from datetime import datetime as dt

dg = DocumentGenerator()
utm = UtmSender()
log = BaseLogger().get_logger('__main__')
last_mark_list = []


def mark_wbgz(marks: list = None, fsrar: str = '030000504835'):
    if marks is None:
        dg.set_document_type('marks')
        marks_ = dg.__gen__(mark_type='150', product_code='200', number='64856485', ver='001', amount=20)

    else:
        marks_ = marks

    dg.set_document_type('wbgz')
    wbgz = dg.__gen__(fsrarid=fsrar, mark_list=marks_)
    filename, filepath = dg.__save__(wbgz)
    dg.__ssh_send__(filename)


def cheques():
    cheq_names = []

    log.info('mark amount?')
    sleep(0.3)
    mark_amount = int(input('> '))

    dg.set_document_type('marks')
    marks = dg.__gen__(mark_type='150', product_code='200', number='64856485', ver='001', amount=mark_amount)
    log.info(json.dumps(marks, indent=2))

    mark_wbgz(marks)
    sleep(10)

    dg.set_document_type('rppv4')
    rpp_filename = str(uuid4())
    rpp = dg.__gen__(rpp_filename, marks)
    _, rpp_filepath = dg.__save__(rpp, filename=rpp_filename)
    log.info(f'RPP filename: {rpp_filename}')
    log.info(f'RPP path: {rpp_filepath}')
    utm.send(rpp_filepath, 'RepProducedProduct_v4')

    sleep(20)
    log.info(
        "\n\n1 mark = 1 cheque    -> y\n"
        "all marks = 1 cheque -> n")
    sleep(0.3)

    dg.set_document_type('cheque')
    if input("> ") == 'y':
        for i, mark in enumerate(marks, 1):
            cheque = dg.__gen__(bc_list=[mark])
            ce_filename, ce_filepath = dg.__save__(
                cheque, filename=f'{rpp_filename}_{i}'
            )
            log.info(f'Cheque filename: {ce_filename}')
            log.info(f'Cheque path: {ce_filepath}')
            utm.send(ce_filepath, 'Cheque')
            cheq_names.append(ce_filename)
    else:
        cheque = dg.__gen__(bc_list=marks)
        ce_filename, ce_filepath = dg.__save__(
            cheque, filename=f'{rpp_filename}_0'
        )
        utm.send(ce_filepath, 'Cheque')
        cheq_names.append(ce_filename)


def main():
    cheques()


if __name__ == '__main__':
    main()

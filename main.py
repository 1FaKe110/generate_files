import json
import DocumentGenerator as DG
from datetime import datetime as dt


def main():
    dg = DG.DocumentGenerator()
    dg.set_document_type('marks')
    marks = dg.__gen__(mark_type='150', product_code='200', number='64856485', ver='001', amount=20)
    js_marks = json.dumps(marks)

    if isinstance(js_marks, str):
        with open(f"./documents/{dg.get_document_type()}/{dt.now().isoformat()}.json", 'w', encoding='utf-8') as doc:
            doc.write(js_marks)

    dg.set_document_type('wbgz')
    wbgz = dg.__gen__(fsrarid='030000504835', mark_list=marks)
    dg.__save__(wbgz)


if __name__ == '__main__':
    main()

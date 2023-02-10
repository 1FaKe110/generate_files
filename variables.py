import generate
import send

generate_documents = {
    'wbgz': generate.wbgz,
    'marks': generate.marks,
    'cheque': generate.cheque,
    'rppv4': generate.rpp4,
    'chequev3': generate.chequev3,
}
send_documents = {
    'wbgz': send.wbgz
}

from os import system as term
from base_logger import BaseLogger

log = BaseLogger().get_logger('__SSH_SENDER__')


def wbgz(filename, username='gabko', machine='dockerHub'):
    cmd = f'curl -F file=@/home/ldapusers/{username}/documents2send/wbgz/{filename} 10.10.4.247:8002/wb'
    exe = f'ssh {username}@{machine} "{cmd}"'
    log.info(exe)
    return term(exe)

from ipaddress import ip_address
from hashlib import md5


def remote_addr(request):
    addr_keys = [
        'HTTP_X_FORWARDED_FOR',
        'REMOTE_ADDR',
    ]
    for key in addr_keys:
        addr = request.META.get(key, None)
        try:
            ia = ip_address(addr)
            return addr
        except ValueError:
            continue
    raise Exception('Could not acquire remote IP from request.')


def user_agent(request):
    agent_keys = [
        'HTTP_USER_AGENT',
    ]
    for key in agent_keys:
        agent = request.META.get(key, None)
        if agent: return agent
    raise Exception('Could not acquire user agent from request.')



def fingerprint(request=None, agent=None, addr=None, fp2=None):
    if not addr:
        addr = remote_addr(request)
    if not agent:
        agent = request.META.get('HTTP_USER_AGENT', '\\\\null')
    raw = f'{addr}@{agent}'
    return str(md5(raw.encode()).hexdigest())

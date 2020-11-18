from ipaddress import ip_address
from hashlib import md5
from django.contrib.sessions.models import Session
from ua_parser import user_agent_parser

@property
def sessions(self):
    from .models import LoggedInUser
    sessions = []
    logged_in = LoggedInUser.objects.filter(user=self)
    for li in logged_in:
        try:
            s = Session.objects.get(session_key=li.session_key)
            puaos = user_agent_parser.ParseOS(li.user_agent)
            puaoss = '.'.join([puaos[k] for k in puaos.keys() if puaos[k] is not None])

            puabr = user_agent_parser.ParseUserAgent(li.user_agent)
            puabrs = '.'.join([puabr[k] for k in puabr.keys() if puabr[k] is not None])

            puad = user_agent_parser.ParseDevice(li.user_agent)
            puads = ' '.join([puad[k] for k in puad.keys() if puad[k] is not None])

            sessions.append((s, ' '.join([puads, puaoss, puabrs])))
        except Session.DoesNotExist:
            li.delete()
    return sessions

@property
def is_shadow(self):
    try:
        is_shadow = self.shadow
        return self.shadow.active
    except:
        return False

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


@property
def agent(self):
    agent_keys = [
        'HTTP_USER_AGENT',
    ]
    for key in agent_keys:
        agent = request.META.get(key, None)
        if agent: return agent
    return None



def fingerprint(request=None, agent=None, addr=None, fp2=None):
    if not addr:
        addr = remote_addr(request)
    if not agent:
        agent = request.META.get('HTTP_USER_AGENT', '\\\\null')
    raw = f'{addr}@{agent}'
    return str(md5(raw.encode()).hexdigest())


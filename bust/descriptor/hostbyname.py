import socket


class HostByName(object):

    def __init__(self, domain):
        self.domain = domain
        self.ip = None

    def __get__(self):
        if self.ip:
            return self.ip

        try:
            self.ip = socket.gethostbyname(self.domain)
        except:
            pass

        return self.ip

    def __set__(self):
        raise AttributeError

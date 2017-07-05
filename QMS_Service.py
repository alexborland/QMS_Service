from requests import Session
from requests_ntlm import HttpNtlmAuth
from zeep import Client
from zeep.transports import Transport
import time

class QMS_Service(object):
    def __init__(self, server_name, username, password):
        self.key_exp = 0
        session = Session()
        session.auth = HttpNtlmAuth(
            username,
            password
        )
        self.c = Client(
            f"http://{server_name}:4799/QMS/Service",
            transport = Transport(session = session)
        )
        print(f"Connected to {server_name}")
        self.api = self.c.service
        self.refresh_key()
        self.services = self.api.GetServices(["All"])

    def refresh_key(self):
        if time.time() >= self.key_exp:
            self.key_exp = time.time()+60
            self.service_key = self.c.service.GetTimeLimitedServiceKey()
            print(f"Checked out service key: {self.service_key}")
            self.c.transport.session.headers.update(
                {"X-Service-Key": self.service_key}
            )

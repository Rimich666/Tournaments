import dataclasses
import requests
import logging
import re
from threading import Thread
from time import sleep
from config import Config

log = logging.getLogger("SMS")


@dataclasses.dataclass()
class TSMSResponse:
    id: str = "0"
    status: int = 0
    status_code: int = -1
    balance: float = 0


class SMSTransport:
    _URL = "https://sms.ru/sms/send"

    def __init__(self, api_id):
        self._api_id = api_id

    def send(self, to: str, msg: str) -> TSMSResponse:
        if not self.validate_phone(to):
            log.error("Invalid phone number")
            return TSMSResponse()

        response = requests.get(self._URL, params=dict(
            api_id=self._api_id,
            to=to,
            msg=msg,
            json=1
        )).json()

        log.debug("Response %s", response)

        if response["status"] == "OK":
            phone = response["sms"][to]

            if phone["status"] == "OK":
                return TSMSResponse(
                    status=1,
                    status_code=phone["status_code"],
                    balance=response['balance'],
                    id=phone["sms_id"]
                )

        log.debug("Error status %s", response)
        return TSMSResponse(
            status_code=response["status_code"]
        )

    @classmethod
    def validate_phone(cls, phone):
        return re.match(r"^7[0-9]{10}$", phone)


class ThreadSMS(Thread):
    def __init__(self, code):
        Thread.__init__(self)
        self.name = 'SMSTread'
        self.api_id = Config.API_ID
        self.phone = Config.PHONE
        self.code = code

    def run(self):
        sms = SMSTransport(self.api_id)
        for i in range(1):
            result = sms.send(Config.PHONE, self.code)
            if result.status_code == 100:
                break
            sleep(10)


def sendSMS(code):
    thread = ThreadSMS(code)
    thread.start()


if __name__ == '__main__':
    sendSMS('Код подтверждения: 123456')

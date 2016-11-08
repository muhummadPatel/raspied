import json


class ClientError(Exception):
    """
    Custom Exception class that allows you to send an error message over the
    specified channel.
    """
    def __init__(self, code):
        super(ClientError, self).__init__(code)
        self.code = code

    def send_to(self, channel):
        channel.send({
            'text': json.dumps({
                'error': self.code,
            }),
        })

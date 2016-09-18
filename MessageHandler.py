import re

class MessageHandler:

    communicator = None

    def __init__(self, communicator):
        self.communicator = communicator

    def pong_server(self):
        self.communicator.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))

    def test_message(self):
        self.communicator.chat("tested!")

    command_map = {
        '!test': test_message
    }

    def handle_response(self, response):
        username = None
        message = None

        print(response)
        username = self.parse_response(r"\w+", response)
        message = self.parse_response("(?<= :).+(?=\r\n)", response)

        command = self.command_map.get(message)
        if command is not None:
            command(self)

    # Parse a response, handling empties and returning none if no matches
    def parse_response(self, expression, response):
        parsed_response = re.search(expression, response)

        if parsed_response is not None:
            return parsed_response.group(0)
        return None

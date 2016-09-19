import re
import RoboGrimConfig
import Modules.Draft


class MessageHandler:

    communicator = None
    module_manager = None

    def __init__(self, communicator, module_manager):
        self.communicator = communicator
        self.module_manager = module_manager

    def test_message(self, arguments):
        self.communicator.chat("tested!")

    def start_draft(self, arguments):
        self.communicator.chat("Starting draft")
        self.module_manager.start_module(Modules.Draft.Draft(self.communicator, arguments))

    def stop_draft(self, arguments):
        print('killing draft')
        self.module_manager.stop_module()

    command_map = {
        '!test': test_message
    }

    mod_command_map = {

    }

    king_command_map = {
        '!startdraft': start_draft,
        '!stopdraft': stop_draft
    }

    def handle_response(self, response):

        username = self.parse_response(r"\w+", response)
        message = self.parse_response("(?<= :).+(?=\r\n)", response)
        command_text = self.parse_response("!\w+", message)
        arguments = []
        parsedMessage = re.findall("\w+", message)
        if len(parsedMessage) > 1:
            junk, *arguments = parsedMessage


        # figure out user authorization level
        is_mod = username in RoboGrimConfig.MODS
        is_king = username == RoboGrimConfig.ME

        # figure out which command to run
        command = None
        if is_king:
            command = self.king_command_map.get(command_text)
        if command is None and is_mod:
            command = self.mod_command_map.get(command_text)
        if command is None:
            command = self.command_map.get(command_text)

        # run the command
        if command is not None:
            command(self, arguments)

        # pass the input to the module maanger
        self.module_manager.input(username, message)


    # Parse a response, handling empties and returning none if no matches
    def parse_response(self, expression, response):
        parsed_response = re.search(expression, response)

        if parsed_response is not None:
            return parsed_response.group(0)
        return None

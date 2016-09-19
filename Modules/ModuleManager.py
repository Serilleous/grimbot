

class ModuleManager:
    active_module = None

    def start_module(self, new_module):
        self.active_module = new_module
        self.active_module.start()

    def start_module(self, new_module):
        self.active_module = new_module
        self.active_module.start()

    def stop_module(self):
        self.active_module = None

    def tick(self):
        if self.active_module is None:
            return

        status = self.active_module.tick()
        if not status:
            self.stop_module()

    def input(self, username, message):
        if self.active_module is not None:
            self.active_module.input(username, message)

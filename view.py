class View:
    def __init__(self):
        self.size = (0, 0)
        self.view_manager = None

    def set_size(self, size):
        self.size = size

    def set_view_manager(self, manager):
        self.view_manager = manager

    def handle_key(self, key_name):
        raise NotImplementedError

    def draw_frame(self, draw):
        raise NotImplementedError

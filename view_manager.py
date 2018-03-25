from PIL import Image
from PIL import ImageDraw

class ViewManager:
    def __init__(self, size, root_view, mode):
        self.size = size
        self.image = Image.new(mode, size)
        self.draw = ImageDraw.Draw(self.image)
        self.views = [root_view]

    def get_frame(self):
        width, height = self.size
        # wipe screen by drawing a black rectangle over it
        self.draw.rectangle((0,0,width,height), outline=0, fill=0)
        self.get_top_view().draw_frame(self.draw)
        return self.image

    def get_top_view(self):
        return self.views[len(self.views)-1]

    def handle_key(self, key_name):
        self.get_top_view().handle_key(key_name)

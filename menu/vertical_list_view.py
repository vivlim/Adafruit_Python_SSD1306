from PIL import ImageFont

class VerticalListView:
    def __init__(self, items, size):
        self.size = (size[0] - 3, size[1])
        self.selected_item = 0
        self.items_to_show_above_selected = 3

        self.font = ImageFont.load("tom-thumb.pil")
        self.font_bbox = self.font.getmask("FOO").getbbox()
        self.font_line_height = self.font_bbox[3] + 1
        self.lines_per_screen = self.size[1] / self.font_line_height
        self.selection_rect_size = (self.size[0], self.font_bbox[3])

        # if you passed in strings, wrap in dict
        if isinstance(items[0], str):
            self.items = [{'label': x} for x in items]
        else:
            self.items = items

    def get_visible_item_bounds(self):
        if len(self.items) > self.lines_per_screen:
            # top item to show on screen
            top_item_num = max(self.selected_item - self.items_to_show_above_selected, 0)
            bottom_item_num = int(min(len(self.items), top_item_num + self.lines_per_screen))
            top_item_num = int(min(top_item_num, bottom_item_num - self.lines_per_screen + 1))
            return top_item_num, bottom_item_num
        return 0, len(self.items)

    def handle_key(self, key_name):
        if key_name == 'up':
            self.selected_item = (self.selected_item - 1) % len(self.items)
        elif key_name == 'down':
            self.selected_item = (self.selected_item + 1) % len(self.items)

    def draw_frame(self, draw):
        screen_line = 0
        bounds = self.get_visible_item_bounds()
        for i in range(bounds[0], bounds[1]):
            item = self.items[i]
            if self.selected_item == i:
                selection_pos = (0, screen_line * self.font_line_height)
                selection_rect = selection_pos + tuple(map(sum, zip(selection_pos, self.selection_rect_size)))
                draw.rectangle(selection_rect, outline=255, fill=255)
                draw.text((0, screen_line * self.font_line_height), item['label'], font=self.font, fill=0)
            else:
                draw.text((0, screen_line * self.font_line_height), item['label'], font=self.font, fill=255)

            screen_line = screen_line + 1

        # scrollbar
        if len(self.items) > self.lines_per_screen:
            bar_percent = self.lines_per_screen / len(self.items)
        else:
            bar_percent = 1

        bar_x = self.size[0] + 2
        bar_pos = bounds[0] / len(self.items) * self.size[1]
        bar_height_pixels = bar_percent * self.size[1]
        draw.line((bar_x, bar_pos, bar_x, bar_height_pixels + bar_pos), fill=255)

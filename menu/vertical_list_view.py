from PIL import ImageFont

class VerticalListView:
    def __init__(self, items, size):
        self.left_margin = 4
        self.right_margin = 3
        self.size = (size[0] - self.right_margin, size[1])
        self.selected_item = 0
        self.items_to_show_above_selected = 3

        self.font = ImageFont.load("tom-thumb.pil")
        self.font_bbox = self.font.getmask("A").getbbox()
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
        elif key_name == 'a':
            item = self.items[self.selected_item]
            if 'action' in item:
                item['action']()

    def draw_frame(self, draw):
        screen_line = 0
        bounds = self.get_visible_item_bounds()
        for i in range(bounds[0], bounds[1]):
            item = self.items[i]
            if self.selected_item == i:
                selection_pos = (0, screen_line * self.font_line_height)
                selection_rect = selection_pos + tuple(map(sum, zip(selection_pos, self.selection_rect_size)))
                draw.rectangle(selection_rect, outline=255, fill=255)
                self.draw_item_label(draw, item, (self.left_margin, screen_line * self.font_line_height), 0)

                if 'action' in item:
                    self.draw_action_marker(draw, (0, screen_line * self.font_line_height), 0)
            else:
                self.draw_item_label(draw, item, (self.left_margin, screen_line * self.font_line_height), 255)
                if 'action' in item:
                    self.draw_action_marker(draw, (0, screen_line * self.font_line_height), 255)

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

    def draw_item_label(self, draw, item, pos, value):
        label = item['label']
        if 'cached_label' in item:
            label = item['cached_label']
        elif 'format_values' in item:
            values = item['format_values']()
            label = label.format(**values)
            item['cached_label'] = label
        draw.text(pos, label, font=self.font, fill=value)

    def draw_action_marker(self, draw, pos, value):
        x, y = pos
        # this is an arrow symbol
        symbol_points = [
            (x, y),
            (x+1, y+1),
            (x+2, y+2),
            (x+1, y+3),
            (x, y+4),
            (x, y+1),
            (x, y+2),
            (x, y+3),
            (x+1, y+2)
        ]
        for point in symbol_points:
            draw.point(point, value)

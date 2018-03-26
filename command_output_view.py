from vertical_list_view import VerticalListView

import subprocess
from threading import Thread
from queue import Queue, Empty

class CommandOutputView(VerticalListView):
    def __init__(self, command):
        super().__init__(["command: " + " ".join(command)])
        self.output_queue = Queue()
        self.proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.stdout_reader_thread = Thread(target=self.read_output, args=(self.proc.stdout, self.output_queue))
        self.stdout_reader_thread.daemon = True
        self.stdout_reader_thread.start()
        self.stderr_reader_thread = Thread(target=self.read_output, args=(self.proc.stderr, self.output_queue))
        self.stderr_reader_thread.daemon = True
        self.stderr_reader_thread.start()

    def read_output(self, stream, queue):
        for line in iter(stream.readline, b''):
            queue.put(line)
        stream.close()

    def draw_frame(self, draw):
        if self.selected_item == len(self.items) - 1:
            scroll_to_bottom = True
        else:
            scroll_to_bottom = False

        try:
            line = self.output_queue.get_nowait()
            new_item = {
                'label': line
            }
            self.items.append(new_item)
        except Empty:
            pass

        if scroll_to_bottom:
            self.selected_item = len(self.items) - 1

        super().draw_frame(draw)

    def handle_key(self, key_name):
        super().handle_key(key_name)
        if key_name == 'b':
            self.proc.kill()
            self.view_manager.remove_top_view()


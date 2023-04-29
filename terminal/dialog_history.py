from datetime import datetime

class DialogHistory:
    def __init__(self):
        self.dialog_history = []
        self.dialog_max_length = 5
        self.message_max_chars = 75

    def add_dialog(self, message):
        timestamp = datetime.now().strftime("%b %d | %I:%M:%S %p | ")
        if self.dialog_history and self.dialog_history[-1] == (timestamp, message):
            return

        self.dialog_history.append((timestamp, message))
        if len(self.dialog_history) > self.dialog_max_length:
            self.dialog_history.pop(0)

    def get_dialog(self, index):
        if index < len(self.dialog_history):
            return self.dialog_history[index]
        return ("", "")

    def clear_history(self):
        self.dialog_history = []
        
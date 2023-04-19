

class DialogHistory:
    def __init__(self):
        self.dialog_history = []
        self.dialog_max_length = 5

    def add_dialog(self, message):
        self.dialog_history.append(message)
        if len(self.dialog_history) > self.dialog_max_length:
            self.dialog_history.pop(0)

    def get_dialog(self, index):
        if index < len(self.dialog_history):
            return self.dialog_history[index]
        return ""

    def clear_history(self):
        self.dialog_history = []

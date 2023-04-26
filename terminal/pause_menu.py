import curses

class PauseMenu:
    def __init__(self, game_terminal):
        self.game_terminal = game_terminal
        self.dialog_history = game_terminal.dialog_history

    def pause(self):
        self.game_terminal.stdscr.clear()
        self.game_terminal.stdscr.refresh()

        self.show_dialog_history()
        self.draw_pause_menu_title()

        self.game_terminal.stdscr.nodelay(True)
        pause_menu_items = ['1. Continue', '2. Options', '3. Quit Game']
        selected_index = 0

        while True:
            key = self.game_terminal.prompt_and_draw_menu(pause_menu_items, selected_index)
            key_actions = self.get_pause_menu_key_actions(selected_index, pause_menu_items)

            if key in key_actions:
                action = key_actions[key]
                result = action()
                if result is not None:
                    selected_index = result
            elif key == ord('\n'):
                if selected_index == 0:
                    self.game_terminal.stdscr.clear()
                    self.game_terminal.stdscr.refresh()
                    break
                elif selected_index == 1:
                    self.show_options()
                elif selected_index == 2:
                    self.game_terminal.close_game_terminal()
                    sys.exit(0)
            elif key == 27:
                self.game_terminal.stdscr.clear()
                self.game_terminal.stdscr.refresh()
                break

        self.game_terminal.stdscr.nodelay(False)
        self.game_terminal.refresh()

    def draw_pause_menu_title(self):
        title = "Pause Menu"
        start_x = (self.game_terminal.WIDTH - len(title)) // 2
        self.game_terminal.stdscr.addstr(0, start_x, title, curses.A_BOLD)

    def get_pause_menu_key_actions(self, selected_index, menu_items):
        KEY_UP, KEY_DOWN, KEY_ENTER, KEY_ESCAPE, _ = self.game_terminal.get_key_variables()

        key_actions = {
            KEY_UP: lambda: (selected_index - 1) % len(menu_items),
            KEY_DOWN: lambda: (selected_index + 1) % len(menu_items),
            KEY_ENTER: lambda: None,
            KEY_ESCAPE: lambda: None,
        }

        return key_actions

    def draw_pause_menu(self, menu_items, selected_index=None):
        start_y = (self.game_terminal.HEIGHT - len(menu_items)) // 2
        start_x = (self.game_terminal.WIDTH - len(menu_items[0])) // 2
        for i, item in enumerate(menu_items):
            self.game_terminal.stdscr.move(start_y + i, start_x)
            self.game_terminal.stdscr.clrtoeol()
            if i == selected_index:
                self.game_terminal.stdscr.addstr(start_y + i, start_x, item.ljust(self.game_terminal.WIDTH), curses.A_REVERSE)
            else:
                self.game_terminal.stdscr.addstr(start_y + i, start_x, item.ljust(self.game_terminal.WIDTH))

    def show_dialog_history(self):
        self.game_terminal.clear_area(self.game_terminal.DIALOG_Y_START, self.game_terminal.DIALOG_Y_END)
        history_start_y = self.game_terminal.DIALOG_Y_START - len(self.dialog_history.dialog_history) - 1
        for i in range(len(self.dialog_history.dialog_history)):
            timestamp, message = self.dialog_history.get_dialog(i)
            self.game_terminal.draw(history_start_y + i, 0, f"{timestamp} {message}")
        self.game_terminal.stdscr.refresh()

    def show_options(self):
        self.game_terminal.clear_area(self.game_terminal.DIALOG_Y_START, self.game_terminal.DIALOG_Y_END)
        self.game_terminal.draw(self.game_terminal.DIALOG_Y_START, 0, "Options menu (to be implemented)")
        self.game_terminal.stdscr.refresh()
        self.game_terminal.stdscr.getch()

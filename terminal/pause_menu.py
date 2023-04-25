import curses
import sys

class PauseMenu:
    def __init__(self, game_terminal):
        self.game_terminal = game_terminal
        self.dialog_history = game_terminal.dialog_history

    def pause(self):
        self.game_terminal.stdscr.nodelay(True)
        pause_menu_items = ['Continue', 'Options', 'Quit Game']
        selected_index = 0

        self.show_dialog_history()

        while True:
            self.draw_pause_menu(pause_menu_items, selected_index)
            self.game_terminal.stdscr.refresh()

            key = self.game_terminal.stdscr.getch()
            if key == curses.KEY_UP:
                selected_index = (selected_index - 1) % len(pause_menu_items)
            elif key == curses.KEY_DOWN:
                selected_index = (selected_index + 1) % len(pause_menu_items)
            elif key == ord('\n'):
                if selected_index == 0:  # Continue
                    self.game_terminal.clear_area(5, self.game_terminal.MENU_Y_START - 1)
                    break
                elif selected_index == 1:  # Options
                    self.show_options()
                elif selected_index == 2:  # Quit Game
                    self.game_terminal.close_game_terminal()
                    sys.exit(0)
            elif key == 27:
                self.game_terminal.clear_area(5, self.game_terminal.MENU_Y_START - 1)
                break

        self.game_terminal.stdscr.nodelay(False)
        self.game_terminal.refresh()

    def draw_pause_menu(self, menu_items, selected_index=None):
        for i, item in enumerate(menu_items):
            self.game_terminal.stdscr.move(self.game_terminal.MENU_Y_START + i, 0)
            self.game_terminal.stdscr.clrtoeol()
            if i == selected_index:
                self.game_terminal.stdscr.addstr(self.game_terminal.MENU_Y_START + i, 0, item.ljust(self.game_terminal.WIDTH), curses.A_REVERSE)
            else:
                self.game_terminal.stdscr.addstr(self.game_terminal.MENU_Y_START + i, 0, item.ljust(self.game_terminal.WIDTH))

    def show_dialog_history(self):
        self.game_terminal.clear_area(self.game_terminal.DIALOG_Y_START, self.game_terminal.DIALOG_Y_END)
        for i in range(len(self.dialog_history.dialog_history)):
            self.game_terminal.draw(self.game_terminal.DIALOG_Y_START + i, 0, self.dialog_history.get_dialog(i))
        self.game_terminal.stdscr.refresh()

    def show_options(self):
        self.game_terminal.clear_area(self.game_terminal.DIALOG_Y_START, self.game_terminal.DIALOG_Y_END)
        self.game_terminal.draw(self.game_terminal.DIALOG_Y_START, 0, "Options menu (to be implemented)")
        self.game_terminal.stdscr.refresh()
        self.game_terminal.stdscr.getch()

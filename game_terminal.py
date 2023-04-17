import curses

class GameTerminal:
    WIDTH = 100
    HEIGHT = 30

    PLAYER_INFO_Y = 0
    COW_INFO_Y = 0
    COW_INFO_X = 50
    TITLE_Y = 2
    SEPARATOR_Y = 4
    ART_Y = 5
    DIALOG_Y = 20
    INSTRUCTIONS_Y = 21
    PROMPT_INPUT = 22
    MENU_Y = 23

    def __init__(self, title="Virtual Cow Tipper"):
        self.title = title
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.stdscr.resize(self.HEIGHT, self.WIDTH)
        self.show_art = False
        self.player_stats = ''
        self.player_weapon = ''
        self.player_shield = ''
        self.cow_stats = 'Diary of a Cow | Solid'

    def enable_mouse(self):
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

    def disable_mouse(self):
        curses.mousemask(0)

    def toggle_art_display(self):
        self.show_art = not self.show_art

    def set_player_stats(self, stats, weapon, shield):
        self.player_stats = stats
        self.player_weapon = weapon
        self.player_shield = shield

    def set_cow_stats(self, stats):
        self.cow_stats = stats

    def draw_separator(self):
        self.draw(self.SEPARATOR_Y, 0, "-" * self.WIDTH)

    def draw_game_title(self):
        x = (self.WIDTH - len(self.title)) // 2
        self.draw(self.TITLE_Y, x, self.title, curses.A_BOLD)

    def draw_player_stats(self):            
        self.draw(self.PLAYER_INFO_Y, 0, self.player_stats)
        self.draw(self.PLAYER_INFO_Y + 1, 0, self.player_weapon)
        self.draw(self.PLAYER_INFO_Y + 2, 0, self.player_shield)

    def draw_cow_stats(self):
        self.draw_from_right(self.COW_INFO_Y, self.cow_stats)

    def draw_menu(self, menu_items, selected_index=None):
        for i, item in enumerate(menu_items):
            if i == selected_index:
                self.stdscr.addstr(self.MENU_Y + i, 0, item.ljust(self.WIDTH), curses.A_REVERSE)
            else:
                self.stdscr.addstr(self.MENU_Y + i, 0, item.ljust(self.WIDTH))
            self.stdscr.clrtoeol()

    def draw_dialog(self, text):
        self.draw(self.DIALOG_Y, 0, text)

    def draw(self, y, x, text, custom_attr=0):
        self.stdscr.addstr(y, x, text, custom_attr)

    def draw_from_right(self, y, text):
        self.stdscr.addstr(y, self.WIDTH - len(text) - 3, text)

    def get_menu_choice(self, menu_items):
        selected_index = 0
        self.enable_mouse()
        while True:
            self.draw_menu(menu_items, selected_index)
            self.stdscr.refresh()

            # Wait for a mouse event or a key press
            event = self.stdscr.getch()
            if event == curses.KEY_MOUSE:
                _, x, y, _, _ = curses.getmouse()
                if y >= self.MENU_Y and y < self.MENU_Y + len(menu_items):
                    selected_index = y - self.MENU_Y
                    break

            elif event == curses.KEY_UP:
                selected_index = (selected_index - 1) % len(menu_items)
            elif event == curses.KEY_DOWN:
                selected_index = (selected_index + 1) % len(menu_items)
            elif event == ord('\n'):
                break

        self.disable_mouse()
        return selected_index + 1

    def refresh(self):
        if self.show_art:
            self.DIALOG_Y = 20
            self.INSTRUCTIONS_Y = 21
            self.PROMPT_INPUT = 22
            self.MENU_Y = 23
        else:
            self.DIALOG_Y = 5
            self.INSTRUCTIONS_Y = 6
            self.PROMPT_INPUT = 7
            self.MENU_Y = 8

        self.draw_game_title()
        self.draw_player_stats()
        self.draw_cow_stats()
        self.draw_separator()
        self.stdscr.refresh()

    def close_game_terminal(self):
        curses.echo()
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.endwin()

import curses


class COLORS:
    TITLE = {"back": curses.COLOR_WHITE, "front": curses.COLOR_MAGENTA}

    STATUS = {"back": curses.COLOR_CYAN, "front": curses.COLOR_BLACK}

    BASE_PASSES_TITLE = {"back": curses.COLOR_BLACK, "front": curses.COLOR_CYAN}

    CHANGING_PASS = {"back": curses.COLOR_BLACK, "front": curses.COLOR_CYAN}

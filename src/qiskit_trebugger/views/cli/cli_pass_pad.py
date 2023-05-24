import curses


class TranspilerPassPad:
    def __init__(self, step, height, width, pad_obj):
        self.transpiler_pass = step
        self.height = height
        self.width = width
        self.pad = pad_obj
        self._start_row = 0

    def _get_center(self, width, string_len, divisor=2):
        return max(0, int(width // divisor - string_len // 2 - string_len % 2))

    def _add_title(self):
        pass_name = f"{self.transpiler_pass.index}. {self.transpiler_pass.name}"[
            : self.width - 1
        ]
        title_offset = self._get_center(self.width, len(pass_name))
        self.pad.addstr(
            self._start_row,
            title_offset,
            pass_name,
            curses.A_BOLD | curses.color_pair(1),
        )
        self._start_row += 1
        self.pad.hline(self._start_row, 0, "_", self.width - 4)

    def _add_information(self):
        pass

    def _add_properties(self):
        pass

    def _add_documentation(self):
        pass

    def _add_circuit(self):
        pass

    def _add_logs(self):
        pass

    def _add_property_set(self):
        pass

    def build_pad(self):
        self._add_title()
        self._add_information()
        self._add_properties()
        self._add_documentation()
        self._add_circuit()
        self._add_logs()
        self._add_property_set()

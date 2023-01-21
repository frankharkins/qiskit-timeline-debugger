"""Implements the module for the transpilation sequence of a quantum circuit.
"""


class TranspilationSequence:
    """Class to implement the transpilation sequence."""

    def __init__(self, on_step_callback) -> None:
        self._original_circuit = None
        self._general_info = {}

        self.on_step_callback = on_step_callback
        self.steps = []
        self._collected_logs = {}

    @property
    def original_circuit(self):
        """Returns the original circuit object"""
        return self._original_circuit

    @original_circuit.setter
    def original_circuit(self, circuit):
        self._original_circuit = circuit

    @property
    def general_info(self):
        """Returns the general_info dictionary"""
        return self._general_info

    @general_info.setter
    def general_info(self, info):
        self._general_info = info

    def add_step(self, step):
        """Adds a transpilation step to the sequence

        Args:
            step (TranspilationStep): a transpilation step
        """
        if step.name in self._collected_logs:
            step.logs = self._collected_logs[step.name]
            self._collected_logs.pop(step.name, None)

        step.index = len(self.steps)
        self.steps.append(step)

        # property set index:
        idx = step.index
        while len(self.steps[idx].property_set) == 0:
            idx = idx - 1
            if idx < 0:
                idx = 0
                break
        self.steps[-1].property_set_index = idx

        # Notify:
        self.on_step_callback(self.steps[-1])

    def add_log_entry(self, pass_name, log_entry):
        """Adds log entry to the transpilation pass

        Args:
            pass_name (str): name of the pass
            log_entry (LogEntry): Log entry to be appended
        """
        if not pass_name in self._collected_logs:
            self._collected_logs[pass_name] = []

        self._collected_logs[pass_name].append(log_entry)

"""
Implements the main Debugger class.
Raises:
    DebuggerError: if multiple quantum circuits supplied for debugging
"""
from typing import Optional, Union
import logging
import warnings
from IPython.display import display


from qiskit import QuantumCircuit, transpile, Aer, __qiskit_version__
from qiskit.providers.backend import Backend, BackendV1, BackendV2
from qiskit.transpiler.basepasses import AnalysisPass, TransformationPass


from qiskit_trebugger.model import TranspilerLoggingHandler
from qiskit_trebugger.model import TranspilerDataCollector
from qiskit_trebugger.model import TranspilationSequence
from qiskit_trebugger.views.widget.timeline_view import TimelineView
from .debugger_error import DebuggerError


class Debugger:
    """Main debugger class for thr qiskit timeline debugger.

    Raises:
        DebuggerError: if multiple quantum circuits are supplied
    """

    @classmethod
    def debug(
        cls,
        circuit: QuantumCircuit,
        backend: Optional[Union[Backend, BackendV1, BackendV2]] = None,
        optimization_level: Optional[int] = 0,
        show: Optional[bool] = True,
        **kwargs,
    ):
        """Calls the transpile method of qiskit with the given parameters
           and populates the view of the widget with circuit diagram and
           statistics.

        Args:
            circuit (QuantumCircuit): quantum circuit to debug
            backend (Optional[Union[Backend, BackendV1, BackendV2]], optional):
                                        Quantum Backend for execution. Defaults to None.
            optimization_level (Optional[int], optional):
                                        Optimization level of transpiler. Defaults to 0.

        Raises:
            DebuggerError: if multiple quantum circuits are supplied
        """

        if not isinstance(circuit, QuantumCircuit):
            raise DebuggerError(
                "Debugger currently supports single QuantumCircuit only!"
            )
        if backend is None:
            backend = Aer.get_backend("qasm_simulator")

        # Create the view:
        cls.view = TimelineView()

        def on_step_callback(step):
            cls.view.add_step(step)

        # Prepare the model:
        transpilation_sequence = TranspilationSequence(on_step_callback)

        if isinstance(backend, BackendV2):
            backend_name = backend.name
        else:
            backend_name = backend.name()

        warnings.simplefilter("ignore")
        transpilation_sequence.general_info = {
            "Backend": backend_name,
            "optimization_level": optimization_level,
            "Qiskit version": __qiskit_version__["qiskit"],
            "Terra version": __qiskit_version__["qiskit-terra"],
        }

        transpilation_sequence.original_circuit = circuit

        warnings.simplefilter("default")

        Debugger.register_logging_handler(transpilation_sequence)
        transpiler_callback = Debugger._get_data_collector(transpilation_sequence)

        # Pass the model to the view:
        cls.view.transpilation_sequence = transpilation_sequence
        cls.view.update_params(**kwargs)

        if show:
            display(cls.view)

        transpile(
            circuit,
            backend,
            optimization_level=optimization_level,
            callback=transpiler_callback,
            **kwargs,
        )

        cls.view.update_summary()
        cls.view.add_class("done")

    @classmethod
    def register_logging_handler(cls, transpilation_sequence):
        """Registers logging handlers of different transpiler passes.

        Args:
            transpilation_sequence (TranspilationSequence):
                                data structure to store the transpiler
                                passes as a sequence of transplation
                                steps
        """

        # TODO: Do not depend on loggerDict
        all_loggers = logging.Logger.manager.loggerDict
        passes_loggers = {
            key: value
            for (key, value) in all_loggers.items()
            if key.startswith("qiskit.transpiler.passes.")
        }

        loggers_map = {}
        for _pass in AnalysisPass.__subclasses__():
            if _pass.__module__ in passes_loggers.keys():
                loggers_map[_pass.__module__] = _pass.__name__

        for _pass in TransformationPass.__subclasses__():
            if _pass.__module__ in passes_loggers.keys():
                loggers_map[_pass.__module__] = _pass.__name__

        handler = TranspilerLoggingHandler(
            transpilation_sequence=transpilation_sequence, loggers_map=loggers_map
        )
        logger = logging.getLogger("qiskit.transpiler.passes")
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    @classmethod
    def _get_data_collector(cls, transpilation_sequence):
        return TranspilerDataCollector(transpilation_sequence).transpiler_callback

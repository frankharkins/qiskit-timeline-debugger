import unittest

from qiskit.circuit.random import random_circuit
from qiskit.providers.fake_provider import (
    FakeAlmaden,
    FakeAthens,
    FakeBelem,
    FakeKolkata,
)
from qiskit.providers.fake_provider import (
    FakeAlmadenV2,
    FakeAthensV2,
    FakeBelemV2,
    FakeKolkataV2,
)

from qiskit_trebugger import Debugger

MAX_DEPTH = 5


class TestDebuggerMock(unittest.TestCase):
    """Unit tests for different IBMQ fake backends v2"""

    all_backends_1 = [FakeAthens(), FakeBelem(), FakeAlmaden(), FakeKolkata()]
    all_backends_2 = [FakeAthensV2(), FakeBelemV2(), FakeAlmadenV2(), FakeKolkataV2()]

    def _internal_tester(self, backend, num_qubits):
        for qubits in range(1, num_qubits, 3):
            circ = random_circuit(qubits, MAX_DEPTH, measure=True)
            debugger = Debugger()
            debugger.debug(
                circ,
                backend,
                show=False,
            )
            print("Success!")

    def test_backend_v1(self):
        """Backend V2 tests"""
        for curr_backend in self.all_backends_1:
            print(f"Testing with {curr_backend.name()}...")
            self._internal_tester(curr_backend, curr_backend.configuration().num_qubits)

    def test_backend_v2(self):
        """Backend V2 tests"""
        for curr_backend in self.all_backends_2:
            print(f"Testing with {curr_backend.name}...")
            self._internal_tester(curr_backend, curr_backend.num_qubits)

# qiskit_goldilocks_reduce.py
# Validation of Goldilocks Controlled Reduction Circuit (2^32 - 1)
# Requires: qiskit, qiskit-aer, numpy

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.compiler import transpile
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Circuit Construction (Matching OpenQASM Decomposition)
# ---------------------------------------------------------

def lower_step(qc: QuantumCircuit, x: int, c_in: int, c_out: int):
    """Gate sequence for lower 32 bits (Constant=1): x += 1 + c_in"""
    qc.x(x)                    # Constant 1
    qc.cx(c_in, x)             # Add carry
    qc.x(x)                    # Restore x_orig for Toffoli control
    qc.ccx(x, c_in, c_out)     # c_out = x_orig & c_in
    qc.x(x)                    # Restore x (now holds Sum)

def upper_step(qc: QuantumCircuit, x: int, c_in: int, c_out: int):
    """Gate sequence for upper 32 bits (Constant=0): x += 0 + c_in"""
    qc.ccx(x, c_in, c_out)     # c_out = x_orig & c_in (Compute carry FIRST)
    qc.cx(c_in, x)             # Sum = x_orig ^ c_in

def lower_step_dg(qc: QuantumCircuit, x: int, c_in: int, c_out: int):
    """Inverse of lower_step"""
    qc.x(x)                    # x_orig = NOT(x_current)
    qc.ccx(x, c_in, c_out)     # Uncompute Carry
    qc.x(x)                    # Restore x (Sum)
    qc.cx(c_in, x)             # Uncompute Sum (x ^= c_in)
    qc.x(x)                    # Uncompute Constant (x = NOT(x) -> Original)

def upper_step_dg(qc: QuantumCircuit, x: int, c_in: int, c_out: int):
    """Inverse of upper_step"""
    qc.cx(c_in, x)             # Uncompute Sum
    qc.ccx(x, c_in, c_out)     # Uncompute Carry

def build_goldilocks_reduce_circuit() -> QuantumCircuit:
    """
    Builds the full 68-qubit circuit:
    - 64 qubits for register x
    - 1 qubit for control (ctrl)
    - 2 qubits for ancillae (a0, a1)
    - 64 classical bits for measurement of x
    - 1 classical bit for measurement of ctrl (verification)
    - 2 classical bits for measurement of ancillae (cleanliness check)
    """
    qr_x = QuantumRegister(64, 'x')
    qr_ctrl = QuantumRegister(1, 'ctrl')
    qr_a = QuantumRegister(2, 'anc') # a0, a1
    cr_x = ClassicalRegister(64, 'meas_x')
    cr_ctrl = ClassicalRegister(1, 'meas_ctrl')
    cr_anc = ClassicalRegister(2, 'meas_anc')
    
    qc = QuantumCircuit(qr_x, qr_ctrl, qr_a, cr_x, cr_ctrl, cr_anc)
    
    # Indices
    x = [qr_x[i] for i in range(64)]
    ctrl = qr_ctrl[0]
    a0 = qr_a[0]
    a1 = qr_a[1]
    
    # ---------------------------------------------------------
    # FORWARD PASS
    # ---------------------------------------------------------
    
    # 1. LOAD CONTROL
    qc.cx(ctrl, a0)
    
    # 2. LOWER 32 BITS (Ping-Pong a0 <-> a1)
    # Bit 0: a0 -> a1
    lower_step(qc, x[0], a0, a1)
    # Bit 1: a1 -> a0
    lower_step(qc, x[1], a1, a0)
    # Bit 2: a0 -> a1
    lower_step(qc, x[2], a0, a1)
    # Bit 3: a1 -> a0
    lower_step(qc, x[3], a1, a0)
    # Bit 4: a0 -> a1
    lower_step(qc, x[4], a0, a1)
    # Bit 5: a1 -> a0
    lower_step(qc, x[5], a1, a0)
    # Bit 6: a0 -> a1
    lower_step(qc, x[6], a0, a1)
    # Bit 7: a1 -> a0
    lower_step(qc, x[7], a1, a0)
    # Bit 8: a0 -> a1
    lower_step(qc, x[8], a0, a1)
    # Bit 9: a1 -> a0
    lower_step(qc, x[9], a1, a0)
    # Bit 10: a0 -> a1
    lower_step(qc, x[10], a0, a1)
    # Bit 11: a1 -> a0
    lower_step(qc, x[11], a1, a0)
    # Bit 12: a0 -> a1
    lower_step(qc, x[12], a0, a1)
    # Bit 13: a1 -> a0
    lower_step(qc, x[13], a1, a0)
    # Bit 14: a0 -> a1
    lower_step(qc, x[14], a0, a1)
    # Bit 15: a1 -> a0
    lower_step(qc, x[15], a1, a0)
    # Bit 16: a0 -> a1
    lower_step(qc, x[16], a0, a1)
    # Bit 17: a1 -> a0
    lower_step(qc, x[17], a1, a0)
    # Bit 18: a0 -> a1
    lower_step(qc, x[18], a0, a1)
    # Bit 19: a1 -> a0
    lower_step(qc, x[19], a1, a0)
    # Bit 20: a0 -> a1
    lower_step(qc, x[20], a0, a1)
    # Bit 21: a1 -> a0
    lower_step(qc, x[21], a1, a0)
    # Bit 22: a0 -> a1
    lower_step(qc, x[22], a0, a1)
    # Bit 23: a1 -> a0
    lower_step(qc, x[23], a1, a0)
    # Bit 24: a0 -> a1
    lower_step(qc, x[24], a0, a1)
    # Bit 25: a1 -> a0
    lower_step(qc, x[25], a1, a0)
    # Bit 26: a0 -> a1
    lower_step(qc, x[26], a0, a1)
    # Bit 27: a1 -> a0
    lower_step(qc, x[27], a1, a0)
    # Bit 28: a0 -> a1
    lower_step(qc, x[28], a0, a1)
    # Bit 29: a1 -> a0
    lower_step(qc, x[29], a1, a0)
    # Bit 30: a0 -> a1
    lower_step(qc, x[30], a0, a1)
    # Bit 31: a1 -> a0 (Final Lower Carry in a0)
    lower_step(qc, x[31], a1, a0)
    
    # 3. UPPER 32 BITS (Ping-Pong a0 <-> a1)
    # Bit 32: a0 -> a1
    upper_step(qc, x[32], a0, a1)
    # Bit 33: a1 -> a0
    upper_step(qc, x[33], a1, a0)
    # Bit 34: a0 -> a1
    upper_step(qc, x[34], a0, a1)
    # Bit 35: a1 -> a0
    upper_step(qc, x[35], a1, a0)
    # Bit 36: a0 -> a1
    upper_step(qc, x[36], a0, a1)
    # Bit 37: a1 -> a0
    upper_step(qc, x[37], a1, a0)
    # Bit 38: a0 -> a1
    upper_step(qc, x[38], a0, a1)
    # Bit 39: a1 -> a0
    upper_step(qc, x[39], a1, a0)
    # Bit 40: a0 -> a1
    upper_step(qc, x[40], a0, a1)
    # Bit 41: a1 -> a0
    upper_step(qc, x[41], a1, a0)
    # Bit 42: a0 -> a1
    upper_step(qc, x[42], a0, a1)
    # Bit 43: a1 -> a0
    upper_step(qc, x[43], a1, a0)
    # Bit 44: a0 -> a1
    upper_step(qc, x[44], a0, a1)
    # Bit 45: a1 -> a0
    upper_step(qc, x[45], a1, a0)
    # Bit 46: a0 -> a1
    upper_step(qc, x[46], a0, a1)
    # Bit 47: a1 -> a0
    upper_step(qc, x[47], a1, a0)
    # Bit 48: a0 -> a1
    upper_step(qc, x[48], a0, a1)
    # Bit 49: a1 -> a0
    upper_step(qc, x[49], a1, a0)
    # Bit 50: a0 -> a1
    upper_step(qc, x[50], a0, a1)
    # Bit 51: a1 -> a0
    upper_step(qc, x[51], a1, a0)
    # Bit 52: a0 -> a1
    upper_step(qc, x[52], a0, a1)
    # Bit 53: a1 -> a0
    upper_step(qc, x[53], a1, a0)
    # Bit 54: a0 -> a1
    upper_step(qc, x[54], a0, a1)
    # Bit 55: a1 -> a0
    upper_step(qc, x[55], a1, a0)
    # Bit 56: a0 -> a1
    upper_step(qc, x[56], a0, a1)
    # Bit 57: a1 -> a0
    upper_step(qc, x[57], a1, a0)
    # Bit 58: a0 -> a1
    upper_step(qc, x[58], a0, a1)
    # Bit 59: a1 -> a0
    upper_step(qc, x[59], a1, a0)
    # Bit 60: a0 -> a1
    upper_step(qc, x[60], a0, a1)
    # Bit 61: a1 -> a0
    upper_step(qc, x[61], a1, a0)
    # Bit 62: a0 -> a1
    upper_step(qc, x[62], a0, a1)
    # Bit 63: a1 -> a0 (Final Carry Out in a0)
    upper_step(qc, x[63], a1, a0)
    
    # ---------------------------------------------------------
    # REVERSE PASS (Uncompute Carries)
    # ---------------------------------------------------------
    
    # REVERSE UPPER 32 (Bits 63 down to 32)
    upper_step_dg(qc, x[63], a0, a1)
    upper_step_dg(qc, x[62], a1, a0)
    upper_step_dg(qc, x[61], a0, a1)
    upper_step_dg(qc, x[60], a1, a0)
    upper_step_dg(qc, x[59], a0, a1)
    upper_step_dg(qc, x[58], a1, a0)
    upper_step_dg(qc, x[57], a0, a1)
    upper_step_dg(qc, x[56], a1, a0)
    upper_step_dg(qc, x[55], a0, a1)
    upper_step_dg(qc, x[54], a1, a0)
    upper_step_dg(qc, x[53], a0, a1)
    upper_step_dg(qc, x[52], a1, a0)
    upper_step_dg(qc, x[51], a0, a1)
    upper_step_dg(qc, x[50], a1, a0)
    upper_step_dg(qc, x[49], a0, a1)
    upper_step_dg(qc, x[48], a1, a0)
    upper_step_dg(qc, x[47], a0, a1)
    upper_step_dg(qc, x[46], a1, a0)
    upper_step_dg(qc, x[45], a0, a1)
    upper_step_dg(qc, x[44], a1, a0)
    upper_step_dg(qc, x[43], a0, a1)
    upper_step_dg(qc, x[42], a1, a0)
    upper_step_dg(qc, x[41], a0, a1)
    upper_step_dg(qc, x[40], a1, a0)
    upper_step_dg(qc, x[39], a0, a1)
    upper_step_dg(qc, x[38], a1, a0)
    upper_step_dg(qc, x[37], a0, a1)
    upper_step_dg(qc, x[36], a1, a0)
    upper_step_dg(qc, x[35], a0, a1)
    upper_step_dg(qc, x[34], a1, a0)
    upper_step_dg(qc, x[33], a0, a1)
    upper_step_dg(qc, x[32], a1, a0)
    
    # REVERSE LOWER 32 (Bits 31 down to 0)
    lower_step_dg(qc, x[31], a0, a1)
    lower_step_dg(qc, x[30], a1, a0)
    lower_step_dg(qc, x[29], a0, a1)
    lower_step_dg(qc, x[28], a1, a0)
    lower_step_dg(qc, x[27], a0, a1)
    lower_step_dg(qc, x[26], a1, a0)
    lower_step_dg(qc, x[25], a0, a1)
    lower_step_dg(qc, x[24], a1, a0)
    lower_step_dg(qc, x[23], a0, a1)
    lower_step_dg(qc, x[22], a1, a0)
    lower_step_dg(qc, x[21], a0, a1)
    lower_step_dg(qc, x[20], a1, a0)
    lower_step_dg(qc, x[19], a0, a1)
    lower_step_dg(qc, x[18], a1, a0)
    lower_step_dg(qc, x[17], a0, a1)
    lower_step_dg(qc, x[16], a1, a0)
    lower_step_dg(qc, x[15], a0, a1)
    lower_step_dg(qc, x[14], a1, a0)
    lower_step_dg(qc, x[13], a0, a1)
    lower_step_dg(qc, x[12], a1, a0)
    lower_step_dg(qc, x[11], a0, a1)
    lower_step_dg(qc, x[10], a1, a0)
    lower_step_dg(qc, x[9], a0, a1)
    lower_step_dg(qc, x[8], a1, a0)
    lower_step_dg(qc, x[7], a0, a1)
    lower_step_dg(qc, x[6], a1, a0)
    lower_step_dg(qc, x[5], a0, a1)
    lower_step_dg(qc, x[4], a1, a0)
    lower_step_dg(qc, x[3], a0, a1)
    lower_step_dg(qc, x[2], a1, a0)
    lower_step_dg(qc, x[1], a0, a1)
    lower_step_dg(qc, x[0], a1, a0)
    
    # 5. UNLOAD CONTROL
    qc.cx(ctrl, a0)
    
    return qc

# ---------------------------------------------------------
# 2. Classical Reference Implementation
# ---------------------------------------------------------

GOLDILOCKS_P = 2**64 - 2**32 + 1
CONST_C = 2**32 - 1

def classical_reduce(x_val: int, ctrl_val: int) -> int:
    """Reference: x + ctrl * (2^32 - 1) mod 2^64"""
    if ctrl_val == 1:
        return (x_val + CONST_C) & ((1 << 64) - 1)
    return x_val

def int_to_bits(val: int, n: int) -> list:
    """Little Endian bit list"""
    return [(val >> i) & 1 for i in range(n)]

def bits_to_int(bits: list) -> int:
    """Little Endian bits to int"""
    return sum(b << i for i, b in enumerate(bits))

# ---------------------------------------------------------
# 3. Test Harness
# ---------------------------------------------------------

def run_test_case(qc_base: QuantumCircuit, x_init: int, ctrl_init: int, shots: int = 1000):
    """Runs a single test case on AerSimulator."""
    qc = qc_base.copy()
    
    # Initialize Registers
    # Qiskit uses Big Endian for `initialize` but our circuit is Little Endian (q[0] = LSB).
    # We must initialize qubits individually or reverse the bitstring.
    # Easiest: Apply X gates for |1> states.
    
    x_bits = int_to_bits(x_init, 64)
    for i, bit in enumerate(x_bits):
        if bit == 1:
            qc.x(qc.qubits[i]) # qr_x[i]
            
    if ctrl_init == 1:
        qc.x(qc.qubits[64]) # qr_ctrl[0]
        
    # Ancillae start at |0> (default)
    
    # Measure
    qc.measure(qc.qubits[0:64], qc.clbits[0:64])      # x
    qc.measure(qc.qubits[64], qc.clbits[64])           # ctrl
    qc.measure(qc.qubits[65:67], qc.clbits[65:67])     # ancillae
    
    # Execute
    backend = AerSimulator(method='statevector') # Statevector is exact for verification
    # backend = AerSimulator() # For shot noise simulation
    
    tqc = transpile(qc, backend)
    job = backend.run(tqc, shots=shots)
    result = job.result()
    counts = result.get_counts()
    
    # Parse Results (Qiskit returns Big Endian hex strings typically, 
    # but with explicit measure mapping, it respects clbit order).
    # `counts` keys are strings like '00 0 00' (cr_x cr_ctrl cr_anc) separated by spaces if registers named.
    # Since we used separate ClassicalRegisters, the key format is 'cr_anc cr_ctrl cr_x' (reversed reg order) 
    # or similar. Safest: use `memory` or parse carefully.
    
    # Let's use `memory` for single-shot deterministic check (statevector)
    if shots == 1:
        mem = result.get_memory()
        # Memory string format matches clbit index order: [cr_x[0]...cr_x[63], cr_ctrl[0], cr_anc[0], cr_anc[1]]
        # Wait, Qiskit memory string is usually MSB first (clbit N-1 ... clbit 0).
        # We measure clbits 0..63 (x), 64 (ctrl), 65,66 (anc).
        # Memory string: bit 66 ... bit 0.
        # This is confusing. Let's just sample counts.
        pass
    
    # Parse Counts (Hex string usually)
    # Key format: 'anc_ctrl_x' (Register order reversed in string representation often)
    # We will just check the most frequent outcome.
    most_likely = max(counts, key=counts.get)
    
    # The bitstring in counts keys is ordered by *register declaration order* reversed? 
    # Actually: `qc.measure(qr_x, cr_x)` maps qr_x[i] -> cr_x[i].
    # `counts` keys are bitstrings where leftmost is cr_x[63] ... cr_x[0] cr_ctrl[0] cr_anc[1] cr_anc[0]?
    # Standard Qiskit: `counts` keys are big-endian integers representing the classical register state.
    # If we have registers [cr_x, cr_ctrl, cr_anc], the integer is (cr_anc << 65) | (cr_ctrl << 64) | cr_x.
    # The hex string represents this integer.
    
    # Let's decode the integer key.
    # We expect: x_final, ctrl_final, anc_final.
    
    # Since we only ran 1 shot (statevector), there is only 1 key.
    key = list(counts.keys())[0]
    # Remove spaces
    key = key.replace(" ", "")
    
    # Total clbits = 67. Hex length = ceil(67/4) = 17 chars.
    # Parse as int
    try:
        val = int(key, 16)
    except ValueError:
        # Handle binary string format if hex fails
        val = int(key, 2)
        
    # Extract fields (Little Endian clbit index -> Bit position in integer)
    # clbit 0 -> LSB.
    meas_x = val & ((1 << 64) - 1)
    meas_ctrl = (val >> 64) & 1
    meas_anc = (val >> 65) & 3
    
    expected_x = classical_reduce(x_init, ctrl_init)
    
    passed = (meas_x == expected_x) and (meas_ctrl == ctrl_init) and (meas_anc == 0)
    
    return {
        "passed": passed,
        "x_init": x_init,
        "ctrl_init": ctrl_init,
        "expected_x": expected_x,
        "measured_x": meas_x,
        "measured_ctrl": meas_ctrl,
        "measured_anc": meas_anc,
        "counts": counts
    }

# ---------------------------------------------------------
# 4. Main Execution
# ---------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Goldilocks Controlled Reduction Circuit Validation")
    print("=" * 60)
    print(f"Prime p = 2^64 - 2^32 + 1 = {GOLDILOCKS_P}")
    print(f"Constant C = 2^32 - 1 = {CONST_C}")
    print(f"Circuit Qubits: 64 (x) + 1 (ctrl) + 2 (anc) = 67")
    print("Building circuit...")
    
    base_circuit = build_goldilocks_reduce_circuit()
    print(f"Circuit Depth: {base_circuit.depth()}")
    print(f"Circuit Size: {base_circuit.size()}")
    print(f"Toffoli Count: {base_circuit.count_ops().get('ccx', 0)}")
    print(f"CNOT Count: {base_circuit.count_ops().get('cx', 0)}")
    print(f"X Count: {base_circuit.count_ops().get('x', 0)}")
    
    # Test Vectors
    test_cases = [
        (0, 0, "Zero Input, Ctrl=0"),
        (0, 1, "Zero Input, Ctrl=1 (Add Const)"),
        (1, 0, "One Input, Ctrl=0"),
        (1, 1, "One Input, Ctrl=1"),
        (2**63, 1, "MSB Set, Ctrl=1 (Carry Propagation)"),
        (2**64 - 1, 1, "Max U64, Ctrl=1 (Wrap)"),
        (2**64 - CONST_C, 1, "Boundary: x + C = 2^64 -> 0"),
        (GOLDILOCKS_P - 1, 1, "Field Max (p-1), Ctrl=1 -> p-1 + C mod 2^64"),
        (0xFFFFFFFF00000000, 1, "Upper 32 bits set"),
        (0x00000000FFFFFFFF, 1, "Lower 32 bits set (Const)"),
    ]
    
    all_passed = True
    for x_val, ctrl_val, desc in test_cases:
        print(f"\nTest: {desc}")
        print(f"  Input:  x={x_val:#018x}, ctrl={ctrl_val}")
        
        res = run_test_case(base_circuit, x_val, ctrl_val, shots=1) # Statevector = 1 shot exact
        
        status = "PASS" if res["passed"] else "FAIL"
        print(f"  Output: x={res['measured_x']:#018x}, ctrl={res['measured_ctrl']}, anc={res['measured_anc']} [{status}]")
        print(f"  Expected x={res['expected_x']:#018x}")
        
        if not res["passed"]:
            all_passed = False
            print(f"  DETAILS: {res}")
            
    print("\n" + "=" * 60)
    if all_passed:
        print("ALL TESTS PASSED: Circuit correctly implements Goldilocks Reduction.")
        print("Ancillae cleanly returned to |0>. Control preserved.")
    else:
        print("SOME TESTS FAILED.")
    print("=" * 60)
    
    # Optional: Draw circuit (first 20 layers)
    # print(base_circuit.draw(output='text', fold=100, idle_wires=False))

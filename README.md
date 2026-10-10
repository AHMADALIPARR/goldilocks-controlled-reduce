# Goldilocks Field Reduction: Controlled Add Constant

OpenQASM 3.0 implementation of the controlled addition of the constant `(2^32 - 1)` for Goldilocks field reduction.

## Operation

```
|x⟩ |c⟩ → |x + c ⋅ (2^{32} - 1) mod 2^{64}⟩ |c⟩
```

When `c = 1` (typically from a 2^64 overflow), this performs the reduction step modulo the Goldilocks prime `p = 2^{64} - 2^{32} + 1`.

## Resources

| Resource | Count |
|----------|-------|
| Qubits (Total) | 68 (64 data + 1 control + 2 ancilla) |
| Toffoli (CCX) | 128 |
| CNOT (CX) | 128 |
| X Gates | 192 (Clifford) |
| Circuit Depth (Toffoli layers) | 128 (sequential ripple-carry) |
| Ancillae | 2 clean qubits (`a0`, `a1`) |

## Design Notes

- Uses a **ping-pong carry** scheme with two ancillae to avoid a full-width carry register.
- Lower 32 bits add the constant `1` (via X) plus carry; upper 32 bits add only the carry.
- Forward pass computes the sum; reverse pass uncomputes the carries so ancillae return to `|0⟩`.
- Compatible with IBM OpenQASM 3.0, Qiskit, and Amazon Braket.

## Verification Checklist

1. **Ancilla cleanliness**: `a0` and `a1` return to `|0⟩` (final `ctrl cnot a0` + ping-pong symmetry).
2. **Functionality**: Implements the controlled modular add of `2^{32}-1`.
3. **Goldilocks correctness**: Adding `2^{32}-1` when the high bit overflows implements reduction modulo `p = 2^{64} - 2^{32} + 1`.

## Files

- `circuits/goldilocks_controlled_reduce.qasm` — Full explicit unrolled OpenQASM 3.0 circuit.
- `python/qiskit_validate.py` — Optional Qiskit circuit builder / AerSimulator validation stub.

## Citation / Provenance

SnapKitty Research Lab — Ahmad Ali Parr.

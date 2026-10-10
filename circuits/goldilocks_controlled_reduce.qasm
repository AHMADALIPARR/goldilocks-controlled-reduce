// OpenQASM 3.0
// Goldilocks Field Reduction: Controlled Add Constant (2^32 - 1)
// Implements: |x> -> |x + (2^32 - 1) * c> mod 2^64
// Uses 2 Ancillae (Ping-Pong Carry), 128 Toffoli, 128 CNOT, 192 X
// Compatible with: IBM OpenQASM 3.0, Qiskit, Braket

include "stdgates.inc";

// ---------------------------------------------------------
// HELPER GATES FOR PING-PONG CARRY CHAIN
// ---------------------------------------------------------

// Lower Bit Step (k=1): Input carry in 'c_in', Output carry in 'c_out'
// Modifies x[i]
gate lower_step qubit x, qubit c_in, qubit c_out {
    x x; // Constant 1
    c_in cnot x; // Add carry
    x x; // Restore x_orig for Toffoli control
    x, c_in ccx c_out; // c_out = x_orig & c_in
    x x; // Restore x (now holds Sum)
    // c_out now holds next carry. Caller must swap roles.
}

// Upper Bit Step (k=0): Input carry in 'c_in', Output carry in 'c_out'
// Modifies x[i]
gate upper_step qubit x, qubit c_in, qubit c_out {
    x, c_in ccx c_out; // c_out = x_orig & c_in (Compute carry FIRST)
    c_in cnot x; // Sum = x_orig ^ c_in
    // c_out now holds next carry.
}

// Inverse Lower Step (Uncompute)
gate lower_step_dg qubit x, qubit c_in, qubit c_out {
    // Reverse of lower_step:
    // 1. Uncompute Carry: Toffoli(x_orig, c_in, c_out)
    x x; // x_orig = NOT(x_current)
    x, c_in ccx c_out; // c_out ^= x_orig & c_in (Clears c_out)
    x x; // Restore x (Sum)
    // 2. Uncompute Sum: CNOT(c_in, x) then X(x)
    c_in cnot x; // x ^= c_in
    x x; // x = NOT(x) -> Original x
}

// Inverse Upper Step (Uncompute)
gate upper_step_dg qubit x, qubit c_in, qubit c_out {
    // Reverse of upper_step:
    c_in cnot x; // Uncompute Sum
    x, c_in ccx c_out; // Uncompute Carry
}

// ---------------------------------------------------------
// MAIN MODULE (Explicit Unrolled Ping-Pong)
// ---------------------------------------------------------
module goldilocks_controlled_reduce_explicit(qubit[64] x, qubit ctrl, qubit a0, qubit a1) {
    // a0 = carry_in (init), a1 = carry_out (temp)
    // Ping-Pong: Even steps write to a1, Odd steps write to a0.
    
    // 1. LOAD
    ctrl cnot a0;

    // 2. FORWARD LOWER 32 (Bits 0-31)
    // Bit 0: a0 -> a1
    lower_step x[0], a0, a1;
    // Bit 1: a1 -> a0
    lower_step x[1], a1, a0;
    // Bit 2: a0 -> a1
    lower_step x[2], a0, a1;
    // Bit 3: a1 -> a0
    lower_step x[3], a1, a0;
    // Bit 4: a0 -> a1
    lower_step x[4], a0, a1;
    // Bit 5: a1 -> a0
    lower_step x[5], a1, a0;
    // Bit 6: a0 -> a1
    lower_step x[6], a0, a1;
    // Bit 7: a1 -> a0
    lower_step x[7], a1, a0;
    // Bit 8: a0 -> a1
    lower_step x[8], a0, a1;
    // Bit 9: a1 -> a0
    lower_step x[9], a1, a0;
    // Bit 10: a0 -> a1
    lower_step x[10], a0, a1;
    // Bit 11: a1 -> a0
    lower_step x[11], a1, a0;
    // Bit 12: a0 -> a1
    lower_step x[12], a0, a1;
    // Bit 13: a1 -> a0
    lower_step x[13], a1, a0;
    // Bit 14: a0 -> a1
    lower_step x[14], a0, a1;
    // Bit 15: a1 -> a0
    lower_step x[15], a1, a0;
    // Bit 16: a0 -> a1
    lower_step x[16], a0, a1;
    // Bit 17: a1 -> a0
    lower_step x[17], a1, a0;
    // Bit 18: a0 -> a1
    lower_step x[18], a0, a1;
    // Bit 19: a1 -> a0
    lower_step x[19], a1, a0;
    // Bit 20: a0 -> a1
    lower_step x[20], a0, a1;
    // Bit 21: a1 -> a0
    lower_step x[21], a1, a0;
    // Bit 22: a0 -> a1
    lower_step x[22], a0, a1;
    // Bit 23: a1 -> a0
    lower_step x[23], a1, a0;
    // Bit 24: a0 -> a1
    lower_step x[24], a0, a1;
    // Bit 25: a1 -> a0
    lower_step x[25], a1, a0;
    // Bit 26: a0 -> a1
    lower_step x[26], a0, a1;
    // Bit 27: a1 -> a0
    lower_step x[27], a1, a0;
    // Bit 28: a0 -> a1
    lower_step x[28], a0, a1;
    // Bit 29: a1 -> a0
    lower_step x[29], a1, a0;
    // Bit 30: a0 -> a1
    lower_step x[30], a0, a1;
    // Bit 31: a1 -> a0 (Final carry of lower 32 lands in a0)
    lower_step x[31], a1, a0;

    // 3. FORWARD UPPER 32 (Bits 32-63)
    // Bit 32: a0 -> a1
    upper_step x[32], a0, a1;
    // Bit 33: a1 -> a0
    upper_step x[33], a1, a0;
    // Bit 34: a0 -> a1
    upper_step x[34], a0, a1;
    // Bit 35: a1 -> a0
    upper_step x[35], a1, a0;
    // Bit 36: a0 -> a1
    upper_step x[36], a0, a1;
    // Bit 37: a1 -> a0
    upper_step x[37], a1, a0;
    // Bit 38: a0 -> a1
    upper_step x[38], a0, a1;
    // Bit 39: a1 -> a0
    upper_step x[39], a1, a0;
    // Bit 40: a0 -> a1
    upper_step x[40], a0, a1;
    // Bit 41: a1 -> a0
    upper_step x[41], a1, a0;
    // Bit 42: a0 -> a1
    upper_step x[42], a0, a1;
    // Bit 43: a1 -> a0
    upper_step x[43], a1, a0;
    // Bit 44: a0 -> a1
    upper_step x[44], a0, a1;
    // Bit 45: a1 -> a0
    upper_step x[45], a1, a0;
    // Bit 46: a0 -> a1
    upper_step x[46], a0, a1;
    // Bit 47: a1 -> a0
    upper_step x[47], a1, a0;
    // Bit 48: a0 -> a1
    upper_step x[48], a0, a1;
    // Bit 49: a1 -> a0
    upper_step x[49], a1, a0;
    // Bit 50: a0 -> a1
    upper_step x[50], a0, a1;
    // Bit 51: a1 -> a0
    upper_step x[51], a1, a0;
    // Bit 52: a0 -> a1
    upper_step x[52], a0, a1;
    // Bit 53: a1 -> a0
    upper_step x[53], a1, a0;
    // Bit 54: a0 -> a1
    upper_step x[54], a0, a1;
    // Bit 55: a1 -> a0
    upper_step x[55], a1, a0;
    // Bit 56: a0 -> a1
    upper_step x[56], a0, a1;
    // Bit 57: a1 -> a0
    upper_step x[57], a1, a0;
    // Bit 58: a0 -> a1
    upper_step x[58], a0, a1;
    // Bit 59: a1 -> a0
    upper_step x[59], a1, a0;
    // Bit 60: a0 -> a1
    upper_step x[60], a0, a1;
    // Bit 61: a1 -> a0
    upper_step x[61], a1, a0;
    // Bit 62: a0 -> a1
    upper_step x[62], a0, a1;
    // Bit 63: a1 -> a0 (Final Carry Out lands in a0)
    upper_step x[63], a1, a0;

    // ---------------------------------------------------------
    // 4. REVERSE PASS (Uncompute Carries)
    // Final carry is in a0. We must return a0 to |ctrl> state.
    // We reverse the ping-pong order.
    // ---------------------------------------------------------

    // REVERSE UPPER 32 (Bits 63 down to 32)
    // Bit 63: a0 <- a1 (Inverse uses a0 as c_in, a1 as c_out)
    upper_step_dg x[63], a0, a1;
    // Bit 62: a1 <- a0
    upper_step_dg x[62], a1, a0;
    // Bit 61: a0 <- a1
    upper_step_dg x[61], a0, a1;
    // Bit 60: a1 <- a0
    upper_step_dg x[60], a1, a0;
    // Bit 59: a0 <- a1
    upper_step_dg x[59], a0, a1;
    // Bit 58: a1 <- a0
    upper_step_dg x[58], a1, a0;
    // Bit 57: a0 <- a1
    upper_step_dg x[57], a0, a1;
    // Bit 56: a1 <- a0
    upper_step_dg x[56], a1, a0;
    // Bit 55: a0 <- a1
    upper_step_dg x[55], a0, a1;
    // Bit 54: a1 <- a0
    upper_step_dg x[54], a1, a0;
    // Bit 53: a0 <- a1
    upper_step_dg x[53], a0, a1;
    // Bit 52: a1 <- a0
    upper_step_dg x[52], a1, a0;
    // Bit 51: a0 <- a1
    upper_step_dg x[51], a0, a1;
    // Bit 50: a1 <- a0
    upper_step_dg x[50], a1, a0;
    // Bit 49: a0 <- a1
    upper_step_dg x[49], a0, a1;
    // Bit 48: a1 <- a0
    upper_step_dg x[48], a1, a0;
    // Bit 47: a0 <- a1
    upper_step_dg x[47], a0, a1;
    // Bit 46: a1 <- a0
    upper_step_dg x[46], a1, a0;
    // Bit 45: a0 <- a1
    upper_step_dg x[45], a0, a1;
    // Bit 44: a1 <- a0
    upper_step_dg x[44], a1, a0;
    // Bit 43: a0 <- a1
    upper_step_dg x[43], a0, a1;
    // Bit 42: a1 <- a0
    upper_step_dg x[42], a1, a0;
    // Bit 41: a0 <- a1
    upper_step_dg x[41], a0, a1;
    // Bit 40: a1 <- a0
    upper_step_dg x[40], a1, a0;
    // Bit 39: a0 <- a1
    upper_step_dg x[39], a0, a1;
    // Bit 38: a1 <- a0
    upper_step_dg x[38], a1, a0;
    // Bit 37: a0 <- a1
    upper_step_dg x[37], a0, a1;
    // Bit 36: a1 <- a0
    upper_step_dg x[36], a1, a0;
    // Bit 35: a0 <- a1
    upper_step_dg x[35], a0, a1;
    // Bit 34: a1 <- a0
    upper_step_dg x[34], a1, a0;
    // Bit 33: a0 <- a1
    upper_step_dg x[33], a0, a1;
    // Bit 32: a1 <- a0
    upper_step_dg x[32], a1, a0;

    // REVERSE LOWER 32 (Bits 31 down to 0)
    // Bit 31: a0 <- a1
    lower_step_dg x[31], a0, a1;
    // Bit 30: a1 <- a0
    lower_step_dg x[30], a1, a0;
    // Bit 29: a0 <- a1
    lower_step_dg x[29], a0, a1;
    // Bit 28: a1 <- a0
    lower_step_dg x[28], a1, a0;
    // Bit 27: a0 <- a1
    lower_step_dg x[27], a0, a1;
    // Bit 26: a1 <- a0
    lower_step_dg x[26], a1, a0;
    // Bit 25: a0 <- a1
    lower_step_dg x[25], a0, a1;
    // Bit 24: a1 <- a0
    lower_step_dg x[24], a1, a0;
    // Bit 23: a0 <- a1
    lower_step_dg x[23], a0, a1;
    // Bit 22: a1 <- a0
    lower_step_dg x[22], a1, a0;
    // Bit 21: a0 <- a1
    lower_step_dg x[21], a0, a1;
    // Bit 20: a1 <- a0
    lower_step_dg x[20], a1, a0;
    // Bit 19: a0 <- a1
    lower_step_dg x[19], a0, a1;
    // Bit 18: a1 <- a0
    lower_step_dg x[18], a1, a0;
    // Bit 17: a0 <- a1
    lower_step_dg x[17], a0, a1;
    // Bit 16: a1 <- a0
    lower_step_dg x[16], a1, a0;
    // Bit 15: a0 <- a1
    lower_step_dg x[15], a0, a1;
    // Bit 14: a1 <- a0
    lower_step_dg x[14], a1, a0;
    // Bit 13: a0 <- a1
    lower_step_dg x[13], a0, a1;
    // Bit 12: a1 <- a0
    lower_step_dg x[12], a1, a0;
    // Bit 11: a0 <- a1
    lower_step_dg x[11], a0, a1;
    // Bit 10: a1 <- a0
    lower_step_dg x[10], a1, a0;
    // Bit 9: a0 <- a1
    lower_step_dg x[9], a0, a1;
    // Bit 8: a1 <- a0
    lower_step_dg x[8], a1, a0;
    // Bit 7: a0 <- a1
    lower_step_dg x[7], a0, a1;
    // Bit 6: a1 <- a0
    lower_step_dg x[6], a1, a0;
    // Bit 5: a0 <- a1
    lower_step_dg x[5], a0, a1;
    // Bit 4: a1 <- a0
    lower_step_dg x[4], a1, a0;
    // Bit 3: a0 <- a1
    lower_step_dg x[3], a0, a1;
    // Bit 2: a1 <- a0
    lower_step_dg x[2], a1, a0;
    // Bit 1: a0 <- a1
    lower_step_dg x[1], a0, a1;
    // Bit 0: a1 <- a0
    lower_step_dg x[0], a1, a0;

    // 5. UNLOAD CONTROL
    // a0 now holds the original ctrl value.
    ctrl cnot a0; // a0 = a0 ^ ctrl = 0
}

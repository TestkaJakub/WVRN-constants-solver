ACCUMULATOR_MAX = 256
ADDI_MIN = -8
ADDI_MAX = 7

def declaration(fsm):
    for constant in range(ACCUMULATOR_MAX):
        fsm.add_state(str(constant))

    for constant in range(ACCUMULATOR_MAX):
        for addi in range(ADDI_MIN, ADDI_MAX + 1):
            target = (constant + addi) % ACCUMULATOR_MAX
            fsm.add_transition(str(constant), f"addi {addi}", str(target))

        target = (constant * 2) % ACCUMULATOR_MAX
        fsm.add_transition(str(constant), "add acc", str(target))

        flipped = ~constant & 0xFF  # Flip bits and ensure 8-bit range
        fsm.add_transition(str(constant), "nand acc", str(flipped))

    fsm.set_initial_state("0")
    
    return fsm
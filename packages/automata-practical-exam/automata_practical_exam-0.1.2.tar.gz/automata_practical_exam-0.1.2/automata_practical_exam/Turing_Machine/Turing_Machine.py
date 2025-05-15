# Function to validate if the input is a binary string
def is_binary(s):
    for bit in s:
        if bit not in {"0", "1"}:
            return False
    return True


# Simulate a Turing Machine that accepts binary strings divisible by 3
def turing_machine_binary_numbers_divBy_3(s):
    if not is_binary(s):
        return "Rejected"

    # Add two blank symbols at both ends
    tape = ['B', 'B'] + list(s) + ['B', 'B']
    head = 2  
    state = "q0"

    print("\n--- Turing Machine Trace ---")
    while head < len(tape) - 2:  
        bit = tape[head]

        # Show tape, head, state
        print(f"Tape: {''.join(tape)}")
        print(f"Head: {' ' * head + '^'}")
        print(f"State: {state}, Read: '{bit}', Move: R")

        # Write X or Y if it's 0 or 1
        if bit == "0":
            tape[head] = "X"
        elif bit == "1":
            tape[head] = "Y"

        # State transitions
        if state == "q0":
            if bit == "0":
                state = "q0"
            elif bit == "1":
                state = "q1"
        elif state == "q1":
            if bit == "0":
                state = "q2"
            elif bit == "1":
                state = "q0"
        elif state == "q2":
            if bit == "0":
                state = "q1"
            elif bit == "1":
                state = "q2"

        head += 1  

    print(f"Final Tape: {''.join(tape)}")
    print(f"Final State: {state}")
    print("--- End of Trace ---\n")

    return "Accepted" if state == "q0" else "Rejected"

def main():
    s = input("Enter a binary string: ").strip()
    result = turing_machine_binary_numbers_divBy_3(s)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
# Function to validate if the input is a binary string
def is_binary(s):
    for bit in s:
        if bit not in {"0", "1"}:
            return False
    return True


# Function to simulate the Turing Machine
def turing_machine_binary_numbers_divBy_3(s):
    # Handle non-binary input
    if not is_binary(s):
        return "Rejected"

    state = "q0"
    
    for bit in s:
        if(state == "q0"):
            if(bit == "0"): state = "q0"
            else: state = "q1"
        elif (state == "q1"):
            if(bit == "0"): state = "q2"
            else: state = "q0"
        else:
            if(bit == "0"): state = "q1"
            else: state = "q2"
    
    # Accept if final state is q0 (remainder 0) Or Empty String represent 0 and it divisable by 3 
    if state == "q0" or s == "c":
        return "Accepted"
    else:
        return "Rejected"

def main():
    s = input("Enter a binary string: ").strip()
    print(turing_machine_binary_numbers_divBy_3(s))

if __name__ == "__main__":
    main()

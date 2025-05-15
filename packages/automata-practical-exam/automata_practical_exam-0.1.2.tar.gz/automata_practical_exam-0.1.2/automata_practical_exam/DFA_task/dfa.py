# Function to validate if the input is a binary string
def is_binary(s):
    for bit in s:
        if bit not in {"0", "1"}:
            return False
    return True

# Function to simulate the DFA for all binary string where the substring "101" appear at least once.
def accepts_all_strings_substring_101(s):

    # Handle non-binary input and empty string
    if not is_binary(s) or s == "":
        return "Rejected"
        
    state = "q0"
    for bit in s:
        pre_state = state
        if state=="q0":
            if bit=="1":state="q1"
        elif state=='q1':
            if bit=="0":state="q2"
        elif state=="q2":
            if bit =="0":state="q0"
            else: state ="q3" 
        else: state="q3"
        print(pre_state + " --- "+ bit +" ---> "+state)

    if state == "q3":
        return "Accepted" 
    else: return "Rejected"


def main():
    s = input("Enter a binary string: ").strip()
    print(accepts_all_strings_substring_101(s))

if __name__ == "__main__":
    main()
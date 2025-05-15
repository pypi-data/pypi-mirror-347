def accepts_binary_string(s: str) -> bool:

    state = 0
    for char in s:
        if char not in ('0', '1'):
            raise ValueError(f"Invalid character '{char}' in input string")
        if char == '1':
            state = (state + 1) % 3
            
    return state == 0

print(accepts_binary_string("1101"))  # True
print(accepts_binary_string("101"))   

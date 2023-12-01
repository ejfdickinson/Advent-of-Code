###

# Horrible solution, first day back!

###

from string import digits

SPELLED_DIGITS = ["one","two","three","four","five","six","seven","eight","nine"]
MAP_SPELLED_DIGITS = { name: value for name, value in zip(SPELLED_DIGITS,range(1,10)) }

def find_first_digit(s, check_for_spelled_digits=True):
    for i in range(len(s)):
        if s[i] in digits:
            return int(s[i])
        
        if check_for_spelled_digits:
            for k in MAP_SPELLED_DIGITS:
                if s[i:].startswith(k):
                    return MAP_SPELLED_DIGITS[k]

def find_last_digit(s, check_for_spelled_digits=True):
    n_chars = len(s)

    for i in reversed(range(len(s))):
        if s[i] in digits:
            return int(s[i])
        
        if check_for_spelled_digits:
            for k in MAP_SPELLED_DIGITS:
                if s[:(i+1)].endswith(k):
                    return MAP_SPELLED_DIGITS[k]

def get_calibration_value(s, check_for_spelled_digits=True):
    first_digit = find_first_digit(s, check_for_spelled_digits=check_for_spelled_digits)
    last_digit  = find_last_digit (s, check_for_spelled_digits=check_for_spelled_digits)
    
    return (10*first_digit + last_digit)

def run(data):
    calibration_values_raw = [
        get_calibration_value(line, check_for_spelled_digits=False)
        for line in data.splitlines()
    ]
    calibration_values_spelled = [
        get_calibration_value(line, check_for_spelled_digits=True)
        for line in data.splitlines()
    ]
    
    return (sum(calibration_values_raw), sum(calibration_values_spelled))

# Running script
fp = "2023/inputs/day1"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)

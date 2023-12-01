from string import digits

def get_first_digit(s):
    chars = [*s]
    for char in chars:
        if char in digits:
            return int(char)

def get_calibration_value(s):
    first_digit = get_first_digit(s)
    last_digit  = get_first_digit(reversed(s))
    
    return (10*first_digit + last_digit)    

def run(data):
    calibration_values = [get_calibration_value(line) for line in data.splitlines()]
    return sum(calibration_values)

fp = "2023/inputs/day1"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)

import math
import unittest
import sys

class Tests(unittest.TestCase):
    def test_calc_fuel(self):
        cases = [(12, 2), (14, 2), (1969, 654), (100756, 33583)]
        for mass, expected_fuel in cases:
            self.assertEqual(expected_fuel, calc_fuel(mass))

    def test_calc_fuel2(self):
        cases = [(12, 2), (14, 2), (1969, 966), (100756, 50346)]
        for mass, expected_fuel in cases:
            self.assertEqual(expected_fuel, calc_fuel2(mass))


def calc_fuel(mass: int):
    return (mass // 3) -2

def calc_fuel2(mass: int):
    fuel = 0
    while True:
        fuel_mass = calc_fuel(mass)
        if fuel_mass < 1:
            break

        fuel += fuel_mass
        mass = fuel_mass

    return fuel

if __name__ == '__main__':
    function_to_call = sys.argv[1] if len(sys.argv) > 1 else "1"

    total_fuel = 0
    with open("input.txt") as inf:
        for line in inf:
            stripped_line = line.strip()
            if len(stripped_line) > 0:
                mass = int(stripped_line)
                if function_to_call == "2":
                    total_fuel += calc_fuel2(mass)
                else:
                    total_fuel += calc_fuel(mass)
    print(total_fuel)
import unittest
import sys


class Tests(unittest.TestCase):
    def test_prog_1(self):
        self.assertEqual([2,0,0,0,99], execute([1,0,0,0,99]))

    def test_prog_2(self):
        self.assertEqual([2,3,0,6,99], execute([2,3,0,3,99]))

    def test_prog_3(self):
        self.assertEqual([2,4,4,5,99,9801], execute([2,4,4,5,99,0]))

    def test_prog_4(self):
        self.assertEqual([30,1,1,4,2,5,6,0,99], execute([1,1,1,4,99,5,6,0,99]))

    def test_line_to_state(self):
        self.assertEqual([1, 2, 3], line_to_state("1,2,3"))


def execute(state):
    program_counter = 0

    while True:
        if state[program_counter] == 99:
            return state

        read_loc_1 = state[program_counter + 1]
        read_loc_2 = state[program_counter + 2]
        write_loc = state[program_counter + 3]

        if state[program_counter] == 1:
            state[write_loc] = state[read_loc_1] + state[read_loc_2]
        elif state[program_counter] == 2:
            state[write_loc] = state[read_loc_1] * state[read_loc_2]

        program_counter += 4


def line_to_state(line: str):
    return [int(s.strip()) for s in line.split(",")]


def read_initial_state():
    with open("input.txt", "r") as inf:
        return line_to_state(inf.read())


if __name__ == '__main__':
    state = read_initial_state()
    state[1] = 12
    state[2] = 2
    print(execute(state))

from contextlib import redirect_stdout
from io import StringIO
import unittest
import sys


class Tests(unittest.TestCase):
    def test_prog_1(self):
        state, _ = execute([1,0,0,0,99])
        self.assertEqual([2,0,0,0,99], state)

    def test_prog_2(self):
        state, _ = execute([2,3,0,3,99])
        self.assertEqual([2,3,0,6,99], state)

    def test_prog_3(self):
        state, _ = execute([2,4,4,5,99,0])
        self.assertEqual([2,4,4,5,99,9801], state)

    def test_prog_4(self):
        state, _ = execute([1,1,1,4,99,5,6,0,99])
        self.assertEqual([30,1,1,4,2,5,6,0,99], state)

    def test_line_to_state(self):
        self.assertEqual([1, 2, 3], line_to_state("1,2,3"))

    def test_input(self):
        state, _ = execute([3,3,99,0], [7])
        self.assertEqual([3,3,99,7], state)

    def test_output(self):
        state, outputs = execute([4,3,99,7])
        self.assertEqual([4,3,99,7], state)
        self.assertEqual([7], outputs)

    def test_input_output(self):
        state, outputs = execute([3,0,4,0,99], [7])
        self.assertEqual([7,0,4,0,99], state)
        self.assertEqual([7], outputs)

    def test_decode(self):
        self.assertEqual([2, 0, 1, 0], decode_instruction(1002))
        self.assertEqual([2, 0, 0, 0], decode_instruction(2))
        self.assertEqual([1, 1, 1, 0], decode_instruction(1101))
        self.assertEqual([99], decode_instruction(99))
        self.assertEqual([3, 0], decode_instruction(3))
        self.assertEqual([3, 1], decode_instruction(103))
        self.assertEqual([4, 1], decode_instruction(104))

    def test_immediate_mode(self):
        state, _ = execute([1002,4,3,4,33])
        self.assertEqual([1002,4,3,4,99], state)

    def test_immediate_mode_2(self):
        state, _ = execute([1101, 100, -1, 4, 0])
        self.assertEqual([1101, 100, -1, 4, 99], state)


def decode_instruction(instruction):
    param_counts = {
        99: 0,
        1: 3,
        2: 3,
        3: 1,
        4: 1
    }
    params, opcode = divmod(instruction, 100)
    result = [opcode]
    while params:
        params, param = divmod(params, 10)
        result.append(param)

    return result + ([0] * (1 + param_counts[opcode] - len(result)))


def fetch_param(state, param_mode, param):
    if param_mode == 0:
        return state[state[param]]
    else:
        return state[param]


def execute(state, inputs=[]):
    program_counter = 0
    outputs = []

    while True:
        instruction_decoded = decode_instruction(state[program_counter])
        opcode = instruction_decoded[0]
        param_modes = instruction_decoded[1:]

        if opcode == 99:
            return state, outputs

        if opcode == 1: # ADD
            param_1 = fetch_param(state, param_modes[0], program_counter + 1)
            param_2 = fetch_param(state, param_modes[1], program_counter + 2)
            write_loc = state[program_counter + 3]
            state[write_loc] = param_1 + param_2
            program_counter += 4
        elif opcode == 2: # MULTIPLY
            param_1 = fetch_param(state, param_modes[0], program_counter + 1)
            param_2 = fetch_param(state, param_modes[1], program_counter + 2)
            write_loc = state[program_counter + 3]
            state[write_loc] = param_1 * param_2
            program_counter += 4
        elif opcode == 3: # INPUT
            write_loc = state[program_counter + 1]
            state[write_loc] = inputs.pop(0)
            program_counter += 2
        elif opcode == 4: # OUTPUT
            param = fetch_param(state, param_modes[0], program_counter + 1)
            outputs.append(param)
            program_counter += 2


def line_to_state(line: str):
    return [int(s.strip()) for s in line.split(",")]


def read_initial_state():
    with open("input.txt", "r") as inf:
        return line_to_state(inf.read())


if __name__ == '__main__':
    state = read_initial_state()
    final_state, outputs = execute(state, [1])
    print(outputs)

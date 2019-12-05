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

    def test_example_jump_1(self):
        _, outputs = execute([3,9,8,9,10,9,4,9,99,-1,8], [7])
        self.assertEqual(outputs, [0])

        _, outputs = execute([3,9,8,9,10,9,4,9,99,-1,8], [8])
        self.assertEqual(outputs, [1])

    def test_example_jump_2(self):
        _, outputs = execute([3,9,7,9,10,9,4,9,99,-1,8], [9])
        self.assertEqual(outputs, [0])

        _, outputs = execute([3,9,7,9,10,9,4,9,99,-1,8], [7])
        self.assertEqual(outputs, [1])

    def test_example_jump_3(self):
        _, outputs = execute([3,3,1108,-1,8,3,4,3,99], [7])
        self.assertEqual(outputs, [0])

        _, outputs = execute([3,3,1108,-1,8,3,4,3,99], [8])
        self.assertEqual(outputs, [1])

    def test_example_jump_4(self):
        _, outputs = execute([3,3,1107,-1,8,3,4,3,99], [9])
        self.assertEqual(outputs, [0])

        _, outputs = execute([3,3,1107,-1,8,3,4,3,99], [7])
        self.assertEqual(outputs, [1])

    def test_example_jump_5(self):
        _, outputs = execute([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [0])
        self.assertEqual(outputs, [0])

        _, outputs = execute([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [-1])
        self.assertEqual(outputs, [1])

    def test_example_jump_6(self):
        _, outputs = execute([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [0])
        self.assertEqual(outputs, [0])

        _, outputs = execute([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [-1])
        self.assertEqual(outputs, [1])

    def test_example_jump_7(self):
        program = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
        _, outputs = execute(program, [0])
        self.assertEqual(outputs, [999])

        _, outputs = execute(program, [8])
        self.assertEqual(outputs, [1000])

        _, outputs = execute(program, [100])
        self.assertEqual(outputs, [1001])


def decode_instruction(instruction):
    param_counts = {
        99: 0,
        1: 3,
        2: 3,
        3: 1,
        4: 1,
        5: 2,
        6: 2,
        7: 3,
        8: 3
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
        elif opcode == 5: # JUMP IF TRUE
            param_1 = fetch_param(state, param_modes[0], program_counter + 1)
            param_2 = fetch_param(state, param_modes[1], program_counter + 2)
            if param_1:
                program_counter = param_2
            else:
                program_counter += 3
        elif opcode == 6: # JUMP IF FALSE
            param_1 = fetch_param(state, param_modes[0], program_counter + 1)
            param_2 = fetch_param(state, param_modes[1], program_counter + 2)
            if not param_1:
                program_counter = param_2
            else:
                program_counter += 3
        elif opcode == 7: # LESS THAN
            param_1 = fetch_param(state, param_modes[0], program_counter + 1)
            param_2 = fetch_param(state, param_modes[1], program_counter + 2)
            write_loc = state[program_counter + 3]

            if param_1 < param_2:
                state[write_loc] = 1
            else:
                state[write_loc] = 0

            program_counter += 4
        elif opcode == 8: # EQUALS
            param_1 = fetch_param(state, param_modes[0], program_counter + 1)
            param_2 = fetch_param(state, param_modes[1], program_counter + 2)
            write_loc = state[program_counter + 3]

            if param_1 == param_2:
                state[write_loc] = 1
            else:
                state[write_loc] = 0

            program_counter += 4


def line_to_state(line: str):
    return [int(s.strip()) for s in line.split(",")]


def read_initial_state():
    with open("input.txt", "r") as inf:
        return line_to_state(inf.read())


if __name__ == '__main__':
    state = read_initial_state()
    final_state, outputs = execute(state, [5])
    print(outputs)

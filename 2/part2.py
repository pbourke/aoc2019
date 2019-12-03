from part1 import execute, read_initial_state

if __name__ == '__main__':
    initial_state = read_initial_state()

    for noun, verb in ((n, v) for v in range(100) for n in range(100)):
        state = initial_state.copy()
        state[1] = noun
        state[2] = verb

        end_state = execute(state)
        if end_state[0] == 19690720:
            print(end_state)
            break

import unittest
from typing import List, Tuple


class Tests(unittest.TestCase):
    def test_wire_to_points_and_distances(self):
        points, distances = wire_to_points_and_distances("R8,U5,L5,D3")
        self.assertTrue((1, 0) in points)
        self.assertEqual(1, distances[(1, 0)])
        self.assertEqual(21, len(points))
        self.assertEqual(21, max(distances.values()))

    def test_example1(self):
        self.assertEqual(30, min_steps("R8,U5,L5,D3", "U7,R6,D4,L4"))

    def test_example2(self):
        self.assertEqual(610, min_steps("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"))

    def test_example3(self):
        self.assertEqual(410, min_steps("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"))


def wire_to_points_and_distances(wire_str):
    moves = wire_str.split(",")
    points = set()
    distances = dict()
    x, y = 0, 0
    total_steps = 0

    for move in moves:
        direction = move[0]
        steps = int(move[1:])

        while steps > 0:
            steps = steps - 1
            if direction == "R":
                x = x + 1
            elif direction == "L":
                x = x - 1
            elif direction == "U":
                y = y + 1
            else:
                y = y - 1

            point = (x, y)
            points.add(point)
            total_steps = total_steps + 1
            if point not in distances:
                distances[point] = total_steps

    return points, distances


def min_steps(wire1, wire2):
    (points1, distances1) = wire_to_points_and_distances(wire1)
    (points2, distances2) = wire_to_points_and_distances(wire2)

    common_points = points1.intersection(points2)
    crossing_distances = [distances1[p] + distances2[p] for p in common_points]
    return min(crossing_distances)


if __name__ == '__main__':
    with open("input.txt", "r") as infile:
        lines = infile.readlines()
        print(min_steps(lines[0], lines[1]))

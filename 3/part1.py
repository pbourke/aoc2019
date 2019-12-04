import unittest
from typing import List, Tuple


class Tests(unittest.TestCase):
    def test_next_segment(self):
        self.assertEqual(((0, 0), (8, 0)), next_segment((0, 0), "R8"))
        self.assertEqual(((0, 0), (-8, 0)), next_segment((0, 0), "L8"))
        self.assertEqual(((0, 0), (0, 8)), next_segment((0, 0), "U8"))
        self.assertEqual(((0, 0), (0, -8)), next_segment((0, 0), "D8"))

    def test_moves_to_segments(self):
        self.assertEqual([((0, 0), (8, 0))], moves_to_segments(["R8"]))
        self.assertEqual([((0, 0), (8, 0)), ((8, 0), (0, 0))], moves_to_segments(["R8", "L8"]))
        self.assertEqual([((0, 0), (8, 0)), ((8, 0), (8, 8))], moves_to_segments(["R8", "U8"]))

    def test_align_segments(self):
        self.assertEqual([((-8, 0), (0, 0)), ((1, 1), (2, 2))], align_segments([((0, 0), (-8, 0)), ((1, 1), (2, 2))]))

    def test_get_intersection(self):
        s1 = ((0, 0), (5, 0))
        s2 = ((1, 1), (1, -1))
        s3 = ((-1, 1), (10, 1))
        s4 = ((3, -10), (3, 20))

        self.assertEqual((1, 0), get_intersection(s1, s2))
        self.assertEqual((1, 0), get_intersection(s2, s1))
        self.assertIsNone(get_intersection(s1, s1))
        self.assertIsNone(get_intersection(s1, s3))
        self.assertIsNone(get_intersection(s3, s1))
        self.assertIsNone(get_intersection(s4, s2))
        self.assertEqual((3, 0), get_intersection(s4, s1))
        self.assertEqual((3, 1), get_intersection(s3, s4))

    def test_distance_to_origin(self):
        self.assertEqual(0, distance_to_origin((0, 0)))
        self.assertEqual(1, distance_to_origin((0, 1)))
        self.assertEqual(1, distance_to_origin((-1, 0)))
        self.assertEqual(2, distance_to_origin((-1, 1)))

    def test_example1(self):
        self.assertEqual(6, min_distance("R8,U5,L5,D3", "U7,R6,D4,L4"))
        self.assertEqual(159, min_distance("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"))
        self.assertEqual(135, min_distance("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"))


def next_segment(pt, move: str):
    x1, y1 = pt

    direction = move[0]
    magnitude = int(move[1:])

    if direction == "R":
        return (pt, (x1 + magnitude, y1))
    elif direction == "L":
        return (pt, (x1 - magnitude, y1))
    elif direction == "U":
        return (pt, (x1, y1 + magnitude))
    else: # "D"
        return (pt, (x1, y1 - magnitude))


def moves_to_segments(moves: List[str]):
    segments = []
    pos = (0, 0)
    for move in moves:
        segment = next_segment(pos, move)
        segments.append(segment)
        pos = segment[1]

    return segments


def string_to_moves(s: str):
    return s.split(",")

def align_segment(segment: Tuple[Tuple[int, int], Tuple[int, int]]):
    ((x1, y1), (x2, y2)) = segment

    # left to right
    if x1 > x2:
        return ((x2, y2), (x1, y1))

    # bottom to top
    if y1 > y2:
        return ((x2, y2), (x1, y1))

    return segment


def align_segments(segments: List[Tuple[Tuple[int, int], Tuple[int, int]]]):
    return list(map(align_segment, segments))


def get_intersection(s1, s2):
    horizontal = align_segment(s1)
    vertical = align_segment(s2)

    # if the x values for s1 are equal
    if s1[0][0] == s1[1][0]:
        horizontal, vertical = vertical, horizontal

    ((hx1, hy1), (hx2, hy2)) = horizontal
    ((vx1, vy1), (vx2, vy2)) = vertical

    if hx1 < vx1 < hx2 and vy1 < hy1 < vy2:
        return (vx1, hy1)

    return None


def distance_to_origin(pt):
    x, y = pt
    return abs(x) + abs(y)


def min_distance(first_wire_moves: str, second_wire_moves: str):
    first_wire_segments = moves_to_segments(string_to_moves(first_wire_moves))
    second_wire_segments = moves_to_segments(string_to_moves(second_wire_moves))

    intersections = (get_intersection(s1, s2) for s1 in first_wire_segments for s2 in second_wire_segments)
    distances = (distance_to_origin(p) for p in intersections if p is not None)
    return min(distances)


if __name__ == '__main__':
    with open("input.txt", "r") as infile:
        lines = infile.readlines()
        print(min_distance(lines[0], lines[1]))

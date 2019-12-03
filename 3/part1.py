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

        self.assertEqual((1, 0), get_intersection(s1, s2))


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


def align_segments(segments: List[Tuple[Tuple[int, int], Tuple[int, int]]]):
    def align_segment(segment: Tuple[Tuple[int, int], Tuple[int, int]]):
        ((x1, y1), (x2, y2)) = segment
        if x1 > x2:
            return ((x2, y2), (x1, y1))
        return segment

    return list(map(align_segment, segments))


def get_intersection(s1, s2):
    ((s1x1, s1y1), (s1x2, s1y2)) = s1
    ((s2x1, s2y1), (s2x2, s2y2)) = s2

    #blah

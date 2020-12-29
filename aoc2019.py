#! /usr/bin/env python
import argparse

from all_days import day1

def main():
    parser = argparse.ArgumentParser(description="Advent of Code 2019")
    parser.add_argument("--day", type=int, help="Puzzle day")
    parser.add_argument("--star", type=int, help="Puzzle star")
    parser.add_argument('--dir', type=str, help='Input data directory')
    args = parser.parse_args()

    if args.day == 1:
        day1.run(args.dir, args.star)
    else:
        raise Exception("Day isn't already coded")


if __name__ == "__main__":
    main()
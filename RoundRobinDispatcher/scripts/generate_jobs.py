#!/usr/bin/env python3
"""
scripts/generate_jobs.py

Generate a dispatchlist file (dispatchlist.txt) for testing.

Usage examples:
  python3 scripts/generate_jobs.py --n 5 --max-arrival 20 --max-burst 8
  python3 scripts/generate_jobs.py --n 20 --outfile data/test_dispatch.txt --seed 42
"""

import argparse
import random
import os

def generate_jobs(n=10, max_arrival=30, max_burst=10, seed=None):
    if seed is not None:
        random.seed(seed)
    jobs = []
    # create random arrival times then sort them
    arrivals = [random.randint(0, max_arrival) for _ in range(n)]
    arrivals.sort()
    for i in range(n):
        arrival = arrivals[i]
        priority = 3  # keep 3 for compatibility with your project
        burst = random.randint(1, max_burst)
        # format matches the project: arrival, priority, totalCPU, 64, 0,0,0,0
        line = f"{arrival}, {priority}, {burst}, 64, 0, 0, 0, 0"
        jobs.append(line)
    return jobs

def main():
    parser = argparse.ArgumentParser(description="Generate dispatchlist test file.")
    parser.add_argument("--n", type=int, default=10, help="Number of jobs")
    parser.add_argument("--max-arrival", type=int, default=30, help="Max arrival time")
    parser.add_argument("--max-burst", type=int, default=10, help="Max burst length")
    parser.add_argument("--outfile", type=str, default="data/dispatchlist.txt", help="Output file path")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.outfile) or ".", exist_ok=True)
    jobs = generate_jobs(args.n, args.max_arrival, args.max_burst, args.seed)
    with open(args.outfile, "w") as f:
        for line in jobs:
            f.write(line + "\n")
    print(f"Wrote {len(jobs)} jobs to {args.outfile}")

if __name__ == "__main__":
    main()

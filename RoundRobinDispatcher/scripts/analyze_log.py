#!/usr/bin/env python3

import sys
import os
import pandas as pd

def read_dispatch(dispatch_path):
    jobs = {}
    with open(dispatch_path, "r") as f:
        jobid = 1
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",") if p.strip()]
            if len(parts) < 3:
                continue
            arrival = int(parts[0])
            priority = int(parts[1])
            burst = int(parts[2])
            jobs[jobid] = {"arrival": arrival, "priority": priority, "burst": burst}
            jobid += 1
    return jobs

def analyze(gantt_csv, dispatch_path, out_path="data/results.txt"):
    df = pd.read_csv(gantt_csv)
    df = df.sort_values("time").reset_index(drop=True)

    dispatch = read_dispatch(dispatch_path)

    stats = {}
    for job in df["jobId"].unique():
        if job == -1:
            continue
        times = df[df["jobId"] == job]["time"].tolist()
        start = min(times)
        end = max(times) + 1
        burst = len(times)
        arrival = dispatch[job]["arrival"]

        turnaround = end - arrival
        waiting = turnaround - dispatch[job]["burst"]
        response = start - arrival

        stats[job] = {
            "Job": job,
            "Arrival": arrival,
            "Start": start,
            "Completion": end,
            "Burst": dispatch[job]["burst"],
            "Turnaround": turnaround,
            "Waiting": waiting,
            "Response": response,
        }

    os.makedirs("data", exist_ok=True)

    with open(out_path, "w") as f:
        f.write("Job\tArrival\tStart\tCompletion\tBurst\tTurnaround\tWaiting\tResponse\n")
        for s in stats.values():
            f.write(f"{s['Job']}\t{s['Arrival']}\t{s['Start']}\t{s['Completion']}\t{s['Burst']}\t{s['Turnaround']}\t{s['Waiting']}\t{s['Response']}\n")

        avg_TA = sum(s["Turnaround"] for s in stats.values()) / len(stats)
        avg_WT = sum(s["Waiting"] for s in stats.values()) / len(stats)
        avg_RT = sum(s["Response"] for s in stats.values()) / len(stats)

        f.write("\nAverages:\n")
        f.write(f"Average Turnaround Time: {avg_TA:.2f}\n")
        f.write(f"Average Waiting Time: {avg_WT:.2f}\n")
        f.write(f"Average Response Time: {avg_RT:.2f}\n")

    print("Analysis written to", out_path)

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/analyze_log.py data/gantt.csv data/dispatchlist.txt")
        sys.exit(1)

    analyze(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()

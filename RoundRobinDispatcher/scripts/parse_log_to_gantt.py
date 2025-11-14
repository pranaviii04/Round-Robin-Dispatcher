#!/usr/bin/env python3
"""
scripts/parse_log_to_gantt.py

Parse data/log.txt (chronological logger output) and produce:
 - data/gantt.csv         (columns: time,jobId)  (-1 = idle)
 - data/results_from_log.txt  (per-job metrics and averages)

Usage:
  python3 scripts/parse_log_to_gantt.py data/log.txt [data/dispatchlist.txt]

Behavior:
 - Parses lines like: "[   0s] Job 1 - started (remaining: 3)"
 - Treats every 'started' or 'resumed' at time t as a running segment from t to (next_event_time - 1).
 - Correctly uses the current event time as the segment start (bug fix).
 - If next event is at same timestamp, end will equal start (keeps at least 1 second run).
 - Fallback for arrival time:
     * uses dispatchlist arrival if provided and consistent,
     * otherwise uses first observed appearance (prevents negative response times).
"""

import sys
import os
import re
import csv
from collections import defaultdict

LINE_RE = re.compile(r'^\s*\[\s*(\d+)\s*s\]\s+Job\s+(\d+)\s*-\s*([A-Za-z]+)', re.IGNORECASE)

def parse_log(log_path):
    events = []  # list of tuples (time:int, job:int, action:str, raw_line)
    with open(log_path, 'r') as f:
        for raw in f:
            line = raw.rstrip('\n')
            m = LINE_RE.search(line)
            if not m:
                continue
            t = int(m.group(1))
            jid = int(m.group(2))
            action = m.group(3).lower()
            events.append((t, jid, action, line))
    # keep stable sorting by time (preserve original order for same-time lines)
    events.sort(key=lambda x: x[0])
    return events

def build_intervals(events):
    """
    Build intervals list of [jobId, start, end] (inclusive).
    For each 'started' or 'resumed' event at index i with time t:
      start = t
      if i+1 < n: end = events[i+1].time - 1
      else: end = last_event_time
    Adjust if end < start (happens when next event has same time): set end = start
    """
    intervals = []
    if not events:
        return intervals

    last_time = max(e[0] for e in events)

    n = len(events)
    for i, (t, jid, action, _) in enumerate(events):
        if action in ('started', 'resumed'):
            start = t
            if i + 1 < n:
                next_time = events[i+1][0]
                end = next_time - 1
            else:
                end = last_time
            # ensure inclusive segment has at least start..start
            if end < start:
                end = start
            intervals.append([jid, start, end])
    return intervals

def finalize_intervals(intervals):
    # merge adjacent intervals for same job optionally (not necessary here),
    # but ensure intervals are valid.
    cleaned = []
    for jid, s, e in intervals:
        if e < s:
            e = s
        cleaned.append((jid, s, e))
    return cleaned

def write_gantt_csv(intervals, out_csv, min_time_hint=0):
    """Create per-second timeline from intervals and write csv."""
    timeline = {}
    for jid, s, e in intervals:
        for t in range(s, e+1):
            timeline[t] = jid  # later intervals overwrite (shouldn't commonly happen)

    if timeline:
        tmin = min(timeline.keys())
        tmax = max(timeline.keys())
    else:
        tmin = min_time_hint
        tmax = min_time_hint

    # ensure we include any gap before first recorded run (we use tmin as start)
    with open(out_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'jobId'])
        for t in range(tmin, tmax + 1):
            jid = timeline.get(t, -1)
            writer.writerow([t, jid])
    return tmin, tmax, timeline

def read_dispatchlist(dispatch_path):
    dispatch = {}
    if not dispatch_path or not os.path.exists(dispatch_path):
        return dispatch
    with open(dispatch_path, 'r') as f:
        jobid = 1
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            parts = [p.strip() for p in line.split(',') if p.strip() != ""]
            if len(parts) < 3:
                continue
            try:
                arrival = int(parts[0])
                priority = int(parts[1]) if len(parts) > 1 else 0
                burst = int(parts[2])
            except:
                continue
            dispatch[jobid] = {'arrival': arrival, 'priority': priority, 'burst_input': burst}
            jobid += 1
    return dispatch

def compute_metrics_from_timeline_csv(csv_path, dispatch):
    # read per-second timeline
    timeline_by_job = defaultdict(list)
    times = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = int(row['time'])
            jid = int(row['jobId'])
            timeline_by_job[jid].append(t)
            times.append(t)
    if not times:
        return {}, 0, 0

    tmin = min(times)
    tmax = max(times)
    total_time = tmax - tmin + 1
    busy_seconds = sum(len(v) for k, v in timeline_by_job.items() if k != -1)

    # observed arrivals from log (first appearance)
    observed_arrival = {}
    for jid, secs in timeline_by_job.items():
        if jid == -1:
            continue
        observed_arrival[jid] = min(secs)

    stats = {}
    for jid, secs in timeline_by_job.items():
        if jid == -1:
            continue
        start = min(secs)
        completion = max(secs) + 1  # completion moment
        burst_observed = len(secs)
        dispatch_info = dispatch.get(jid, {})
        arrival_dispatch = dispatch_info.get('arrival', None)
        burst_input = dispatch_info.get('burst_input', burst_observed)

        # choose arrival: prefer dispatch if consistent, otherwise observed
        if arrival_dispatch is None:
            arrival = observed_arrival.get(jid, start)
        else:
            # if dispatch arrival is later than observed start, prefer observed arrival
            if start < arrival_dispatch:
                arrival = observed_arrival.get(jid, start)
            else:
                arrival = arrival_dispatch

        turnaround = completion - arrival
        waiting = turnaround - burst_input
        response = start - arrival

        stats[jid] = {
            'JobID': jid,
            'Arrival': arrival,
            'StartTime': start,
            'CompletionTime': completion,
            'BurstInput': burst_input,
            'BurstObserved': burst_observed,
            'Turnaround': turnaround,
            'Waiting': waiting,
            'Response': response
        }

    return stats, total_time, busy_seconds

def write_results(stats, total_time, busy_seconds, out_path):
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    jids_sorted = sorted(stats.keys())
    with open(out_path, 'w') as f:
        f.write("JobID\tArrival\tStart\tCompletion\tBurstInput\tBurstObserved\tTurnaround\tWaiting\tResponse\n")
        for jid in jids_sorted:
            s = stats[jid]
            f.write(f"{s['JobID']}\t{s['Arrival']}\t{s['StartTime']}\t{s['CompletionTime']}\t{s['BurstInput']}\t{s['BurstObserved']}\t{s['Turnaround']}\t{s['Waiting']}\t{s['Response']}\n")

        # averages: consider only jobs with numeric Turnaround
        tvals = [s['Turnaround'] for s in stats.values() if s['Turnaround'] is not None]
        wvals = [s['Waiting'] for s in stats.values() if s['Waiting'] is not None]
        rvals = [s['Response'] for s in stats.values() if s['Response'] is not None]
        avg_tat = sum(tvals)/len(tvals) if tvals else 0
        avg_wt = sum(wvals)/len(wvals) if wvals else 0
        avg_rt = sum(rvals)/len(rvals) if rvals else 0
        cpu_util = (busy_seconds / total_time * 100) if total_time > 0 else 0
        throughput = (len(stats) / total_time) if total_time > 0 else 0

        f.write("\nAverages:\n")
        f.write(f"Average Turnaround Time: {avg_tat:.2f}\n")
        f.write(f"Average Waiting Time: {avg_wt:.2f}\n")
        f.write(f"Average Response Time: {avg_rt:.2f}\n")
        f.write(f"CPU Utilization (%): {cpu_util:.2f}\n")
        f.write(f"Throughput (jobs/sec): {throughput:.4f}\n")

    print(f"Wrote results to {out_path}")
    print(f"Average Turnaround: {avg_tat:.2f}, Waiting: {avg_wt:.2f}, Response: {avg_rt:.2f}")
    print(f"CPU Utilization: {cpu_util:.2f}%  Throughput: {throughput:.4f} jobs/sec")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/parse_log_to_gantt.py data/log.txt [data/dispatchlist.txt]")
        sys.exit(1)

    log_path = sys.argv[1]
    dispatch_path = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(log_path):
        print("Log file not found:", log_path)
        sys.exit(1)

    events = parse_log(log_path)
    if not events:
        print("No events parsed from log.")
        sys.exit(1)

    intervals = build_intervals(events)
    intervals = finalize_intervals(intervals)

    # write per-second CSV
    out_csv = "data/gantt.csv"
    tmin, tmax, timeline = write_gantt_csv(intervals, out_csv, min_time_hint=0)
    print(f"Wrote timeline to {out_csv}  (time {tmin}..{tmax})")

    # read dispatchlist if provided
    dispatch = read_dispatchlist(dispatch_path) if dispatch_path else {}
    stats, total_time, busy_seconds = compute_metrics_from_timeline_csv(out_csv, dispatch)
    write_results(stats, total_time, busy_seconds, "data/results_from_log.txt")

if __name__ == "__main__":
    main()

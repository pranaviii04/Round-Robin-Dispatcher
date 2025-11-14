import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import sys

# Load CSV from command line
if len(sys.argv) < 2:
    print("Usage: python3 scripts/gantt.py data/gantt.csv")
    sys.exit(1)

csv_path = sys.argv[1]
df = pd.read_csv(csv_path)

# Remove idle
clean = df[df["jobId"] != -1].reset_index(drop=True)

# Assign colors
unique_jobs = clean["jobId"].unique()
colors = list(mcolors.TABLEAU_COLORS.values())
job_colors = {job: colors[i % len(colors)] for i, job in enumerate(unique_jobs)}

# ----------------------------
#   Scheduling Calculations
# ----------------------------
report = []
full_df = df

for job in unique_jobs:
    start_time = full_df[full_df["jobId"] == job]["time"].min()
    completion_time = full_df[full_df["jobId"] == job]["time"].max() + 1
    burst_time = len(full_df[full_df["jobId"] == job])
    tat = completion_time - 0
    wt = tat - burst_time
    rt = start_time - 0
    report.append([job, start_time, completion_time, burst_time, tat, wt, rt])

report_df = pd.DataFrame(report, columns=[
    "JobID", "StartTime", "CompletionTime", "BurstTime",
    "TurnaroundTime", "WaitingTime", "ResponseTime"
])

avg_tat = report_df["TurnaroundTime"].mean()
avg_wt = report_df["WaitingTime"].mean()
avg_rt = report_df["ResponseTime"].mean()

# ----------------------------
#   COMBINED VISUALIZATION
# ----------------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 8))

# ---- Gantt Chart ----
segments = []
for i in range(len(clean)):
    row = clean.iloc[i]
    segments.append((row["time"], 1, row["jobId"]))

for start, dur, job in segments:
    ax1.barh(0, dur, left=start, color=job_colors[job], height=0.5)
    ax1.text(start + 0.5, 0, str(job), ha='center', va='center')

ax1.set_yticks([])
ax1.set_xlabel("Time")
ax1.set_title("Gantt Chart")
ax1.grid(axis="x", linestyle="--", alpha=0.4)

# *** FIX: INTEGER X-AXIS TICKS ***
ax1.set_xticks(range(0, df["time"].max() + 2, 1))

# ---- Scheduling Table ----
ax2.axis("tight")
ax2.axis("off")

table_data = report_df.round(2).values.tolist()
column_labels = report_df.columns.tolist()

table = ax2.table(
    cellText=table_data,
    colLabels=column_labels,
    loc='center',
    cellLoc='center'
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

ax2.text(
    0.02, -0.2,
    f"Average Turnaround Time: {avg_tat:.2f}\n"
    f"Average Waiting Time: {avg_wt:.2f}\n"
    f"Average Response Time: {avg_rt:.2f}",
    transform=ax2.transAxes,
    fontsize=12,
    verticalalignment='top'
)

plt.tight_layout()

# SAVE IMAGE HERE
plt.savefig("data/gantt.png", dpi=300, bbox_inches="tight")
print("Saved Gantt chart to: data/gantt.png")

plt.show()

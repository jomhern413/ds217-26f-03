"""Assignment 03: summarize a telemetry ward's systolic readings.

Run from the assignment directory with the project environment active:

    python3 analysis.py
"""

import numpy as np


def load_readings(filename):
    """Return (patient_ids, monitors, hour_columns, readings) from the supplied CSV.

    readings is a 2D array of integers: one row per patient, one column per
    monitored hour, in the order the header lists them.
    """
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    header = lines[0].strip().split(",")
    rows = [line.strip().split(",") for line in lines[1:] if line.strip()]

    patient_ids = np.array([row[0] for row in rows])
    monitors = np.array([row[1] for row in rows])
    hour_columns = np.array(header[2:])
    readings = np.array([row[2:] for row in rows]).astype(int)
    return patient_ids, monitors, hour_columns, readings


def main():
    patient_ids, monitors, hour_columns, readings = load_readings("data/bp_readings.csv")
    monitor_means = []
    monitor_count = 0
    for monitor in sorted(set(monitors)):
            monitor_means = np.append(monitor_means,readings[monitors == monitor].mean().max())
            monitor_count=monitor_count+1

    with open("output/vitals_summary.txt", "w", encoding="utf-8") as theReport:
        theReport.write("")
        print(f"Loaded {readings.shape[0]} patients x {readings.shape[1]} hours.",file=theReport)
        print(f"patients: {patient_ids.size}",file=theReport)
        print(f"readings: {readings.size}",file=theReport)
        print(f"mean_sbp: {readings.mean():.1f} mmHg",file=theReport)
        print(f"sd_sbp: {readings.std():.1f} mmHg",file=theReport)
        print(f"min_sbp: {readings.min()} mmHg",file=theReport)
        print(f"max_sbp: {readings.max()} mmHg",file=theReport)
        print(f"stage2_patients: {((readings.mean(axis=1))>=140).sum()}",file=theReport)
        print(f"highest_patient: {patient_ids[((readings.mean(axis=1)).argmax())]}", file=theReport)
        print(f"highest_patient_mean: {((readings.mean(axis=1)).max())} mmHg", file=theReport)
        print(f"peak_hour_column: {hour_columns[(readings.mean(axis=0)).argmax()]}", file=theReport)
        print(f"peak_hour_mean: {(readings.mean(axis=0)).max()} mmHg", file=theReport)
        print(f"high_monitor: {monitors[monitor_means.argmax()]}", file=theReport)
        print(f"monitor_offset: {monitor_means.max()-(((monitor_means.sum()-monitor_means.max()))/((monitor_means.size)-1))}", file=theReport)
        print(f"stage2_other_monitors: {(((readings[(~(monitors == monitors[np.array(monitor_means).argmax()]))])).mean(axis=1) >= 140).sum()}", file=theReport)

if __name__ == "__main__":
    main()

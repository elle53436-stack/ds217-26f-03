"""Assignment 03: summarize a telemetry ward's systolic readings.

Run from the assignment directory with the project environment active:

    python3 analysis.py
"""

from pathlib import Path

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
    print(f"Loaded {readings.shape[0]} patients x {readings.shape[1]} hours")

    patients = int(readings.shape[0])
    total_readings = int(readings.size)
    mean_sbp = float(readings.mean())
    sd_sbp = float(readings.std())
    min_sbp = int(readings.min())
    max_sbp = int(readings.max())


    patient_means = readings.mean(axis=1)
    stage2_patients = int(np.sum(patient_means >= 140))


    highest_idx = int(np.argmax(patient_means))
    highest_patient = str(patient_ids[highest_idx])
    highest_patient_mean = float(patient_means[highest_idx])

    hour_means = readings.mean(axis=0)
    peak_hour_idx = int(np.argmax(hour_means))
    peak_hour_column = str(hour_columns[peak_hour_idx])
    peak_hour_mean = float(hour_means[peak_hour_idx])


    monitor_names = np.array(sorted(list(set(monitors))))
    monitor_avg_list = []
    for m in monitor_names:
        m_mask = (monitors == m)
        monitor_avg_list.append(patient_means[m_mask].mean())

    monitor_avg_array = np.array(monitor_avg_list)
    top_m_idx = int(np.argmax(monitor_avg_array))
    high_monitor = str(monitor_names[top_m_idx])
    high_monitor_avg = float(monitor_avg_array[top_m_idx])


    other_mask = ~(monitors == high_monitor)
    other_avg = float(patient_means[other_mask].mean())
    monitor_offset = float(high_monitor_avg - other_avg)
    stage2_other_monitors = int(np.sum(patient_means[other_mask] >= 140))


    summary_lines = [
        f"patients: {patients}",
        f"readings: {total_readings}",
        f"mean_sbp: {mean_sbp:.2f} mmHg",
        f"sd_sbp: {sd_sbp:.2f} mmHg",
        f"min_sbp: {min_sbp} mmHg",
        f"max_sbp: {max_sbp} mmHg",
        f"stage2_patients: {stage2_patients}",
        f"highest_patient: {highest_patient}",
        f"highest_patient_mean: {highest_patient_mean:.2f} mmHg",
        f"peak_hour_column: {peak_hour_column}",
        f"peak_hour_mean: {peak_hour_mean:.2f} mmHg",
        f"high_monitor: {high_monitor}",
        f"monitor_offset: {monitor_offset:.2f} mmHg",
        f"stage2_other_monitors: {stage2_other_monitors}",
    ]

    output_file = Path("output") / "vitals_summary.txt"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        for line in summary_lines:
            f.write(line + "\n")

    print("\n--- output/vitals_summary.txt ---")
    with open(output_file, "r", encoding="utf-8") as f:
        print(f.read())


if __name__ == "__main__":
    main()
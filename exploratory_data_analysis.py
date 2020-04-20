import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics
import datetime as dt
from scipy import stats


def get_seconds(s):
    m, s = s.split(":")
    return int(m)*60 + int(s)


def print_summary_statistics(data):
    data = data.apply(get_seconds)

    min_val = min(data)
    max_val = max(data)
    median = statistics.median(data)
    mean = statistics.mean(data)
    std = statistics.stdev(data)
    iqr = stats.iqr(data)

    print(f"Min {min_val}")
    print(f"Max {max_val}")
    print(f"Median {median}")
    print(f"Mean {mean}")
    print(f"Std {std}")
    print(f"Interquartile Range {iqr}")


def construct_histogram(ax, data, title=""):
    data = data.apply(get_seconds)
    ax.hist(data)
    ax.set_xlabel("Response Time (s)")
    ax.set_ylabel("Count")
    ax.set_title(title)


def construct_ecdf(ax, data, title=""):
    data = data.apply(get_seconds)
    data = data.sort_values()
    p = [i/data.shape[0] for i in range(data.shape[0])]
    ax.plot(data, p)
    ax.set_xlabel("Response Time (s)")
    ax.set_ylabel("Pr < X")
    ax.set_title(title)


def analyze_response_times():
    data = pd.read_csv(os.path.join("data", "FDNY_Monthly_Response_Times.csv"))

    plt.style.use('Solarize_Light2')
    font = {'family': 'normal',
            'weight': 'bold',
            'size': 22}

    plt.rc('font', **font)

    response_times = data["AVERAGERESPONSETIME"]
    fig, ax = plt.subplots()
    construct_histogram(ax, response_times, "Average Response Time in New York City")
    plt.show()
    fig, ax = plt.subplots()
    construct_ecdf(ax, response_times, "Average Response Time in New York City")
    plt.show()
    print_summary_statistics(response_times)

    boroughs = set(data["INCIDENTBOROUGH"])
    fig, axs = plt.subplots(3, 2)
    fig.tight_layout()
    for ax, borough in zip(axs.reshape(-1), boroughs):
        response_times = data.loc[data["INCIDENTBOROUGH"] == borough]["AVERAGERESPONSETIME"]
        construct_ecdf(ax, response_times, borough)
        print(f"\n{borough}...")
        print_summary_statistics(response_times)
    fig.suptitle("Fire Fighter Response Based on Borough")
    plt.show()

    incident_types = set(data["INCIDENTCLASSIFICATION"])
    fig, axs = plt.subplots(3, 3)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    for ax, incident in zip(axs.reshape(-1), incident_types):
        response_times = data.loc[data["INCIDENTCLASSIFICATION"] == incident]["AVERAGERESPONSETIME"]
        construct_ecdf(ax, response_times, incident)
        print(f"\n{incident}...")
        print_summary_statistics(response_times)
    fig.suptitle("Fire Fighter Response Based on Incident Type")
    plt.show()


def main():
    analyze_response_times()


main()

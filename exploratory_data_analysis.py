"""This file performs an exploratory analysis of the data."""

import os
import statistics
from collections import defaultdict

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

from file_paths import get_output_file_path, create_output_directory


def get_seconds(s):
    """This function returns the number of seconds from the string."""

    m, s = s.split(":")
    return int(m)*60 + int(s)


def load_nyc_response_time_dataset():
    """Returns a dataframe containing the fire department's response times."""

    data = pd.read_csv(os.path.join("data", "FDNY_Monthly_Response_Times.csv"))
    data["AVERAGERESPONSETIME"] = data["AVERAGERESPONSETIME"].apply(get_seconds)

    return data


def compute_summary_statistics(data_dict, file_path):
    """Prints out summary statistics for the data."""

    # compute summary statistics
    summary_statistics = defaultdict(list)
    for data in data_dict.values():
        summary_statistics['Minimum'].append(min(data))
        summary_statistics['Maximum'].append(max(data))
        summary_statistics['Median'].append(statistics.median(data))
        summary_statistics['Mean'].append(statistics.mean(data))
        summary_statistics['Standard Deviation'].append(statistics.stdev(data))
        summary_statistics['Interquartile Range'].append(stats.iqr(data))

    # write a table to a file
    df = pd.DataFrame(summary_statistics, index=data_dict.keys())
    df.round(2)
    with open(file_path, 'w+') as f:
        f.write(df.to_latex())


def add_histogram(ax, data, title=""):
    """Adds a histogram to the passed axes."""

    ax.hist(data)
    ax.set_xlabel("Response Time (s)", fontsize=22)
    ax.set_ylabel("Count", fontsize=22)
    ax.set_title(title, fontsize=30)


def get_ECDF_values(data):
    """This functions returns the values and corresponding probabilities for plotting an ECDF."""

    values = sorted(data)
    p = [i / len(data) for i in range(len(data))]

    return values, p


def add_ECDF(ax, data, title=""):
    """Adds an ECDF to the passed axes."""

    ax.plot(*get_ECDF_values(data))
    ax.set_xlabel("Response Time (s)", fontsize=22)
    ax.set_ylabel("Pr < X", fontsize=22)
    ax.set_title(title, fontsize=30)


def analyze_response_times():
    """
    Performs a full analysis of New York City's fire department response times.
    This function will...
    1.) Save summary statistics.
    2.) Save histograms.
    3.) Save ECDFs.
    """

    # load data and set plot parameters
    create_output_directory()
    data = load_nyc_response_time_dataset()
    plt.style.use('Solarize_Light2')
    font = {'weight': 'bold', 'size': 22}
    plt.rc('font', **font)

    # construct a histogram of citywide response times
    response_times = data["AVERAGERESPONSETIME"]
    fig, ax = plt.subplots(figsize=(15, 8))
    add_histogram(ax, response_times, "Response Times in New York City")
    plt.savefig(os.path.join(get_output_file_path("response_times_hist.png")))

    # construct an EDCF of citywide response times
    fig, ax = plt.subplots(figsize=(15, 8))
    add_ECDF(ax, response_times, "Response Times in New York City")
    plt.savefig(os.path.join(get_output_file_path("response_times_ECDF.png")))

    # analyze the response time for each borough
    borough_response_times = {borough: data.loc[data["INCIDENTBOROUGH"] == borough]["AVERAGERESPONSETIME"]
                              for borough in set(data["INCIDENTBOROUGH"])}
    fig, axs = plt.subplots(3, 2, figsize=(30, 30))
    for ax, name, values in zip(axs.reshape(-1), *zip(*borough_response_times.items())):
        add_ECDF(ax, values, name)
    fig.suptitle("Fire Fighter Response Based on Borough")
    plt.savefig(os.path.join(get_output_file_path("borough_response_times_ECDF.png")))
    compute_summary_statistics(borough_response_times, os.path.join(get_output_file_path("borough_response_times.txt")))

    # analyze the response times to different types of incidents
    incident_response_times = {borough: data.loc[data["INCIDENTCLASSIFICATION"] == borough]["AVERAGERESPONSETIME"]
                               for borough in set(data["INCIDENTCLASSIFICATION"])}
    fig, axs = plt.subplots(3, 3, figsize=(40, 30))
    for ax, name, values in zip(axs.reshape(-1), *zip(*incident_response_times.items())):
        add_ECDF(ax, values, name)
    plt.savefig(os.path.join(get_output_file_path("incident_response_times_ECDF.png")))
    compute_summary_statistics(incident_response_times,
                               os.path.join(get_output_file_path("incident_response_times.txt")))


def main():
    analyze_response_times()


if __name__ == "__main__":
    main()

import base64
import matplotlib.pyplot as plt
from .models import *
from datetime import datetime as dt

def plot_numTracker(tracker_id, logs):
    x_values = []
    y_values = []
    values = {}
    for log in logs:
        values[log.timestamp] = int(log.value)

    for key in sorted(values):
        x_values.append(key)
        y_values.append(values[key])

    x_label = plt.xlabel("Time")
    y_label = plt.ylabel("Logged Value")
    title = plt.title("Log Trendline")
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig = plt.plot(x_values, y_values)
    filename_path = "static/images/num_tracker_" + str(tracker_id) + ".png"
    plt.savefig(filename_path, bbox_inches = 'tight')
    plt.close()
    with open(filename_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode('utf-8')
    return b64_string

def plot_boolTracker(tracker_id, logs):
    true_count = 0
    false_count = 0
    freq_x = []
    freq_y = []
    for log in logs:
        freq_x.append(log.timestamp)
        freq_y.append(log.value)
        if log.value == 'True':
            true_count += 1
        elif log.value == 'False':
            false_count += 1

    x_list = ["True", "False"]
    y_list = [true_count, false_count]
    x_label = plt.xlabel("Value")
    y_label = plt.ylabel("Frequency")
    title = plt.title("Log Bar Chart")
    plt.bar(x_list, y_list, color=['cornflowerblue', 'palevioletred'])
    plt.xticks(rotation=45)
    plt.tight_layout()
    filename_path = "static/images/bool_tracker_" + str(tracker_id) + ".png"
    plt.savefig(filename_path, bbox_inches = 'tight')
    plt.close()
    with open(filename_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode('utf-8')
    return b64_string


def plot_mcqTracker(tracker_id, logs, mcq):
    options = mcq.split(",")
    mcq_dict ={}
    for i in options:
        i = i.strip()
        mcq_dict[i] = 0
    print(options, " ", mcq_dict)
    for log in logs:
        j = log.value.strip()
        mcq_dict[j]+=1

    x_list = list(mcq_dict.keys())
    y_list = list(mcq_dict.values())

    x_label = plt.xlabel("Choices")
    y_label = plt.ylabel("No. of selected")
    title = plt.title("Logs Bar Chart")

    # plt.xticks(rotation=45)
    # plt.tight_layout()
    y_range = [i for i in range(0, 100)]
    plt.yticks(y_range)
    plt.bar(x_list, y_list, color=['firebrick', 'palegreen', 'teal', 'cyan', 'orange', 'deeppink'])


    filename_path = "static/images/mcq_tracker_" + str(tracker_id) + ".png"
    plt.savefig(filename_path, bbox_inches = 'tight')
    plt.close()
    with open(filename_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode('utf-8')
    return b64_string


def plot_timeTracker(tracker_id, logs):
    x_values = []
    y_values = []
    values = {}
    for log in logs:
        i = log.value.split(":")
        h = int(i[0])
        m = int(i[1])
        t = h + (m/60.0)
        values[log.timestamp] = t

    for key in sorted(values):
        x_values.append(key)
        y_values.append(values[key])

    x_label = plt.xlabel("Time")
    y_label = plt.ylabel("Logged Value in hours")
    title = plt.title("Log Trendline")
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig = plt.plot(x_values, y_values, color='red')
    filename_path = "static/images/time_tracker_" + str(tracker_id) + ".png"
    plt.savefig(filename_path, bbox_inches = 'tight')
    plt.close()
    with open(filename_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode('utf-8')
    return b64_string

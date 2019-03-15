import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import sys


def calculate_Deltas(data, files):
    t_min = int(data.index.min())
    t_max = int(data.index.max())
    ts = np.arange(t_min, t_max)
    rel_data = data.iloc[data.index.isin(ts)]
    DeltaX, DeltaY, DeltaR = [], [], []
    for idx, f in enumerate(files):
        col_x = "x_{}".format(idx)
        col_y = "y_{}".format(idx)
        x_i = rel_data[col_x].iloc[0]
        y_i = rel_data[col_y].iloc[0]
        xs = rel_data[col_x].apply(lambda x, x_i: x - x_i, args = (x_i,))
        ys = rel_data[col_y].apply(lambda y, y_i: y - y_i, args = (y_i,))
        rs = np.sqrt(xs**2 + ys**2)
        DeltaX.append(xs.values[1:])
        DeltaY.append(ys.values[1:])
        DeltaR.append(rs.values[1:])
    DeltaX = np.mean(np.column_stack(DeltaX)**2, axis = 1)
    DeltaY = np.mean(np.column_stack(DeltaY)**2, axis = 1)
    DeltaR = np.mean(np.column_stack(DeltaR)**2, axis = 1)
    return rel_data.index.values[1:], DeltaX, DeltaY, DeltaR


def get_save_path(files):
    if type([]) == type(files):
        f = files[0]
    else:
        f = files
    bar = bar = '/' if 'win' not in sys.platform else '\\'
    path = bar.join(f.split(bar)[:-1]) + bar
    return path


def load_data(files, file_format):
    def transform_replaces(string, replacers):
        for replacer in replacers:
            string = string.replace(replacer[0], replacer[1])
        return string

    data = pd.DataFrame()
    bar = '/' if 'win' not in sys.platform else '\\'
    replacers = [["\n", ""], [",", "."], ["e", "E"]]
    for idx, f in enumerate(files):
        columns = ["time", "x_{}".format(idx), "y_{}".format(idx)]
        file_data = []
        with open(f, "r") as f_open:
            for line in f_open.readlines():
                points = transform_replaces(line, replacers).split("   ")[1:]
                file_data.append([float(point) for point in points])
        cur_data = pd.DataFrame(np.array(file_data))
        cur_data.columns = columns
        cur_data.index = cur_data.iloc[:, 0]
        cur_data = cur_data.iloc[:, [1, 2]]
        if idx == 0:
            data = data.append(cur_data)
        else:
            data = pd.merge(data, cur_data, left_index = True,
                                                            right_index = True)
    return data


def plot_deltas(path, times, DeltaX, DeltaY, DeltaR):
    datasets = [DeltaX, DeltaY, DeltaR]
    y_labels = [r"$<\Delta x^2>$", r"$<\Delta y^2>$", r"$<\Delta \vec{R}^2>$"]
    outputs = ["delta_x.eps", "delta_y.eps", "delta_R.eps"]
    for idx, data in enumerate(datasets):
        fig, ax = plt.subplots()
        ax.scatter(times, data, c = "black")
        ax.set_xlabel(r"$t(s)$")
        ax.set_ylabel(y_labels[idx])
        ax.set_xscale("log")
        fig.savefig(path + outputs[idx], format = "eps", bbox_inches = "tight")
        plt.close()


def save_to_file(path, times, DeltaX, DeltaY, DeltaR):
    data = np.stack((times, DeltaX, DeltaY, DeltaR), axis = 1)
    np.savetxt(path + "time_deltas.csv", data, delimiter = ",")


def position_variation(files, file_format):
    data = load_data(files, file_format)
    times, DeltaX, DeltaY, DeltaR = calculate_Deltas(data, files)
    save_path = get_save_path(files)
    save_to_file(save_path, times, DeltaX, DeltaY, DeltaR)
    plot_deltas(save_path, times, DeltaX, DeltaY, DeltaR)

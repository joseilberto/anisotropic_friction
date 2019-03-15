import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re


def calculate_Deltas(data, files):
    t_min = int(data.index.min())
    t_max = int(data.index.max())
    ts = np.arange(t_min, t_max)
    rel_data = data.iloc[data.index.isin(ts)]
    DeltaX, DeltaY = [], []
    for idx, f in enumerate(files):
        col_x = "x_{}".format(idx)
        col_y = "y_{}".format(idx)
        x_i = rel_data[col_x].iloc[0]
        y_i = rel_data[col_y].iloc[0]
        xs = rel_data[col_x].apply(lambda x, x_i: x - x_i, args = (x_i,))
        ys = rel_data[col_y].apply(lambda y, y_i: y - y_i, args = (y_i,))
        DeltaX.append(xs.values[1:])
        DeltaY.append(ys.values[1:])
    DeltaX = np.mean(np.column_stack(DeltaX)**2, axis = 1)
    DeltaY = np.mean(np.column_stack(DeltaY)**2, axis = 1)
    return rel_data.index.values[1:], DeltaX, DeltaY


def get_save_file(files):
    if type([]) == type(files):
        f = files[0]
    else:
        f = files
    path = '/'.join(f.split("/")[:-1])
    return path + "/time_deltas.csv"


def load_data(files, file_format):
    data = pd.DataFrame()
    pattern = "/data/(.*?){}".format(file_format)
    for idx, f in enumerate(files):
        key = re.search(pattern, f)
        columns = ["time", "x_{}".format(idx), "y_{}".format(idx)]
        if not key:
            continue
        key = key.group(1)
        cur_data = pd.read_csv(f, sep = "  ", decimal = ",", header = None)
        cur_data = cur_data.applymap(lambda string: float(string.replace(",",
                                                        ".").replace("e", "E")))
        cur_data.columns = columns
        cur_data.index = cur_data.iloc[:, 0]
        cur_data = cur_data.iloc[:, [1, 2]]
        if idx == 0:
            data = data.append(cur_data)
        else:
            data = pd.merge(data, cur_data, left_index = True, right_index = True)
    return data


def plot_deltas(times, DeltaX, DeltaY):
    fig, ax = plt.subplots()
    ax.scatter(times, DeltaX, c = "black")
    ax.set_title(r"$<\Delta x^2>$")
    ax.set_xscale("log")
    # ax.set_yscale("log")
    fig.savefig("delta_x.eps", format = "eps", bbox_inches = 'tight')
    plt.close()
    fig, ax = plt.subplots()
    ax.scatter(times, DeltaY, c = "black")
    ax.set_title(r"$<\Delta y^2>$")
    ax.set_xscale("log")
    ax.set_yscale("log")
    fig.savefig("delta_y.eps", format = "eps", bbox_inches = 'tight')
    plt.close()


def save_to_file(save_file, times, DeltaX, DeltaY):    
    data = np.stack((times, DeltaX, DeltaY), axis = 1)
    np.savetxt(save_file, data, delimiter = ",")


def position_variation(files, file_format):
    data = load_data(files, file_format)
    times, DeltaX, DeltaY = calculate_Deltas(data, files)
    save_to_file(get_save_file(files), times, DeltaX, DeltaY)
    plot_deltas(times, DeltaX, DeltaY)

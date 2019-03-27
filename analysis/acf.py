from statsmodels.tsa.stattools import acf

import numpy as np
import pandas as pd
import os
import sys


def autocorrelate_data(files):
    for file in files:
        data = load_data(file)
        n, L = data.shape
        headers = "time,x,y,acf_x,acf_y" if L > 2 else "time,V,acf_V"
        for i in range(L - 1):
            acf_data = acf(data[:, i + 1], nlags = len(data[:, i + 1]))
            data = np.column_stack((data, acf_data))
        name, _ = os.path.splitext(file)
        np.savetxt(name + "_acf.csv", data, delimiter = ",", header = headers,
                                                                comments = "")


def load_data(file):
    def transform_replaces(string, replacers):
        for replacer in replacers:
            string = string.replace(replacer[0], replacer[1])
        return string

    replacers = [["\n", ""], [",", "."], ["e", "E"]]
    if "Vx" in file or "Vy" in file:
        return pd.read_csv(file, sep = ";", decimal = ',', header = None).values
    else:
        file_data = []
        with open(file, "r") as f_open:
            for line in f_open.readlines():
                points = transform_replaces(line, replacers).split("   ")[1:]
                file_data.append([float(point) for point in points])
        return np.array(file_data)

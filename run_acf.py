from run import process_args
from analysis.acf import autocorrelate_data


if __name__ == "__main__":
    files, _ = process_args()
    autocorrelate_data(files)

import argparse
import os

from methods import init_wrapper
from analysis.processors import *


def get_files(path, file_format):
    """
    Verify if the file is of the given format or verifies if a folder was
    given, for such case it finds all files with the given extension.
    """
    if os.path.isfile(path):
        _, file_ext = os.path.splitext(path)
        file_format = (file_format if path.endswith(file_format)
                                        else file_ext)
        return [path], file_format
    files = ([path] if path.endswith(file_format)
                else [path + file1 for file1 in os.listdir(path)
                        if file1.endswith(file_format)])
    return sorted(files), file_format


def set_args():
    """
    Set all arguments and return them parsed.
    """
    args_dic = {
        '-fmt': ['--format', str, 'Define the extension of data files to be '
        'used, if not given the standard is .dat'],
        '-p': ['--path', str, 'Define the file to be processed. If no file with'
        ' the given format is given, it searches the directory given for all '
        'files with the given format.'],
        '-nf': ['--n_files', int, 'Determines the number of files to be '
        'processed. If not given, processes all the files.'],
    }
    parser = argparse.ArgumentParser(description = 'Process video files '
                                    'extracting the centers of each bead.')
    for key, value in args_dic.items():
        parser.add_argument(key, value[0], type = value[1], help = value[2])
    return parser.parse_args()


@init_wrapper(set_args)
def process_args(args):
    """
    Process the arguments got from argparse. Also sets the standard values if
    not given.
    """
    file_format = args.format if args.format else ".dat"
    files, file_format = get_files(args.path, file_format)
    n_files = args.n_files if args.n_files else len(files)
    return files[:n_files], file_format


if __name__ == "__main__":
    files, file_format = process_args()
    position_variation(files, file_format)

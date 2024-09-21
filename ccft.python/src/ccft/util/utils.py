import os

import dill
import numpy as np

from ccft.util.exceptions.error_code import ErrorCode
from ccft.util.exceptions.exception import CustomException


def sorted_dict_values(adict, reverse=True):
    sorted_dict = sorted(adict.items(), key=lambda x: x[1], reverse=reverse)

    keys = [item[0] for item in sorted_dict]
    values = [item[1] for item in sorted_dict]

    return keys, values


def sorted_dict_keys(adict, reverse=True):
    sorted_dict = sorted(adict.items(), key=lambda x: x[0], reverse=reverse)

    keys = [item[0] for item in sorted_dict]
    values = [item[1] for item in sorted_dict]

    return keys, values


def normalization(values, log: bool = False, use_standardzation: bool = True, use_min_max_normalization: bool = True):
    if isinstance(values, dict):
        keys = values.keys()
        std_values = normalization(values.values(), log, use_standardzation, use_min_max_normalization)
        values = dict(zip(keys, std_values))
    else:
        if not isinstance(values, list) and not isinstance(values, np.ndarray):
            values = list(values)

        if log:
            the_list = np.array([item + 1 for item in values])
            values = np.log(the_list)
        if use_standardzation:
            mean = np.mean(values)
            std = np.std(values)
            z_scores = (values - mean) / std
            values = z_scores
        if use_min_max_normalization:
            min_bc = min(values)
            max_bc = max(values)
            c = max_bc - min_bc
            res = np.array([(item - min_bc) / c for item in values])
            values = res

    return values


def serialize_in_dir(directory: str, file_name: str, data):
    if not os.path.isdir(directory):
        os.makedirs(directory)

    with open('%s\\%s.bin' % (directory, file_name), 'wb') as file_to_write:
        dill.dump(data, file_to_write, dill.HIGHEST_PROTOCOL)


def serialize(path: str, data):
    directory = os.path.dirname(path)
    if not os.path.isdir(directory):
        os.makedirs(directory)

    with open(path, 'wb') as file_to_write:
        dill.dump(data, file_to_write, dill.HIGHEST_PROTOCOL)


def deserialize(data_path: str):
    if not os.path.isfile(data_path):
        raise CustomException(ErrorCode.File_NotFound, "The image data file does not exist: " + data_path)

    try:
        with open(data_path, 'rb') as file_to_read:
            data = dill.load(file_to_read)
        return data
    except Exception as exc:
        raise CustomException(ErrorCode.IO_Error, f'Data file read failed: {exc.__str__()}')


def get_all_files_in_directory(directory) -> tuple[list[str], list[str]]:
    all_full_paths = []
    all_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            all_full_paths.append(full_path)
            all_files.append(file)

    return all_files, all_full_paths


def get_file_name_without_extension(filename: str):
    idx = filename.rfind('\\')
    if idx > -1:
        filename = filename[idx + 1:]
    idx = filename.rfind('.')
    if idx > -1:
        filename = filename[:idx]
    return filename


def get_cpp_file_type(filename: str):
    idx = filename.rfind('.')
    if idx > -1:
        ex = filename[idx + 1]
        if ex == 'c':
            return 'source_file'
        elif ex == 'h':
            return 'head_file'
    return ''


def get_file_name(name: str):
    idx = name.rfind('.')
    if idx == -1:
        return name
    else:
        return name[0:idx]

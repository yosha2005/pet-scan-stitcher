import numpy as np
import os

def save_PET_scan(scan_array: np.ndarray, path_to_reconstructions, scan_name):
    scan_array_shape = scan_array.shape
    save_array_length = scan_array_shape[0] * scan_array_shape[1] * scan_array_shape[2]

    save_path = os.path.join(path_to_reconstructions, scan_name)
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    scan_array = scan_array.reshape(save_array_length).astype(np.float32)
    scan_array.tofile(save_path + '\\{}.v'.format(scan_name))
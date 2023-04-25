import numpy as np

def save_PET_scan(scan_array: np.ndarray, save_path):
    scan_array_shape = scan_array.shape
    save_array_length = scan_array_shape[0] * scan_array_shape[1] * scan_array_shape[2]

    scan_array = scan_array.reshape(save_array_length).astype(np.float32)
    scan_array.tofile(save_path + '\\test.v')
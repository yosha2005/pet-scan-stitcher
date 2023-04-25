import numpy as np
import os

import config

def get_header_contents(path_to_reconstructions, patient_name, segment_name, activity_level):
    file_name = '{}_{}_{}_000_000.v.hdr'.format(patient_name, segment_name, activity_level)
    path_to_file = os.path.join(
        path_to_reconstructions,
        segment_name,
        activity_level,
        file_name
    )

    header = open(path_to_file, 'r')
    header_contents = header.readlines()
    header.close

    return header_contents    

def generate_stitched_PET_scan_header(path_to_reconstructions, scan_name: str, save_path, number_transversal_slices):

    # get header file of upper segment
    patient_name = scan_name.split('_')[0]
    name_upper_segment = config.PATIENT_SEGMENTS[0]
    name_lower_segment = config.PATIENT_SEGMENTS[1]
    activity_level = config.ACTIVITY_LEVEL

    upper_header_contents = get_header_contents(path_to_reconstructions, patient_name, name_upper_segment, activity_level)
    lower_header_contents = get_header_contents(path_to_reconstructions, patient_name, name_lower_segment, activity_level)

    # generate path to header file
    header_file_name = scan_name + '.v.hdr'
    path_to_header_file = os.path.join(save_path, header_file_name)

    if len(upper_header_contents) == len(lower_header_contents):
        with open(path_to_header_file, 'w') as header_file:

            # iterate lines of original header files
            for i in range(len(upper_header_contents)):

                # handle lines that are not commented out
                if upper_header_contents[i][0] != '%':

                    # handle lines that do not share values
                    if upper_header_contents[i] != lower_header_contents[i]:
                        if 'start horizontal bed position' in upper_header_contents[i]:
                            header_file.write(lower_header_contents[i])
                        if 'end horizontal bed position' in upper_header_contents[i]:
                            header_file.write(upper_header_contents[i])
                        if '!name of data file' in upper_header_contents[i]:
                            header_file.write('!name of data file:={}\n'.format(scan_name + '.v'))
                        if 'maximum pixel count' in upper_header_contents[i]:
                            upper_max_pixel_count = float(upper_header_contents[i].split(':=')[1])
                            lower_max_pixel_count = float(lower_header_contents[i].split(':=')[1])

                            max_pixel_count = max([upper_max_pixel_count, lower_max_pixel_count])

                            header_file.write('maximum pixel count:={}\n'.format(max_pixel_count))

                        # TODO: ask Jörg about these
                        if '!image duration' in upper_header_contents[i]:
                            header_file.write(upper_header_contents[i])
                        if 'total prompts' in upper_header_contents[i]:
                            header_file.write(upper_header_contents[i])

                    # handle lines that share values
                    else:
                        if 'matrix size[3]' in upper_header_contents[i]:
                            header_file.write('matrix size[3]:={}\n'.format(number_transversal_slices))
                        else:
                            header_file.write(upper_header_contents[i])

                # TODO: handle lines that are commented out
                # else:
                #     print(upper_header_contents[i])

    # change number of transversal slices
    # save new header file

def save_PET_scan(scan_array: np.ndarray, path_to_reconstructions, scan_name):
    scan_array_shape = scan_array.shape
    save_array_length = scan_array_shape[0] * scan_array_shape[1] * scan_array_shape[2]

    save_path = os.path.join(path_to_reconstructions, scan_name)
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    generate_stitched_PET_scan_header(path_to_reconstructions, scan_name, save_path, scan_array_shape[0])

    scan_array = scan_array.reshape(save_array_length).astype(np.float32)
    scan_array.tofile(save_path + '\\{}.v'.format(scan_name))
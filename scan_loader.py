import numpy as np
import os

import config

class Segment:
    def read_header_file(self, path_to_header_file):
        scan_dimensions = np.zeros(3, 'int')
        voxel_size = np.zeros(3)
        bed_position = {}

        with open(path_to_header_file) as header_file:
            for line in header_file:

                # get scan dimensions
                if 'matrix size[1]' in line:
                    scan_dimensions[0] = int(line.split(':=')[1][:-1])  # x
                if 'matrix size[2]' in line:
                    scan_dimensions[1] = int(line.split(':=')[1][:-1])  # y
                if 'matrix size[3]' in line:
                    scan_dimensions[2] = int(line.split(':=')[1][:-1])  # z

                # get voxel size
                if 'scale factor (mm/pixel) [1]' in line:
                    voxel_size[0] = float(line.split(':=')[1][:-1])   # x
                if 'scale factor (mm/pixel) [2]' in line:
                    voxel_size[1] = float(line.split(':=')[1][:-1])   # y
                if 'scale factor (mm/pixel) [3]' in line:
                    voxel_size[2] = float(line.split(':=')[1][:-1])   # z

                # get bed position
                if 'end horizontal bed position (mm)' in line:
                    bed_position['end_horizontal'] = float(line.split(':=')[1][:-1])
                if 'start vertical bed position (mm)' in line:
                    bed_position['start_vertical'] = float(line.split(':=')[1][:-1])

        return scan_dimensions, voxel_size, bed_position
    
    def load_PET_scan(self, path_to_segment_file, scan_dimensions):
        num = scan_dimensions[2]    # z
        rows = scan_dimensions[1]   # y
        cols = scan_dimensions[0]   # x

        with open(path_to_segment_file, 'rb') as scan_file:
            segment = np.fromfile(scan_file, dtype='float32').reshape((num, rows, cols))

        return segment
    
    def get_z_positions(self, scan_dimensions_z, bed_position_z, voxel_size_z):
        z_positions = bed_position_z - np.arange(0, scan_dimensions_z) * voxel_size_z

        return z_positions

    def __init__(self, segment_information) -> None:
        self.scan_dimensions, self.voxel_size, self.bed_position = self.read_header_file(segment_information['segment_header'])
        self.segment = self.load_PET_scan(segment_information['segment_file'], self.scan_dimensions)

        self.z_positions = self.get_z_positions(self.scan_dimensions[2], self.bed_position['end_horizontal'], self.voxel_size[2])

def get_segment_information(patient_name):
    path_to_reconstructions = os.path.join(config.BASE_PATH, patient_name, 'Reconstructions')

    if os.path.exists(path_to_reconstructions):
        segments = []

        # get paths to reconstructions of individual segments
        for segment in config.PATIENT_SEGMENTS:

            segment_file_name = patient_name + '_' + segment + '_' + config.ACTIVITY_LEVEL + '_000_000.v'
            segment_header_file_name = segment_file_name + '.hdr'

            path_to_segment_directory = os.path.join(path_to_reconstructions, segment, config.ACTIVITY_LEVEL)
            path_to_segment_file = os.path.join(path_to_segment_directory, segment_file_name)
            path_to_segment_header = os.path.join(path_to_segment_directory, segment_header_file_name)

            if os.path.exists(path_to_segment_file) and os.path.exists(path_to_segment_header):
                segment_information = {
                    'segment_file': path_to_segment_file,
                    'segment_header': path_to_segment_header
                }

                segments.append(segment_information)

            else:
                print('ERROR: Either reconstruction or header file are missing for patient {}_{}'.format(patient_name, segment))

        return segments

    else:
        print('ERROR: Path to reconstructions does not exist for patient {}'.format(patient_name))

def scan_properties_match(upper_segment, lower_segment):
    # determine whether scan_dimensions, voxel sizes, and vertical bed positions match
    scan_dimensions_match = False
    voxel_sizes_match = False
    vertical_bed_positions_match = False

    # compare scan dimensions
    if np.linalg.norm(upper_segment.scan_dimensions - lower_segment.scan_dimensions) == 0:
        scan_dimensions_match = True

    # compare voxel sizes
    if np.linalg.norm(upper_segment.voxel_size - lower_segment.voxel_size) == 0:
        voxel_sizes_match = True

    # compare vertical bed positions
    vertical_difference = abs(upper_segment.bed_position['start_vertical'] - lower_segment.bed_position['start_vertical'])
    if vertical_difference == 0:
        vertical_bed_positions_match = True

    if scan_dimensions_match and voxel_sizes_match and vertical_bed_positions_match:
        return True
    else:
        if not scan_dimensions_match:
            print('ERROR: Scan dimensions did not match.')
        if not voxel_sizes_match:
            print('ERROR: Voxel sizes did not match.')
        if not vertical_bed_positions_match:
            print('ERROR: Vertical bed position did not match.')

        return False
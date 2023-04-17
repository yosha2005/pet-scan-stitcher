import os

import config

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

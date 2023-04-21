import numpy as np

def stitch_scans_together(upper_segment, lower_segment, scaling_function):
    diff_up_low = np.abs(lower_segment.z_positions - upper_segment.z_positions[-1])
    index_minimum = np.argmin(diff_up_low)

    overlap = index_minimum + 1
    stitched_scan_length = len(upper_segment.segment) + len(lower_segment.segment) - overlap

    # initialize stitched scan
    stitched_scan = np.zeros((stitched_scan_length, upper_segment.scan_dimensions[1], upper_segment.scan_dimensions[0]))

    # populate stitched scan with information from upper segment
    scaling_iterator_upper_segment = 0
    
    for i in range(len(upper_segment.segment)):
        scaling_factor = 1.
        if i >= (len(upper_segment.segment) - overlap) and i < len(upper_segment.segment):
            scaling_factor = scaling_function(scaling_iterator_upper_segment, overlap)
            scaling_iterator_upper_segment += 1

        stitched_scan[i] += scaling_factor * upper_segment.segment[i]

    # populate stitched scan with information from lower segment
    scaling_iterator_lower_segment = 0

    for i in range(len(lower_segment.segment)):
        scaling_factor = 1.
        if i >= 0 and i < overlap:
            scaling_factor= 1 - scaling_function(scaling_iterator_lower_segment, overlap)
            scaling_iterator_lower_segment += 1

        stitched_scan[len(upper_segment.segment) - overlap + i] += scaling_factor * lower_segment.segment[i]
    
    return stitched_scan
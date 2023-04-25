# custom files
import config
import scan_loader
import scan_stitcher
import scan_saver

def linear_scaling(x, overlap = 1):
    return 1 - (x / overlap)

for patient_name in config.PATIENT_NAMES:
    # initialize scans

    # get segment information (scan file location and header file location)
    segment_information, save_path, scan_name = scan_loader.get_segment_information(patient_name)

    if len(segment_information) == 2:
        upper_segment = scan_loader.Segment(segment_information[0])
        lower_segment = scan_loader.Segment(segment_information[1])

        if scan_loader.scan_properties_match(upper_segment, lower_segment):
            stitched_scan = scan_stitcher.stitch_scans_together(upper_segment, lower_segment, linear_scaling)

            # save stitched PET scan
            scan_saver.save_PET_scan(stitched_scan, config.PATH_TO_DESKTOP)
        
    else:
        print('ERROR: Wrong number of segments was supplied for patient {}.'.format(patient_name))
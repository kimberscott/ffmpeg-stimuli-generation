import os
import subprocess as sp
from videotools import prep_mp4_and_webm

this_path = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(this_path, "example_input")
calibration_vid_orig = os.path.join(input_path, "attentiongrabber.mp4")

output_path = os.path.join(this_path, "example_output")
calibration_vid_640 = os.path.join(output_path, "attentiongrabber640.mp4")
calibration_vid_L = os.path.join(output_path, "attentiongrabberL.mp4")
calibration_vid_R = os.path.join(output_path, "attentiongrabberR.mp4")
calibration_vid_final_LR = os.path.join(output_path, "final", "calibration_LR.mp4")
calibration_vid_final_RL = os.path.join(output_path, "final", "calibration_RL.mp4")

# First make a 640x640 version by padding

command = """[0:v]pad=width=640:height=640:x=160:y=160:color=white[out]"""

sp.call(
    [
        "ffmpeg",
        "-i",
        calibration_vid_orig,
        "-filter_complex",
        command,
        "-map",
        """[out]""",
        "-loglevel",
        "error",
        "-t",
        "5.0",
        calibration_vid_640,
    ]
)

# Then make the left-sided & right-sided versions

sp.call(
    [
        "ffmpeg",
        "-i",
        calibration_vid_640,
        "-filter_complex",
        """[0:v]pad=width=iw*3:height=ih:x=0:y=0:color=white[out]""",
        "-map",
        """[out]""",
        "-loglevel",
        "error",
        calibration_vid_L,
    ]
)

sp.call(
    [
        "ffmpeg",
        "-i",
        calibration_vid_640,
        "-filter_complex",
        """[0:v]pad=width=iw*3:height=ih:x=1280:y=0:color=white[out]""",
        "-map",
        """[out]""",
        "-loglevel",
        "error",
        calibration_vid_R,
    ]
)

# Concatenate the two videos, one after the other
sp.call(
    [
        "ffmpeg",
        "-i",
        calibration_vid_L,
        "-i",
        calibration_vid_R,
        "-filter_complex",
        """[0:v][1:v]concat=n=2:v=1:a=0[out]""",
        "-map",
        """[out]""",
        "-loglevel",
        "error",
        calibration_vid_final_LR,
    ]
)

sp.call(
    [
        "ffmpeg",
        "-i",
        calibration_vid_R,
        "-i",
        calibration_vid_L,
        "-filter_complex",
        """[0:v][1:v]concat=n=2:v=1:a=0[out]""",
        "-map",
        """[out]""",
        "-loglevel",
        "error",
        calibration_vid_final_RL,
    ]
)

# Make compressed versions for use online
prep_mp4_and_webm(
    os.path.join(calibrationDir, "final"), width="original", overwrite=True
)

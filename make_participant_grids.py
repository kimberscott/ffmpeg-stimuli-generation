"""
Bare-bones script to create cute grids of participant videos.
"""

import os
from videotools import *
import sys


this_path = os.path.dirname(os.path.abspath(__file__))
# Directory that contains collections of participant videos to make grids of. Each
# subdirectory is for one participant.
input_path = os.path.join(this_path, "example_input")
# Where to put collages that are created
output_path = os.path.join(this_path, "example_output")

participantDirs = [
    os.path.join(input_path, d)
    for d in os.listdir(input_path)
    if os.path.isdir(os.path.join(input_path, d))
]

for partDir in participantDirs:

    vids = [
        f
        for f in os.listdir(partDir)
        if (not (os.path.isdir(os.path.join(partDir, f))) and f[-4:] == ".mp4")
    ]

    collageName = os.path.split(partDir)[1]

    if len(vids):

        print("Making " + collageName)
        print(vids)

        doSound = True
        make_collage(
            partDir,
            vids,
            min(4, len(vids)),
            os.path.join(output_path, collageName),
            doSound,
            0,
            vidHeight=480
        )

        print("Exporting compressed")
        make_mp4(
            os.path.join(output_path, collageName + ".mp4"),
            output_path,
            width=min(1920, 480 * len(vids)),
        )

"""
Example of generating a whole bunch of dummy "videos" that are just black with the filename text and a beep.
Useful approach if you want to set up counterbalancing etc. ahead of actually having stimuli ready.
"""

import os
import subprocess as sp

events = [
    "table",
    "ramp",
    "toss",
    "stop",
    "reverse",
    "fall",
    "stay",
    "same",
    "salience",
]

outcomes = [
    ["down", "up", "continue"],
    ["up", "down"],
    ["up", "down"],
    ["hand", "nohand"],
    ["barrier", "nobarrier"],
    ["slightly", "mostly", "next", "near"],
    ["slightly", "mostly", "next", "near"],
    ["A", "B"],
    ["interesting", "boring"],
]

objects = [
    ["apple", "cup", "orangeball", "soap", "spraybottle", "whiteball"],
    ["apple", "cup", "orangeball", "soap", "spraybottle", "whiteball"],
    ["apple", "cup", "orangeball", "soap", "spraybottle", "whiteball"],
    ["train", "marker", "toycar", "sunglasses", "flashlight", "block"],
    ["train", "marker", "toycar", "sunglasses", "flashlight", "block"],
    ["hammer", "tissues", "duck", "book", "shoe", "bowl"],
    ["hammer", "tissues", "duck", "book", "shoe", "bowl"],
    ["A", "B", "C", "D", "E", "F"],
    ["A", "B", "C", "D", "E", "F"],
]

cams = [
    ["c1", "c2"],
    ["c1", "c2"],
    ["c1", "c2"],
    ["c1", "c2"],
    ["c1", "c2"],
    ["c1"],
    ["c1"],
    ["c1"],
    ["c1"],
]

bgs = [
    ["b1", "b2"],
    ["b1", "b2"],
    ["b1", "b2"],
    ["b1"],
    ["b1"],
    ["b1", "b2"],
    ["b1", "b2"],
    ["b1", "b2"],
    ["b1", "b2"],
]

flips = [
    ["NN"],
    ["NN"],
    ["NN", "RR"],
    ["RR"],
    ["RR", "NN"],
    ["NN", "NR", "RN", "RR"],
    ["NN", "NR", "RN", "RR"],
    ["NN", "NR", "RN", "RR"],
    ["NN", "NR", "RN", "RR"],
]

this_path = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(this_path, "example_input")
dummy_path = os.path.join(this_path, "example_output")
blank = os.path.join(this_path, "example_input", "black.mp4")
doEvents = ["fall", "stay", "same", "salience"]

for (iEvent, event) in enumerate(events):
    if event in doEvents:
        for (iOut1, outcome1) in enumerate(outcomes[iEvent]):
            for outcome2 in outcomes[iEvent][(iOut1 + 1) :]:
                for object in objects[iEvent]:
                    for cam in cams[iEvent]:
                        for bg in bgs[iEvent]:
                            for flip in flips[iEvent]:
                                shortname = (
                                    "sbs_"
                                    + event
                                    + "_"
                                    + outcome1
                                    + "_"
                                    + outcome2
                                    + "_"
                                    + object
                                    + "_"
                                    + cam
                                    + "_"
                                    + bg
                                    + "_"
                                    + flip
                                )
                                fname = os.path.join(dummy_path, shortname + ".mp4")
                                sp.call(
                                    [
                                        "ffmpeg",
                                        "-i",
                                        blank,
                                        "-ar",
                                        "22050",
                                        "-q:v",
                                        "1",
                                        "-vf",
                                        "drawtext='fontfile=/Library/Fonts/Arial Black.ttf:text='"
                                        + shortname
                                        + "':fontsize=40:fontcolor=white:x=100:y=40'",
                                        fname,
                                    ]
                                )
                                shortname = (
                                    "sbs_"
                                    + event
                                    + "_"
                                    + outcome2
                                    + "_"
                                    + outcome1
                                    + "_"
                                    + object
                                    + "_"
                                    + cam
                                    + "_"
                                    + bg
                                    + "_"
                                    + flip
                                )
                                fname = os.path.join(dummy_path, shortname + ".mp4")
                                sp.call(
                                    [
                                        "ffmpeg",
                                        "-i",
                                        blank,
                                        "-ar",
                                        "22050",
                                        "-q:v",
                                        "1",
                                        "-vf",
                                        "drawtext='fontfile=/Library/Fonts/Arial Black.ttf:text='"
                                        + shortname
                                        + "':fontsize=40:fontcolor=white:x=100:y=40'",
                                        fname,
                                    ]
                                )

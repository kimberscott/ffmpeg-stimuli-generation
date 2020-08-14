"""
Examples of using the functions in videotools.py to generate videos.
This file will not run as-is - it is just intended to provide reference commands you might copy and edit.
"""

import os
from videotools import *

this_path = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(this_path, "example_input")
output_path = os.path.join(this_path, "example_output")

# Put two videos side-by-side
makeSideBySide(os.path.join(input_path, "cropped_book.mp4"), os.path.join(input_path, "cropped_box.mp4"), "right", os.path.join(output_path, "side_by_side.mp4"))

# Make a collage of the object-introduction videos
vids = [
    "apple",
    "cup",
    "lotion",
    "spray",
    "whiteball",
    "orangeball",
    "train",
    "toycar",
    "sunglasses",
    "marker",
    "flashlight",
    "block",
]
vids = ["cropped_" + v + ".mp4" for v in vids]
make_collage(input_path, vids, 4, os.path.join(output_path, "0_introsA"), True, 1920, vidHeight=640)

# Replace the audio in VIDEO_1 with a different mp3 file NEW_AUDIO
sp.call([
    "ffmpeg",
    "-i",
    VIDEO_1,
    "-i",
    NEW_AUDIO,
    "-map",
    "0:v",
    "-map",
    "1:a",
    "-shortest",
    OUTPUT_VIDEO_NAME,
])

# Make a video where the input video plays backwards then forwards
sp.call(
    [
        "ffmpeg",
        "-i",
        INPUT_VIDEO,
        "-i",
        INPUT_VIDEO,
        "-filter_complex",
        "[1:v]reverse[secondhalf];[0:v][secondhalf]concat[out]",
        "-map",
        """[out]""",
        "-loglevel",
        "error",
        OUTPUT_VIDEO,
    ]
)

# The following are included for reference about potentially useful ffmpeg commands only - they are very specialized
# for particular stimuli!


def combineVideos(croppedVideoDir, sidebysideDir, regularOrderDict, whichVersions, minimal=False):
    '''Generate all versions of side-by-side videos needed for Lookit physics study.
    i.e. A / B, flippedA / B, A / flippedB, flippedA / flippedB.'''

    make_sure_path_exists(sidebysideDir)
    commands = ["""[0:v]setpts=PTS-STARTPTS,pad=iw*3:ih:color=white[a];[1:v]setpts=PTS-STARTPTS[z];[a][z]overlay=x=2*w:repeatlast=1:shortest=1:eof_action=repeat[out]""", \
                """[0:v]setpts=PTS-STARTPTS,hflip,pad=iw*3:ih:color=white[b];[1:v]setpts=PTS-STARTPTS[z];[b][z]overlay=x=2*w:repeatlast=1:shortest=1:eof_action=repeat[out]""", \
                """[0:v]setpts=PTS-STARTPTS,pad=iw*3:ih:color=white[b];[1:v]setpts=PTS-STARTPTS[z];[z]hflip[c];[b][c]overlay=x=2*w:repeatlast=1:shortest=1:eof_action=repeat[out]""", \
                """[0:v]setpts=PTS-STARTPTS,hflip,pad=iw*3:ih:color=white[b];[1:v]setpts=PTS-STARTPTS[z];[z]hflip[c];[b][c]overlay=x=2*w:repeatlast=1:shortest=1:eof_action=repeat[out]"""]
    suffixes = ['NN', 'RN', 'NR', 'RR']

    allfiles = os.listdir(croppedVideoDir)

    for iVid1, video1 in enumerate(allfiles):
        (shortname1, ext1) = os.path.splitext(video1)
        if not(os.path.isdir(os.path.join(croppedVideoDir, video1))) and ext1 == VIDEXT:
            for iVid2 in range(len(allfiles)):
                if iVid2 == iVid1:
                    continue
                if minimal and iVid2 <= iVid1:
                    continue
                else:
                    video2 = allfiles[iVid2]
                    (shortname2, ext2) = os.path.splitext(video2)
                    if not(os.path.isdir(os.path.join(croppedVideoDir, video2))) and ext2 == VIDEXT:
                        labels = [parse_video_filename(v, regularOrderDict) for v in [video1, video2]]
                        if labels[0][0] == labels[1][0] and \
                            labels[0][2] == labels[1][2] and \
                            labels[0][3] == labels[1][3] and \
                            labels[0][4] == labels[1][4]:


                            outfilenameBase = 'sbs_' + labels[0][0] + '_' + labels[0][1] + '_' + labels[1][1] + '_'  + \
                                labels[0][2] + '_' + labels[0][3] + '_' + labels[0][4] + '_'

                            for iVid in range(len(commands)):
                                if suffixes[iVid] in whichVersions:
                                    sp.call(["ffmpeg", "-i", os.path.join(croppedVideoDir, video1), \
                                                   "-i", os.path.join(croppedVideoDir, video2), \
                                                   "-filter_complex", \
                                                   commands[iVid], \
                                                "-map", """[out]""", "-loglevel", "error", \
                                                os.path.join(sidebysideDir, outfilenameBase + suffixes[iVid] + '.mp4')])

def flipVideos(rawVideoDir, origVideoDir, unflippedOrderDict):
    vidLengths = {
        "apple": 66,
        "cup": 86,
        "lotion": 68,
        "orangeball": 76,
        "spray": 90,
        "whiteball": 64,
    }
    fadeFrames = 10

    make_sure_path_exists(origVideoDir)
    for f in os.listdir(rawVideoDir):
        if not (os.path.isdir(os.path.join(rawVideoDir, f))):
            (shortname, ext) = os.path.splitext(f)
            if ext in ORIGEXT:
                (event, outcome, object, camera,
                 background) = parse_video_filename(
                    shortname, unflippedOrderDict
                )
                if outcome == "up":
                    continue

                sp.call(
                    [
                        "ffmpeg",
                        "-i",
                        os.path.join(rawVideoDir, f),
                        "-vf",
                        """vflip,fade=type=in:start_frame=1:nb_frames={}:color=0x009EFC,fade=type=out:start_frame={}:color=0x009EFC""".format(
                            fadeFrames, vidLengths[object] - fadeFrames
                        ),
                        "-loglevel",
                        "error",
                        os.path.join(
                            origVideoDir,
                            event
                            + "_up_"
                            + object
                            + "_"
                            + background
                            + "_"
                            + camera
                            + ".mp4",
                        ),
                    ]
                )
                sp.call(
                    [
                        "ffmpeg",
                        "-i",
                        os.path.join(rawVideoDir, f),
                        "-vf",
                        """fade=type=in:start_frame=1:nb_frames={}:color=0x009EFC,fade=type=out:start_frame={}:color=0x009EFC""".format(
                            fadeFrames, vidLengths[object] - fadeFrames
                        ),
                        "-loglevel",
                        "error",
                        os.path.join(
                            origVideoDir,
                            event
                            + "_down_"
                            + object
                            + "_"
                            + background
                            + "_"
                            + camera
                            + ".mp4",
                        ),
                    ]
                )
    return 0


### Crops and rescales 640px wide.
def cropVideos(
    origVideoDir,
    croppedVideoDir,
    regularOrderDict,
    originalSizes=[],
    cropStrings=[],
    which=[],
    cropByName=[],
    timecrop=[],
    fadeParams=[],
    doCrossFade=False,
):
    """TODO: docstring
    timecrop: list of (ID, start, stop, padStart, padStop) tuples.
        ID: dict containing any keys in ['object', 'event', 'outcome', 'camera', 'background'] and values.
            This time cropping will be applied to any videos that match the values for all
            the specified keys.
        start, stop: start and stop times in s.
        padStart, padStop: amount of time to extend first and last frames by, in s.
    fadeParams: (fadeFrames, fadeColor)
    """

    make_sure_path_exists(croppedVideoDir)
    for f in os.listdir(origVideoDir):
        if not (os.path.isdir(os.path.join(origVideoDir, f))):
            (shortname, ext) = os.path.splitext(f)
            if ext in ORIGEXT:
                if regularOrderDict:
                    (event, outcome, object, camera, background) = parse_video_filename(
                        shortname, regularOrderDict
                    )
                    thisID = {
                        "event": event,
                        "outcome": outcome,
                        "object": object,
                        "camera": camera,
                        "background": background,
                    }
                    if len(which) == 2 and not (object, event) == which:
                        continue
                    if len(which) == 3 and not (object, event, outcome) == which:
                        continue

                    timecropCommand = []
                    doTimeCrop = False
                    if timecrop:
                        for (ID, s, e, pS, pE) in timecrop:
                            if all([thisID[key] == val for (key, val) in ID.items()]):
                                startTime = s
                                endTime = e
                                padStart = pS
                                padEnd = pE
                                doTimeCrop = True
                        if doTimeCrop:
                            if not startTime == -1:
                                timecropCommand = ["-ss", str(startTime)]
                                if not endTime == -1:
                                    timecropCommand = timecropCommand + [
                                        "-t",
                                        str(endTime - startTime),
                                    ]
                        else:
                            warnings.warn("No time cropping for this video")

                if cropByName:
                    for (vidNames, cropStrForNames) in cropByName:
                        if f in vidNames:
                            cropStr = cropStrForNames

                else:
                    if originalSizes == "*":
                        cropStr = cropStrings[0]
                    else:
                        res = findVideoResolution(os.path.join(origVideoDir, f))
                        if res in originalSizes:
                            cropStr = cropStrings[originalSizes.index(res)]
                        else:
                            cropStr = """scale=640:-2"""

                cropStr = cropStr + ",setpts=PTS-STARTPTS"

                if doTimeCrop:
                    croppedVid = os.path.join(
                        croppedVideoDir, shortname + "_middle.mp4"
                    )
                    croppedVidFinal = os.path.join(croppedVideoDir, shortname + ".mp4")
                else:
                    croppedVid = os.path.join(croppedVideoDir, shortname + ".mp4")
                    croppedVidFinal = croppedVid

                command = (
                    ["ffmpeg", "-i", os.path.join(origVideoDir, f), "-vf", cropStr]
                    + timecropCommand
                    + ["-loglevel", "error", croppedVid]
                )

                sp.call(command)

                if doTimeCrop:
                    firstImg = os.path.join(croppedVideoDir, shortname + "_first.png")
                    lastImg = os.path.join(croppedVideoDir, shortname + "_last.png")
                    firstVid = os.path.join(croppedVideoDir, shortname + "_first.mp4")
                    lastVid = os.path.join(croppedVideoDir, shortname + "_last.mp4")

                    sp.call(
                        [
                            "ffmpeg",
                            "-i",
                            croppedVid,
                            "-vframes",
                            "1",
                            "-f",
                            "image2",
                            firstImg,
                            "-loglevel",
                            "error",
                        ]
                    )
                    [nF, dur, x, y] = get_video_details(
                        croppedVid, ["nframes", "vidduration", "width", "height"]
                    )
                    sp.call(
                        [
                            "ffmpeg",
                            "-i",
                            croppedVid,
                            "-vf",
                            "select='eq(n,{})'".format(nF - 1),
                            "-vframes",
                            "1",
                            "-f",
                            "image2",
                            lastImg,
                            "-loglevel",
                            "error",
                        ]
                    )
                    sp.call(
                        [
                            "ffmpeg",
                            "-loop",
                            "1",
                            "-i",
                            firstImg,
                            "-t",
                            str(padStart),
                            firstVid,
                            "-loglevel",
                            "error",
                        ]
                    )
                    sp.call(
                        [
                            "ffmpeg",
                            "-loop",
                            "1",
                            "-i",
                            lastImg,
                            "-t",
                            str(padEnd),
                            lastVid,
                            "-loglevel",
                            "error",
                        ]
                    )

                    if not doCrossFade:
                        concat_mp4s(croppedVidFinal, [firstVid, croppedVid, lastVid])

                    else:
                        unfaded = os.path.join(
                            croppedVideoDir, shortname + "_beforecrossfade.mp4"
                        )
                        concat_mp4s(unfaded, [croppedVid, lastVid])
                        # see crossfade advice at http://superuser.com/a/778967
                        sp.call(
                            [
                                "ffmpeg",
                                "-i",
                                unfaded,
                                "-i",
                                firstVid,
                                "-f",
                                "lavfi",
                                "-i",
                                "color=white:s={}x{}".format(int(x), int(y)),
                                "-filter_complex",
                                "[0:v]format=pix_fmts=yuva420p,fade=t=out:st={}:d={}:alpha=1,setpts=PTS-STARTPTS[va0];\
                            [1:v]format=pix_fmts=yuva420p,fade=t=in:st=0:d={}:alpha=1,setpts=PTS-STARTPTS+{}/TB[va1];\
                            [2:v]scale={}x{},trim=duration={}[over];\
                            [over][va0]overlay=format=yuv420[over1];\
                            [over1][va1]overlay=format=yuv420[outv]".format(
                                    dur + padEnd,
                                    padEnd,
                                    padEnd,
                                    dur,
                                    int(x),
                                    int(y),
                                    dur + padStart + padEnd,
                                ),
                                "-vcodec",
                                "libx264",
                                "-map",
                                "[outv]",
                                croppedVidFinal,
                                "-loglevel",
                                "error",
                            ]
                        )
                        os.remove(unfaded)

                    os.remove(firstImg)
                    os.remove(lastImg)
                    os.remove(firstVid)
                    os.remove(lastVid)
                    os.remove(croppedVid)

                if fadeParams:
                    (fadeFrames, fadeColor) = fadeParams
                    nF = get_video_details(croppedVidFinal, "nframes")
                    unfaded = os.path.join(croppedVideoDir, shortname + "_unfaded.mp4")
                    os.rename(croppedVidFinal, unfaded)

                    sp.call(
                        [
                            "ffmpeg",
                            "-i",
                            unfaded,
                            "-vf",
                            """fade=type=in:start_frame=1:nb_frames={}:color={},fade=type=out:start_frame={}:color={}""".format(
                                fadeFrames, fadeColor, nF - fadeFrames, fadeColor
                            ),
                            "-loglevel",
                            "error",
                            croppedVidFinal,
                        ]
                    )

                    os.remove(unfaded)
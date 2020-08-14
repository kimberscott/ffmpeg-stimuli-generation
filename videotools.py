import os
import subprocess as sp
import math
import errno
import warnings
import shlex
import json

ORIGEXT = [".mov", ".mp4"]
VIDEXT = ".mp4"

def makeSideBySide(leftVideoPath, rightVideoPath, whichAudio, outputPath):
    """Simple utility for making paired left/right video for Halie :) 
    Each video takes up 1/3 of horizontal space, should be same size.
    whichAudio should be "left" or "right" to use audio from left or right video."""
    audioChoice = "0" if whichAudio == "left" else "1"
    sp.call(
        [
            "ffmpeg",
            "-i",
            leftVideoPath,
            "-i",
            rightVideoPath,
            "-filter_complex",
            """[0:v]setpts=PTS-STARTPTS,pad=iw*3:ih:color=white[a];[1:v]setpts=PTS-STARTPTS[z];[a][z]overlay=x=2*w:repeatlast=1:shortest=1:eof_action=repeat[out]""",
            """-map""",
            """[out]""",
            """-map""",
            audioChoice + ":a:0",
            "-loglevel",
            "error",
            outputPath,
        ]
    )


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
        return 1
    except OSError as exception:
        return 0
        if exception.errno != errno.EEXIST:
            raise


def make_mp4(inputpath, mp4dir, width="original", overwrite=True, rate=1000):
    """Export an mp4 version of a video for the web.
    
    Arguments:
    inputpath - the full path to the video file to export
    mp4dir - the directory where the new file should go
    
    Keyword arguments:
    width - either 'original' to keep width of input file, or width in pixels
    
    The mp4 version will have the same filename as the input video + '_compressed',
    with an mp4 extension. Aspect ratio is preserved if changing width."""

    (shortname, ext) = os.path.splitext(os.path.basename(inputpath))
    command = [
        "ffmpeg",
        "-i",
        inputpath,
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-b:v",
        str(rate) + "k",
        "-maxrate",
        str(rate) + "k",
        "-bufsize",
        str(2 * rate) + "k",
        "-c:a",
        "libfdk_aac",
        "-b:a",
        "128k",
    ]
    if not (width == "original"):
        command = command + ["-vf", "scale=" + str(width) + ":-2"]

    outpath = os.path.join(mp4dir, shortname + "_compressed.mp4")
    if not (overwrite) and os.path.exists(outpath):
        return
    else:
        sp.check_call(command + [outpath])


def make_webm(inputpath, webmdir, width="original", overwrite=True, rate=1000):
    """Export an webm version of a video for the web.
    
    Arguments:
    inputpath - the full path to the video file to export
    webmdir - the directory where the new file should go
    
    Keyword arguments:
    width - either 'original' to keep width of input file, or width in pixels
    
    The webm version will have the same filename as the input video + '_compressed',
    with an webm extension. Aspect ratio is preserved if changing width."""

    (shortname, ext) = os.path.splitext(os.path.basename(inputpath))
    command = [
        "ffmpeg",
        "-i",
        inputpath,
        "-c:v",
        "libvpx",
        "-b:v",
        str(rate) + "k",
        "-maxrate",
        str(rate) + "k",
        "-bufsize",
        str(2 * rate) + "k",
        "-c:a",
        "libvorbis",
        "-b:a",
        "128k",
        "-speed",
        "2",
    ]
    if not (width == "original"):
        command = command + ["-vf", "scale=" + str(width) + ":-2"]
    outpath = os.path.join(webmdir, shortname + "_compressed.webm")
    if not (overwrite) and os.path.exists(outpath):
        return
    else:
        sp.check_call(command + [outpath])


def prep_mp4_and_webm(inputpath, width="original", overwrite=True):
    """Export all video files in a directory to both webm and mp4 for the web.
    
    Arguments:
    inputpath - the video directory to process
    
    Keyword arguments:
    width - either 'original' to keep width of input file, or width in pixels (applied to 
        all files)
    
    mp4 and webm versions will have the same filenames as the originals, but appropriate
    extensions. Aspect ratio is preserved if changing width."""

    if not (os.path.isdir(inputpath)):
        raise ValueError("prep_mp4_and_webm requires a path to a directory with videos")

    (parent, child) = os.path.split(inputpath)
    webmdir = os.path.join(parent, child, "webm")
    mp4dir = os.path.join(parent, child, "mp4")

    make_sure_path_exists(webmdir)
    make_sure_path_exists(mp4dir)

    videoExts = [".mov", ".mp4", ".flv", ".webm", ".ogv", ".avi"]
    for f in os.listdir(inputpath):
        if not (os.path.isdir(os.path.join(inputpath, f))):
            (shortname, ext) = os.path.splitext(f)
            if ext in videoExts:
                make_mp4(os.path.join(inputpath, f), mp4dir, width, overwrite)
                make_webm(os.path.join(inputpath, f), webmdir, width, overwrite)


def make_collage(
    videoDir,
    videoList,
    nCols,
    outPath,
    doSound,
    exportWidth,
    vidHeight=[],
    cropSquare=False,
):
    """Make a grid of videos (mp4 format).
    
    Arguments:
    videoDir - directory where the input videos are (use '/' to just give full paths 
        in videoList
    videoList - list of videos to include in the grid. They will appear in reading order.
        Videos should all be the same size! (But any aspect ratio is fine.)
    nCols - number of columns for the grid. The number of rows will be set accordingly.
    outPath - where to put the collage (full path and filename, excluding extension)
    doSound - boolean, whether to include sound in the collage. 
    exportWidth - 0 not to export, otherwise width in pixels of mp4 & webm to create
    
    If doing sound, this creates a few temporary files in the same directory as the final 
    collage, named (if the final output is collage.mp4) collage_silent.mp4 and 
    collage_sound.wav.
    
    Sizes of input videos is unchanged, so final collage size is (originalWidth * nCols) x 
    (originalHeight * nRows). """

    if doSound:
        (outPathDir, outPathFname) = os.path.split(outPath)
        outPathSilent = os.path.join(outPathDir, outPathFname + "_silent.mp4")
        outPathSound = os.path.join(outPathDir, outPathFname + ".wav")
    else:
        outPathSilent = outPath + ".mp4"

    outPath = outPath + ".mp4"

    # Step 1: make a silent collage

    nRows = int(math.ceil(len(videoList) / nCols))

    inputList = []
    for (iV, vidName) in enumerate(videoList):
        inputList = inputList + ["-i", os.path.join(videoDir, vidName)]

    command = ["ffmpeg"] + inputList

    border = 10
    # In general, use 'ih' and 'h'; if heights vary, input here.
    if vidHeight:
        vidHeight = str(vidHeight)
        vidHeightOverlay = vidHeight
    else:
        vidHeight = "ih"
        vidHeightOverlay = "h"


    filterStr = (
        "[0:v]pad="
        + str(border * (nCols - 1))
        + "+"
        + "iw*"
        + str(nCols)
        + ":"
        + str(border * (nRows - 1))
        + "+"
        + vidHeight
        + "*"
        + str(nRows)
        + "[x0];"
    )
    for iVid in range(1, len(videoList)):
        if iVid == (len(videoList) - 1):
            outStr = "[out]"
        else:
            outStr = "[x" + str(iVid) + "]"

        thisY = iVid // nCols
        thisX = iVid % nCols

        if cropSquare:
            filterStr = (
                filterStr
                + "["
                + str(iVid)
                + ":v]crop=iw:iw:0:0[y"
                + str(iVid - 1)
                + "];"
            )

            filterStr = (
                filterStr
                + "[x"
                + str(iVid - 1)
                + "][y"
                + str(iVid - 1)
                + "]overlay=x="
                + str(border * (thisX))
                + "+("
                + str(thisX)
                + "*w):y="
                + str(border * (thisY))
                + "+("
                + str(thisY)
                + "*"
                + vidHeightOverlay
                + "):repeatlast=1:shortest=0:eof_action=repeat"
                + outStr
                + ";"
            )
        else:
            filterStr = (
                filterStr
                + "[x"
                + str(iVid - 1)
                + "]["
                + str(iVid)
                + ":v]overlay=x="
                + str(border * (thisX))
                + "+("
                + str(thisX)
                + "*w):y="
                + str(border * (thisY))
                + "+("
                + str(thisY)
                + "*"
                + vidHeightOverlay
                + "):repeatlast=1:shortest=0:eof_action=repeat"
                + outStr
                + ";"
            )

    command = command + [
        "-filter_complex",
        filterStr[:-1],
        "-c:v",
        "libx264",
        "-map",
        "[out]",
        outPathSilent,
    ]

    sp.check_call(command)

    if doSound:

        # Step 2: make sound mix

        filterStr = (
            "amix=inputs="
            + str(len(videoList))
            + ":duration=first:dropout_transition=3"
        )

        command = ["ffmpeg"] + inputList + ["-filter_complex", filterStr, outPathSound]

        sp.check_call(command)

        command = [
            "ffmpeg",
            "-i",
            outPathSilent,
            "-i",
            outPathSound,
            "-c:v",
            "copy",
            "-c:a",
            "libfdk_aac",
            "-shortest",
            outPath,
        ]
        sp.check_call(command)

        # Clean up intermediate files

        sp.call(["rm", outPathSilent])
        sp.call(["rm", outPathSound])

    if exportWidth != 0:
        (exportDir, baseFilename) = os.path.split(outPath)
        exportDir = os.path.join(exportDir, "export")
        make_sure_path_exists(exportDir)
        make_mp4(outPath, exportDir, exportWidth, rate=2000)
        make_webm(outPath, exportDir, exportWidth, rate=2000)


def make_dummies(outDir, blankVideoPath, vidNames):
    """Make blank labeled videos.
    
    outDir: directory to put the blank videos in
    blankVideoPath: full path to the mp4 video to use as the starting point
    vidNames: array of video filenames (no extension). One mp4 video will be created for 
        each; it will just be the blank video with the vidName written on it. """

    make_sure_path_exists(outDir)

    for vidName in vidNames:

        sp.call(
            [
                "ffmpeg",
                "-i",
                blankVideoPath,
                "-ar",
                "22050",
                "-q:v",
                "1",
                "-vf",
                "drawtext='fontfile=/Library/Fonts/Arial Black.ttf:text='"
                + vidName
                + "':fontsize=40:fontcolor=white:x=100:y=40'",
                os.path.join(outDir, vidName),
            ]
        )


# function to find the resolution of the input video file
# http://stackoverflow.com/a/34356719
def findVideoResolution(pathToInputVideo):
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = shlex.split(cmd)
    args.append(pathToInputVideo)
    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
    ffprobeOutput = sp.check_output(args).decode("utf-8")
    ffprobeOutput = json.loads(ffprobeOutput)

    # find height and width
    height = ffprobeOutput["streams"][0]["height"]
    width = ffprobeOutput["streams"][0]["width"]

    return height, width


def concat_mp4s(concatPath, vidPaths):
    """Concatenate a list of mp4s into a single new mp4, video only.

    concatPath: full path to the desired new mp4 file, including
        extension 
    vidPaths: full paths to the videos to concatenate. 
    
    Videos will be concatenated in the order they appear in this list."""

    concat = ["ffmpeg"]
    inputList = ""

    # If there are no files to concat, immediately return 0.
    if not len(vidPaths):
        return 0

    # Build the concatenate command
    for (iVid, vid) in enumerate(vidPaths):
        concat = concat + ["-i", vid]
        inputList = inputList + "[{}:0]".format(iVid)

    # Concatenate the videos
    concat = concat + [
        "-filter_complex",
        inputList + "concat=n={}:v=1:a=0".format(len(vidPaths)) + "[out]",
        "-map",
        "[out]",
        concatPath,
        "-loglevel",
        "error",
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-b:v",
        "1000k",
        "-maxrate",
        "1000k",
        "-bufsize",
        "2000k",
    ]

    sp.call(concat)


# function to find the resolution of the input video file
# http://stackoverflow.com/a/34356719
def get_video_details(vidPath, whichAttr):
    """Uses ffprobe to retrieve details about a video.

    get_video_details(vidPath, whichAttr)

    vidPath: full path to video file

    whichAttr: single attribute or list of attributes to retrieve. Options are:
        duration - duration of video in seconds
        bitrate - bit rate of video
        starttime - start time of video
        [All options below require a video stream; will warn and return 0 if
        no video stream is available]
        height - height in pixels
        width - width in pixels
        nframes - number of frames
        vidduration - duration of video stream in seconds
        audduration - duration of audio stream in seconds

        Returns a single value if whichAttr is a string, or a list of values
        corresponding to those requested if whichAttr is a list of strings.
        """

    # Ensure whichAttr is a list
    if isinstance(whichAttr, str):
        whichAttr = [whichAttr]

    # Run ffprobe and collect output with data about video
    cmd = "ffprobe -v quiet -show_format -print_format json -show_streams -count_frames"
    args = shlex.split(cmd)
    args.append(vidPath)
    try:
        ffprobeOutput = sp.check_output(args).decode("utf-8")
    except:
        warnings.warn(
            "Error running ffprobe command {} to get video details about {}, returning -1".format(
                " ".join(args), vidPath
            )
        )
        if len(whichAttr) == 1:
            return -1
        else:
            return [-1] * len(whichAttr)

    ffprobeOutput = json.loads(ffprobeOutput)

    # Loop through attributes and collect specific information
    attributes = []
    for attr in whichAttr:
        returnVal = -1
        if attr == "duration":
            returnVal = float(ffprobeOutput["format"]["duration"])
        elif attr == "bitrate":
            returnVal = float(ffprobeOutput["format"]["bit_rate"])
        elif attr == "starttime":
            returnVal = float(ffprobeOutput["format"]["start_time"])
        # Attributes that require a video/audio stream...
        elif attr in ["nframes", "height", "width", "vidduration", "audduration"]:
            audioStream = -1
            videoStream = -1
            for iStream in range(len(ffprobeOutput["streams"])):
                if ffprobeOutput["streams"][iStream]["codec_type"] == "audio":
                    audioStream = iStream
                elif ffprobeOutput["streams"][iStream]["codec_type"] == "video":
                    videoStream = iStream

            if videoStream == -1:
                warnings.warn("Missing video stream for video {}".format(vidPath))
                if attr in ["nframes", "height", "width", "vidduration"]:
                    returnVal = 0
                    attributes.append(returnVal)
                    continue

            if audioStream == -1:
                # warnings.warn('Missing audio stream for video {}'.format(vidPath))
                if attr in ["audduration"]:
                    returnVal = 0
                    attributes.append(returnVal)
                    continue

            if attr == "nframes":
                if "nb_read_frames" in ffprobeOutput["streams"][videoStream].keys():
                    returnVal = float(
                        ffprobeOutput["streams"][videoStream]["nb_read_frames"]
                    )
                else:
                    returnVal = 0
                    warnings.warn("No frame data for {}".format(vidPath))
            elif attr == "width":
                returnVal = float(ffprobeOutput["streams"][videoStream]["width"])
            elif attr == "height":
                returnVal = float(ffprobeOutput["streams"][videoStream]["height"])
            elif attr == "vidduration":
                returnVal = float(ffprobeOutput["streams"][videoStream]["duration"])
            elif attr == "audduration":
                returnVal = float(ffprobeOutput["streams"][audioStream]["duration"])
        else:
            raise ValueError("Unrecognized attribute requested")
        attributes.append(returnVal)

    # Return just a string if there's only one return value in the list
    if len(attributes) == 1:
        attributes = attributes[0]

    return attributes

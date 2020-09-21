# ffmpeg-stimuli-generation

Snippets and examples of using ffmpeg to manipulate experiment stimuli. Ffmpeg is a powerful command-line tool for editing media files. You can use it directly from the command line, but if you're processing lots of videos for stimuli, you may want to write some scripts to help out. (This also makes it much easier to remake everything after your advisor says that gee that red backdrop is a bit much or to add a few more videos in a consistent way, and to publish the methods you used to create your stimuli!)

The scripts here are in Python, using subprocess to make the calls to ffmpeg. These are intended as potentially useful references for ffmpeg commands and short scripts that handle common tasks (e.g., creating side-by-side videos from two inputs for preferential looking), rather than as ready-to-go tools.

## Prerequisite: installing ffmpeg

You can download a ready-to-go executable file for any OS or (on Mac) install ffmpeg using Homebrew.

### Using a static build (ready-to-go executable file)

After installing ffmpeg from [this link](https://ffmpeg.org/download.html) and unzipping the file, you will likely need to add it to your system path. See [instructions here](https://superuser.com/questions/624561/install-ffmpeg-on-os-x) under "Static Builds."

### Using Homebrew on OSX

First install Homebrew (can type `brew` in the terminal to see if you already have it installed - if that prints out a bunch of example usage / torubleshooting commands, you have it.)

See [ffmpeg's instructions](https://trac.ffmpeg.org/wiki/CompilationGuide/macOS) for installing via Homebrew. You have two options:

Option 1: You can get a basic install using `brew install ffmpeg`.

Option 2: If you want additional options, you can instead use the third-party formula homebrew-ffmpeg. Get this formula and look at the options:

```
brew tap homebrew-ffmpeg/ffmpeg
brew options homebrew-ffmpeg/ffmpeg/ffmpeg
```

Then install with as many as you want (`brew install homebrew-ffmpeg/ffmpeg/ffmpeg --option-1 --option-2 ...`). 

## See also

* [Official ffmpeg documentation](https://ffmpeg.org/ffmpeg.html)
* [Common tasks in ffmpeg](https://www.labnol.org/internet/useful-ffmpeg-commands/28490/)
* [Ffmpeg snippets/cheatsheet gist](https://gist.github.com/martinruenz/537b6b2d3b1f818d500099dde0a38c5f)
* [Converting to mp4 and webm](https://gist.github.com/princenaman/174eae80f8269c759e4f3f7fe505ea54)
* [More snippets](https://jonlabelle.com/snippets/view/shell/ffmpeg-command)

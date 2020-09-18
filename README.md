# ffmpeg-stimuli-generation

Snippets and examples of using ffmpeg to manipulate experiment stimuli. These are intended as potentially useful references for ffmpeg commands and short scripts that handle common tasks (e.g., creating side-by-side videos from two inputs for preferential looking), rather than as ready-to-go tools.

## Installing ffmpeg

You can install ffmpeg using Homebrew (on Mac) or you can download a ready-to-go executable file [here](https://ffmpeg.org/download.html). 

### Using Homebrew

First install Homebrew (can type `brew` in the terminal to see if you already have it installed - if that prints out a bunch of example usage / torubleshooting commands, you have it.)

See [ffmpeg's instructions](https://trac.ffmpeg.org/wiki/CompilationGuide/macOS) for installing via Homebrew. You have two options:

Option 1: You can get a basic install using `brew install ffmpeg`.

Option 2: If you want additional options, you can instead use the third-party formula homebrew-ffmpeg. Get this formula and look at the options:

```
brew tap homebrew-ffmpeg/ffmpeg
brew options homebrew-ffmpeg/ffmpeg/ffmpeg
```

Then install with as many as you want (`brew install homebrew-ffmpeg/ffmpeg/ffmpeg --option-1 --option-2 ...`). 

### Using a static build (ready-to-go executable file)

After installing ffmpeg from the link above and unzipping the file, you will likely need to add it to your system path. See [instructions here](https://superuser.com/questions/624561/install-ffmpeg-on-os-x) under "Static Builds."

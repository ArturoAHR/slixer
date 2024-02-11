# Slixer

A terminal audio file slicer that works by timestamps.

## Usage

To use slixer you will need an audio file and a text file with timestamps, the timestamps must follow the following format:

```
<hh:mm:ss or mm:ss> <Audio segment title>
```

For example:

```
0:00:00 Segment A
0:01:00 Segment B
0:02:30 Segment C
```

or

```
00:00 Segment A
01:00 Segment B
02:30 Segment C
```

After having these two files, you can slice an audio file based on the timestamps in the following manner.

`slixer /path/to/audio.mp3 -t /path/to/timestamps.txt`

If we were to use the example timestamps, the result will be the creation of three files called `Segment A.mp3`, `Segment B.mp3` and `Segment C.mp3` in the directory that this commands was run.

## Dependencies

For usage with non-wav formats such as mp3, installing ffmpeg or libav and adding them to your PATH environment variable is necessary. You can follow [pydub's guide to set ffmpeg or libav up](https://github.com/jiaaro/pydub?tab=readme-ov-file#getting-ffmpeg-set-up).

## Installation for Development

Make sure you have Pipenv installed and are in a virtual environment with:

```pipenv shell```

After you're inside a virtual environment, you can install the dependencies needed for development with:

```pipenv install --dev```

To build an executable you may use:

```invoke build```

The executable will be generated in the `dist` directory.

## Other Development Commands

```invoke lint```

Lints the project to find issues.

```invoke lint --fix```

Fixes any lint issues the Black formatter can solve.
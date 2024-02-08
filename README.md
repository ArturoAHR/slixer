# Slixer

A terminal audio file slicer that works by timestamps.

## Dependencies

For usage on non-wav formats such as mp3, installing ffmpeg or libav. You can follow [pydub's guide to set ffmpeg or libav up](https://github.com/jiaaro/pydub?tab=readme-ov-file#getting-ffmpeg-set-up).

## Installation for Development

Make sure you have Pipenv installed and are in a virtual environment with:

```pipenv shell```

After you're inside a virtual environment, you can install the dependencies needed for development with:

```invoke install```

To build an executable you may use:

```invoke build```

The executable will be generated in the `dist` directory.
import argparse
from commands.slixer.command import slixer


def main():
    parser = argparse.ArgumentParser(
        prog="slixer",
        description="A terminal audio file slicer that works by timestamps",
    )

    parser.add_argument("audio_file_path", help="Path to audio file")
    parser.add_argument(
        "-t",
        "--timestamps-file",
        dest="timestamps_file_path",
        help="Path to text file with timestamps",
        required=True,
    )

    parser.set_defaults(func=slixer)

    args = parser.parse_args()

    if hasattr(args, "func"):
        try:
            args.func(args)
        except Exception as e:
            print(f"Error: {e}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

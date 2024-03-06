def preview_slixer_output(timestamps: list):
    print("Output Preview: ")
    for index, timestamp in enumerate(timestamps):
        start_hours, start_minutes, start_seconds = timestamp["start_time"]
        start_time = (
            f"{start_hours:02d}:{start_minutes:02d}:{start_seconds:02d}"
        )

        segment_title = timestamp["segment_title"]

        print(
            f"({index + 1}/{len(timestamps)}) "
            f"{start_time} - "
            f"{segment_title}"
        )

    print("\nDo you wish to proceed? (y/n)\n")

    while True:
        user_input = input().lower()
        if user_input == "y":
            break
        elif user_input == "n":
            print("Aborting...")
            exit()
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

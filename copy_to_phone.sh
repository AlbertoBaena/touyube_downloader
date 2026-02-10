#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DIR="$SCRIPT_DIR/mp3_downloads"

if [ ! -d "$DIR" ]; then
    echo "Error: Directory does not exist:"
    echo "$DIR"
    exit 1
fi

cd "$DIR" || exit 1


adb push . /sdcard/Music/

rm -f *

echo
echo "Files copied successfully."
read -rp "Press Enter to exit..."

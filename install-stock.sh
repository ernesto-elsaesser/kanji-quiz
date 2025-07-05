#!/bin/bash

SOURCE_DIR="/mnt/usb/kanji-quiz"
APPS_DIR="/mnt/mmc/Roms/APPS"
GAME_DIR="$APPS_DIR/quiz"

{
    echo "$(date)"
    mkdir -p "$GAME_DIR"
    echo "mkdir $?"
    cp "$SOURCE_DIR/quiz.py" "$GAME_DIR/"
    echo "quiz.py $?"
    cp "$SOURCE_DIR/sdl.py" "$GAME_DIR/main.py"
    echo "main.py $?"
    cp -r "$SOURCE_DIR/sets" "$GAME_DIR/"
    echo "sets $?"
    cp -r "$SOURCE_DIR/pysdl" "$GAME_DIR/"
    echo "pysdl $?"

} 2>&1 | tee -a install.log

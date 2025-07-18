#!/bin/bash

SOURCE_DIR="/media/SHUTTLE/kanji-quiz"
PYGAME_DIR="/userdata/roms/pygame"
IMAGE_DIR="$PYGAME_DIR/images"
GAME_DIR="$PYGAME_DIR/quiz"

{
    echo "$(date)"
    mkdir -p "$GAME_DIR"
    echo "mkdir $?"
    cp "$SOURCE_DIR/quiz.py" "$GAME_DIR/"
    echo "quiz.py $?"
    cp -r "$SOURCE_DIR/sets.py" "$GAME_DIR/"
    echo "sets.py $?"
    cp "$SOURCE_DIR/pyg.py" "$GAME_DIR/kanji-quiz.pygame"
    echo "kanji-quiz.pygame $?"
    cp "$SOURCE_DIR/DejaVuSansMono.ttf" "$GAME_DIR/"
    echo "font $?"
    cp "$SOURCE_DIR/kanji.png" "$IMAGE_DIR/kanji-quiz.png"
    echo "kanji-quiz.png $?"

} 2>&1 | tee -a install.log

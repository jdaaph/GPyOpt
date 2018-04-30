#!/bin/bash

palette="/tmp/palette.png"

filters="fps=2,scale=1280:-1:flags=lanczos"

ffmpeg -v warning -i $1 -vf "$filters,palettegen" -y $palette
ffmpeg -framerate 2 -v warning -i $1 -i $palette -lavfi "$filters [x]; [x][1:v] paletteuse" -y $2
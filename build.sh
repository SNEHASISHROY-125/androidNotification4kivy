#! /bin/sh

docker run --interactive --tty --rm \
    --volume "$HOME/.buildozer":/home/user/.buildozer \
    --volume "$HOME/.gradle":/home/user/.gradle \
    --volume "$PWD":/home/user/hostcwd \
    kivy/buildozer android debug

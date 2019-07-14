#!/bin/bash
for file in `git status -s | sed "s/^[[:space:]]*.*?[[:space:]]*//"`
do
        if [[ $file =~ \.py$ ]] ; then
                echo "Running for ${file}"
                black $file --line-length 79 --target-version py37
                git add $file
        fi
done

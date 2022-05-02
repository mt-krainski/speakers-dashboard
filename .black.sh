#!/bin/bash
for file in `git status -s | sed "s/^[[:space:]]*.*?[[:space:]]*//"`
do
        if [[ $file =~ \.py$ ]] ; then
                echo "Running for ${file}"
                black $file --target-version py39
                git add $file
        fi
done

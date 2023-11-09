# Opal

## Description

Opal is a programming language made mostly for the purpose of learning, but also with the hopes to be used in future projects. I also hope to eventually have Opal's compiler be self-hosted.

Check the [documentation](DOCS.md) to see what's currently implemented.

## Usage

> python3 opal.py {file_path} -c

The {file_path} argument should be replaced by the path to the .opl file you want to compile.

The -c flag is optional and causes the program to run gcc on the resulting file once it's finished compiling. If the flag is not included, the program will only output an out.c file and not an executable.
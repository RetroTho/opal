# Opal

## Description

Opal is a programming language made mostly for the purpose of learning, but also with the hopes to be used in future projects. I also hope to eventually have Opal's compiler be self-hosted.

Check the [documentation](DOCS.md) to see what's currently implemented.

## Usage

> python3 opal.py {file_path} {-c, -r}

The {file_path} argument should be replaced by the path to the .opl file you want to compile.

Either a -c flag or -r flag can optionally be included; however not both at once.

The -c flag causes the program to run gcc on the resulting file once it's finished compiling. If the flag is not included, the program will only output an out.c file and not an executable.

The -r flag causes the program to run gcc on the resulting file once it's finished compiling and then proceed to remove the resulted out.c file leaving only an executable.
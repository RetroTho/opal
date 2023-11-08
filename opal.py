import os
import sys
import subprocess
from modules.tokenizer import Tokenizer
from modules.parser import Parser
from modules.generator import Generator


def readFile(file_name: str) -> str:
    try:
        with open(file_name, "r") as file:
            src = file.read()
            return src
    except FileNotFoundError:
        print("Error: the file '" + file_name + "' could not be found")
        exit()
    except:
        print("Error: issue reading file")
        exit()


def writeFile(output: str):
    with open("out.c", "w") as file:
        file.write(output)


def compile(file_name: str = ""):
    do_gcc = False
    if file_name:
        src = readFile(file_name)
    else:
        if len(sys.argv) == 2:
            src = readFile(sys.argv[1])
        elif len(sys.argv) == 3:
            src = readFile(sys.argv[1])
            if sys.argv[2] == "-c":
                do_gcc = True
            else:
                print("Error: invalid second argument")
                exit()
        else:
            print("Error: invalid usage")
            exit()
    tokens = Tokenizer(src).tokenize()
    prog = Parser(tokens).parse()
    output = Generator(prog).generate()
    writeFile(output)

    if do_gcc:
        subprocess.run(["gcc", os.getcwd() + "/out.c"])


if __name__ == "__main__":
    compile()

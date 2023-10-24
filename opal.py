import sys
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
    if file_name:
        src = readFile(file_name)
    else:
        if len(sys.argv) == 2:
            src = readFile(sys.argv[1])
        else:
            print("Error: invalid usage")
            exit()
    tokens = Tokenizer(src).tokenize()
    prog = Parser(tokens).parse()
    output = Generator(prog).generate()
    writeFile(output)


if __name__ == "__main__":
    compile()

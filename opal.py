import sys
from modules.tokenizer import Tokenizer


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
    print(tokens)


if __name__ == "__main__":
    compile()

# Opal

Opal is a statically-typed, compiled programming language. The Opal compiler
reads `.opl` source files, transpiles them to C, and then invokes `gcc` to
produce a native executable. It started as a learning project and is being
developed with the long-term goal of becoming self-hosted.

For the current state of the language, see the [documentation](DOCS.md).

## Requirements

- Python 3
- GCC

## Usage

```
python3 opal.py {file_path} [-c | -r]
```

`{file_path}` is the path to the `.opl` source file you want to compile. An
optional flag controls what happens after transpilation:

| Flag | Behavior                                                                 |
| ---- | ------------------------------------------------------------------------ |
| _none_ | Transpile only. Writes `out.c` to the working directory.               |
| `-c` | Transpile, then run `gcc` on `out.c` to produce a native executable.     |
| `-r` | Transpile, run `gcc`, then remove `out.c`, leaving only the executable. |

The `-c` and `-r` flags are mutually exclusive.

## Quick Start

Hello, world (`hello.opl`):

```
print('hello, world')
exit(0)
```

Build and run it:

```
python3 opal.py hello.opl -r
./a.out
```

A small program with a function:

```
function add(takes(int, a), takes(int, b), returns(int)){
    return(a + b)
}

variable result(int, add(2, 3))
print(result)
exit(0)
```

## Language Overview

A quick tour of the syntax. See [DOCS.md](DOCS.md) for the full reference.

### Primitive types

Opal currently has two primitive types: `int` and `str`. Strings use single
quotes.

```
variable count(int, 10)
variable name(str, 'opal')
```

### Variables

A variable is declared with the `variable` keyword, followed by an identifier
and a detailer with its type (and optional initial value).

```
variable x(int)
variable y(int, 42)
x = 7
```

### Functions

Functions are declared with the `function` keyword. Arguments are described
with `takes(type, ident)` and the return type with `returns(type)`.

```
function square(takes(int, n), returns(int)){
    return(n * n)
}
```

### Control flow

```
if(x == 10){
    print('ten')
}

while(x == 10){
    print('still ten')
    x = 0
}
```

### Built-ins

- `print(value)` — write a value to stdout
- `exit(code)` — exit the program with the given status

## Roadmap

Done:

- [x] Tokenizer
- [x] Parser
- [x] C code generation
- [x] `int` and `str` primitive types
- [x] Variables
- [x] Functions (with typed arguments and return values)
- [x] Control flow (`if`, `while`)

Planned:

- [ ] More primitive types (e.g. `bool`, `float`, `char`)
- [ ] Arrays and composite types
- [ ] Standard library modules
- [ ] Improved error messages and diagnostics
- [ ] Self-hosted compiler

## License

Opal is released under the [MIT License](LICENSE.md).


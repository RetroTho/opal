# Opal Documentation

Accurate as of **Nov. 15th, 2023**

## Surrounders

### Scope

- Opens with a left curly bracket and closes with a right curly bracket.
- Holds statements.

#### Ex:

> {  
> *statement1*  
> *statement2*  
> }

### Detailer

- Opens with a left parenthesis and closes with a right parenthesis.
- Holds details of its caster.
- Details are seperated by commas.

#### Ex:

> (*detail*)  
> OR  
> (*detail1*, *detail2*, ...)

### String

- Opens and closes with single quotation marks.
- Holds any characters other than single quotation marks.

#### Ex:

> 'hello'

## Primative Data Types

### Integer

- A basic integer number.

#### Ex:

> **Keyword**  
> int  
> **Value**  
> 10

### String

- A basic string.
- Use string surrounder to form a string.

#### Ex:

> **Keyword**  
> str  
> **Value**  
> 'hello'

## Binary Operations

### (Re)Assignment

- Used to assign a value to a specified identifier.

#### Ex:

> x = 10  
> OR  
> y = 'hello'

### Addition

- Used to add numbers.

#### Ex:

> 2 + 2  
> OR  
> 1 + 10 + 100

### Subtraction

- Used to subtract numbers.

#### Ex:

> 2 - 2  
> OR  
> 100 - 10 - 1

### Multiplication

- Used to multiply numbers.

#### Ex:

> 2 * 2  
> OR  
> 1 * 10 * 100

### Division

- Used to divide numbers.

#### Ex:

> 2 / 2  
> OR  
> 100 / 10 / 1

### Equality

- Used to check equality of numbers.

#### Ex:

> 2 == 2  
> OR  
> 10 == 5 + 5

## Details

### Returns

- Sets the return data type of a function.

#### Ex:

> returns(int)

### Takes

- Sets an argument of a function's identifier and data type.

#### Ex:

> takes(int, *ident*)
> OR
> takes(str, *ident*)

## Declaration Initializers

### Variable

- Used to initialize the declaration of a variable.
- Should be followed by an identifier, then a detailer.

#### Ex:

> **variable** *ident*(int)  
> ***OR***  
> **variable** *ident*(int, *int*)

### Function

- Used to initialize the declaration of a function.
- Should be followed by an identifier, then a detailer, and finally a scope.

#### Ex:

> **function** *ident*(*detail1*, *detail2*){  
> *statement*  
> }

## Built-In Statements

### Exit

- Exits the program with specified exit value.

#### Ex:

> **exit**(10)

### Print

- Prints given value to console.

#### Ex:

> **print**(10)  
> OR  
> **print**('hello')

### If

- Executes scope if an expression evaluates to true.

#### Ex:

> **if**(1 == 1){  
> *statement*  
> }

### While

- Executes scope while an expression evaluates to true, checking the expression each time at the end of the scope.

#### Ex:

> **while**(1 == 1){  
> *statement*  
> }

### Return

- Returns specified value from function and ends function.

#### Ex:

> **return**(10)

### Function Call

- Calls a function.

#### Ex:

> ***ident***()  
> OR  
> ***ident***(*arg1*, *arg2*)
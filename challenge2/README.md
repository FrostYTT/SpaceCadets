# Bare Bones Language

## Assumptions

### Comments

In this implementation, a `#` character introduces a comment, which continues to the end of the source line.


---
### Reserved words:

The words in the following list are reserved, and may not be used as identifiers:

- clear
- copy
- decr
- do
- end
- incr
- not
- to
- while

Reserved words are case-insensitive.

---
### Identifiers:

Identifiers must begin with an alphabetic character, and may contain alphabetic, numeric, and underscore characters.  Identifiers are case-insensitive, thus "FOO", "Foo", and "foo" are the same identifier.  Reserved words may not be used as identifiers.

---
### Variables:

In Bare Bones, variables are named by an identifier and may contain any arbitrarily large non-negative integer values.

---
### I/O:

Bare Bones does not provide any I/O facilities.  Input may be accomplished by using the "clear" and "incr" statements in the program.

The state of variables is alwas output when the program halts, and by default also upon the interpretation and execution of each line (this can be disabled by running the interpreter with `-s` or `--silent` in terminal).

Variable names and contents will be printed to standard output.

---
### Statements:

    clear <var>;            # Set the variable to zero.

    incr <var>;             # Increment the value of the variable.

    decr <var>;             # Decrement the value of the variable,
                            # except that if the value was already zero,
                            # it remains zero.

    while <var> not 0 do;   # Loop while the variable's value is not zero.
      <statements>          # may contain one or more statements, including
    end;                    # nested while loops.  If the statements do not
                            # alter the value of the loop variable, the loop
                            # will never terminate.

    copy <var> to <var>;    # Copy one variable to another, preserving
                            # value of original.

---
### Language extensions

The `init` extension will not be used in this implementation.

---
## Usage:

BareBones should be invoked from the command line with the name of
the source file given as an argument:

```
barebones prog1.bb
```

By default, any reference to an uninitialized variable, other than in a clear statement, will result in a run time error.

---
### Bare Bones Sample Program

One sample Bare Bones program is provided in the "examples" subdirectory. factorial.bb computes the factorial of a (small) positive integer. It is configured to 3 by default.

To compute the factorial of 3:

```
barebones examples/factorial.bb
```
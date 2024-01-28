# Compiler Project

run the program with this commands.

## Phase 1 (Lexer)
```bash
python lexer.py input_file output_file
```
## Phase 2 (Parser)
```bash
python parser.py input_file output_file
```
or defer output_file to print to stdout.

## Phase 3 (Code Generator)
```bash
python code_gen.py input_file output_file
```
or defer output_file to print to stdout.

then compile the output_file with a C compiler (for example gcc) and run it.

```bash
gcc output_file
./a.out
```

# For Future
maybe create a real runtime or use LLVM project to get this to a real compiler (that needs C++ so no)

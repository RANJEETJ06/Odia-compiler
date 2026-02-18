import sys
import pickle
import os
from lexer import lexer
from parser import parser
from interpreter import interpreter

def build(file_path):
    if not file_path.endswith('.od'):
        print("Error: Kebala .od file compile haba.")
        return

    with open(file_path, 'r') as f:
        code = f.read()

    tokens = lexer(code)
    print(tokens)
    ast = parser(tokens)
    print(ast)  

    if ast:
        # Create a binary compiled file (.odc)
        output_file = file_path + "c"
        with open(output_file, 'wb') as f:
            pickle.dump(ast, f)
        print(f"Successfully compiled: {output_file}")

def run(compiled_file):
    if not compiled_file.endswith('.odc'):
        print("Error: Compiled (.odc) file dakar.")
        return

    try:
        with open(compiled_file, 'rb') as f:
            ast = pickle.load(f)
        interpreter(ast)
    except Exception as e:
        print(f"Runtime Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:\n  od build <file>.od\n  od run <file>.odc")
    else:
        command = sys.argv[1]
        path = sys.argv[2]
        
        if command == "build":
            build(path)
        elif command == "run":
            run(path)

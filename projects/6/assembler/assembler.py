import argparse
import os

from parser import Parser
from code import Code

def main():
    # Create an argument parser
    arg_parser = argparse.ArgumentParser(description="Hack Assembler")
    arg_parser.add_argument("input_file", type=str, help="Path to the input .asm file")
    
    # Parse the arguments
    args = arg_parser.parse_args()
    
    # Access the input file path
    input_file_path = args.input_file
    
    # Automatically generate the output file path by replacing .asm with .hack
    output_file_path = os.path.splitext(input_file_path)[0] + ".hack"
    
    print(f"Input file: {input_file_path}")
    print(f"Output file: {output_file_path}")

    # Create an instance of the parser class
    p = Parser(input_file_path)

    # Create an instance of the code class
    c = Code()

    # Open the output file for writing
    with open(output_file_path, 'w') as output_file:
        while p.hasMoreLines():
            p.advance()
            print(f"Line Number: {p.current_line_num}")
            print(f"Current Line: {p.current_line}")

            # Decode the instruction
            if p.instructionType() == "A_INSTRUCTION":
                print(f"A Instruction: {p.symbol()}")

                # Convert to binary
                symbol = p.symbol()
                binary_code = format(int(symbol), '016b')

                print(f"Binary Code: {binary_code}")
                output_file.write(binary_code + '\n')

            elif p.instructionType() == "C_INSTRUCTION":
                print(f"C Instruction: dest={p.dest()}, comp={p.comp()}, jump={p.jump()}")

                # Convert to binary
                dest = c.dest(p.dest())
                comp = c.comp(p.comp())
                jump = c.jump(p.jump())
                binary_code = f"111{comp}{dest}{jump}"

                print(f"Binary Code: {binary_code}")
                output_file.write(binary_code + '\n')

            elif p.instructionType() == "L_INSTRUCTION":
                print(f"L Instruction: {p.symbol()}")
            else:
                print("Unknown instruction type")

if __name__ == "__main__":
    main()

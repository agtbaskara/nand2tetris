import argparse
import os

from parser import Parser
from code import Code
from symboltable import SymbolTable

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

    # Create an instance of the symbol table class
    s = SymbolTable()

    # First pass: Populate the symbol table
    print(" ============== First Pass ================= ")

    ram_address = 16
    rom_address = 0

    # Parse L_INSTRUCTION and add them to the symbol table
    print(" =============== First Pass: L_INSTRUCTION ================= ")
    while p.hasMoreLines():
        p.advance()
        print(f"Line Number: {p.current_line_num}")
        print(f"Current Line: {p.current_line}")

        # Check for L_INSTRUCTION
        if p.instructionType() == "L_INSTRUCTION":
            label = p.symbol()
            print(f"L Instruction: {label}")

            # Add the label to the symbol table with the current line number
            s.addEntry(label, rom_address)
            print(f"Added label {label} to symbol table with address {rom_address}")

        # Increment the ROM address for A_INSTRUCTION and C_INSTRUCTION
        if p.instructionType() != "L_INSTRUCTION":
            rom_address += 1

    # Parse A_INSTRUCTION and add them to the symbol table
    print(" ================ First Pass: A_INSTRUCTION ================= ")
    p = Parser(input_file_path)

    while p.hasMoreLines():
        p.advance()
        print(f"Line Number: {p.current_line_num}")
        print(f"Current Line: {p.current_line}")

        # Check for A_INSTRUCTION
        if p.instructionType() == "A_INSTRUCTION":
            symbol = p.symbol()
            print(f"A Instruction: {symbol}")

            # If the symbol is not a digit, check if it's already in the symbol table
            if not symbol.isdigit():
                if not s.contains(symbol):
                    # Add the symbol to the symbol table with the current RAM address
                    s.addEntry(symbol, ram_address)
                    print(f"Added symbol {symbol} to symbol table with address {ram_address}")
                    ram_address += 1

    print(" ============== Symbol Table ================= ")
    for symbol, address in s.symbol_table.items():
        print(f"{symbol}: {address}")

    # Second pass: Cconvert instructions to binary
    print(" ============== Second Pass ================= ")

    # Reset the parser for the second pass
    p = Parser(input_file_path)

    # Open the output file for writing
    with open(output_file_path, 'w') as output_file:
        while p.hasMoreLines():
            p.advance()
            print(f"Line Number: {p.current_line_num}")
            print(f"Current Line: {p.current_line}")

            # Decode the instruction
            if p.instructionType() == "A_INSTRUCTION":
                print(f"A Instruction: {p.symbol()}")

                symbol = p.symbol()

                # If the symbol is not a digit, get its address from the symbol table
                if not symbol.isdigit():
                    symbol = s.getAddress(symbol)
                
                # Convert to binary
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

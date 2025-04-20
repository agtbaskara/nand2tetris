class Parser():
    def __init__(self, input_file_path):
        """
        Initialize the parser
        """
        self.input_file_path = input_file_path
        self.file = open(input_file_path, 'r')

        self.current_line_num = 0
        self.current_line = ""
        
    def hasMoreLines(self):
        """
        Return true if there are more lines in the input
        """
        # Save the current position in the file
        current_position = self.file.tell()
        
        # Check if there's more content by reading the next line
        next_line = self.file.readline()
        
        # Restore the file pointer to the original position
        self.file.seek(current_position)
        
        # Return True if the next line is not empty
        return bool(next_line.strip())

    def advance(self):
        """
        Read the next line from the input file and remove comments and whitespace
        """
        # Read the next line from the input file
        self.current_line = self.file.readline().strip()
        
        # Increment the line number
        self.current_line_num += 1
        
        # Remove comments and whitespace
        self.current_line = self.current_line.split("//")[0].strip()
        
        # Skip empty lines
        if not self.current_line:
            return self.advance()

    def instructionType(self):
        """
        Return the type of the current instruction
        """
        if self.current_line.startswith("@"):
            return "A_INSTRUCTION"
        elif self.current_line.startswith("("):
            return "L_INSTRUCTION"
        else:
            return "C_INSTRUCTION"
    
    def symbol(self):
        """
        Return the symbol of the current instruction
        """
        if self.instructionType() == "A_INSTRUCTION":
            return self.current_line[1:]
        elif self.instructionType() == "L_INSTRUCTION":
            return self.current_line[1:-1]
        else:
            raise ValueError("Invalid instruction type for symbol()")
        
    def dest(self):
        """
        Return the destination of the current instruction
        """
        if self.instructionType() == "C_INSTRUCTION":
            if "=" in self.current_line:
                return self.current_line.split("=")[0]
            else:
                return "null"
        else:
            raise ValueError("Invalid instruction type for dest()")
        
    def comp(self):
        """
        Return the computation of the current instruction
        """
        if self.instructionType() == "C_INSTRUCTION":
            if "=" in self.current_line:
                return self.current_line.split("=")[1].split(";")[0]
            else:
                return self.current_line.split(";")[0]
        else:
            raise ValueError("Invalid instruction type for comp()")

    def jump(self):
        """
        Return the jump of the current instruction
        """
        if self.instructionType() == "C_INSTRUCTION":
            if ";" in self.current_line:
                return self.current_line.split(";")[1]
            else:
                return "null"
        else:
            raise ValueError("Invalid instruction type for jump()")

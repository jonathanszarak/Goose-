import sys

class GooseScriptInterpreter:
    def __init__(self):
        self.variables = {}

    def execute(self, code):
        lines = code.strip().split('\n')
        line_number = 0

        while line_number < len(lines):
            line = lines[line_number].strip()

            # Skip empty lines and comments
            if not line or line.startswith("//"):
                line_number += 1
                continue

            # Check for variable assignment
            if line.startswith(('string', 'int', 'float')) and '=' in line:
                parts = line.split('=')
                if len(parts) != 2:
                    print(f"Syntax error at line {line_number + 1}: Invalid variable assignment")
                    return

                var_declaration, var_value = map(str.strip, parts)
                var_type, var_name = var_declaration.split()

                if var_type not in ['string', 'int', 'float']:
                    print(f"Syntax error at line {line_number + 1}: Invalid variable type")
                    return

                if var_value.endswith(';'):
                    var_value = var_value[:-1].strip()
                else:
                    print(f"Syntax error at line {line_number + 1}: Missing semicolon")
                    return

                if var_value.startswith('"') and var_value.endswith('"'):
                    var_value = var_value[1:-1]

                self.variables[var_name] = var_value

            # Check for print statement
            elif line.startswith('print(') and line.endswith(');'):
                content = line[len('print('):-2].strip()

                # Check if content is a variable
                if content in self.variables:
                    print(self.variables[content])  # Print variable value
                else:
                    # Check if content is a string
                    if content.startswith('"') and content.endswith('"'):
                        print(content[1:-1])  # Print string without quotes
                    else:
                        # Check if content is a combination of string and variable
                        parts = content.split('+')
                        if len(parts) == 2:
                            str_content = parts[0].strip()
                            var_content = parts[1].strip()

                            if str_content.startswith('"') and str_content.endswith('"'):
                                str_content = str_content[1:-1]
                            else:
                                print(f"Syntax error at line {line_number + 1}: Invalid string format")
                                return

                            if var_content in self.variables:
                                print(str_content, self.variables[var_content])
                            else:
                                print(f"NameError: name '{var_content}' is not defined at line {line_number + 1}")
                                return
                        else:
                            print(f"Syntax error at line {line_number + 1}: Invalid statement")
                            return

            # Check for input statement
            elif line.startswith('input(') and line.endswith(');'):
                parts = line[len('input('):-2].strip().split('+')
                if len(parts) != 2:
                    print(f"Syntax error at line {line_number + 1}: Invalid input statement")
                    return

                input_message, var_name = map(str.strip, parts)

                if input_message.startswith('"') and input_message.endswith('"'):
                    input_message = input_message[1:-1]

                user_input = input(input_message)
                self.variables[var_name] = user_input

            elif line.startswith('if ') and ' == ' in line and line.endswith(' then'):
                parts = line.split('==')
                if len(parts) != 2:
                    print(f"Syntax error at line {line_number + 1}: Invalid if statement")
                    return

                condition, logic = map(str.strip, parts)
                condition = condition[3:].strip()

                if condition in self.variables:
                    if self.variables[condition] == logic:
                        # Find the corresponding 'then' for the block
                        block_start = line_number + 1
                        block_end = None
                        for i in range(block_start, len(lines)):
                            if lines[i].strip().endswith('then'):
                                block_start = i + 1
                                break
                        for j in range(block_start, len(lines)):
                            if lines[j].strip() == 'end':
                                block_end = j
                                break
                        if block_end is None:
                            print(f"Syntax error at line {line_number + 1}: Missing 'end'")
                            return
                        else:
                            self.execute('\n'.join(lines[block_start:block_end]))
                            line_number = block_end
                    else:
                        # Skip the block
                        for i in range(line_number + 1, len(lines)):
                            if lines[i].strip() == 'end':
                                line_number = i
                                break
                else:
                    print(f"NameError: name '{condition}' is not defined at line {line_number + 1}")
                    return

            # Check for else if statement
            elif line.startswith('else if ') and ' == ' in line and line.endswith(' then'):
                parts = line.split('==')
                if len(parts) != 2:
                    print(f"Syntax error at line {line_number + 1}: Invalid else if statement")
                    return

                condition, logic = map(str.strip, parts)
                condition = condition[7:].strip()

                if condition in self.variables:
                    if self.variables[condition] == logic:
                        # Find the corresponding 'then' for the block
                        block_start = line_number + 1
                        block_end = None
                        for i in range(block_start, len(lines)):
                            if lines[i].strip().endswith('then'):
                                block_start = i + 1
                                break
                            for j in range(block_start, len(lines)):
                                if lines[j].strip() == 'end':
                                    block_end = j
                                    break
                            if block_end is None:
                                print(f"Syntax error at line {line_number + 1}: Missing 'end'")
                                return
                            else:
                                self.execute('\n'.join(lines[block_start:block_end]))
                                line_number = block_end
                    else:
                        # Skip the block
                        for i in range(line_number + 1, len(lines)):
                            if lines[i].strip() == 'end':
                                line_number = i
                                break
                else:
                    print(f"NameError: name '{condition}' is not defined at line {line_number + 1}")
                    return
                
            elif line.startswith('calc(') and line.endswith(');'):
                content = line[len('calc('):-2].strip()

                # Split the content into variable names and operator
                parts = content.split()
                if len(parts) != 3:
                    print(f"Syntax error at line {line_number + 1}: Invalid arithmetic operation")
                    return

                var_name_a, operator, var_name_b = map(str.strip, parts)

                # Check if var_name_a and var_name_b are valid variables
                if var_name_a not in self.variables:
                    print(f"NameError: name '{var_name_a}' is not defined at line {line_number + 1}")
                    return

                if var_name_b not in self.variables:
                    print(f"NameError: name '{var_name_b}' is not defined at line {line_number + 1}")
                    return

                # Get the values of variables a and b
                value_a = self.variables[var_name_a]
                value_b = self.variables[var_name_b]

                # Perform the calculation
                try:
                    if operator == '+':
                        result = float(value_a) + float(value_b)
                    elif operator == '-':
                        result = float(value_a) - float(value_b)
                    elif operator == '*':
                        result = float(value_a) * float(value_b)
                    elif operator == '/':
                        result = float(value_a) / float(value_b)
                    else:
                        print(f"Syntax error at line {line_number + 1}: Invalid operator '{operator}'")
                        return
                    
                    print(result)
                except Exception as e:
                    print(f"Error evaluating expression at line {line_number + 1}: {e}")
                    return


            else:
                print(f"Syntax error at line {line_number + 1}: Invalid statement")
                return

            line_number += 1

# Function to execute GooseScript code from file
def execute_goose_script(filename):
    try:
        with open(filename, 'r') as file:
            script = file.read()

        interpreter = GooseScriptInterpreter()
        interpreter.execute(script)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

# Command-line interface (CLI)
if __name__ == "__main__":
    # Check if the user provided a filename as an argument
    if len(sys.argv) != 2:
        print("Usage: python goose_interpreter.py <filename.gpp>")
        sys.exit(1)

    # Extract the filename from the command-line arguments
    filename = sys.argv[1]

    # Execute the GooseScript code
    execute_goose_script(filename)

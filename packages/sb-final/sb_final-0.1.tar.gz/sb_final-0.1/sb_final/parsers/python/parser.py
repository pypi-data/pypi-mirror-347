# remove blank lines before splitting
# blank line is breaking the code
import ast

class PythonBlockParser:
    def seperateImport(self,code):
        import_lines = []
        tree = ast.parse(code)
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    import_lines.append(f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    import_lines.append(f"from {module} import {alias.name}")

        return import_lines
    
    def clean_parsed_code(self,chunks):
        processed_chunks = []
        memory = []

        for chunk in chunks:
            if "import " in chunk:
                if chunk.count("import ") > 1:
                    for i in self.seperateImport(chunk):
                        processed_chunks.append(i)
                else:
                    processed_chunks.append(chunk)
                continue #start over

            memory.append(chunk)
            if not chunk.startswith("@"):
                processed_chunks.append("\n".join(memory))
                memory = [] #clear memory

        return processed_chunks
    
    def parse_code(self, code_string):
        """Parse Python code into top-level blocks."""
        lines = code_string.split('\n')
        
        blocks = []
        current_block = []
        stack = []  # For tracking delimiters (), [], {}
        
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()
            
            # Skip empty lines between blocks
            if not line.strip():
                if current_block:
                    blocks.append('\n'.join(current_block))
                    current_block = []
                i += 1
                continue
            
            # Calculate indentation
            indent = len(line) - len(line.lstrip())
            
            # Start of a new block
            if not current_block:
                current_block = [line]
                stack = self._update_delimiter_stack(line, [])
                i += 1
                continue
            
            # If we're at the top level (no indent) and there's no open delimiters
            if indent == 0 and not stack and not self._is_incomplete_line(current_block[-1]):
                stripped = line.lstrip()
                # If this is a new top-level construct, start a new block
                if not (stripped.startswith(('elif', 'else', 'except', 'finally'))):
                    blocks.append('\n'.join(current_block))
                    current_block = [line]
                    stack = self._update_delimiter_stack(line, [])
                else:
                    # Continue the current block for elif/else/except/finally
                    current_block.append(line)
            else:
                # Add to current block
                current_block.append(line)
                stack = self._update_delimiter_stack(line, stack)
            
            i += 1
        
        # Add the last block if exists
        if current_block:
            blocks.append('\n'.join(current_block))
        
        new_blocks = [blocks[0]]

        for i in range(1,len(blocks)):
            chunk = blocks[i]
            # print(f"line {chunk}\n\n")
            stack = []
            lines = chunk.split("\n")
            # print(type(chunk)," ",chunk)

            for line in lines:
                stack,has_close_but_no_opening = self._has_close_but_no_opening(line.strip(),stack)


            if chunk.startswith("    ") or has_close_but_no_opening:
                new_blocks[-1] += f"\n\n{chunk}"
            else:
                new_blocks.append(chunk)

        return self.clean_parsed_code(new_blocks)
    
    def _update_delimiter_stack(self, line, stack):
        """Update the stack of delimiters for the line."""
        delimiters = {'(': ')', '[': ']', '{': '}'}
        
        for char in line:
            if char in delimiters:
                stack.append(char)
            elif char in delimiters.values():
                if stack and delimiters[stack[-1]] == char:
                    # print("popping ",line)
                    stack.pop()
        
        return stack
    
    def _has_close_but_no_opening(self, line, stack):
        """Update the stack of delimiters for the line."""
        delimiters = {'(': ')', '[': ']', '{': '}'}
        has_close_but_no_opening = False

        for char in line:
            if char in delimiters:
                stack.append(char)
            elif char in delimiters.values():
                if stack and delimiters[stack[-1]] == char:
                    # print("popping ",line)
                    has_close_but_no_opening = False
                    stack.pop()
                else:
                    has_close_but_no_opening = True
        
        return [stack,has_close_but_no_opening]
    
    def _is_incomplete_line(self, line):
        """Check if the line appears incomplete (e.g., ends with operator)."""
        operators = ['=', '+', '-', '*', '/', '%', '&', '|', '^', ',0', '\\']
        stripped = line.rstrip()
        return any(stripped.endswith(op) for op in operators)


def unindentCode(code):
    block = []
    lines = code.split("\n")
    start = lines[0]
    indent = 0

    for char in start:
        if char == " ":
            indent += 1

    for line in lines:
        while len(line[:indent].strip()) > 0:
            indent -= 1
        # print(line[:indent], "data")
        block.append(line[indent:].strip())
    
    return "\n".join(block)

def indentCode(code, indent=4):
    block = []
    lines = code.split("\n")
    start = lines[0]

    for line in lines:
        block.append(f"{" "*indent}{line}")
    
    return "\n".join(block) 
    
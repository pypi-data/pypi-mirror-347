import re
import ast

from sb_final.utils.var_utils import get_assigned_variables

pattern = r'\b(?:\w+\.)+\w+[,]?\b'

def reformatLine(line, project_name):
    line = line.split(".")
    feature = line.pop()
    file = line.pop()

    if file == project_name:
        return ["/".join(line) + "/" + file + "/" + feature + ".py", "__all__"]
    else:
        file += ".py"

    return ["/".join(line) + "/" + file, feature]

def getFileDependencies(code,project_name):
    matches = re.findall(pattern, code)
    dependencies = []

    for i in matches:
        dependencies.append(reformatLine(i,project_name))

    return dependencies

def extract_words_from_code(code):
    if code == None:
        return set()
    # Remove strings and comments
    code = re.sub(r'(".*?"|".*?")', '', code)  # Remove strings
    code = re.sub(r'#.*', '', code)  # Remove comments
    
    # Extract words using regex (identifiers, keywords, function names, variable names)
    words = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', code)
    
    return set(words)

def getBlockDependencies(block, all_blocks):
    importLine = []
    block_words = extract_words_from_code(block)

    # Get assigned variables in the current block
    assigned_vars = get_assigned_variables(block)

    # Remove assigned variables from the dependencies list
    filtered_words = [word for word in block_words if word not in assigned_vars]
    
    filtered_chunks = []
    other_chunks = [] # for class and functions

    # Exclude class and function definitions from all_blocks
    for chunk in all_blocks:
        stripped_chunk = chunk.strip()
        if not (stripped_chunk.startswith("class ") or stripped_chunk.startswith("def ")):
            filtered_chunks.append(chunk)
        else:
            if block != chunk:
                other_chunks.append(chunk)

    all_words = set()

    # Manage imports
    for line in filtered_chunks:
        if "import" in line:
            if "from " in line:
                package_name = line.split("import")[0].split("from")[1].strip()
            else:
                package_name = line.split("import")[1].strip()
                
            if len(package_name) > 0:
                # if package_name not start with .
                # go to our root folder and try and find the file
                # if package_name.startswith(".") or isFileInRoot(package_name) == True:
                char = extract_words_from_code(line.split("import")[1])
                for word in char:
                    if word in filtered_words:
                        all_words.add(word)
                        importLine.append({"packagePath":package_name,"imports":word})
        else:
            # variables line declaration
            # print("here with line ", line)
            varNames = get_assigned_variables(line)
            for word in varNames:
                if word in filtered_words:
                    all_words.add(word)
                    importLine.append({"packagePath":".","imports":word})

    # manage class and functions
    for chunk in other_chunks:
        # print(chunk)
        name = chunk.split("(")[0]
        name = name.replace("def","")
        name = name.replace("class","").strip()
        # print(name)
        if name in filtered_words:
            importLine.append({"packagePath":".","imports":name})

    return importLine

def get_code_block_names(code,block_name):
    # print(f"code {block_name} ",code, " \n\n\n")
    try:
        tree = ast.parse(code.strip())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):  # Function names
                return node.name == block_name
            elif isinstance(node, ast.ClassDef):  # Class names
                return node.name == block_name
            elif isinstance(node, ast.Assign):  # Direct assignments (x = 5, x, y = 10, 20)
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if target.id == block_name: return True
    except:
        # pass
        # print(code," error jumbo ",block_name)

        return False

def getCodeBlockFromFile(blockName, file_dependencies):
    for chunk in file_dependencies:
        if get_code_block_names(chunk,blockName):
            return chunk
    return None

def removeDuplicates(code):
    cleaned_code = []
    for line in code:
        if line not in cleaned_code:
            cleaned_code.append(line)

    return cleaned_code

def get_if_blocks(code):
    tree = ast.parse(code.strip())
    if_blocks = []

    for node in ast.walk(tree):
        if isinstance(node, ast.If):  # Capture if statements
            if_block = {
                "type": "if",
                "condition": ast.unparse(node.test) if hasattr(ast, "unparse") else "<condition>",
                "body": ast.unparse(node.body) if hasattr(ast, "unparse") else "<body>",
            }
            if_blocks.append(if_block)

            # Process the `orelse` part which may contain elif or else blocks
            else_body = []
            for elif_node in node.orelse:
                if isinstance(elif_node, ast.If):  # Elif case
                    elif_block = {
                        "type": "elif",
                        "condition": ast.unparse(elif_node.test) if hasattr(ast, "unparse") else "<condition>",
                        "body": ast.unparse(elif_node.body) if hasattr(ast, "unparse") else "<body>",
                    }
                    if_blocks.append(elif_block)
                else:  # Else block (contains multiple statements)
                    else_body.append(ast.unparse(elif_node) if hasattr(ast, "unparse") else "<body>")

            if else_body:  # Capture the entire else block as a single entity
                else_block = {
                    "type": "else",
                    "body": "\n".join(else_body)
                }
                if_blocks.append(else_block)

    return if_blocks

def getCodeBlockNameAndType(code, returnVal=False):
    # print(code)
    tree = ast.parse(code.strip())

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):  # Direct assignments (x = 5, x, y = 10, 20)
            for target in node.targets:
    
                if isinstance(target, ast.Name):
                    var_name =  target.id
                
                     # Get the assigned value
                    value = node.value
                    var_type = None  # Default type

                    if isinstance(value, ast.Constant):  # Handles literals (Python 3.8+)
                        var_type = type(value.value).__name__
                    elif isinstance(value, ast.List):
                        var_type = "list"
                    elif isinstance(value, ast.Dict):
                        var_type = "dict"
                    elif isinstance(value, ast.Tuple):
                        var_type = "tuple"
                    elif isinstance(value, ast.Set):
                        var_type = "set"
                    elif isinstance(value, ast.Call):  # Function call
                        var_type = "function_call"
                    elif isinstance(value, ast.BinOp):  # Binary operations (e.g., x + y)
                        var_type = "expression"

                    # print("data ", var_name," ",var_type, " ", val_value)
                    if returnVal:
                        return [var_name,var_type,value]
                    
                    return [var_name,var_type]
                
        elif isinstance(node, ast.If):  # Capture if statements
            condition = ast.unparse(node.test) if hasattr(ast, "unparse") else "<condition>"
            # print(condition, " is this")
            return ["if_"+condition,"if_statement"]

    return None

def remove_multiline_comments(code: str) -> str:
    """
    Removes all multi-line comments (triple-quoted strings that are not docstrings) from Python code.
    """
    pattern = re.compile(r'(""".*?"""|\'\'\'.*?\'\'\')', re.DOTALL)
    
    def replacer(match):
        # Keep docstrings in functions and classes
        before = code[:match.start()].strip().split('\n')
        if before and (before[-1].startswith("def ") or before[-1].startswith("class ")):
            return match.group(0)
        return ""
    
    return pattern.sub(replacer, code)

def removeMethodsFromChunk(chunk):
    """
        Remove methods from class definitions
    """
    lines = chunk.split("\n")
    classWithoutMethod = [lines.pop(0)]

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("def ") or stripped_line.startswith("@"):
            break
        classWithoutMethod.append(line)
    
    return "\n".join(classWithoutMethod)

def arrangeChunks(data,arranged_chunks,processed):
    code_to_name = {}
    sorted_chunks = []

    for chunk in data:
        name = get_assigned_variables(chunk,True)
        code_to_name[name] = chunk

    chunk_order = getArrangeChunksOrder(data,arranged_chunks,processed)
    for i in chunk_order:
        sorted_chunks.append(code_to_name[i])

    return sorted_chunks

def getArrangeChunksOrder(data,arranged_chunks,processed):
    stack = []

    data = [removeMethodsFromChunk(i) for i in data]
    # print(data, "\n\ncleaned\n\n")

    for chunk in data:
        name = get_assigned_variables(chunk,True)
        # chunk_without_method = removeMethodsFromChunk(chunk)
        dep = getBlockDependencies(chunk,data)
        dep = [i['imports'] for i in dep if i['packagePath'] == "."]

        if len(dep) == 0:
            arranged_chunks.append(chunk)
            processed.append(name)
        else:
            addToList = True
            for c in dep:
                if c not in processed:
                    addToList = False
                    stack.append(chunk)
                    break

            if addToList:
                arranged_chunks.append(chunk)
                processed.append(name)

    if len(stack) > 0:
        # print(stack)
        # print("\n\nprocessed\n",processed)
        arranged_chunks = getArrangeChunksOrder(stack,arranged_chunks,processed)

    return processed#arranged_chunks

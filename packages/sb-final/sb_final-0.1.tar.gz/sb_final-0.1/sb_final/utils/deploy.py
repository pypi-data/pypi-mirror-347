import os
from pathlib import Path
import zipfile

from sb_final.parsers.python.parser import PythonBlockParser
from sb_final.utils.extract import getTemplateFileNames
from sb_final.utils.feature_dependencies import removeDuplicates

import yaml

from sb_final.utils.write_dependency import sortFile, writeToFile

user_home = str(Path.home())

def read_yaml(file_path):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data


def getAppFileContent(appName,fileName,project_path):
    imports = []
    code = []

    fileToUpdate = fileName.split("/")[-1]
    filePath = f"{project_path}/{appName}/{fileToUpdate}"

    with open(fileName, "r") as file:
        data = file.read()
        data = PythonBlockParser().parse_code(data)
        for chunk in data:
            if "import " in chunk:
                # individualImports = getIndividualImports(chunk)
                imports.append(chunk)
            else:
                code.append(chunk)

    return [imports,code]


def processFile(fileName,appName,project_path,template_path,feature_app_name=None,django_root=None,processed_file_path={}):
    imports = []
    code = []

    # print(project_path)

    with open(fileName,"r") as file:
        data = file.read()
        data = PythonBlockParser().parse_code(data)
        # if "admin.py" in fileName:
        #     print(data)
        for chunk in data:
            if "import " in chunk:
                # individualImports = getIndividualImports(chunk)
                imports.append(chunk)
            else:
                code.append(chunk)
    

    fileImports, fileCode = getAppFileContent(appName,fileName,project_path)

    fileCode.extend(code)
    fileImports.extend(imports)

    fileCode = removeDuplicates(fileCode)
    fileImports = removeDuplicates(fileImports)


    fileToUpdate = fileName.split("/")[-1]
    filePath = f"{project_path}/{appName}"

    django_files = ["models.py","urls.py","views.py","admin.py"]

    if "sb_app" not in fileName: # also check if filename is custom django names else write file in sb_utils folder
        # print("here broski")

        new_file_path = fileName.replace(template_path,"")
        if new_file_path.startswith("/"):
            new_file_path = new_file_path[1:]

        # print(new_file_path.split("/"), " my filename is this\n\n")

        filePath = filePath.split("/")

        write_to_project_root = len(new_file_path.split("/")) > 1
        # filePath.pop()

        if write_to_project_root:
            # print("update ", fileToUpdate)

            if fileToUpdate not in django_files:
                filePath.append("sb_utils")
                #  update import here
                new_imports = []
                for line in fileImports:
                    path,dependency = line.split("import")
                    path = path.replace("from","").replace(".sb_utils","").strip()
                    if path.startswith("."):
                        path = path[1:]

                    if f"{path}.py" in django_files:
                        new_imports.append(f"from {appName}.{path} import {dependency}")
                        continue

                    new_imports.append(line)

                fileImports = new_imports
        else:
            if django_root:
                # print(" we dey here oo help us #########################")
                # print(fileName)
                # print(f"{project_path}/{django_root}")
                filePath = [project_path,django_root]
            # settings files
            # TODO files to add to the main django folder

        filePath = "/".join(filePath)
        

        if not os.path.exists(filePath):
            os.makedirs(filePath)

    
    # update imports to remove unnecessary imports
    new_imports = []
    for line in fileImports:
        if ".sb_utils" in line:
            path,dependency = line.split("import")
            path = path.replace("from","").strip()
            path = path.replace(".sb_utils.","").strip()
            # print("sb_utils path is ", path)

            if f"{path}.py" in django_files:
                if f"{path}.py" != fileToUpdate:
                    new_imports.append(f"from .{path} import {dependency}")
                continue

            elif path in processed_file_path.keys():
                main_path = processed_file_path[path]
                new_imports.append(f"from {main_path}.{path} import {dependency}")
                continue

        new_imports.append(line)
    fileImports = new_imports

    importAsString = "\n".join(fileImports)
    codeAsString = "\n".join(fileCode)
    fileContent = importAsString + "\n\n" + codeAsString

    # print("############################# new path is ",filePath)

    writeToFile(filePath,fileContent,fileToUpdate)

    if fileToUpdate == "models.py":
        sortFile(f"{filePath}/{fileToUpdate}")

        
def getFeatureFromTemplate(template_path,project_root,template_name,django_root):
    """
    1) Ask for which app to implement feature. -- done
    2) Ask for Customization prompt and customize code. -- done
    3) Copy code and save in the right files (do proper refrencing).
    """
    app_name = input("Which django app do you want to implement feature in : ")
    app_path = f"{project_root}/{app_name}"
    feature_name = template_path.split("/")[-1].split(".")[0]
    
    # path_to_template = f"{project_root}/.sb/{template_name}"

    path_to_template = f"{user_home}/.sb/sb_extracted" #{template_name}"
    
    if not os.path.exists(path_to_template):
        os.makedirs(path_to_template, exist_ok=True)

    processed_file_path = {}

    # print("app path is ", app_path)

    if os.path.exists(app_path) and os.path.isdir(app_path):
        print("\n\n------- Generating Feature -------\n\n")

        print(f"Getting template from {template_path}")

        # # unpack template to .sb folder
        # sb_dir = f"{project_root}/.sb"
        # os.makedirs(sb_dir, exist_ok=True)

        # # clear old content from folder
        # clear_folder(sb_dir)

        template_unpack_path = f"{path_to_template}/{feature_name}"
        os.makedirs(template_unpack_path, exist_ok=True)

        # unpack
        # TODO : clear previous zip content, before unzipping again
        print("Unpacking template")
        with zipfile.ZipFile(template_path, 'r') as zip_ref:
            zip_ref.extractall(template_unpack_path)

        # Get and read template configuration file
        feature_name = template_path.split("_")[-1].replace(".zip","").strip()
        template_root = f"{path_to_template}/{template_name}"
        config_file_path = f"{template_root}/sb_{feature_name}.yaml"
        data = read_yaml(config_file_path)

        feature_app_name = data['feature_file_path'].split("/")[0]

        proceed_with_customization = False
        filtered_files = []
        root_files = []

        while True:
            customize = input("would you like to customize feature (yes or no[default]) : ")
            customize = customize.strip()

            if customize.lower() in ["yes","no","y","n"]:
                if customize.lower() == "yes" : proceed_with_customization = True
                break
            else:
                print("Enter a valid response")
                continue

        if proceed_with_customization:
            prompt = input("Enter Customization prompt (be as detailed as possible) : \n")
            # make agent call here
            # pass prompt and a list of all files in template

            # TODO : leave commented for now
            # actions = query_splitter(prompt)
            # print("all actions are \n", actions)
            # for step in actions:
            #     files = getTemplateFileNames(template_unpack_path)
 
            #     for i in files:
            #         if i not in ["settings.py", f"sb_{feature_name}.yaml"] and i.endswith("md") == False:
            #             if len(i.split("/")) == 1:
            #                 root_files.append(i)

            #             elif len(i.split("/")) > 1:
            #                 filtered_files.append(i)

            #     filtered_files = sorted(filtered_files, key=lambda x: not x.startswith('.sb_utils')) 

            #     for root_file in root_files:
            #         path_name = root_file.replace(".py","").strip()
            #         processed_file_path[path_name] = django_root 

            #     root_files.extend(filtered_files) # merge files NB, made sure root files appear first
            #     filtered_files = root_files

            #     agent(filtered_files,step,app_path,feature_name)
        else:
            files = getTemplateFileNames(template_unpack_path)
 
            for i in files:
                if i not in ["settings.py", f"sb_{feature_name}.yaml"] and i.endswith("md") == False:
                    if len(i.split("/")) == 1:
                        root_files.append(i)

                    elif len(i.split("/")) > 1:
                        filtered_files.append(i)

            filtered_files = sorted(filtered_files, key=lambda x: not x.startswith('.sb_utils')) 

            for root_file in root_files:
                path_name = root_file.replace(".py","").strip()
                processed_file_path[path_name] = django_root 

            root_files.extend(filtered_files) # merge files NB, made sure root files appear first
            filtered_files = root_files

        # TODO: print feature description, along with dependencies and fields

        # print(filtered_files)

        for file in filtered_files:
            file_path = f"{template_root}/{file}"
            # print(file_path)
            processFile(file_path,app_name,project_root,template_root,feature_app_name,django_root,processed_file_path)

    else:
        raise ValueError(f"No app with name {app_name} in {project_root}")
        return None
    
    return [app_name,template_root]

import os
import sys
from pathlib import Path

from sb_final.src.deploy_features import convertFromTemplateToFeature
from sb_final.utils.package_utils import getPackageNameMapping
from sb_final.src.extract_features import create_temp_from_feature
from sb_final.utils.utils import extract_views_from_urls, findFilePath, getAbsolutePath

def createTemplate(file_path, feature,project_name,packageToNameMapping,project_root):

    if file_path.endswith("/"):
        file_path = file_path[:len(file_path)-1]

    file_path = file_path.replace(project_root,"")

    print("\n##### Extracting Feature : ",feature," #####")

    if not os.path.exists(file_path):
        print("invalid feature")
        return

    create_temp_from_feature(
        project_root,
        project_name,
        feature,
        file_path,
        packageToNameMapping
    )

def implementFeature(template_path):
    project_root = getAbsolutePath(".")

    home = str(Path.home())
    template_path = f"{home}/.sb_zip/{template_path}"

    if not os.path.exists(template_path):
        print("invalid template")
        return
    # template_path = getAbsolutePath(args.template_path)

    template_name = template_path.split("/")[-1].replace(".zip","").strip()

    extract_path = f"{home}/.sb/sb_extracted/{template_name}"
    
    convertFromTemplateToFeature(project_root,template_path,template_name)
    print("deploying feature")

def list_features():
    user_home = str(Path.home())
    templates = os.listdir(f"{user_home}/.sb_zip")
    count = 1
    print("## ALL EXTRACTED FEATURES ##\n")
    for template in templates:
        if template.endswith(".zip"):
            print(f"    {count}) {template}")
            count += 1
    print("\n")


def handleExtract(subfolder=None,feature=None,project_path=""):
    # print("project path ", project_path)
    project_root = project_path
    # get project name from root project path
    project_name = [i.strip() for i in project_path.split("/") if len(i.strip()) > 0][-1]

    if subfolder:
        project_path += subfolder

    if not project_path.endswith("/"):
        project_path += "/"

    if feature is not None:
        # print("here ",feature)
        if project_path.endswith("/"):
            project_path = project_path[:len(project_path)-1]

        # get package to name mapping
        packageToNameMapping = getPackageNameMapping(project_root)
        print("\n#####  Extracting ",feature, "from ",project_path,"  #####\n")
        createTemplate(project_path, feature,project_name,packageToNameMapping,project_root)
        return
    
    elif subfolder and feature == None:
        if project_path.endswith("/"):
            project_path = project_path[:len(project_path)-1]

        if project_path.endswith(".py"):
            paths = project_path.split("/")
            paths.pop()
            project_path = "/".join(paths)

        if not project_path.endswith("/"): 
            project_path += "/"

        # print(project_path, " new edited path")

    urls_path = findFilePath(project_path,"urls.py")


    packageToNameMapping = getPackageNameMapping(project_root)
    # print(packageToNameMapping, " for app")

    for filePath in urls_path:
        print(f"\n{"#"*15} {filePath} {"#"*15}\n")
        abs_path = project_path + filePath
        views = extract_views_from_urls(abs_path)

        for view in views:
            view = view.split(".")
            dir_name = view[0]
            if len(dir_name) == 0:
                dir_name = "."

            file_name = view[1]
            feature_name = view[2]

            # if feature_name.endswith("/"):
            #     feature_name = feature_name[:len(feature_name)-1]

            # print("feature is ", feature_name)

            print(f"folder : {dir_name} file : {file_name}.py feature is {feature_name} ",project_path)
            createTemplate(project_path+f"views.py", feature_name,project_name,packageToNameMapping,project_root)


def main(action,secPath,feature,project_path):
    if action == "list":
        list_features()
    
    elif action == "extract":
        handleExtract(secPath,feature,project_path)
    
    elif action == "deploy":
        if secPath is not None and secPath.endswith(".zip"):
            # print("deploying ", secPath)
            implementFeature(secPath)
        else:
            print("Specify a template to deploy\n")
            print("  You can see all extracted templates by running")
            print("  sb.py list ")
    else:
        print("Please Enter a valid action")
        print("  - sb.py list    :\tto see extracted templates")
        print("  - sb.py extract :\tto extract templates")
        print("  - sb.py deploy  :\tto deploy template to a different project")


def start():

    project_path = getAbsolutePath(".")
    
    if not project_path.endswith("/"):
        project_path += "/"

    # Get the action the user want to perform
    # options : list, extract and deploy
    try:
        action = sys.argv[1]

        try:
            secondaryPath = sys.argv[2]
        except IndexError:
            secondaryPath = None

        try:
            feature = sys.argv[3]
        except IndexError:
            feature = None

        main(action,secondaryPath,feature,project_path)

    except IndexError:
        print("Please Enter a valid action kolo")
        print("  - sb.py list    :\tto see extracted templates")
        print("  - sb.py extract :\tto extract templates")
        print("  - sb.py deploy  :\tto deploy template to a different project")

if __name__ == "__main__":
    start()
    

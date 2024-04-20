import os
from pathlib import Path
from fnmatch import fnmatch
import codecs
import ast
import re

def should_ignore(path, gitignore_rules):
    for rule in gitignore_rules:
        if fnmatch(os.path.basename(path), rule):
            return True
        if os.path.isdir(path) and fnmatch(os.path.basename(path) + "/", rule):
            return True
    return False


def read_gitignore(path):
    gitignore_path = os.path.join(path, ".gitignore")
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, "r") as f:
            return [
                line.strip() for line in f if line.strip() and not line.startswith("#")
            ]
    return []


def get_python_code(file_contents):
  """
  Extracts Python code from a file.

  Args:
    file_contents: The contents of the file.

  Returns:
    The Python code, or None if no Python code is found.
  """
  python_code_regex = r"^(?!#)(.*)$"
  match = re.findall(python_code_regex, file_contents, re.MULTILINE)
  if match:
    return "\n".join(match)
  else:
    return None

def get_imports(file_contents):
  """
  Extracts import statements from a Python script.

  Args:
    file_contents: The contents of the Python script.

  Returns:
    A list of import statements.
  """

  python_code = get_python_code(file_contents)
  if python_code is None:
    return []

  tree = ast.parse(python_code)

  imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]

  return [ast.unparse(node) for node in imports]


def cli(path, include_hidden, ignore_gitignore, output_file):
  """
  Takes a path to a folder and outputs every .py file in that folder,
  recursively, each one preceded with its filename, to a text file.
  """
  gitignore_rules = [] if ignore_gitignore else read_gitignore(path)
  list_of_py = ""
  with open(output_file, "w") as f:
    for root, dirs, files in os.walk(path):
      if not include_hidden:
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        files = [f for f in files if not f.startswith(".")]
      if not ignore_gitignore:
        gitignore_rules.extend(read_gitignore(root))
        dirs[:] = [
          d
          for d in dirs
          if not should_ignore(os.path.join(root, d), gitignore_rules)
        ]
        files = [
          f
          for f in files
          if not should_ignore(os.path.join(root, f), gitignore_rules)
        ]
      for file in files:
        if file.endswith(".py") and file != "__init__.py":
          file_path = os.path.join(root, file)
          if file != "__init__.py":
             list_of_py = list_of_py + file + ","
        
          with codecs.open(file_path, "r", encoding="utf-8", errors="ignore") as file_obj:
            file_contents = file_obj.read()
          f.write(file_path + "\n")
          f.write("---\n")
          imports = get_imports(file_contents)
          # f.write(file_contents + "\n")
          for import_statement in imports:
            f.write(import_statement + "\n")
          f.write("---\n\n")
    f.write(list_of_py)

cli(path="backend", include_hidden=False, ignore_gitignore=True, output_file="results.txt")

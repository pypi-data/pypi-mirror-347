import os
import ast
from typing import Dict, Tuple

def count_functions_and_classes(file_path: str) -> Tuple[int, int]:
    """Count the number of functions and classes in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        tree = ast.parse(content)
        
        num_functions = len([node for node in ast.walk(tree) 
                           if isinstance(node, ast.FunctionDef)])
        num_classes = len([node for node in ast.walk(tree) 
                          if isinstance(node, ast.ClassDef)])
        
        return num_functions, num_classes
    except:
        return 0, 0

def get_file_size_kb(file_path: str) -> float:
    """Get file size in KB."""
    return os.path.getsize(file_path) / 1024

def count_lines(file_path: str) -> int:
    """Count number of lines in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return sum(1 for _ in file)
    except:
        return 0

def analyze_directory(directory: str) -> Dict:
    """Analyze a directory and return metrics."""
    total_size = 0
    total_files = 0
    total_functions = 0
    total_classes = 0
    total_lines = 0
    file_structure = []
    lines_by_folder = {}
    
    for root, dirs, files in os.walk(directory):
        if '.git' in root or '__pycache__' in root or '.pytest_cache' in root:
            continue
            
        relative_path = os.path.relpath(root, directory)
        if relative_path == '.':
            relative_path = ''
        
        folder_lines = 0
        folder_files = []
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip non-Python files for function/class counting
            is_python = file.endswith('.py')
            
            size_kb = get_file_size_kb(file_path)
            lines = count_lines(file_path)
            
            if is_python:
                funcs, classes = count_functions_and_classes(file_path)
                total_functions += funcs
                total_classes += classes
            else:
                funcs, classes = 0, 0
            
            total_size += size_kb
            total_files += 1
            total_lines += lines
            folder_lines += lines
            
            file_info = {
                'name': file,
                'size_kb': round(size_kb, 2),
                'lines': lines,
                'functions': funcs,
                'classes': classes
            }
            folder_files.append(file_info)
        
        if folder_files:
            file_structure.append({
                'path': relative_path,
                'files': folder_files
            })
            lines_by_folder[relative_path] = folder_lines
    
    return {
        'total_size_kb': round(total_size, 2),
        'total_files': total_files,
        'total_functions': total_functions,
        'total_classes': total_classes,
        'total_lines': total_lines,
        'file_structure': file_structure,
        'lines_by_folder': lines_by_folder
    }

def generate_report():
    """Generate and print the project analysis report."""
    print("=== BEAMZ Project Analysis Report ===\n")
    
    # Analyze the project
    project_root = '.'
    core_package = './beamz'
    
    project_metrics = analyze_directory(project_root)
    core_metrics = analyze_directory(core_package)
    
    # 1. Project File Structure
    print("1. Project File Structure:")
    for folder in project_metrics['file_structure']:
        path = folder['path']
        print(f"\n{'  ' if path else ''}{path or 'Root'}:")
        for file in folder['files']:
            print(f"  {'  ' if path else ''}{file['name']} "
                  f"({file['size_kb']:.2f}KB, {file['lines']} lines)")
    
    # 2. Project Size
    print(f"\n2. Project Size:")
    print(f"Total size: {project_metrics['total_size_kb']:.2f}KB")
    print(f"Core package size: {core_metrics['total_size_kb']:.2f}KB")
    
    # 3. Number of Files
    print(f"\n3. Number of Files:")
    print(f"Total files: {project_metrics['total_files']}")
    print(f"Core package files: {core_metrics['total_files']}")
    
    # 4. Functions and Classes
    print(f"\n4. Functions and Classes:")
    print(f"Total functions: {project_metrics['total_functions']}")
    print(f"Total classes: {project_metrics['total_classes']}")
    print(f"Core package functions: {core_metrics['total_functions']}")
    print(f"Core package classes: {core_metrics['total_classes']}")
    
    # 5. Lines of Code
    print(f"\n5. Lines of Code:")
    print("By folder:")
    for folder, lines in project_metrics['lines_by_folder'].items():
        if folder.startswith('beamz'):
            print(f"  {folder or 'Root'}: {lines} lines")
    print(f"\nCore package total: {core_metrics['total_lines']} lines")
    print(f"Project total: {project_metrics['total_lines']} lines")

if __name__ == "__main__":
    generate_report() 
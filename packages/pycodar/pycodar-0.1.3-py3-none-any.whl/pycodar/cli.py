#!/usr/bin/env python3
import argparse
from .analyze import analyze_directory
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich import box
import ast
import fnmatch

console = Console()

class TestClass:
    def __init__(self):
        self.name = "Test"

    def test_method(self):
        print("Test")


def extract_code_structure(file_path: str) -> dict:
    """Extract functions, classes, and methods from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        tree = ast.parse(content)
        structure = {
            'functions': [],
            'classes': []
        }
        
        # First pass: set parent relationships
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
        
        # Second pass: collect structure
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not hasattr(node, 'parent') or not isinstance(node.parent, ast.ClassDef):
                    # Top-level function
                    structure['functions'].append({
                        'name': node.name,
                        'lineno': node.lineno
                    })
            elif isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'lineno': node.lineno,
                    'methods': []
                }
                # Collect methods (functions defined within the class)
                for child in node.body:
                    if isinstance(child, ast.FunctionDef):
                        class_info['methods'].append({
                            'name': child.name,
                            'lineno': child.lineno
                        })
                structure['classes'].append(class_info)
        
        return structure
    except Exception as e:
        console.print(f"[yellow]Warning: Could not parse {file_path}: {str(e)}[/yellow]")
        return {'functions': [], 'classes': []}

def create_structure_tree(metrics):
    """Create a rich tree showing file structure with code elements."""
    # Start with root node
    tree = Tree("📁 Root", style="bold blue")
    
    # Sort folders and files for consistent display
    sorted_folders = sorted(metrics['file_structure'], key=lambda x: x['path'] or '')
    
    for folder in sorted_folders:
        path = folder['path'] or 'Root'
        if path == 'Root':
            # Add files directly to root if they're in the root directory
            folder_tree = tree
        else:
            folder_tree = tree.add(f"📁 {path}", style="cyan")
        
        # Sort files for consistent display
        sorted_files = sorted(folder['files'], key=lambda x: x['name'])
        
        for file in sorted_files:
            if file['name'].endswith('.py'):
                # Get code structure for Python files
                file_path = str(Path(folder['path']) / file['name']) if folder['path'] else file['name']
                structure = extract_code_structure(file_path)
                
                # Create file node with code structure
                file_node = folder_tree.add(f"📄 {file['name']}", style="yellow")
                
                # Add classes
                for class_info in structure['classes']:
                    class_node = file_node.add(f"🔷 {class_info['name']}", style="green")
                    for method in class_info['methods']:
                        class_node.add(f"🔹 {method['name']}", style="blue")
                
                # Add top-level functions
                for func in structure['functions']:
                    file_node.add(f"🔸 {func['name']}", style="magenta")
            else:
                # Non-Python files
                folder_tree.add(f"📄 {file['name']}", style="yellow")
    
    return tree

def parse_ignore_file(file_path: Path) -> list:
    """Parse an ignore file and return list of patterns."""
    if not file_path.exists():
        return []
    
    patterns = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                patterns.append(line)
    return patterns

def should_ignore(path: Path, ignore_patterns: list) -> bool:
    """Check if a path should be ignored based on patterns."""
    try:
        # Convert path to string relative to current directory
        rel_path = str(path.relative_to(Path.cwd()))
    except ValueError:
        # If path is in current directory, use just the filename
        rel_path = path.name
    
    for pattern in ignore_patterns:
        # Handle directory patterns (ending with /)
        if pattern.endswith('/'):
            if fnmatch.fnmatch(rel_path, pattern[:-1]) or \
               fnmatch.fnmatch(rel_path, pattern + '*'):
                return True
        # Handle regular patterns
        elif fnmatch.fnmatch(rel_path, pattern):
            return True
    return False

def get_ignore_patterns(base_path: Path) -> list:
    """Get combined ignore patterns from .gitignore and .codarignore."""
    codarignore_path = base_path / '.codarignore'
    gitignore_path = base_path / '.gitignore'
    
    # Get patterns from .codarignore
    codar_patterns = parse_ignore_file(codarignore_path)
    
    # Get patterns from .gitignore
    gitignore_patterns = parse_ignore_file(gitignore_path)
    
    # Always ignore the ignore files themselves
    always_ignore = ['.gitignore', '.codarignore']
    
    # Combine patterns, with .codarignore taking priority
    return always_ignore + codar_patterns + gitignore_patterns

def format_size(size_kb):
    """Format size in KB to a human-readable format."""
    if size_kb < 1024:
        return f"{size_kb:.2f}KB"
    elif size_kb < 1024 * 1024:
        return f"{size_kb/1024:.2f}MB"
    else:
        return f"{size_kb/(1024*1024):.2f}GB"

def count_code_metrics(file_path: str) -> tuple:
    """Count code, comments, and empty lines in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Parse the file
        tree = ast.parse(content)
        
        # Count comments
        comment_lines = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                comment_lines.add(node.lineno)
        
        # Count total lines and empty lines
        total_lines = len(content.splitlines())
        empty_lines = sum(1 for line in content.splitlines() if not line.strip())
        
        # Calculate code lines (total - comments - empty)
        code_lines = total_lines - len(comment_lines) - empty_lines
        
        return code_lines, len(comment_lines), empty_lines
    except:
        return 0, 0, 0

def create_metrics_table(metrics):
    """Create a rich table for basic metrics."""
    table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Total Size", format_size(metrics['total_size_kb']))
    table.add_row("Total Files", str(metrics['total_files']))
    table.add_row("Total Directories", str(metrics['total_directories']))
    table.add_row("Total Lines", f"{metrics['total_lines']:,}")
    table.add_row("Code Lines", f"{metrics['total_code_lines']:,}")
    table.add_row("Comment Lines", f"{metrics['total_comment_lines']:,}")
    table.add_row("Empty Lines", f"{metrics['total_empty_lines']:,}")
    table.add_row("Functions", f"{metrics['total_functions']:,}")
    table.add_row("Classes", f"{metrics['total_classes']:,}")
    
    return table

def create_file_table(metrics):
    """Create a rich table for file distribution."""
    table = Table(box=box.ROUNDED, show_header=True, padding=(0, 2))
    table.add_column("Path", style="cyan")
    table.add_column("File", style="yellow")
    table.add_column("Code", style="green", justify="right")
    table.add_column("Comments", style="blue", justify="right")
    table.add_column("Empty", style="magenta", justify="right")
    table.add_column("Total", style="green", justify="right")
    table.add_column("Size", style="blue", justify="right")
    
    for folder in metrics['file_structure']:
        path = folder['path'] or 'Root'
        for file in folder['files']:
            table.add_row(
                path,
                file['name'],
                f"{file['code_lines']:,}",
                f"{file['comment_lines']:,}",
                f"{file['empty_lines']:,}",
                f"{file['lines']:,}",
                format_size(file['size_kb'])
            )
    
    return table

def print_stats(metrics):
    """Print formatted statistics from the analysis."""

    # Basic Metrics
    console.print("\n[bold cyan]📊 Basic Metrics[/bold cyan]")
    console.print(create_metrics_table(metrics))
    
    # File Structure
    console.print("\n[bold cyan]🌳 File Structure[/bold cyan]")
    console.print(create_structure_tree(metrics))
    
    # File Distribution
    console.print("\n[bold cyan]📁 File Distribution[/bold cyan]")
    console.print(create_file_table(metrics))
    
    console.print("\n")

def main():
    parser = argparse.ArgumentParser(description='Code Architecture System - Code Analysis Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show code metrics and statistics')
    stats_parser.add_argument('--path', default='.', help='Path to analyze (default: current directory)')
    
    args = parser.parse_args()
    
    if args.command == 'stats':
        base_path = Path(args.path)
        if not base_path.exists():
            console.print(f"[red]Error: Path '{base_path}' does not exist[/red]", file=sys.stderr)
            sys.exit(1)
        
        # Get ignore patterns
        ignore_patterns = get_ignore_patterns(base_path)
        
        # Enhance the metrics with code analysis
        metrics = analyze_directory(str(base_path))
        
        # Add code metrics
        total_code_lines = 0
        total_comment_lines = 0
        total_empty_lines = 0
        total_directories = 0
        filtered_file_structure = []
        
        for folder in metrics['file_structure']:
            folder_path = Path(folder['path']) if folder['path'] else Path('.')
            if should_ignore(folder_path, ignore_patterns):
                continue
                
            filtered_files = []
            for file in folder['files']:
                file_path = folder_path / file['name']
                if should_ignore(file_path, ignore_patterns):
                    continue
                    
                if file['name'].endswith('.py'):
                    code_lines, comment_lines, empty_lines = count_code_metrics(str(file_path))
                    file['code_lines'] = code_lines
                    file['comment_lines'] = comment_lines
                    file['empty_lines'] = empty_lines
                    total_code_lines += code_lines
                    total_comment_lines += comment_lines
                    total_empty_lines += empty_lines
                else:
                    file['code_lines'] = 0
                    file['comment_lines'] = 0
                    file['empty_lines'] = 0
                
                filtered_files.append(file)
            
            if filtered_files:
                folder['files'] = filtered_files
                filtered_file_structure.append(folder)
                total_directories += 1
        
        metrics['file_structure'] = filtered_file_structure
        metrics['total_code_lines'] = total_code_lines
        metrics['total_comment_lines'] = total_comment_lines
        metrics['total_empty_lines'] = total_empty_lines
        metrics['total_directories'] = total_directories
        metrics['total_files'] = sum(len(folder['files']) for folder in filtered_file_structure)
        
        print_stats(metrics)
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 
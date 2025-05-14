# PyCodar: A Radar for Your Code
**A simple tool for auditing and understanding your codebase.**

```bash
pip install pycodar
```

You can then call
```bash
pycodar stats
```
in your terminal to get statistics of your directory printed out like:

```bash
📊 Basic Metrics
╭─────────────────────┬───────────╮
│  Total Size         │  49.84KB  │
│  Total Files        │  6        │
│  Total Directories  │  2        │
│  Total Lines        │  620      │
│  Code Lines         │  429      │
│  Comment Lines      │  16       │
│  Empty Lines        │  90       │
│  Functions          │  18       │
│  Classes            │  1        │
╰─────────────────────┴───────────╯

🌳 File Structure
📁 Root
├── 📄 README.md
├── 📄 pyproject.toml
├── 📄 setup.py
└── 📁 pycodar
    ├── 📄 __init__.py
    ├── 📄 analyze.py
    │   ├── 🔸 count_functions_and_classes
    │   ├── 🔸 get_file_size_kb
    │   ├── 🔸 count_lines
    │   ├── 🔸 analyze_directory
    │   └── 🔸 generate_report
    └── 📄 cli.py
        ├── 🔷 TestClass
        │   ├── 🔹 __init__
        │   └── 🔹 test_method
        ├── 🔸 extract_code_structure
        ├── 🔸 create_structure_tree
        ├── 🔸 parse_ignore_file
        ├── 🔸 should_ignore
        ├── 🔸 get_ignore_patterns
        ├── 🔸 format_size
        ├── 🔸 count_code_metrics
        ├── 🔸 create_metrics_table
        ├── 🔸 create_file_table
        ├── 🔸 print_stats
        └── 🔸 main

📁 File Distribution
╭───────────┬──────────────────┬────────┬────────────┬─────────┬─────────┬───────────╮
│  Path     │  File            │  Code  │  Comments  │  Empty  │  Total  │     Size  │
├───────────┼──────────────────┼────────┼────────────┼─────────┼─────────┼───────────┤
│  Root     │  pyproject.toml  │     0  │         0  │      0  │     43  │   1.37KB  │
│  Root     │  README.md       │     0  │         0  │      0  │      6  │   0.13KB  │
│  Root     │  setup.py        │    45  │         0  │      1  │     46  │   1.72KB  │
│  pycodar  │  __init__.py     │     7  │         1  │      3  │     11  │   0.22KB  │
│  pycodar  │  cli.py          │   260  │        10  │     60  │    330  │  12.15KB  │
│  pycodar  │  analyze.py      │   117  │         5  │     26  │    148  │   4.91KB  │
╰───────────┴──────────────────┴────────┴────────────┴─────────┴─────────┴───────────╯
```

from pathlib import Path
import argparse

class DirectoryTree:
    def __init__(self, exclude_dirs=None, exclude_files=None, show_hidden=False):
        self.exclude_dirs = set(exclude_dirs or []) | {'node_modules', '.next', '.vscode'}
        self.exclude_files = set(exclude_files or [])
        self.show_hidden = show_hidden
        self.indent_space = '    '
        self.connectors = {
            'space': '    ',
            'branch': '├── ',
            'vertical': '│   ',
            'last': '└── '
        }

    def generate(self, root_dir, max_depth=None, comments=None):
        root_dir = Path(root_dir).expanduser().resolve()
        comments = comments or {}
        return '\n'.join(self._build_tree(root_dir, max_depth, comments, [], True))

    def _build_tree(self, path, max_depth, comments, prefix, is_last):
        if max_depth is not None and len(prefix) >= max_depth:
            return []

        name = path.name
        if not self.show_hidden and name.startswith('.'):
            return []

        lines = []
        current_line = []
        
        # Build connector
        for p in prefix[:-1]:
            current_line.append(self.connectors['vertical'] if not p else self.indent_space)
        
        if prefix:
            current_line.append(self.connectors['last' if is_last else 'branch'])

        # Add name and comment
        current_line.append(name)
        if path.is_dir():
            current_line.append('/')
        
        comment = comments.get(str(path))
        if comment:
            current_line.append(f' {self._pad_comment(current_line, comment)}')
        
        lines.append(''.join(current_line))

        if path.is_dir():
            try:
                children = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
                children = [c for c in children if self._should_include(c)]
                
                for i, child in enumerate(children):
                    is_child_last = i == len(children) - 1
                    new_prefix = prefix + [is_last]
                    lines.extend(self._build_tree(
                        child, max_depth, comments, new_prefix, is_child_last
                    ))
            except PermissionError:
                lines.append(f"{''.join(current_line[:-1])}(permission denied)")

        return lines

    def _should_include(self, path):
        if path.is_dir() and path.name in self.exclude_dirs:
            return False
        if path.is_file() and path.name in self.exclude_files:
            return False
        return True

    def _pad_comment(self, line_parts, comment):
        line_length = sum(len(part) for part in line_parts)
        padding = max(40 - line_length, 2)
        return f'{" " * padding}# {comment}'

def main ():
    parser = argparse.ArgumentParser(description='Generate clean directory tree')
    parser.add_argument('path', nargs='?', default='.', help='Root directory')
    parser.add_argument('-d', '--depth', type=int, help='Maximum depth')
    parser.add_argument('-H', '--hidden', action='store_true', help='Show hidden items')
    parser.add_argument('-c', '--comments', action='store_true', help='Show comments')
    
    args = parser.parse_args()
    
    comments = {
        'src/app': 'App Router (Next.js 13+)',
        'src/components': 'Reusable UI components',
        'public/assets/images': 'Product images',
    } if args.comments else {}

    tree = DirectoryTree(
        exclude_dirs=['.git', '__pycache__'],
        show_hidden=args.hidden
    )
    
    try:
        result = tree.generate(args.path, args.depth, comments)
        print(result)
    except FileNotFoundError:
        print(f"Error: Directory not found - {args.path}")

if __name__ == '__main__':
    main()

    
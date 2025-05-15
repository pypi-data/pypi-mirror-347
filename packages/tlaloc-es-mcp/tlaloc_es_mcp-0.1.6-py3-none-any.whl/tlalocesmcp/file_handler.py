from mcp.server.fastmcp import FastMCP
import os
from pathlib import Path
import fnmatch

mcp = FastMCP(name="FileAnalicerMCP")


@mcp.tool()
def analyze_project_structure(path: str, ignore_patterns: list[str] = None) -> str:
    """
    Returns the directory tree of the given path, ignoring files/folders matching any of the ignore_patterns (like .gitignore).
    """
    if not os.path.exists(path):
        return f"The path '{path}' does not exist."
    if ignore_patterns is None:
        ignore_patterns = []

    def is_ignored(name, rel_path):
        for pattern in ignore_patterns:
            if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(rel_path, pattern):
                return True
        return False

    tree = []
    base_path = Path(path).resolve()
    for root, dirs, files in os.walk(base_path):
        rel_root = os.path.relpath(root, base_path)
        if rel_root == ".":
            rel_root = ""
        # Filter ignored directories in-place
        dirs[:] = [d for d in dirs if not is_ignored(d, os.path.join(rel_root, d))]
        level = rel_root.count(os.sep)
        indent = "  " * level
        tree.append(f"{indent}{os.path.basename(root)}/")
        subindent = "  " * (level + 1)
        for f in files:
            if not is_ignored(f, os.path.join(rel_root, f)):
                tree.append(f"{subindent}{f}")
    tree_str = "\n".join(tree)
    return tree_str


@mcp.tool()
def show_file_content(path: str) -> str:
    """
    Returns the file name and its content in raw format.
    """

    if not os.path.isfile(path):
        return f"The file '{path}' does not exist."
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        filename = os.path.basename(path)
        return f"# {filename}\n{content}"
    except Exception as e:
        return f"Error reading the file: {str(e)}"


@mcp.tool()
def write_file_content(path: str, content: str) -> str:
    """
    Writes the given content to the specified file.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Content successfully written to '{path}'."
    except Exception as e:
        return f"Error writing to the file: {str(e)}"


@mcp.tool()
def files_to_markdown(
    directory: str, filetypes: list[str] = None, ignore_patterns: list[str] = None
) -> str:
    """
    Recursively collects files in a directory matching given extensions and
    returns their content in markdown format. If no filetypes are provided,
    all files are included. The output is optimized for LLM understanding.
    Optionally ignores files/folders matching any of the ignore_patterns
    (like .gitignore).
    """
    import os
    import fnmatch

    EXT_LANG_MAP = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".json": "json",
        ".md": "markdown",
        ".sh": "bash",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".tf": "hcl",
        ".tfvars": "hcl",
        ".toml": "toml",
        ".ini": "ini",
        ".txt": "text",
        # Add more as needed
    }

    if filetypes is None or len(filetypes) == 0:
        filetypes = []  # Empty means include all files
    if ignore_patterns is None:
        ignore_patterns = []

    def is_ignored(name, rel_path):
        for pattern in ignore_patterns:
            if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(rel_path, pattern):
                return True
        return False

    def get_lang(filename):
        ext = os.path.splitext(filename)[1]
        return EXT_LANG_MAP.get(ext, "")

    def read_file_content(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            return f"Error reading {file_path}: {str(e)}"

    markdown_result = ""
    base_path = os.path.abspath(directory)
    for root, dirs, files in os.walk(base_path):
        rel_root = os.path.relpath(root, base_path)
        if rel_root == ".":
            rel_root = ""
        # Filter ignored directories in-place
        dirs[:] = [d for d in dirs if not is_ignored(d, os.path.join(rel_root, d))]
        for filename in files:
            if is_ignored(filename, os.path.join(rel_root, filename)):
                continue
            if not filetypes or any(filename.endswith(ext) for ext in filetypes):
                file_path = os.path.join(root, filename)
                content = read_file_content(file_path)
                lang = get_lang(filename)
                markdown_result += f"### {filename}\n"
                markdown_result += f"_Path: {file_path}_\n\n"
                markdown_result += f"```{lang}\n"
                markdown_result += f"{content}\n"
                markdown_result += "```\n\n"
    return markdown_result

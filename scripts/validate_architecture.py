import ast
import sys
from pathlib import Path

FORBIDDEN_FOLDERS = {"misc", "helpers", "utils"}
FORBIDDEN_DEPS = {"langchain", "crewai", "autogen", "neo4j", "redis", "celery", "kafka"}

MAX_FILE_LINES = 1000
MAX_CLASS_LINES = 600
MAX_FUNC_LINES = 100


def get_line_count(node: ast.AST, source_lines: list[str]) -> int:
    if not hasattr(node, "end_lineno") or not hasattr(node, "lineno"):
        return 0
    end_line = getattr(node, "end_lineno", getattr(node, "lineno", 0))
    start_line = getattr(node, "lineno", 0)
    return end_line - start_line + 1


def check_docs(docs_dir: Path) -> list[str]:
    errors = []
    required_docs = [
        "01_ENGINEERING_CHARTER.md",
        "02_PHASE1_MASTER_SPEC.md",
        "03_PHASE1_TDD.md",
        "04_DATA_CONTRACTS.md",
        "05_TESTING_CHARTER.md",
        "06_ACCEPTANCE_CRITERIA.md",
        "07_CODE_QUALITY_RULES.md",
        "08_OBSERVABILITY_SPEC.md",
        "09_PERFORMANCE_SPEC.md",
        "10_IMPLEMENTATION_ORDER.md",
        "11_PHASE1_IMPLEMENTATION_PROMPT.md",
    ]
    for doc in required_docs:
        if not (docs_dir / doc).exists():
            errors.append(f"Missing doc: docs/{doc}")
    return errors


def check_folders(src_dir: Path) -> list[str]:
    errors = []
    if not src_dir.exists():
        return errors
    for d in src_dir.rglob("*"):
        if d.is_dir() and d.name in FORBIDDEN_FOLDERS:
            errors.append(f"Forbidden folder: {d}")
    return errors


def analyze_ast(tree: ast.AST, py_file: Path, lines: list[str]) -> tuple[list[str], list[str]]:
    errors = []
    file_deps = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            lc = get_line_count(node, lines)
            if lc > MAX_CLASS_LINES:
                errors.append(f"Class '{node.name}' in {py_file} > {MAX_CLASS_LINES} lines")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            lc = get_line_count(node, lines)
            if lc > MAX_FUNC_LINES:
                errors.append(f"Function '{node.name}' in {py_file} > {MAX_FUNC_LINES} lines")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                base = alias.name.split(".")[0]
                if base in FORBIDDEN_DEPS:
                    errors.append(f"Forbidden dep '{base}' in {py_file}")
                file_deps.append(base)
        elif isinstance(node, ast.ImportFrom) and node.module:
            base = node.module.split(".")[0]
            if base in FORBIDDEN_DEPS:
                errors.append(f"Forbidden dep '{base}' in {py_file}")
            file_deps.append(base)
    return errors, file_deps


def check_python_files(root: Path) -> tuple[list[str], dict[str, list[str]]]:
    errors = []
    graph: dict[str, list[str]] = {}
    for py_file in root.rglob("*.py"):
        if any(p in py_file.parts for p in [".venv", ".tox", "node_modules"]):
            continue
        try:
            content = py_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        lines = content.splitlines()
        if len(lines) > MAX_FILE_LINES:
            errors.append(f"File {py_file} > {MAX_FILE_LINES} lines")
        try:
            tree = ast.parse(content, filename=str(py_file))
        except SyntaxError as e:
            errors.append(f"SyntaxError in {py_file}: {e}")
            continue
        file_errors, file_deps = analyze_ast(tree, py_file, lines)
        errors.extend(file_errors)
        graph[str(py_file.relative_to(root))] = file_deps
    return errors, graph


def find_cycles(graph: dict[str, list[str]]) -> list[str]:
    src_mods = {k for k in graph if k.startswith("src")}

    def dfs(node: str, path: list[str], visited: set[str]) -> list[str] | None:
        if node in path:
            return path[path.index(node) :] + [node]
        if node in visited:
            return None
        visited.add(node)
        path.append(node)
        for dep in graph.get(node, []):
            if not dep.startswith("src."):
                continue
            for possible_file in src_mods:
                p_mod = possible_file.replace(".py", "").replace("\\", "/").replace("/", ".")
                if p_mod.startswith(dep):
                    res = dfs(possible_file, path, visited)
                    if res:
                        return res
        path.pop()
        return None

    visited: set[str] = set()
    for src_file in src_mods:
        cycle = dfs(src_file, [], visited)
        if cycle:
            return cycle
    return []


def main() -> None:
    root = Path(__file__).parent.parent
    errors = []
    errors.extend(check_docs(root / "docs"))
    errors.extend(check_folders(root / "src"))

    py_errors, graph = check_python_files(root)
    errors.extend(py_errors)

    cycle = find_cycles(graph)
    if cycle:
        errors.append(f"Circular import: {' -> '.join(cycle)}")

    if errors:
        print("Architecture Validation Failed:")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)
    print("Architecture Validation Passed!")


if __name__ == "__main__":
    main()

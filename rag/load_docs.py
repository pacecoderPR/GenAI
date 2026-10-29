from pathlib import Path
import re


def extract_title(text: str) -> str:
    """Extract the first Markdown heading, or use the filename."""
    ...
    match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)

    if not match:
        return ""

    title = match.group(1).strip()
    title = re.sub(r"\s*\{\s*#[^}]+\}", "", title).strip()
    return title

def clean_markdown(text: str) -> str:
    # 1. Remove front matter
    text = re.sub(
        r"\A---[ \t]*\r?\n.*?\r?\n---[ \t]*(?:\r?\n|$)",
        "",
        text,
        count=1,
        flags=re.DOTALL
    )

    # 2. Remove HTML comments
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)

    # 3. Remove include macros
    text = re.sub(r"\{\*.*?\*\}", "", text, flags=re.DOTALL)

    # 4. Normalize excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # print(f"stating text: {text[:200]}")

    return text.strip()

def load_docs(docs_dir: Path, limit: int = 40) -> list[dict]:
    """Load a deterministic selection of Markdown pages."""
    ...
    if not docs_dir.exists():
        raise FileNotFoundError(f"Directory not found: {docs_dir}")

    if not docs_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {docs_dir}")

    files = sorted(docs_dir.glob("**/*.md"))
    non_empty_files = [f for f in files if f.stat().st_size > 0]
    final_files = non_empty_files[:limit]
    file_data = []
    for file in final_files:
        if not file.is_file():
            raise FileNotFoundError(f"File not found: {file}")
        if file.stat().st_size == 0:
            raise ValueError(f"File is empty: {file}")
        text = file.read_text(encoding="utf-8")
        cleaned_text = clean_markdown(text)
        title = extract_title(cleaned_text) or file.stem
        file_data.append({ "path": str(file.relative_to(docs_dir.parents[3])), "title": title, "text": cleaned_text})
    return file_data



def main():
    """Print statistics and a sample page."""
    ...
    docs_dir = Path(__file__).resolve().parent.parent.parent / "fastapi/docs/en/docs/tutorial"
    file_data = load_docs(docs_dir, limit=40)
    if not file_data:
        print("No non-empty Markdown pages found.")
        return

    # 1. Page count
    print(f"Page count: {len(file_data)}")

    # 2. Total characters across cleaned pages
    total_chars = sum(len(doc["text"]) for doc in file_data)
    print(f"Total characters: {total_chars}")

    # 3. Shortest and longest pages
    shortest = min(file_data, key=lambda doc: len(doc["text"]))
    longest = max(file_data, key=lambda doc: len(doc["text"]))

    print(f"\nShortest page: {shortest['path']}")
    print(f"Characters: {len(shortest['text'])}")

    print(f"\nLongest page: {longest['path']}")
    print(f"Characters: {len(longest['text'])}")

    # 4. First 500 characters of one cleaned page
    print("\nFirst 500 characters of a cleaned page:")
    print(file_data[0]["text"][:500])


if __name__ == "__main__":
    main()
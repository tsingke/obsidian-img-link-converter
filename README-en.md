# Obsidian Image Link Converter

A lightweight Python script to convert Obsidian-style image wiki links `![[image.png]]` to standard Markdown format `![](path/image.png)` and rename image files by replacing spaces with hyphens.

This tool enhances Markdown document compatibility across editors like Typora, VS Code, and GitHub.

---

## Features

- Prompt user to enter the image folder path dynamically
- Automatically rename image files containing spaces
- Convert Obsidian wiki-style image links to standard Markdown syntax
- Recursively process all `.md` files
- Prevent filename collisions with auto-numbering
- Supports common image formats: png, jpg, jpeg, gif, bmp, svg, webp, tiff

---

## Usage

### 1. Requirements

- Python 3.6+
- Works on Windows, macOS, Linux

Place `convert_enhanced.py` in the root directory of your Obsidian vault.

### 2. Run the Script

```bash
python3 convert_enhanced.py
```

When prompted, enter the image folder path relative to the current directory. For example:

```
Please enter the image folder path (relative to current directory): assets/images
```

The script will:

- Rename image files containing spaces
- Scan Markdown files and replace image links
- Log all progress to the terminal

---

## Example

**Before:**

```markdown
![[diagram 1.png]]
```

**After:**

```markdown
![](assets/images/diagram-1.png)
```

---

## Notes

- This script modifies files in-place. Back up your vault before use.
- Recursively processes all subdirectories.

---

## License

This project is licensed under the MIT License.

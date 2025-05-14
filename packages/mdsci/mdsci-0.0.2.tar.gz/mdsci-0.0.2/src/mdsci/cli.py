from pathlib import Path
import sys
import shutil
import subprocess
from mdsci import get_css_path

def main():
    if len(sys.argv) != 2:
        print("Usage: mdsci <input_markdown_file>")
        sys.exit(1)

    # Get input & output file paths
    input_fname = sys.argv[1]
    input_fpath = Path(input_fname)
    if not input_fpath.is_file():
        print(f"Error: File '{input_fname}' is not found.")
        sys.exit(1)
    output_fpath = input_fpath.with_suffix(".html")

    # Choose the CSS style
    css_style = "mdsci"
    css_fpath = Path(get_css_path(css_style))
    css_cmd_args = []
    if css_fpath.is_file():
        current_dir = Path.cwd()
        css_pasted_fpath = current_dir / (input_fpath.stem + "-mdsci.css")
        shutil.copy(css_fpath, css_pasted_fpath)
        css_cmd_args = ["-c", css_pasted_fpath.name]
    else:
        print(f"WARNING: CSS file '{css_fpath.name}' is not found in mdsci package.")


    # Prepare the command (filter name should be the same as in pyproject.toml)
    filter_name = "mdsci-filter"
    cmd = [
        "pandoc",
        str(input_fpath),
        "-s",
        "-f", "markdown",
        "-t", "html",
        *css_cmd_args,
        f"--filter={filter_name}",
        "-o", str(output_fpath)
    ]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()
# Stash CLI

Stash CLI is a command-line interface (CLI) tool built with Python for interacting with the FileStash server (https://filestash.xyz). It simplifies file management by using content hashes to manage uploads, downloads, analysis and listing of files.  It supports both public and private file uploads.  The tool also includes an analysis feature, enabling informative descriptions about uploaded files.

This CLI is designed to be a convenient tool for developers and users who need a way to store, share, and retrieve files securely and efficiently.  The server component is built as a proxy in front of a cloud storage bucket, with added functionalities.

## Installation

Stash CLI requires Python 3.10 or later and the `pipx` package manager. We recommend using `pipx` to manage your Python installations, which can help prevent dependency conflicts.

1. **Install or upgrade `pipx`:**
   ```bash
   pip install --user pipx
   python3 -m pipx ensurepath
   ```

2. **Install stash:**
   ```bash
   pipx install stash
   ```

Stash CLI will then be available in your system's PATH.

## Usage

### Uploading a File

```bash
stash up <file_path> [--server <server_url>] [--token <token>] [--analyze <boolean>]
```

*   `<file_path>`: Path to the file to upload (required).
*   `--server`: URL of the FileStash server. Defaults to `https://filestash.xyz/upload`. For local development against a local instance of the server, set it to `http://localhost:8181/upload` (see `constants.py` for server defaults if running a local instance).
*   `--token`: Authentication token (optional, required for private uploads). If not provided, it uses the `FILESTASH_TOKEN` environment variable. Set this variable in a `.env` file or directly in your environment. Set `FILESTASH_TOKEN = <YOUR_TOKEN>`.
*   `--analyze`: Analyze the contents of the file and describe it (default is True).

### Downloading a File

```bash
stash down <hash> [--server <server_url>] [--token <token>] [--output-dir <output_directory>]
```

*   `<hash>`: Hash of the file to download (required).
*   `--server`: URL of the FileStash server. Defaults to `https://filestash.xyz/download`. For local development against a local instance of the server, set it to `http://localhost:8181/download`.
*   `--token`: Authentication token (optional, required for private downloads). If not provided, it uses the `FILESTASH_TOKEN` environment variable.
*   `--output-dir`: Directory to save the downloaded file (optional; defaults to the current directory).

### Listing Files

```bash
stash list [--server <server_url>] [--token <token>] [--limit <integer>] [--filter-by <string>]
```

*   `--server`: URL of the FileStash server. Defaults to `https://filestash.xyz/list`. For local development against a local instance of the server, set it to `http://localhost:8181/list`.
*   `--token`: Authentication token (optional but recommended).  If not provided, it uses the `FILESTASH_TOKEN` environment variable. The token increases the number of files that can be listed.
*   `--limit`: Maximum number of files to list (optional; defaults to 50).
*   `--filter-by`: Filter the files by a string pattern (optional).

### Version

```bash
stash version
```

Displays the installed version of Stash CLI.

## Development

Stash CLI uses `poetry` for dependency management.

1. **Install Poetry:**  `pipx install poetry` (recommended)
2. **Clone the Repository:** `git clone https://github.com/ogre-run/stash-cli.git`
3. **Navigate to Project:** `cd stash-cli`
4. **Install Dependencies:** `poetry install`
5. **Activate Virtual Environment:** `poetry shell`

You can now run the CLI from within the virtual environment using `stash <command>`. You can also install Stash CLI locally using `poetry build && pip install dist/*.whl`, which is the recommended way for developing and testing local changes.  For a full uninstall, `rm -r dist` followed by `pipx uninstall filestash` is the recommended procedure.

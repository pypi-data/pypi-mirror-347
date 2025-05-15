import os
import re
import json
import requests
import importlib.metadata
import platform
import subprocess
import argparse
import rich

from dotenv import load_dotenv
from typing import Optional
from rich.table import Table
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path

from .actions import *
from .config import *

# Load environment variables from .env file
load_dotenv()

# Get the current project path
project_path = os.getcwd()

console = Console()

def up(args):
    """
    Upload a single file to FileStash.
    """
    display_figlet()  # Display stash logo
    starting_emoji()  # Display starting emoji

    file_path = Path(args.file_path)
    server = args.server
    token = args.token
    analyze = args.analyze

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Create a progress task
            task = progress.add_task(f"Uploading {file_path.name}...", total=None)

            # Get token from environment if not provided
            if token is None:
                stash_token = os.getenv("FILESTASH_TOKEN", FILESTASH_TOKEN)
            else:
                stash_token = token

            # Open file in binary read mode
            with open(file_path, 'rb') as file:
                # Prepare the multipart form data
                files = {
                    'file': (file_path.name, file, 'application/octet-stream')
                }
                
                # Prepare the JSON payload
                data = {
                    'json_payload': json.dumps({'stash_token': stash_token,
                                                'analyze': analyze})
                }

                # Send the file to the server
                response = requests.post(
                    server,
                    files=files,
                    data=data
                )

                if response.status_code == 200:
                    progress.update(task, completed=True)
                    try:
                        response_data = response.json()
                        console.print(response_data['terminal_message'])  # Print only the terminal message
                    except json.JSONDecodeError:
                        # Fallback in case response is not JSON
                        console.print(response.text)
                else:
                    error_msg = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                    console.print(f"\n❌ Upload failed: {error_msg}", style="bold red")
                    return 1

    except requests.exceptions.RequestException as e:
        console.print(f"\n❌ Network error: {str(e)}", style="bold red")
        return 1
    except Exception as e:
        console.print(f"\n❌ Unexpected error: {str(e)}", style="bold red")
        return 1
    
    return 0
           
def down(args):
    """
    Download file from FileStash.
    If the file is public, token is not required.
    """
    display_figlet()  # Display stash logo
    starting_emoji()  # Display starting emoji
    
    hash = args.hash
    server = args.server
    token = args.token
    output_dir = args.output_dir
    
    try:
        # Prepare the download URL and parameters
        params = {'url_hash': hash}
            
        # Show progress spinner while downloading
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Create a progress task
            task = progress.add_task(f"Downloading {hash}...", total=None)
           
            # Get token from environment if not provided
            if token is None:
                stash_token = os.getenv("FILESTASH_TOKEN", FILESTASH_TOKEN)
            else:
                stash_token = token
            params['token'] = stash_token
           
            # Make the request
            response = requests.get(server, params=params, stream=True)
            
            # Access the Content-Disposition header
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition:
                # Updated regex pattern to match filename without quotes
                filename_match = re.search(r'filename=([^;]+)', content_disposition)
                if filename_match:
                    download_name = filename_match.group(1)
                else:
                    download_name = 'downloaded_file'
            else:
                download_name = 'downloaded_file'
                
            # Check if the request was successful
            if response.status_code == 200:
                # Determine output path
                filename = download_name
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                    output_path = os.path.join(output_dir, filename)
                else:
                    output_path = filename
                
                # Save the file
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                progress.update(task, completed=True)
                console.print(f"\n✅ Successfully downloaded {filename} to {output_path}")
                
            else:
                error_msg = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                console.print(f"\n❌ Failed to download file: {error_msg}", style="bold red")
                return 1
                
    except requests.exceptions.RequestException as e:
        console.print(f"\n❌ Network error: {str(e)}", style="bold red")
        return 1
    except Exception as e:
        console.print(f"\n❌ Unexpected error: {str(e)}", style="bold red")
        return 1
    
    return 0

def list_files(args):
    """
    List all files in the FileStash storage bucket.
    Displays file information in a tabular format, including analysis details.
    """
    display_figlet()  # Display stash logo
    starting_emoji()  # Display starting emoji

    server = args.server
    token = args.token
    limit = args.limit
    filter_by = args.filter_by

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Create a progress task
            task = progress.add_task("Fetching file list...", total=None)

            # Get token from environment if not provided
            if token is None:
                stash_token = os.getenv("FILESTASH_TOKEN", FILESTASH_TOKEN)
            else:
                stash_token = token

            # Prepare request parameters
            params = {
                'token': stash_token,
                'limit': limit
            }
            
            if filter_by:
                params['filter'] = filter_by

            # Send the request to get file list
            response = requests.get(
                server,
                params=params
            )

            if response.status_code == 200:
                progress.update(task, completed=True)
                
                try:
                    files_data = response.json()
                    
                    # If no files found
                    if not files_data or len(files_data.get('files', [])) == 0:
                        console.print("\n📂 No files found in your FileStash storage.", style="bold yellow")
                        return 0
                    
                    # Create a table to display file information
                    from rich.table import Table
                    from rich import box
                    
                    table = Table(show_header=True, header_style="bold blue", box=box.ROUNDED)
                    table.add_column("Filename", style="dim")
                    table.add_column("Hash", style="dim")
                    table.add_column("Size", justify="right")
                    table.add_column("Upload Date", justify="center")
                    table.add_column("Analysis", style="green")
                    
                    # Add each file to the table
                    for file in files_data.get('files', []):
                        # Format file size
                        size = file.get('size', 0)
                        size_str = format_file_size(size)
                        
                        # Get and truncate hash
                        hash_value = file.get('hash', 'N/A')
                        if hash_value and hash_value != 'N/A' and len(hash_value) > 9:
                            hash_value = hash_value[:9] + "..."
                            
                        # Format upload date
                        upload_date = file.get('upload_date', 'N/A')
                        
                        # Extract just the analysis field
                        analysis_data = file.get('analysis', 'N/A')
                        
                        # Extract the value depending on the data type
                        if isinstance(analysis_data, dict):
                            # If analysis is a dictionary, extract the analysis field
                            analysis = analysis_data.get('analysis', 
                                     # Fallback to other common analysis fields if 'analysis' not present
                                     analysis_data.get('summary',
                                     analysis_data.get('description',
                                     str(analysis_data))))
                        elif isinstance(analysis_data, str):
                            # If it's already a string, use it directly
                            analysis = analysis_data
                        elif analysis_data is None:
                            analysis = "N/A"
                        else:
                            # For any other type, convert to string
                            analysis = str(analysis_data)
                        
                        # Truncate if too long
                        if analysis and len(analysis) > 50:
                            analysis = analysis[:47] + "..."
                        
                        table.add_row(
                            str(file.get('filename', 'Unknown')),
                            str(hash_value),
                            str(size_str),
                            str(upload_date),
                            str(analysis)
                        )
                    
                    # Print the table
                    console.print("\n📂 Files in your FileStash storage:")
                    console.print(table)
                    
                    # Print total count
                    total_files = len(files_data.get('files', []))
                    console.print(f"\nTotal files: {total_files}", style="bold")
                    
                except json.JSONDecodeError:
                    console.print("\n❌ Error parsing server response. Response was not valid JSON.", style="bold red")
                    return 1
            else:
                error_msg = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                console.print(f"\n❌ Failed to list files: {error_msg}", style="bold red")
                return 1

    except requests.exceptions.RequestException as e:
        console.print(f"\n❌ Network error: {str(e)}", style="bold red")
        return 1
    except Exception as e:
        console.print(f"\n❌ Unexpected error: {str(e)}", style="bold red")
        return 1
    
    return 0

def show_version(args):
    """
    Display the version of stash.
    """
    display_figlet()  # Display the stash logo
    version_string = importlib.metadata.version("stash")
    print("{}".format(version_string))
    return 0

def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(
        description="FileStash CLI - A simple file sharing tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Create subparsers for each command
    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        description="valid commands",
        help="additional help",
    )
    
    # Create the parser for the "up" command
    parser_up = subparsers.add_parser("up", help="Upload a file to FileStash")
    parser_up.add_argument(
        "file_path", 
        help="Path to the file you want to upload",
        type=str
    )
    parser_up.add_argument(
        "--server", 
        help="Proxy server URL for deployment (default: %(default)s)",
        default="https://filestash.xyz/upload"
    )
    parser_up.add_argument(
        "--token", 
        help="Authentication token for private uploads. If not provided, it gets value from FILESTASH_TOKEN environment variable",
        default=None
    )
    parser_up.add_argument(
        "--analyze", 
        help="Analyze the file to generate a meaningful description (default: %(default)s)",
        default=True,
        action="store_true"
    )
    parser_up.set_defaults(func=up)
    
    # Create the parser for the "down" command
    parser_down = subparsers.add_parser("down", help="Download a file from FileStash")
    parser_down.add_argument(
        "hash", 
        help="Hash of the file to download",
        type=str
    )
    parser_down.add_argument(
        "--server", 
        help="Proxy server URL for downloading (default: %(default)s)",
        default="https://filestash.xyz/download"
    )
    parser_down.add_argument(
        "--token", 
        help="Authentication token for private downloads. If not provided, it gets value from FILESTASH_TOKEN environment variable",
        default=None
    )
    parser_down.add_argument(
        "--output-dir", 
        help="Directory to save the downloaded file",
        default=None
    )
    parser_down.set_defaults(func=down)
    
    # Create the parser for the "list" command
    parser_list = subparsers.add_parser("list", help="List all files in FileStash storage")
    parser_list.add_argument(
        "--server", 
        help="Proxy server URL for listing files (default: %(default)s)",
        default="https://filestash.xyz/list"
    )
    parser_list.add_argument(
        "--token", 
        help="Authentication token for file listing. If not provided, it gets value from FILESTASH_TOKEN environment variable",
        default=None
    )
    parser_list.add_argument(
        "--limit", 
        help="Maximum number of files to list (default: %(default)s)",
        type=int,
        default=50
    )
    parser_list.add_argument(
        "--filter-by", 
        help="Filter files by name pattern",
        default=None
    )
    parser_list.set_defaults(func=list_files)
    
    # Create the parser for the "version" command
    parser_version = subparsers.add_parser("version", help="Display the version of stash")
    parser_version.set_defaults(func=show_version)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute the appropriate function
    if hasattr(args, 'func'):
        return args.func(args)
    else:
        # If no command is provided, show help
        parser.print_help()
        return 0

if __name__ == "__main__":
    exit(main())

#!/usr/bin/env python3
import os
import platform
import subprocess
import sys
import shutil
import xml.etree.ElementTree as ET

# Directory where builder.py is run from (this is where the executable will be copied)
RUN_DIR = os.getcwd()

def parse_csproj(csproj_path):
    """Parse the .csproj file to get the target .NET version."""
    try:
        tree = ET.parse(csproj_path)
        root = tree.getroot()
        target_framework = root.find(".//TargetFramework")
        if target_framework is not None and target_framework.text:
            return target_framework.text  # e.g., 'net9.0'
        else:
            print("Error: Could not find TargetFramework in .csproj")
            sys.exit(1)
    except ET.ParseError:
        print(f"Error: Could not parse {csproj_path}")
        sys.exit(1)

def check_os_and_install_instructions(required_version):
    """Provide .NET SDK installation instructions based on the OS."""
    os_name = platform.system().lower()
    print(f"Detected Operating System: {os_name.capitalize()}")

    dotnet_version = required_version.replace("net", "")  # e.g., '9.0'
    if os_name == "windows":
        print(f"\nWindows Installation Instructions for .NET SDK {dotnet_version}:")
        print(f"- Download the installer from: https://dotnet.microsoft.com/en-us/download/dotnet/{dotnet_version}")
        print("- Run the installer and follow the prompts.")
    elif os_name == "linux":
        print(f"\nLinux Installation Instructions for .NET SDK {dotnet_version}:")
        print(f"- Open a terminal and run:")
        print(f"  sudo apt-get update && sudo apt-get install -y dotnet-sdk-{dotnet_version}")
        print(f"- If the above fails, download the binary:")
        print(f"  https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/sdk-{dotnet_version}.202-linux-x64-binaries")
        print(f"- Extract it, then create a symlink:")
        print(f"  sudo ln -s $(pwd)/dotnet /usr/bin/dotnet")
    else:
        print(f"Error: Unsupported OS '{os_name}'. This script supports Windows and Linux only.")
        sys.exit(1)

def check_dotnet_installed(required_version):
    """Check if the .NET SDK is installed and provide feedback."""
    dotnet_version = required_version.replace("net", "")  # e.g., '9.0'
    try:
        result = subprocess.run(["dotnet", "--version"], capture_output=True, text=True, check=True)
        installed_version = result.stdout.strip()
        print(f"dotnet CLI is installed with version {installed_version}")
        # Check version match, but don't exit on mismatch
        if dotnet_version not in installed_version:
            print(f"Warning: Installed version {installed_version} does not match required version {dotnet_version}")
        else:
            print(f"Version matches required version {dotnet_version}")
        return True
    except FileNotFoundError:
        print("Error: 'dotnet' CLI not found on your system.")
        check_os_and_install_instructions(required_version)
        print("Please install the .NET SDK using the instructions above and rerun this script (as root if necessary).")
        sys.exit(1)

def add_package_and_publish(project_dir):
    """Add the NuGet package and publish the project."""
    os.chdir(project_dir)
    print(f"Changed directory to: {project_dir}")

    # Add the required package
    print("Adding package 'Microsoft.CodeAnalysis.CSharp.Scripting'...")
    subprocess.run(
        ["dotnet", "add", "package", "Microsoft.CodeAnalysis.CSharp.Scripting"],
        check=True
    )

    # Publish the project
    print("Publishing project for win-x64...")
    subprocess.run(
        ["dotnet", "publish", "-c", "Release", "-r", "win-x64", "--self-contained", "true", "-o", "out"],
        check=True
    )

def copy_executable(project_dir):
    """Copy the Weaponised-DFE.exe to the run directory."""
    # The executable is in the 'out' directory as specified in the publish command
    exe_name = "Weaponised-DFE.exe"
    source_path = os.path.join(project_dir, "out", exe_name)
    dest_path = os.path.join(RUN_DIR, exe_name)

    if not os.path.exists(source_path):
        print(f"Error: {source_path} not found after publishing.")
        sys.exit(1)

    print(f"Copying {source_path} to {dest_path}")
    shutil.copy2(source_path, dest_path)

def main():
    # Define paths
    builder_dir = os.path.dirname(os.path.abspath(__file__))  # e.g., /home/hamy/Weaponised-DFE
    project_dir = os.path.join(builder_dir, "Weaponised-DFE")  # e.g., /home/hamy/Weaponised-DFE/Weaponised-DFE
    csproj_path = os.path.join(project_dir, "Weaponised-DFE.csproj")

    # Verify the .csproj file exists
    if not os.path.exists(csproj_path):
        print(f"Error: .csproj file not found at {csproj_path}")
        sys.exit(1)

    # Parse .csproj to get required .NET version first (needed for installation instructions)
    required_version = parse_csproj(csproj_path)
    print(f"Required .NET version from .csproj: {required_version}")

    # Check if dotnet CLI is installed
    check_dotnet_installed(required_version)

    # If we reach here, dotnet is installed, so proceed with the rest
    add_package_and_publish(project_dir)

    # Copy the executable
    copy_executable(project_dir)

    print(f"Success! Weaponised-DFE.exe has been built and copied to {RUN_DIR}")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        sys.exit(1)
    except PermissionError:
        print("Error: Permission denied. Please run this script with sudo/root privileges.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
#!/usr/bin/env python3
import os
import subprocess
import sys
import shutil
import xml.etree.ElementTree as ET
import re


# Directory where builder.py is run from (this is where the executable will be copied)
RUN_DIR = os.getcwd()


def parse_csproj(csproj_path):
    """Parse the .csproj file to get the target .NET version."""
    try:
        tree = ET.parse(csproj_path)
        root = tree.getroot()
        target_framework = root.find(".//TargetFramework")
        if target_framework is None or not target_framework.text:
            print("[!] Error: Could not find TargetFramework in .csproj")
            sys.exit(1)
        
        # Find or create PropertyGroup
        property_group = root.find(".//PropertyGroup")
        if property_group is None:
            property_group = ET.SubElement(root, "PropertyGroup")
        
        # Set or update AssemblyName
        assembly_name = property_group.find("AssemblyName")
        if assembly_name is None:
            assembly_name = ET.SubElement(property_group, "AssemblyName")
        
        # Save the modified .csproj
        tree.write(csproj_path, encoding="utf-8", xml_declaration=True)
        return target_framework.text
    except ET.ParseError:
        print(f"[!] Error: Could not parse {csproj_path}")
        sys.exit(1)


def check_dotnet_installed(required_version):
    """Check if the .NET SDK is installed and provide install instructions if not."""
    dotnet_version = required_version.replace("net", "")
    try:
        result = subprocess.run(["dotnet", "--version"], capture_output=True, text=True, check=True)
        installed_version = result.stdout.strip()
        print(f"[*] dotnet CLI is installed with version {installed_version}")
        if dotnet_version not in installed_version:
            print(f"[!] Warning: Installed version {installed_version} does not match required version {dotnet_version}")
        return True
    except FileNotFoundError:
        print(f"[!] [!] Error: 'dotnet' CLI not found. Install .NET SDK {dotnet_version}:")
        print(f"[*] Download from https://dotnet.microsoft.com/en-us/download/dotnet/{dotnet_version}")
        print("[*] Install it, then rerun this script.")
        sys.exit(1)


def add_package(project_dir):
    """Add the NuGet package and publish the project."""
    os.chdir(project_dir)
    print(f"[>] Changed directory to: {project_dir}")

    print("[>] Adding package 'Microsoft.CodeAnalysis.CSharp.Scripting'...")
    subprocess.run(
        ["dotnet", "add", "package", "Microsoft.CodeAnalysis.CSharp.Scripting"],
        check=True,
        capture_output=True
    )

def main():
    builder_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(builder_dir, "Weaponised-DFE")
    csproj_path = os.path.join(project_dir, "Weaponised-DFE.csproj")
    
    if not os.path.exists(csproj_path):
        print(f"[!] Error: .csproj file not found at {csproj_path}")
        sys.exit(1)
    
    # Read config.ini
    config_path = os.path.join(project_dir, "config.ini")
    if not os.path.exists(config_path):
        print(f"[!] Error: config.ini not found at {config_path}")
        sys.exit(1)
    with open(config_path, "r") as f:
        config_content = f.read()
    
    # Parse and update .csproj
    required_version = parse_csproj(csproj_path)
    print(f"[>] Required .NET version from .csproj: {required_version}")
    
    check_dotnet_installed(required_version)
    add_package(project_dir)
    print(f"[+] Success! Weaponised-DFE has been built.")
    print("[>] Go to the \"Weaponised-DFE\" sub-directory and")
    print("[*] Use \"dotnet run\" to get the code working...")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"[!] Error executing command: {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"[!] Error: Permission denied - {e}. Fix directory permissions and rerun.")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
        sys.exit(1)
    
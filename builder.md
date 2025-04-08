# builder.md - Documentation for builder.py

## Overview

`builder.py` is a Python script designed to automate the setup and build process for the "Weaponised-DFE" .NET application. It handles dependency verification, project configuration, NuGet package installation, and SSL certificate generation using the `cryptography` library. The script is built for reliability and portability, eliminating external tool dependencies like OpenSSL, and provides clear feedback for troubleshooting.


## Demo Screenshots

| Certificate Generation | Project Build Success |
|------------------------|-----------------------|
| ![Cert Generation](path/to/cert-gen-image.png) | ![Build Success](path/to/build-success-image.png) |

*Note*: Replace placeholders with actual image paths after capturing screenshots.

---

## Features

- **.NET SDK Verification**: Ensures the required .NET SDK is installed, offering guidance if absent.
- **Project File Management**: Parses and updates the `.csproj` file for proper configuration.
- **NuGet Integration**: Installs the `Microsoft.CodeAnalysis.CSharp.Scripting` package.
- **SSL Certificate Creation**: Generates a 4096-bit RSA key and self-signed X.509 certificate (valid for 10,000 days).
- **Error Handling**: Catches and reports issues like file access, permissions, or command failures.
- **Platform Agnostic**: Works consistently across Windows, macOS, and Linux using Python standard libraries and `cryptography`.

---

## Prerequisites

To use `builder.py`, ensure the following are installed:

1. **Python 3.x**: Requires Python 3 (uses `#!/usr/bin/env python3` shebang).
2. **.NET SDK**: Needed for the .NET project (version specified in `Weaponised-DFE.csproj`).
3. **`cryptography` Library**: Install with pip:
   - pip install cryptography

---

## How to Use

1. **Setup**:
   - Place `builder.py` in the root directory containing the "Weaponised-DFE" subdirectory.

2. **Execution**:
   - Run from a terminal in the script’s directory:
     - python3 builder.py
   - On Unix-like systems, make it executable:
     - chmod +x builder.py
     - ./builder.py

3. **Output**:
   - The script will:
     - Check for .NET SDK.
     - Add the NuGet package.
     - Create an `auth` directory with `key.pem` and `cert.pem`.
     - Display paths to generated files and instructions.

4. **Run the Application**:
   - Navigate to the project directory and launch:
     - cd Weaponised-DFE
     - dotnet run

---

## Functionality

### .NET SDK Check
- Confirms the .NET CLI is installed and matches the required version from `Weaponised-DFE.csproj`.
- If missing, provides a download URL and exits.

### .csproj Parsing
- Reads `Weaponised-DFE.csproj`, ensuring `TargetFramework` and `AssemblyName` are present or added.

### NuGet Package Installation
- Executes `dotnet add package Microsoft.CodeAnalysis.CSharp.Scripting` in the project directory.

### SSL Certificate Generation
- Creates an `auth` directory if it doesn’t exist.
- Generates:
  - A 4096-bit RSA private key (`key.pem`), unencrypted.
  - A self-signed X.509 certificate (`cert.pem`), valid for 10,000 days with "localhost" as the common name and SAN.
- Uses the `cryptography` library for generation, avoiding external tools.

### Error Handling
- Handles missing files, permission issues, and subprocess failures with descriptive messages.

---

## Troubleshooting

- **Missing `cryptography`**: Install with `pip install cryptography` and rerun.
- **Permission Denied**: Ensure write access to the script’s directory.
- **.NET SDK Not Found**: Follow the provided download link and install the correct version.

---

## Notes

- The script assumes `Weaponised-DFE.csproj` and `config.ini` exist in the "Weaponised-DFE" subdirectory.
- Generated certificates are stored in `auth/` with absolute paths displayed for reference.
- No root/admin privileges are required; permission issues will prompt the user to fix directory access.

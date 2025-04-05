# Weaponised-DFE Build Documentation

This document covers the `config.ini` file and the `builder.py` script used to build the Weaponised-DFE project.

## config.ini

The `config.ini` file sits in the `Weaponised-DFE` directory and tells the program and build process what to do. It’s got three key-value pairs in a simple format: `key=[value]`. Here’s what each one means:

- **endpoint**: The URL path slapped onto the base URL for HTTP requests. Example: `endpoint=[dDZRSlfTMxwmIeK]` means the program hits something like `https://192.168.51.75/dDZRSlfTMxwmIeK`.
- **url**: The base URL for the program’s network calls. Example: `url=[https://192.168.51.75/]` sets the root address.
- **exe_name**: The name of the final executable file. Example: `exe_name=[Ballon]` makes the build spit out `Ballon.exe` instead of the default `Weaponised-DFE.exe`.

Sample `config.ini`:
```
endpoint=[dDZRSlfTMxwmIeK]
url=[https://192.168.51.75/]
exe_name=[Ballon]
```

The program (`Program.cs`) reads `endpoint` and `url` at runtime to figure out where to send requests. The `builder.py` script reads `exe_name` to name the `.exe`.

## builder.py

The `builder.py` script builds the Weaponised-DFE project using the .NET CLI (`dotnet`). It’s a Python script that lives next to the `Weaponised-DFE` directory and does the heavy lifting. Here’s what it does:

1. **Checks for config.ini**:
   - Looks in `Weaponised-DFE/config.ini`.
   - Pulls `exe_name` using regex (`exe_name=\[(.*?)\]`). If it’s missing, it bails with an error.

2. **Sets the Executable Name**:
   - Opens `Weaponised-DFE/Weaponised-DFE.csproj`.
   - Adds or updates `<AssemblyName>` with the `exe_name` (e.g., `<AssemblyName>Ballon</AssemblyName>`).
   - Saves the `.csproj` so `dotnet` builds the right `.exe`.

3. **Checks .NET SDK**:
   - Runs `dotnet --version` to see if the CLI’s there.
   - Grabs the required version from `.csproj` (e.g., `net9.0`).
   - If `dotnet`’s not found, it prints install instructions and exits:
     - Windows: Download link.
     - Linux: `sudo apt-get` command (for install, not script).
   - If versions don’t match, it warns but keeps going.

4. **Builds the Project**:
   - Switches to `Weaponised-DFE` dir.
   - Runs `dotnet add package Microsoft.CodeAnalysis.CSharp.Scripting` to grab the scripting dependency.
   - Runs `dotnet publish -c Release -r win-x64 --self-contained true -o out` to build a standalone `.exe` for Windows x64.
   - Output lands in `Weaponised-DFE/out` as `<exe_name>.exe` (e.g., `Ballon.exe`).

5. **Copies the Executable**:
   - Takes `<exe_name>.exe` from `out` and copies it to the directory where `builder.py` is run.
   - Example: If `exe_name=Ballon`, you get `Ballon.exe` in the current dir.

6. **Error Handling**:
   - No `config.ini`? Exits with a message.
   - No `exe_name`? Exits.
   - No `dotnet`? Exits with instructions.
   - Permission issues? Tells you to fix perms, no `sudo` nonsense.


### Sample run:
```
{20:55}~/Weaponised-DFE:main ✗ ➭ python3 builder.py
Required .NET version from .csproj: net9.0
dotnet CLI is installed with version 9.0.202
Changed directory to: /home/hamy/Weaponised-DFE/Weaponised-DFE
Adding package 'Microsoft.CodeAnalysis.CSharp.Scripting'...

Build succeeded in 1.0s
info : X.509 certificate chain validation will use the fallback certificate bundle at '/home/hamy/Downloads/dotnet-sdk-9.0.202-linux-x64/sdk/9.0.202/trustedroots/codesignctl.pem'.
info : X.509 certificate chain validation will use the fallback certificate bundle at '/home/hamy/Downloads/dotnet-sdk-9.0.202-linux-x64/sdk/9.0.202/trustedroots/timestampctl.pem'.
info : Adding PackageReference for package 'Microsoft.CodeAnalysis.CSharp.Scripting' into project '/home/hamy/Weaponised-DFE/Weaponised-DFE/Weaponised-DFE.csproj'.
info :   CACHE https://api.nuget.org/v3/registration5-gz-semver2/microsoft.codeanalysis.csharp.scripting/index.json
info :   CACHE https://api.nuget.org/v3/registration5-gz-semver2/microsoft.codeanalysis.csharp.scripting/page/1.1.0-rc1-20151109-01/3.4.0.json
info :   CACHE https://api.nuget.org/v3/registration5-gz-semver2/microsoft.codeanalysis.csharp.scripting/page/3.5.0-beta1-final/4.7.0-2.final.json
info :   CACHE https://api.nuget.org/v3/registration5-gz-semver2/microsoft.codeanalysis.csharp.scripting/page/4.7.0/4.13.0.json
info : Restoring packages for /home/hamy/Weaponised-DFE/Weaponised-DFE/Weaponised-DFE.csproj...
info :   CACHE https://api.nuget.org/v3/vulnerabilities/index.json
info :   CACHE https://api.nuget.org/v3-vulnerabilities/2025.04.04.23.31.17/vulnerability.base.json
info :   CACHE https://api.nuget.org/v3-vulnerabilities/2025.04.04.23.31.17/2025.04.04.23.31.17/vulnerability.update.json
info : Package 'Microsoft.CodeAnalysis.CSharp.Scripting' is compatible with all the specified frameworks in project '/home/hamy/Weaponised-DFE/Weaponised-DFE/Weaponised-DFE.csproj'.
info : PackageReference for package 'Microsoft.CodeAnalysis.CSharp.Scripting' version '4.13.0' updated in file '/home/hamy/Weaponised-DFE/Weaponised-DFE/Weaponised-DFE.csproj'.
info : Writing assets file to disk. Path: /home/hamy/Weaponised-DFE/Weaponised-DFE/obj/project.assets.json
log  : Restored /home/hamy/Weaponised-DFE/Weaponised-DFE/Weaponised-DFE.csproj (in 265 ms).
Publishing project for win-x64...
Restore complete (1.1s)
  Weaponised-DFE succeeded (6.6s) → out/

Build succeeded in 8.6s
Copying /home/hamy/Weaponised-DFE/Weaponised-DFE/out/Ballon.exe to /home/hamy/Weaponised-DFE/Ballon.exe
Success! Ballon.exe has been built and copied to /home/hamy/Weaponised-DFE

```

### Usage
- Put `config.ini` in `Weaponised-DFE`.
- Run `python3 builder.py` from its dir.
- Make sure `dotnet` (e.g., 9.0) is installed first.
- Get `<exe_name>.exe` in the current dir.

That’s it, `config.ini` drives the runtime and build, `builder.py` makes it happen.

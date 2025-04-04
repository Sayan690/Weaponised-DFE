I want to create a builder to create `Weaponised-DFE.exe` in the current directory or the directory where builder.py was run.
builder.py is stored at `/home/hamy/Weaponised-DFE` and .csproj file & other code files is inside `/home/hamy/Weaponised-DFE/Weaponised-DFE`


### Step 1
check if the operating system is windows or linux, give installation instructions for windows or linux 
check `.csproj` file for .NET version being used; check the system to see if that version is installed;

### Step 2
check if dotnet-cli is installed by running `dotnet --version`, if not found, throw this link for installation:
https://dotnet.microsoft.com/en-us/download/dotnet/9.0

this will be different based on what version of .net is used in .csproj; shutdown program and ask user to run it as root 

suggest binaries if other methods fail:
https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/sdk-9.0.202-linux-x64-binaries

Download the binary, cd into directory and create a symlink:
```
sudo ln -s $(pwd)/dotnet /usr/bin/dotnet
dotnet --version
9.0.202
```

### Step 3
cd into `/home/hamy/Weaponised-DFE/Weaponised-DFE` or any directory with `.csproj` file 
run `dotnet add package Microsoft.CodeAnalysis.CSharp.Scripting` to add package to project
then compile and create executable `dotnet publish -c Release -r win-x64 --self-contained true -o out`


### Step 4
Copy executable from `/home/hamy/Weaponised-DFE/Weaponised-DFE/bin/Release/net9.0/win-x64/Weaponised-DFE.exe` to current directory (the place where builder was run from)









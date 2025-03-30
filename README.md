# DotnetFilelessExecution

## Overview

Weaponised DFE is the advanced implementation of DotnetFilelessExecution. It can fetch a remote .NET Assembly, and execute it filelessly (in memory), i.e., without having to save it on the disk, all while being more secure, and undetectable than the previous DotnetFilelessExecution.

## Compilation

I have used direct command-line compilation using the `dotnet` command, but of course you can use Visual Studio.

Btw, before compiling make sure to change the attacker ip address.

For me, here are the compilation steps ...
```cmd
cd Weaponised-DFE
dotnet add package Microsoft.CodeAnalysis.CSharp.Scripting
dotnet run
```
or

```cmd
dotnet publish -c Release -r win-x64 --self-contained true -o out
```

## Usage

- Create openssl keys and certs, as under the auth directory.

```bash
openssl req -new -x509 -newkey rsa:4096 -nodes -keyout auth/key.pem -out auth/cert.pem -days 10000
```

- Rename the listening host, port, and the name of the .NET Assembly you want to execute in the `https.py`.

- Rename the connect back attacker ip address in the `toExec.cs`.

- Rename the connect back attacker ip address in the `Program.cs` inside the `Weaponised-DFE` directory before compilation.

- Start the https server on the attacker side

```bash
python3 https.py
```

- Run Weaponised-DFE on victim side.

```cmd
dotnet run
```

or

```cmd
.\Weaponised-DFE.exe
```

## Note
For demonstration purposes, the connect back address is hard coded inside the program, which can be changed as needed.

## Disclaimer
This project is intended for educational and security testing purposes only. The author is not responsible for any misuse of this tool.

## Author
Developed by **Sayan Ray** [@BareBones90](https://x.com/BareBones90)

## License
This project is licensed under the MIT License - see the LICENSE file for details.

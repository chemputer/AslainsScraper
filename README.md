# AslainsScraper
Automatically downloads the latest version of Aslain's Mod Pack for World of Warships.

Contains options for different programs to download, including Chrome, Firefox, Edge, and IDM. Also includes an option for the user to specify another program.

```text
aslains_scraper --help
usage: aslains_scraper [-h] [-P {chrome,firefox,edge,idm,other}] [-O OTHER]
                       [-A FLAGS] [-F]

Downloads the latest Aslain's WoWS Mod Pack

optional arguments:
  -h, --help                                     show this help message and exit
  -P, --program {chrome,firefox,edge,idm,other}  Which program to use to download the mod pack
                                                 (default: chrome)
  -O, --other OTHER                              Specify a program to use to download the mod pack.
                                                 Use the program's full path if not in the system PATH variable
  -A, --args FLAGS                               Add other arguments when using another program. They will be
                                                 called before the download link
  -F, --force                                    Forcefully download the latest version, even if
                                                 it's already downloaded
```

## Disclaimer

In v1.0.0, the program options must be present in your system PATH variable. [Here's a guide on how to add to your PATH
variable](https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/).

## Examples

Download the mod pack using Internet Download Manager (IDM)

```text
aslains_scraper --program idm
```

Download the mod pack using a different program

```text
aslains_scraper --program other --other "C:/Program Files/OtherProgram/OtherProgram.exe"
```

Download the mod pack using a different program with additional flags

```text
aslains_scraper --program other --other "C:/Program Files/OtherProgram/OtherProgram.exe" --args "/n /d"
```
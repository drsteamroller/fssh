# FSSH.py - SSH session broker 

## Why?

FortiGate's CLI comes with a built-in grep module to help search output. FortiManager and FortiAnalyzer lack this entirely, this script helps facilitate the connection and add grep searching to outputs.

## How to use:

The tool aims to mimic the functionality of `ssh` and `grep` (in the context of FortiProducts). To connect to a sample FortiManager with a default administrator name (assuming you have the fingerprint already recorded on the client system):

`python fssh.py admin@<fmg-ip>`

With nonstandard ports:

`python fssh.py -p 2222 admin@<fmg-ip>`

If the fingerprint of the FortiManager/FortiAnalyzer is not present on the client system:

`python fssh.py -aa admin@<fmg-ip>`

If using a ssh secret key:

`python fssh.py -i <KEYFILEPATH> admin@<fmg-ip>`

## Dependencies

`pip install paramiko`

## Notes

Due to the nature of paramiko's `exec_command()` function, this tool is not useful for facilitating anything other than Fortinet `diagnose` command parsing. Every instance of `exec_command()` is run in a new context, which means the configuration bucket context is reset. (This means `config` commands are entirely useless)

In order to use grep on scoped bucket levels, use a `get` or `show` on that bucket level. Example:

`show system interface | grep /24`
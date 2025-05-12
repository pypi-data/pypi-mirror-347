# SPDX-FileCopyrightText: 2025-present Guille on a Raspberry pi <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from ..api import advanced

def main():
    if sys.argv[1]=="run":
        advanced.run_entry(sys.argv[2])
    elif sys.argv[1]=="run_local":
        advanced.run_entry(sys.argv[2], True)
    elif sys.argv[1]=="get":
        if sys.argv[2]=="local_repos":
            repos=advanced.get_repos(True)
            for repo in repos:
                print(f"[+] Repo: {repo} [+]")
        elif sys.argv[2]=="repos":
            repos=advanced.get_repos()
            for repo in repos:
                print(f"[+] Repo: {repo} [+]")
        elif sys.argv[2]=="local_pkg":
            advanced.install_pkg(sys.argv[3], True)
        elif sys.argv[2]=="pkg":
            advanced.install_pkg(sys.argv[3])
    elif sys.argv[1]=="local_post_install":
        advanced.post_install()
    elif sys.argv[1]=="post_install":
        advanced.post_install(False)
    elif sys.argv[1]=="init":
        advanced.init_pkg(sys.argv[2])
    elif sys.argv[1]=="repo":
        if sys.argv[2]=="add":
            advanced.add_repo(sys.argv[3])
        elif sys.argv[2]=="remove":
            advanced.remove_repo(sys.argv[3])
        elif sys.argv[2]=="add_local":
            advanced.add_repo(sys.argv[3], True)
        elif sys.argv[2]=="remove_local":
            advanced.remove_repo(sys.argv[3], True)
    elif sys.argv[1]=="compress":
        advanced.compress(sys.argv[2])
    elif sys.argv[1]=="extract":
        advanced.extract(sys.argv[2])
    elif sys.argv[1]=="local_extract":
        advanced.extract(sys.argv[2], True)
    elif sys.argv[1]=="help":
        print("[+] ----- Help Message ----- [+]")
        print("[*] run                      [*]")
        print("[*] run_local                [*]")
        print("[*] get local_repos          [*]")
        print("[*] get repos                [*]")
        print("[*] get local_pkg            [*]")
        print("[*] get pkg                  [*]")
        print("[*] local_post_install       [*]")
        print("[*] post_install             [*]")
        print("[*] init                     [*]")
        print("[*] repo add                 [*]")
        print("[*] repo remove              [*]")
        print("[*] repo add_local           [*]")
        print("[*] repo remove_local        [*]")
        print("[*] compress                 [*]")
        print("[*] extract                  [*]")
        print("[*] local_extract            [*]")
        print("[*] help                     [*]")
        print("[+] --- Help Message End --- [+]")
    else:
        print("[!] Command Not Found    [!]")
        print("[*] Try with 'cpkg help' [*]")
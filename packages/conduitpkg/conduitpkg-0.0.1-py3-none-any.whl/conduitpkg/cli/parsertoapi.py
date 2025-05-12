# SPDX-FileCopyrightText: 2025-present Guille on a Raspberry pi <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from ..api import advanced

def main():
    if sys.argv[0]=="run":
        advanced.run_entry(sys.argv[1])
    elif sys.argv[0]=="run_local":
        advanced.run_entry(sys.argv[1], True)
    elif sys.argv[0]=="get":
        if sys.argv[1]=="local_repos":
            repos=advanced.get_repos(True)
            for repo in repos:
                print(f"[+] Repo: {repo} [+]")
        elif sys.argv[1]=="repos":
            repos=advanced.get_repos()
            for repo in repos:
                print(f"[+] Repo: {repo} [+]")
        elif sys.argv[1]=="local_pkg":
            advanced.install_pkg(sys.argv[2], True)
        elif sys.argv[1]=="pkg":
            advanced.install_pkg(sys.argv[2])
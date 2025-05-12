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
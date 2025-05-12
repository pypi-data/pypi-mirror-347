# SPDX-FileCopyrightText: 2025-present Guille on a Raspberry pi <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import shutil
import os
import json

def compress():
    current = os.getcwd()
    try:
        with open("package.json", "r") as f:
            name = json.load(f)["name"]
    except Exception:
        print("[!] Not in a package directory [!]")
    try:
        os.mkdir("dist")
    except Exception:
        pass
    os.chdir("dist")
    dist_path = os.path.join("dist", name)
    if name in os.listdir("."):
        shutil.rmtree(name)
    os.mkdir(name)
    os.chdir("..")
    shutil.copy("package.json", dist_path)
    shutil.copytree("src", dist_path)
    shutil.copy("builder.zl", dist_path)
    shutil.copy("LICENSE.txt", dist_path)
    shutil.copy("README.md", dist_path)
    shutil.make_archive(dist_path, "zip", dist_path+".zip")
    os.chdir(current)

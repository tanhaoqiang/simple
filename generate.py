#!/usr/bin/env python3

import json
import sys
import os
from urllib.request import urlopen

def get_release_files(repo, release, exts):
    with urlopen(f"https://api.github.com/repos/{repo}/releases/tags/{release}") as f:
        data = json.load(f)
    for asset in data["assets"]:
        name = asset["name"]
        if not any(name.endswith(ext) for ext in exts):
            continue
        yield name, asset["browser_download_url"]

def main(filename, outdir):
    with open(filename) as f:
        packages = json.load(f)

    os.makedirs(outdir, exist_ok=True)

    for name, config in packages.items():
        repo = config["repo"]
        exts = config["exts"]
        releases = config["releases"]

        dirname = os.path.join(outdir, name)
        os.makedirs(dirname, exist_ok=True)
        with open(os.path.join(dirname, 'index.html'), 'w') as f:
            f.write("<!DOCTYPE html><html><body>")
            for release in releases:
                for asset, url in get_release_files(repo, release, exts):
                    f.write(f'<a href="{url}">{asset}</a>')
            f.write("</body></html>")

    with open(os.path.join(outdir, "index.html"), "w") as f:
        f.write("<!DOCTYPE html><html><body>")
        for name in packages:
            f.write(f'<a href="{name}/">{name}</a>')
        f.write("</body></html>")

if __name__ == '__main__':
    main(*sys.argv[1:])

#!/usr/bin/env python3
# file generated with AI assistance: Claude Code - 2026-07-01 17:10:01 UTC
#
# Regenerate the flattened recipe files (<package_dotted>.<version>.json) and the
# `recipes` map in index.json from the source tree <vendor>/<pkg>/<version>/.
#
# Flex's Downloader base64_decodes file `contents` (Downloader.php:290), so file
# contents MUST be base64-encoded here. Run after adding/editing a recipe:
#
#   python3 bin/build-recipes.py
#
import base64
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# Packages present in the tree but intentionally NOT served (none for now).
SKIP = set()

recipes = {}
for manifest_path in sorted(glob.glob("*/*/*/manifest.json")):
    vendor, pkg, version, _ = manifest_path.split(os.sep)
    name = f"{vendor}/{pkg}"
    if name in SKIP:
        continue
    base = os.path.join(vendor, pkg, version)
    manifest = json.load(open(manifest_path))

    files = {}
    for root, _dirs, names in os.walk(base):
        for n in sorted(names):
            full = os.path.join(root, n)
            rel = os.path.relpath(full, base)
            if rel == "manifest.json":
                continue
            with open(full, "rb") as f:
                raw = f.read()
            files[rel] = {
                "contents": base64.b64encode(raw).decode("ascii"),
                "executable": os.access(full, os.X_OK),
            }

    flat = {"manifests": {name: {"manifest": manifest, "files": files, "ref": version}}}
    dotted = name.replace("/", ".")
    with open(f"{dotted}.{version}.json", "w") as f:
        json.dump(flat, f, separators=(",", ":"))
        f.write("\n")

    recipes.setdefault(name, []).append(version)

for versions in recipes.values():
    versions.sort()

index = json.load(open("index.json"))
index["recipes"] = dict(sorted(recipes.items()))
with open("index.json", "w") as f:
    json.dump(index, f, indent=4)
    f.write("\n")

print("regenerated recipes:", index["recipes"])

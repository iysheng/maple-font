from enum import Enum, unique
import json
from os import getcwd, path, listdir, makedirs
import sys

try:
    import fontforge
except ImportError:
    print(
        "fail to load fontforge module. On Windows, you can execute `fontforge-console.bat` first and then call this script"
    )
    sys.exit(1)

if len(sys.argv) < 3:
    print("config is incorrect or not set, switch to default 'nf' and 'Maple Mono'")
    base_font = "nf"
    family = "Maple Mono"
else:
    base_font = sys.argv[1]
    family = sys.argv[2]

suffix = "SC-NF" if base_font == "nf" else "SC"
suffix_alt = suffix.replace("-", " ")

root = getcwd()
sc_path = path.join(root, "SC")
output_path = path.join(path.dirname(root), "output")
sc_nf_path = path.join(output_path, suffix)
base_font_path = path.join(output_path, base_font)

family_name = f"{family} {suffix_alt}"
file_name = f"{family.replace(' ', '')}-{suffix}"

if not path.exists(sc_nf_path):
    makedirs(sc_nf_path)


def get_subfamily_name(f: str):
    return f.split("-")[-1].split(".")[0]


def generate(f: str):
    sub = get_subfamily_name(f)
    nf = fontforge.open(path.join(base_font_path, f))
    sc = fontforge.open(path.join(root, "SC", f"{sub}.ttf"))

    for item in sc.glyphs():
        if item.unicode == -1:
            continue
        sc.selection.select(("more", None), item.unicode)
        nf.selection.select(("more", None), item.unicode)

    sc.copy()
    nf.paste()

    nf.generate(path.join(output_path, suffix, f"{file_name}-{sub}.ttf"))
    sc.close()
    nf.close()


with open(path.join(output_path, "build-config-sc.json"), "w") as f:
    c = {"base": ""}
    if base_font == "nf":
        c["base"] = "nerd font"
    elif base_font == "ttf-autohint":
        c["base"] = "autohint ttf"
    else:
        c["base"] = "ttf"
    f.write(json.dumps(c, indent=4))

for f in listdir(base_font_path):
    if f.endswith(".ttf"):
        generate(f)
        print("generated:", f)
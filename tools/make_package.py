#!/usr/bin/env python3
"""Assembles a ReCoF Server package from builds of its parts.

usage: python tools/make_package.py --platform windows|linux --version X.Y.Z
           --engine <folder> --hl <hl.dll or hl.so> --metamod <metamod.dll or metamod_i386.so>
           --amxx <AMX Mod X package's addons/amxmodx folder> --amxx-repo <ReCoF-AMXX checkout>
           [--steam-api <steam_api.dll or libsteam_api.so>] [--sources NAME=COMMIT ...] [--out dist]

--engine is the folder with the engine, the dedicated launcher and the filesystem (Windows: msvc/Release of this
repository; Linux: the folder holding engine_i486.so, hlds_linux and filesystem_stdio.so). The package also gets
package/common, package/<platform>, the Cry of Fear gamedata of --amxx-repo (newer than a package build may have),
a SOURCES.txt with the commits it was built from, and is zipped (Windows) or tarred (Linux) into --out.
"""
import argparse
import os
import shutil
import stat
import sys
import tarfile
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENGINE = {
    "windows": ["hlds.exe", "swds.dll", "filesystem_stdio.dll"],
    "linux": ["hlds_linux", "engine_i486.so", "filesystem_stdio.so"],
}
STEAM_API = {"windows": "steam_api.dll", "linux": "libsteam_api.so"}
HL = {"windows": "hl.dll", "linux": "hl.so"}
METAMOD = {"windows": "metamod.dll", "linux": "metamod_i386.so"}
TEXT = (".txt", ".cfg", ".ini", ".bat", ".sh", ".inc", ".sma")


def copy(src, dst):
    if not os.path.isfile(src):
        sys.exit("missing: " + src)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree(src, dst):
    if not os.path.isdir(src):
        sys.exit("missing folder: " + src)
    for base, dirs, files in os.walk(src):
        rel = os.path.relpath(base, src)
        for f in files:
            copy(os.path.join(base, f), os.path.join(dst, rel, f))


def line_endings(folder, platform):
    """Our text files in the line endings of the platform; .sh always LF."""
    for base, dirs, files in os.walk(folder):
        for f in files:
            if not f.endswith(TEXT):
                continue
            p = os.path.join(base, f)
            data = open(p, "rb").read()
            if b"\0" in data:
                continue
            text = data.replace(b"\r\n", b"\n")
            if platform == "windows" and not f.endswith(".sh"):
                text = text.replace(b"\n", b"\r\n")
            open(p, "wb").write(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--platform", required=True, choices=["windows", "linux"])
    ap.add_argument("--version", required=True)
    ap.add_argument("--engine", required=True)
    ap.add_argument("--steam-api")
    ap.add_argument("--hl", required=True)
    ap.add_argument("--metamod", required=True)
    ap.add_argument("--amxx", required=True)
    ap.add_argument("--amxx-repo", required=True)
    ap.add_argument("--sources", nargs="*", default=[])
    ap.add_argument("--out", default=os.path.join(ROOT, "dist"))
    a = ap.parse_args()

    name = f"ReCoF-Server-{a.version}-{a.platform}"
    out = os.path.join(a.out, name)
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)

    for f in ENGINE[a.platform]:
        copy(os.path.join(a.engine, f), os.path.join(out, f))
    steam_api = a.steam_api or os.path.join(ROOT, "rehlds", "lib",
                                            "steam_api.dll" if a.platform == "windows" else "linux32/libsteam_api.so")
    copy(steam_api, os.path.join(out, STEAM_API[a.platform]))

    game = os.path.join(out, "cryoffear")
    copy(a.hl, os.path.join(game, "cl_dlls", HL[a.platform]))
    copy(a.metamod, os.path.join(game, "addons", "metamod", "dlls", METAMOD[a.platform]))
    copy_tree(a.amxx, os.path.join(game, "addons", "amxmodx"))
    gamedata = os.path.join(a.amxx_repo, "gamedata", "common.games")
    copy(os.path.join(gamedata, "master.games.txt"),
         os.path.join(game, "addons", "amxmodx", "data", "gamedata", "common.games", "master.games.txt"))
    copy_tree(os.path.join(gamedata, "virtual.games", "cryoffear"),
              os.path.join(game, "addons", "amxmodx", "data", "gamedata", "common.games", "virtual.games", "cryoffear"))

    copy_tree(os.path.join(ROOT, "package", "common"), out)
    copy_tree(os.path.join(ROOT, "package", a.platform), out)

    with open(os.path.join(out, "SOURCES.txt"), "w") as f:
        f.write(f"ReCoF Server {a.version} for {a.platform}, built from:\n")
        for s in a.sources:
            f.write(f"  {s}\n")
    line_endings(out, a.platform)

    if a.platform == "linux":
        for f in ("hlds_linux", "start_server.sh"):
            p = os.path.join(out, f)
            os.chmod(p, os.stat(p).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        archive = out + ".tar.gz"
        with tarfile.open(archive, "w:gz") as t:
            t.add(out, arcname=name)
    else:
        archive = out + ".zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
            for base, dirs, files in os.walk(out):
                for f in files:
                    p = os.path.join(base, f)
                    z.write(p, os.path.join(name, os.path.relpath(p, out)))
    print(f"{archive} ({os.path.getsize(archive) // 1024} KiB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

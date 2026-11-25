#!/usr/bin/env python3
"""news-image-20261125 entry: copy the artwork to /output/entry.png.

The artwork is entry.png beside this file: a one-page newspaper front
page summing up Wednesday 25 November 2026 in six stories (Houthis hit
Riyadh's tallest tower, wounding 11, in a second strike in under a
week; Zelenskiy confirms Ukraine hit the Russian ship Sparta II in the
Gulf of Finland; Nvidia's bounce fades as shares slide 6%; 25 people
held hostage in a Cartagena supermarket; Real Madrid rout PSV 5-1;
England crush Australia in the second T20I).
Standard library only, no network, deterministic: the same bytes are
written on every run.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # The gate reads exactly the bytes written: refuse a partial copy.
    if os.path.getsize(dst) != os.path.getsize(src):
        raise SystemExit("entry.png copy incomplete")


if __name__ == "__main__":
    main()

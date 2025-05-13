import argparse
import logging
import os
import random
import sys
import urllib.request
from pathlib import Path

import mapillary.interface as mly

CONFIG_DIR = Path.home() / ".config" / "mapillary-nearby"
TOKEN = CONFIG_DIR / "token"

def build_parser():
    parser = argparse.ArgumentParser(description='Fetch a random image near a particular location.', epilog="@readwithai 📖 https://readwithai.substack.com/p/habits ⚡️ machine-aided reading ✒️")
    parser.add_argument('--latitude', '--lat', type=float, required=True)
    parser.add_argument('--longitude', '--long', type=float, required=True)
    parser.add_argument('--radius', type=unit_float, required=True)
    parser.add_argument('--debug', action='store_true', default=False)

    parser.add_argument("filename")
    return parser


def main():
    unlog("mapillary.utils.client") # was logging to stdout

    args = build_parser().parse_args()
    os.makedirs(CONFIG_DIR, exist_ok=True)


    if args.debug:
        logging.basicConfig(stream=sys.stderr)

    if TOKEN.exists():
        with TOKEN.open() as stream:
            token = stream.read()
    else:
        token = input("Go to https://www.mapillary.com/dashboard/developers and create token (see readme)")
        with TOKEN.open("w") as stream:
            stream.write(token)

    mly.set_access_token(token)
    data = mly.get_image_close_to(args.latitude, args.longitude, radius=args.radius).to_dict()

    image_id = random.choice(data["features"])["properties"]["id"]
    url = mly.image_thumbnail(image_id)

    with urllib.request.urlopen(url) as stream:
        data = stream.read()

    with open(args.filename, "wb") as stream:
        stream.write(data)

def unit_float(s):
    digits = []
    units = []
    it = iter(s)
    for x in it:
        if x.isdigit() or x == ".":
            digits.append(x)
        else:
            units.append(x)
            break
    units.extend(it)

    digits = "".join(digits)
    units = "".join(units)

    match units:
        case "km":
            return 1000 * float(digits)
        case "m":
            return float(digits)
        case _:
            raise Exception(f'Could not recognise unit {units}')

def unlog(name):
    logger = logging.getLogger(name)
    for h in logger.handlers:
        logger.removeHandler(h)

import subprocess
import re

# partially based on code from https://github.com/skagedal/svgclip/blob/master/svgclip.py

def query_svg(svgfile):
    """Parses the output from inkscape --query-all"""
    fields = ('name', 'x', 'y', 'width', 'height')

    output = subprocess.check_output(["inkscape", "--query-all", svgfile])
    for line in output.strip().decode().split('\n'):
        split = line.split(',')
        yield dict(zip(fields, [split[0]] + [float(x) for x in split[1:]]))

def do_crop(svgfile, outfile, margin):
    querylines = list(query_svg(svgfile))

    page = querylines[0] # root element
    minX = page["width"]
    minY = page["height"]
    maxX = 0
    maxY = 0

    for line in querylines[1:]:
        if (line["width"] < page["width"]
            and line["height"] < page["height"]):
            minX = min(minX, line["x"])
            minY = min(minY, line["y"])
            maxX = max(maxX, line["x"] + line["width"])
            maxY = max(maxY, line["y"] + line["height"])

    x = max(minX - margin/2, 0)
    y = max(minY - margin/2, 0)
    width = min(maxX - minX + margin, page["width"])
    height = min(maxY - minY + margin, page["height"])

    lines = []
    with open(svgfile) as f:
        lines = f.readlines()

    lines[0] = re.sub("width='[^']*' height='[^']*'",
                      f"width='{width}px' height='{height}px' " +
                      f"viewBox='{x} {y} {width} {height}'",
                      lines[0])

    with open(outfile, "w") as f:
        f.writelines(lines)

do_crop("/home/adam/scratch/whatever_page001.svg", "out.svg")

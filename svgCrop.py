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

lines = list(query_svg("whatever_page001.svg"))

minX = lines[0]["width"]
minY = lines[0]["height"]
maxX = 0
maxY = 0

for line in lines[1:]:
    if (line["width"] < lines[0]["width"]
        and line["height"] < lines[0]["height"]):
        minX = min(minX, line["x"])
        minY = min(minY, line["y"])
        maxX = max(maxX, line["x"] + line["width"])
        maxY = max(maxY, line["y"] + line["height"])

print(minX, minY, maxX-minX, maxY-minY)

lines = []
with open("whatever_page001.svg") as f:
    lines = f.readlines()

lines[0] = re.sub("width='[^']*' height='[^']*'",
                  f"width='{maxX-minX}px' height='{maxY-minY}px' " +
                  f"viewBox='{minX} {minY} {maxX-minX} {maxY-minY}'", lines[0])

with open("out.svg", "w") as f:
    f.writelines(lines)

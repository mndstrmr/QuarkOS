import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

GENERATION_MESSAGE = """\
This file was generated by a script. Any changes made to it are temporary.
See $PROJECT_ROOT/fontchars/main.py\
"""

outh = """\
#ifndef _WINDOWSERVER_FONTCHARS_H
#define _WINDOWSERVER_FONTCHARS_H

/*
{}
*/

typedef struct {{
	int width;
	int height;
	char* raw;
}} FontChar;

{}

#define FONT_SIZE {}

FontChar fontchar_for_char(char chr);

#endif\
"""

outc = """\
#include <windowserver/fontchars.h>

/*
{}
*/

FontChar fontchar_for_char(char chr) {{
	switch (chr) {{
	case ' ': return (FontChar) {{ .width=FONTCHAR_61_W, .height=0, .raw=0 }};
{}
	default: return (FontChar) {{ .width=0, .height=0, .raw=0 }};
	}}
}}
"""

values = []
switch_values = []

h2 = lambda x: ("0" + hex(x)[2:])[-2:]

alpha = "".join([chr(a + ord('a')) for a in range(26)])
alpha = alpha + alpha.upper() + "".join([chr(a + ord('0')) for a in range(10)]) + "-+=*/\\?()[]{}'\"<>,.#!:"
print(alpha)

FONT_SIZE = 32

font = ImageFont.truetype("fontchars/JetBrains_Mono/static/JetBrainsMono-Regular.ttf", FONT_SIZE)
h = font.getsize(alpha)[1]

for char in alpha:
	image = Image.new("RGBA", (font.getsize(char)[0], h))
	draw = ImageDraw.Draw(image)
	draw.text((0, 0), char, (255, 255, 255, 255), font=font)

	pixels = image.load()

	pixels_str = ""
	for y in range(image.height):
		for x in range(image.width):
			r, g, b, a = pixels[x, y]
			pixels_str += f"\\x{h2(r)}\\x{h2(g)}\\x{h2(b)}\\x{h2(a)}"

	hchar = hex(ord(char))[2:]
	values.append(f"#define FONTCHAR_{hchar}_RAW \"{pixels_str}\"")
	values.append(f"#define FONTCHAR_{hchar}_W {image.width}")
	values.append(f"#define FONTCHAR_{hchar}_H {image.height}")
	values.append("")

	switch_values.append(f"\tcase 0x{hchar}:\n\t\treturn (FontChar) {{ .width=FONTCHAR_{hchar}_W, .height=FONTCHAR_{hchar}_H, .raw=FONTCHAR_{hchar}_RAW }};")


outh = outh.format(GENERATION_MESSAGE, "\n".join(values), FONT_SIZE)
outc = outc.format(GENERATION_MESSAGE, "\n".join(switch_values))

with open("src/user/windowserver/include/windowserver/fontchars.h", "w") as f: f.write(outh)
with open("src/user/windowserver/utils/fontchars.c", "w") as f: f.write(outc)

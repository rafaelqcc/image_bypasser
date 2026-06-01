from PIL import Image

TEMPLATE_FILE = 'image.rbxmx'
OUTPUT_FILE = 'new_image.rbxmx'
IMAGE_FILE = 'test.jpg'

def load_template(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def load_image(path, size=(128, 96)):
    img = Image.open(path).convert('RGB')
    return img.resize(size)

def rgb_to_str(rgb):
    return f"{rgb[0]},{rgb[1]},{rgb[2]}"

def build_image_data(image):
    pixels = image.load()
    width, height = image.size

    lines = ["local image = {"]

    for y in range(height):
        row = ['    [{}] = "'.format(y)]

        for x in range(width):
            r, g, b = pixels[x, y]
            color = f'rgb({r},{g},{b})'

            row.append(
                f'<stroke color="{color}">'
                f'<font color="{color}">□</font></stroke>'
            )

        row.append('",')
        lines.append(''.join(row))

    lines.append("}\n\nreturn image")

    return '\n'.join(lines)

def main():
    base_xml = load_template(TEMPLATE_FILE)
    image = load_image(IMAGE_FILE)

    image_data = build_image_data(image)

    result = base_xml.replace('___', image_data)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(result)

    print("Done:", OUTPUT_FILE)

if __name__ == "__main__":
    main()

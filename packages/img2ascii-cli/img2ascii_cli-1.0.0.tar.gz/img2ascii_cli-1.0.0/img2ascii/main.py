
from PIL import Image
import argparse

ASCII_CHARS = ['@', '%', '#', '*', '+', '=', '-', ':', '.', ' ']

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width / 1.65
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters

def convert_image_to_ascii(path, new_width=100):
    try:
        image = Image.open(path)
    except Exception as e:
        print(f"Unable to open image file {path}. Error: {e}")
        return

    image = resize_image(image, new_width)
    image = grayify(image)
    ascii_str = pixels_to_ascii(image)
    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = "\n".join([ascii_str[index:(index + img_width)] for index in range(0, ascii_str_len, img_width)])
    print(ascii_img)
    return ascii_img

def main():
    parser = argparse.ArgumentParser(description="Convert images to ASCII art")
    parser.add_argument("image_path", help="Path to the image file")
    parser.add_argument("--width", type=int, default=100, help="Width of the ASCII art")
    parser.add_argument("--out", help="Output text file (optional)")
    args = parser.parse_args()

    ascii_img = convert_image_to_ascii(args.image_path, args.width)

    if args.out:
        with open(args.out, "w") as f:
            f.write(ascii_img)
    else:
        print(ascii_img)

if __name__ == "__main__":
    main()

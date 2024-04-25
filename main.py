import math
import os
import requests
from PIL import Image  # pip install Pillow

# Just set this. It should be in the URL
image_id = 102774



def image_exists(width, height):
    wquotient, wremainder = divmod(width, 512)
    hquotient, hremainder = divmod(height, 512)
    if wremainder == 0: wremainder += 512
    if hremainder == 0: hremainder += 512
    url = "https://iiif.dx.artsmia.org/" + str(image_id) + ".jpg/" + str(wquotient * 512) + "," + str(hquotient * 512) + "," + str(wremainder) + "," + str(hremainder) + "/" + str(wremainder) + ",/0/default.jpg"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False


def get_image_dimensions():
    print("Finding image dimensions")
    width = 0
    while image_exists(width, 0):
        width += 512
    width += 512
    while not image_exists(width, 0):
        width -= 1
    print("Found an image width of " + str(width))
    
    height = 0
    while image_exists(0, height):
        height += 512
    height += 512
    while not image_exists(0, height):
        height -= 1
    print("Found an image height of " + str(height))
    
    return width, height


def download_images(max_width, max_height):
    print("Downloading image pieces")
    urls = []
    # iterate through heights (we will do first row first)
    for i in range(0, max_height, 512):
        width = 512
        height = 512
        # iterate through widths
        for j in range(0, max_width, 512):
            if j > max_width - 512:
                width = max_width - j
            if i > max_height - 512:
                height = max_height - i
            urls.append("https://iiif.dx.artsmia.org/" + str(image_id) + ".jpg/" +
                        str(j) + "," +
                        str(i) + "," +
                        str(width) + "," +
                        str(height) + "/" +
                        str(width) + ",/0/default.jpg")

    # Create images directory if not exists
    if not os.path.exists('images'):
        os.makedirs('images')

    for i, url in enumerate(urls, start=1):
        filename = f"images/image_{i}.jpg"
        download_image(url, filename)


def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download image from {url}")


def combine_images(max_width, max_height):
    print("Combining images")
    columns = math.ceil(max_width/512)
    rows = math.ceil(max_height/512)

    width = 512
    height = 512

    # Create a new image to hold the combined image
    combined_image = Image.new("RGB", (width * columns, height * rows))

    # Loop through each image file
    image_index = 1
    for y in range(rows):
        for x in range(columns):

            # Open the image
            image_path = f"images/image_{image_index}.jpg"
            image = Image.open(image_path)

            # Paste the image onto the combined image
            combined_image.paste(image, (x * width, y * height))

            image_index += 1

    # Save the combined image
    combined_image.save("full_resolution_image.png")
    print("Full resolution image created successfully!")


def main():
    width, height = get_image_dimensions()
    download_images(width, height)
    combine_images(width, height)

main()

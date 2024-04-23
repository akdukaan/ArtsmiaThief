import math
import os
import requests
from PIL import Image  # pip install Pillow

# Just set these three
# Open developer settings and go to the networks tab
# Zoom in all the way and go to the bottom right of the image
# In the network requests, there should've been many response named default.jpg
# You'll want to find the one that's the bottom right corner when it's zoomed in the most
# That'll typically mean it has the smallest size and you can double click the thumbnail to verify
# Single clicking on default.jpg will bring up a menu named headers.
# In the headers menu, find the request URL. 
# Here's an example of a request url https://iiif.dx.artsmia.org/102774.jpg/6144,4608,151,385/151,/0/default.jpg
# The numbers before ".jpg" is the image id. (102774)
# The width can be found by summing up the first and third numbers after ".jpg" (6144 + 151)
# The height can be found by summing up the second and fourth numbers after ".jpg" (4608 + 385)

image_id = 102774
max_width = 6295
max_height = 4993


def download_images():
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
        print(f"Downloaded {url} and saved as {filename}")
    else:
        print(f"Failed to download image from {url}")


def combine_images():
    print("Combining images")
    columns = math.ceil(max_width/512)
    rows = math.ceil(max_height/512)

    # Define width and height based on first image
    first_image = Image.open("images/image_1.jpg")
    width, height = first_image.size

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
    combined_image.save("combined_image.png")

    print("Combined image created successfully!")


def main():
    download_images()
    combine_images()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

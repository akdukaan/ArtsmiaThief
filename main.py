import os
import requests
from PIL import Image # pip install Pillow


def download_images():
    urls = []
    # iterate through heights (do first column first)
    for i in range(0, 4609, 512):
        height = 512
        width = 512
        # iterate through widths
        for j in range(0, 6145, 512):
            if j == 6144:
                height = 151
            if i == 4608:
                width = 385
            urls.append("https://iiif.dx.artsmia.org/102774.jpg/" +
                        str(j) + "," +
                        str(i) + "," +
                        str(height) + "," +
                        str(width) + "/" +
                        str(height) + ",/0/default.jpg")

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
    columns = 13
    rows = 10

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

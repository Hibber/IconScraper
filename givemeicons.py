import os

import requests
from bs4 import *


# CREATE FOLDER
def folder_create(images):
    try:
        folder_name = input("Enter Folder Name:- ")
        # folder creation
        os.mkdir(folder_name)

    # if folder exists with that name, ask another name
    except:
        print("Folder already exists with that name!")
        folder_create()

    # image downloading start
    print("Downloading Images...")
    download_images(images, folder_name)


# DOWNLOAD ALL IMAGES FROM THAT URL
def download_images(images, folder_name):
    # initial count is zero
    count = 0

    # print total images found in URL
    print(f"Total {len(images)} Image Found!")

    # checking if images is not zero
    if len(images) != 0:
        for i, image in enumerate(images):
            # From image tag fetch image source URL

            # First we will search for "data-srcset" in img tag
            try:
                # In image tag, search for "data-srcset"
                image_link = image["data-srcset"]

            # then we will search for "data-src" in img
            except:
                try:
                    # Search for "data-src"
                    image_link = image["data-src"]
                except:
                    try:
                        # Search for "data-fallback-src"
                        image_link = image["data-fallback-src"]
                    except:
                        try:
                            # Search for "src"
                            image_link = image["src"]

                        # if no source URL found
                        except:
                            pass

            # After getting image source URL
            # We will try to get the content of image
            try:
                r = requests.get(image_link).content
                try:

                    r = str(r, "utf-8")

                except UnicodeDecodeError:

                    # After checking above condition, download image
                    with open(f"{folder_name}/images{i + 1}.png", "wb+") as f:
                        f.write(r)

                    # counting number images downloaded
                    count += 1
            except:
                pass

        # if all images download
        if count == len(images):
            print("All Images Downloaded!")

        else:
            print(f"Total {count} Images Downloaded Out of {len(images)}")


def main(url):
    # content of URL
    r = requests.get(url)

    # Parse HTML Code
    soup = BeautifulSoup(r.text, "html.parser")

    # find all images in URL
    images = soup.findAll("img")

    # Call folder create function
    folder_create(images)


url = input("Enter URL:- ")
main(url)

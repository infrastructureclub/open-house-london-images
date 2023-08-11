#!/usr/bin/python
import os
import sys
import json
import urllib

from github import Github

year = 2023

g = Github(os.environ["GITHUB_TOKEN"])
repo = g.get_repo("jonty/open-house-london-data")
contents = repo.get_contents("data/%s" % year)
for content_file in contents:
    data = json.loads(content_file.decoded_content)
    print("\nChecking %s images for location %s..." % (len(data["images"]), data["id"]))

    path = "images/%s/%s" % (year, data["id"])
    os.makedirs(path, exist_ok=True)

    for image in data["images"]:
        if image["url"].startswith("/"):
            print("SKIPPING INVALID IMAGE: %s" % image)
            continue

        filename = os.path.basename(image["url"])
        file_path = "%s/%s" % (path, filename)

        if not os.path.isfile(file_path):
            print("Downloading %s" % image["url"])
            urllib.request.urlretrieve(image["url"], file_path)

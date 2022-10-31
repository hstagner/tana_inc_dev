import datetime
import requests  # This may need to be installed from pip
import json
import re

token = '<Insert Readwise Token Here>'

def fetch_from_export_api(updated_after=None):
    full_data = []
    next_page_cursor = None
    while True:
        params = {}
        if next_page_cursor:
            params['pageCursor'] = next_page_cursor
        if updated_after:
            params['updatedAfter'] = updated_after
        print("Making export api request with params " + str(params) + "...")
        response = requests.get(
            url="https://readwise.io/api/v2/export/",
            params=params,
            headers={"Authorization": f"Token {token}"}, verify=False
        )
        full_data.extend(response.json()['results'])
        next_page_cursor = response.json().get('nextPageCursor')
        if not next_page_cursor:
            break

    return full_data

# Get all of a user's books/highlights from all time
all_data = fetch_from_export_api()

json_object_string = json.dumps(all_data, indent=4)

json_object = json.loads(json_object_string)

for item in json_object:

    with open("readwise-tana-export", "a") as outfile:
        outfile.write("%%tana%%\n")

    highlights = item["highlights"]
    title = item["title"]
    url = item["source_url"]
    category = item["category"]
    author = item["author"]
    with open("readwise-tana-export", "a") as outfile:

        outfile.write(f"- {title} #readwise\n")
        outfile.write(f"  - URL:: \n")
        outfile.write(f"  - type:: {category}\n")
        outfile.write(f"  - author:: {author}\n")
        outfile.write("  - Highlights\n")

        for highlight in highlights:

            highlightText = highlight["text"]
            lines = highlightText.split("\n");

            for line in lines:

                cleanedLine = re.sub("/•\s+/", "", line.strip());

                if (len(cleanedLine) > 0):

                    outfile.write(f"    - {cleanedLine} \n")

    print(item["title"])



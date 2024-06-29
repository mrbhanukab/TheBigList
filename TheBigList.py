import json
import requests


def extract_urls_from_json(json_data):
    trackers = []
    ads = []
    annoyances = []

    for category, category_data in json_data.items():
        if category in ["trackers", "ads", "annoyances"]:
            for data in category_data:
                repo = data.get('repo')
                sources = data.get('sources')
                if repo and sources:
                    for source in sources:
                        source_urls = source.split(',')
                        for source_url in source_urls:
                            try:
                                response = requests.get(source_url.strip())
                                if response.status_code == 200:
                                    urls = response.text.split('\n')

                                    # Remove "0.0.0.0 " from URLs
                                    urls = [url.strip().replace("0.0.0.0 ", "")
                                            for url in urls]

                                    # Filter out comments and empty lines
                                    urls = [
                                        url for url in urls if url and not url.startswith(('#', '!'))]

                                    if category == "trackers":
                                        trackers.extend(urls)
                                        print(f"👍 Added URLs from ({
                                              source_url}) to trackers list")
                                    elif category == "ads":
                                        ads.extend(urls)
                                        print(f"👍 Added URLs from ({
                                              source_url}) to ads list")
                                    elif category == "annoyances":
                                        annoyances.extend(urls)
                                        print(f"👍 Added URLs from ({
                                              source_url}) to annoyances list")
                                else:
                                    print(f"??  Error loading URLs from {
                                          source_url}: Status code {response.status_code}")
                            except Exception as e:
                                print(f"??  Error loading URLs from {
                                      source_url}: {e}")
    return trackers, ads, annoyances


def remove_duplicates(urls):
    return list(set(urls))


def write_to_file(filename, urls):
    with open(filename, 'w') as file:
        for url in urls:
            file.write(url + '\n')
    print(f"✅ File '{filename}' saved with {len(urls)} URLs.")


# Load JSON data
with open('projects.json') as json_file:
    data = json.load(json_file)

# Extract URLs and load from files
trackers, ads, annoyances = extract_urls_from_json(data)

# Remove duplicates
trackers, ads, annoyances = remove_duplicates(
    trackers), remove_duplicates(ads), remove_duplicates(annoyances)

# Write to files
write_to_file('ads.txt', ads)
write_to_file('trackers.txt', trackers)
write_to_file('annoyances.txt', annoyances)

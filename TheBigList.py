import json
import requests

def extract_urls_from_json(json_data):
    trackers = []
    ads = []
    
    for category, url_list in json_data.items():
        for url in url_list:
            try:
                response = requests.get(url)
                print(f"->  Loading URL : {url}")
                if response.status_code == 200:
                    urls = response.text.split('\n')
                    
                    # Remove "0.0.0.0 " from URLs
                    urls = [url.strip().replace("0.0.0.0 ", "") for url in urls]
                    
                    # Filter out comments and empty lines
                    urls = [url for url in urls if url and not url.startswith(('#', '!'))]
                    
                    if category == "trackers":
                        trackers.extend(urls)
                        print(f"👍 Added URL ({url}) to trackers.txt")
                    elif category == "ads":
                        ads.extend(urls)
                        print(f"👍 Added URL ({url}) to ads.txt")
                else:
                    print(f"??  Error loading URLs from {url}: Status code {response.status_code}")
            except Exception as e:
                print(f"??  Error loading URLs from {url}: {e}")
    return trackers, ads


def remove_duplicates(urls):
    return list(set(urls))

def write_to_file(filename, urls):
    with open(filename, 'w') as file:
        for url in urls:
            file.write(url + '\n')

# Load JSON data
with open('urls.json') as json_file:
    data = json.load(json_file)

# Extract URLs and load from files
trackers, ads = extract_urls_from_json(data)

# remove duplicates
trackers, ads = remove_duplicates(trackers), remove_duplicates(ads)

# write_to_file
write_to_file('ads.txt', ads)
write_to_file('trackers.txt', trackers)

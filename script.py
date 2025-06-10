import os
import json
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree

# --- Configuration ---
ANIWATCH_BASE_URL = "https://aniwatchtv.to" # IMPORTANT: Verify this is the current domain for Aniwatch
REQUEST_DELAY_SECONDS = 2 # Adjust this value (e.g., 1 to 5 seconds) to avoid getting blocked.
                          # Higher values are safer but will make the script run slower.

def fetch_mal_id_from_detail_page(anime_url):
    """
    Fetches the MAL ID from an anime's detail page on Aniwatch.
    """
    try:
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = session.get(anime_url, headers=headers, timeout=10)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')
        sync_data_script = soup.find('script', id='syncData', type='application/json')

        if sync_data_script:
            json_data = json.loads(sync_data_script.string)
            mal_id = json_data.get('mal_id')
            if mal_id:
                print(f"  -> Found MAL ID: {mal_id}")
                return str(mal_id)
        print(f"  -> MAL ID not found on page: {anime_url}")
        return "0" # Default if not found
    except requests.exceptions.RequestException as e:
        print(f"  -> Error fetching {anime_url}: {e}")
        return "0"
    except json.JSONDecodeError as e:
        print(f"  -> Error parsing JSON on {anime_url}: {e}")
        return "0"
    except Exception as e:
        print(f"  -> An unexpected error occurred for {anime_url}: {e}")
        return "0"

def parse_aniwatch_html(file_path, category):
    """
    Parses an Aniwatch HTML file and extracts anime information,
    then fetches MAL ID from detail pages.
    """
    anime_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        flw_items = soup.find_all('div', class_='flw-item')

        print(f"  Found {len(flw_items)} anime entries in {os.path.basename(file_path)}.")

        for i, item in enumerate(flw_items):
            print(f"    Processing anime {i+1}/{len(flw_items)}...")

            title_element = item.find('h3', class_='film-name')
            if not title_element:
                print(f"    Skipping entry {i+1}: Title element not found.")
                continue
            title_link = title_element.find('a')
            anime_title = title_link['title'] if title_link else "Unknown Title"
            
            detail_path = title_link['href'] if title_link and 'href' in title_link.attrs else None

            mal_id = "0"
            if detail_path:
                full_detail_url = f"{ANIWATCH_BASE_URL}{detail_path}"
                mal_id = fetch_mal_id_from_detail_page(full_detail_url)
                time.sleep(REQUEST_DELAY_SECONDS) # Be polite and avoid getting blocked
            else:
                print(f"    Skipping MAL ID lookup for {anime_title}: Detail link not found.")

            mal_status_text = {
                'watching': 'Watching',
                'completed': 'Completed',
                'plantowatch': 'Plan to Watch',
                'dropped': 'Dropped'
            }.get(category, 'Unknown')

            anime_entry = {
                "series_animedb_id": mal_id,
                "series_title": anime_title,
                "my_status": mal_status_text,
                "update_on_import": "1"
            }
            anime_list.append(anime_entry)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return anime_list

def main():
    """
    Main function to process all HTML files, fetch MAL IDs, and generate the MAL import XML.
    """
    html_files_config = "html_files.txt"
    files_to_process = []

    if not os.path.exists(html_files_config):
        print(f"Error: '{html_files_config}' not found. Please create this file with your HTML list configurations.")
        return

    try:
        with open(html_files_config, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue # Skip empty lines and comments
                
                parts = line.split(':', 1)
                if len(parts) == 2:
                    file_path = parts[0].strip()
                    category = parts[1].strip().lower() # Ensure category is lowercase
                    files_to_process.append((file_path, category))
                else:
                    print(f"Warning: Skipping malformed line in {html_files_config}: '{line}'. Expected 'filename:category'")
    except Exception as e:
        print(f"Error reading '{html_files_config}': {e}")
        return

    if not files_to_process:
        print(f"No HTML files configured in '{html_files_config}'. Exiting.")
        return

    all_anime_entries = []
    
    for file_path, category in files_to_process:
        if os.path.exists(file_path):
            print(f"\n--- Processing '{file_path}' for category: '{category}' ---")
            anime_entries = parse_aniwatch_html(file_path, category)
            all_anime_entries.extend(anime_entries)
        else:
            print(f"\n--- Skipping '{file_path}': File not found. ---")

    if not all_anime_entries:
        print("\nNo anime entries were found or processed. No XML file will be generated.")
        return

    # Create the root element for the XML
    myanimelist_root = etree.Element("myanimelist")

    # Add the "myinfo" section
    myinfo = etree.SubElement(myanimelist_root, "myinfo")
    etree.SubElement(myinfo, "user_export_type").text = "1"

    # Add each anime entry to the XML
    for anime_data in all_anime_entries:
        anime_element = etree.SubElement(myanimelist_root, "anime")
        
        # Elements are created in the exact order specified in your latest example
        etree.SubElement(anime_element, "series_animedb_id").text = anime_data["series_animedb_id"] 
        etree.SubElement(anime_element, "series_title").text = anime_data["series_title"]
        etree.SubElement(anime_element, "my_status").text = anime_data["my_status"]
        etree.SubElement(anime_element, "update_on_import").text = anime_data["update_on_import"]

    # Create the XML tree and write to file
    tree = etree.ElementTree(myanimelist_root)
    output_file_name = "mal_import.xml"
    with open(output_file_name, 'wb') as f:
        f.write(etree.tostring(tree, pretty_print=True, encoding='utf-8', xml_declaration=True))

    print(f"\n\n--- Process Complete ---")
    print(f"Successfully generated '{output_file_name}' with {len(all_anime_entries)} anime entries.")
    print("You can now proceed to import this XML file into MyAnimeList.")
    print("Remember to check the generated 'mal_import.xml' file for any issues before importing.")

if __name__ == "__main__":
    main()
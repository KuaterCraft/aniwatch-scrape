# Aniwatch to MyAnimeList XML Exporter

A Python script to help you migrate your anime watching lists from Aniwatch (aniwatchtv.to) to MyAnimeList (MAL) by generating a compatible XML import file.

## ✨ Why this script?

Aniwatch (and similar sites) often lack a direct export feature for your watch lists. MyAnimeList, however, supports importing lists via an XML file. This script bridges that gap by:

1.  **Scraping your locally saved Aniwatch list HTML files.**
2.  **Fetching the correct MyAnimeList (MAL) IDs** for each anime from Aniwatch's own detail pages. This is crucial for MAL to correctly identify and update your entries.
3.  **Generating an XML file** in the precise format required by MyAnimeList for import.
4.  **Handling multiple categories** like Watching, On hold, Completed, Plan to Watch, and Dropped.
5.  **Creating a separate file** for any anime entries where the MAL ID could not be found, so you can manually check and update them later.

## 🔒 Is this safe?

Yes, this script is designed to be safe and transparent:

- **Open Source**: You have full access to review all the code (`script.py`). You can see exactly what it does.
- **Local Execution**: It's a Python script that runs on your local machine. It does not send your data to any third-party server.
- **No Credentials**: The script **does NOT** ask for or require any of your Aniwatch or MyAnimeList login credentials.
- **Read-Only Operations (mostly)**:
  - It **reads** your local HTML files.
  - It makes **HTTP GET requests** to a public website (`aniwatchtv.to` or its current domain) to fetch additional publicly available data (like MAL IDs).
  - It **creates** two new files: `mal_import.xml` and `not_found_mal_ids.txt` in the same directory.
- **Standard Libraries**: It uses well-known and widely adopted Python libraries (`requests`, `BeautifulSoup`, `lxml`) for web interaction and parsing.
- **No Modifications**: It does NOT modify any of your existing local HTML files or any other files on your system, other than creating the output XML.

The script's purpose is purely to help you transfer your list data.

## 🚀 How to Use

Follow these steps to get your Aniwatch list into MyAnimeList.

### Step 1: Download Your Aniwatch List Pages

You need to save the HTML content of your Aniwatch "My List" pages.

1.  Go to [Aniwatch (or aniwatchtv.to)](https://aniwatchtv.to/) and navigate to your "My List".
2.  For each category (`Watching`, `On Hold`, `Completed`, `Plan to Watch`, `Dropped`), you'll need to save the entire page.
    - **Right-click** on the page (or press `Ctrl+S` / `Cmd+S`).
    - Choose "Save As..." or "Save Page As...".
    - Select "Webpage, Complete" (or "Webpage, HTML Only" if "Complete" gives issues with file paths).
    - **Name your files clearly** based on the category and page number.
      - Example: `watching.html`, `dropped.html`
      - If a category has multiple pages (e.g., your "Completed" list might span several pages), save each page individually: `completed_1.html`, `completed_2.html`, `completed_3.html`, etc.
      - Similarly, if "Plan to Watch" or "Dropped" has multiple pages: `plantowatch.html`, `plantowatch_2.html`, etc.
3.  Place all these saved HTML files in the same directory where you will put the `script.py` and `html_files.txt`.

### Step 2: Prepare the `html_files.txt` Configuration

This file tells the script which local HTML files to read and what MyAnimeList status they correspond to.

1.  In the same directory where you saved your HTML files, create a new plain text file named `html_files.txt`.
2.  Open `html_files.txt` and list each HTML file you saved, followed by a colon (`:`) and its corresponding category.
    - **Supported Categories**: `watching`, `onhold`, `completed`, `plantowatch`, `dropped`. (These are case-insensitive, but using lowercase is good practice).
    - **Example `html_files.txt` content**:
      ```
      # Each line should contain the filename of your Aniwatch list HTML file,
      # followed by a colon (:) and the category name.
      #
      # Examples:
      watching.html:watching
      dropped.html:dropped
      plantowatch.html:plantowatch
      plantowatch_2.html:plantowatch
      completed_1.html:completed
      completed_2.html:completed
      completed_3.html:completed
      completed_4.html:completed
      completed_5.html:completed
      ```
3.  Save the `html_files.txt` file.

### Step 3: Setup Your Python Environment

1.  **Install Python**: If you don't have Python installed, download and install the latest version (Python 3.x) from [python.org](https://www.python.org/downloads/). Make sure to check the box "Add Python to PATH" during installation.

- (Optional Step) **Install a Virtual Environment**: It's a good practice to use a virtual environment for Python projects. You can create one using:
  `bash
    python -m venv myenv
    `
  Activate it with:

      - On Windows: `myenv\Scripts\activate`
      - On macOS/Linux: `source myenv/bin/activate`

      then proceed with the installation of required libraries.

2.  **Install Required Libraries**: Open your terminal or command prompt and navigate to the directory where you saved `script.py` and your HTML files. Then, run the following command to install the necessary libraries:
    ```bash
    pip install requests beautifulsoup4 lxml
    ```

### Step 4: Configure the Script (`script.py`)

Open `script.py` in a text editor (like Notepad, VS Code, Sublime Text, etc.).

1.  **`ANIWATCH_BASE_URL`**:
    - Locate the line: `ANIWATCH_BASE_URL = "https://aniwatchtv.to"`
    - **IMPORTANT**: Double-check that `https://aniwatchtv.to` is still the current and correct domain for Aniwatch. If the domain changes, update this URL accordingly.
2.  **`REQUEST_DELAY_SECONDS`**:
    - Locate the line: `REQUEST_DELAY_SECONDS = 2`
    - This is the delay between each web request the script makes to Aniwatch's detail pages.
    - A higher value (e.g., 3-5 seconds) is **safer** to avoid getting temporarily blocked by Aniwatch for too many requests, but it will make the script run **slower**.
    - If you encounter errors related to fetching data or "Connection refused," try increasing this value.

### Step 5: Run the Script

1.  Open your terminal or command prompt.
2.  Navigate to the directory where you have `script.py`, `html_files.txt`, and your downloaded HTML files.
    - (Optional) If you created a virtual environment, make sure to activate it first.
      - On Windows: `myenv\Scripts\activate`
      - On macOS/Linux: `source myenv/bin/activate`
3.  Execute the script using:
    ```bash
    python script.py
    ```
4.  The script will print progress messages to your terminal as it processes each file and fetches MAL IDs.
5.  Once finished, it will generate a file named `mal_import.xml` in the same directory.

### Step 6: Import to MyAnimeList

1.  Go to MyAnimeList.net and log in.
2.  Navigate to your anime list.
3.  Find the "Import/Export" option. This is usually under your username dropdown menu or directly on your list page (e.g., "Export My List" / "Import My List").
4.  Select "Import My List".
5.  Choose the `mal_import.xml` file that the script generated.
6.  Click the "Import" or "Upload" button.

MyAnimeList should now process your list. It might take a few moments. If successful, you'll see a confirmation message and your list updated.

---

## ⚠️ Limitations & Caveats

- **Internet Connection Required**: The script needs an active internet connection to fetch the `mal_id` for each anime from Aniwatch's website.
- **Runtime**: The process can be slow, especially for large lists, due to the necessary delays between web requests.
- **Potential IP Blocking**: While delays are implemented, there's always a slight risk of your IP being temporarily blocked by Aniwatch if you make too many requests too quickly. If this happens, wait a while and try again with a higher `REQUEST_DELAY_SECONDS`.
- **Aniwatch HTML Structure**: The script relies on the specific HTML structure of Aniwatch's list pages and detail pages (`<script id="syncData">`). If Aniwatch changes its website layout, the script might break and require updates.
- **Partial Data Import**: This script primarily imports `series_animedb_id` (MAL ID), `series_title`, and `my_status` (Watching, Completed, etc.). Other fields like `my_watched_episodes` (your specific progress), `my_score`, `my_start_date`, `my_finish_date`, etc., are **not available** from the Aniwatch list pages and will not be imported by this script. You'll need to update these manually on MyAnimeList if desired.
- **Title Matching**: While `series_animedb_id` greatly helps, occasionally MyAnimeList might still struggle with obscure titles or direct title mismatches if Aniwatch's title differs from MAL's. Manual corrections might be needed post-import.
- **Use VPN**: If you are in a region where Aniwatch is blocked, you may need to use a VPN to access the site and run the script.

---

Feel free to fork this repository, make improvements, and share it with others!# Aniwatch to MyAnimeList XML Exporter

A Python script to help you migrate your anime watching lists from Aniwatch (aniwatchtv.to) to MyAnimeList (MAL) by generating a compatible XML import file.

I wont take credits for this script as i am a JS developer not python 😅 so credits to Gemini AI for this script 😋

import requests
from bs4 import BeautifulSoup
import json
from urls import urls_dict
import os


def extract_data_by_header(soup, header_name):
    div_elements = soup.find_all("div", class_="textBlock")

    for div in div_elements:
        header = div.find("h2")
        if header and header.get_text(strip=True) == header_name:
            # Final list to hold paragraphs and list items in order
            result = []

            # Loop through direct children of the div
            for child in div.find_all(recursive=False):
                if child.name == "p":
                    result.append(child.get_text(strip=True))
                elif child.name in ["ul", "ol"]:
                    # Append each list item individually in order
                    for li in child.find_all("li"):
                        result.append(li.get_text(strip=True))

            return result

    return []


def fetch_html_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch content from {url}, status code: {response.status_code}")


def extract_table_data(soup, header_name):
    header = soup.find("h2", string=header_name)
    if header:
        table = header.find_next_sibling("table")
        if table:
            rows = table.find_all("tr")
            headers = [header.get_text(strip=True) for header in rows[0].find_all("th")]
            data = []
            for row in rows[1:]:
                cells = row.find_all("td")
                row_data = {headers[i]: cell.get_text(strip=True) for i, cell in enumerate(cells)}
                data.append(row_data)
            return data
    return []


def fetch_course_data(url):
    html_content = fetch_html_from_url(url)
    soup = BeautifulSoup(html_content, "html.parser")

    data = {
        "title": soup.find("h1", class_="collectionPageTitle").get_text(strip=True) if soup.find("h1",
                                                                                                 class_="collectionPageTitle") else "Unknown Title",
        "url": url,
        "description": extract_data_by_header(soup, "Description"),
        "topics_covered": extract_data_by_header(soup, "Topics covered"),
        "learning_outcomes": extract_data_by_header(soup, "Learning outcomes"),
        "prerequisites": extract_data_by_header(soup, "Pre-requisites"),
        "level": extract_data_by_header(soup, "Level"),
        "upcoming_courses": extract_table_data(soup, "Upcoming courses"),
        "previous_courses": extract_table_data(soup, "Previous courses"),
    }
    return data


# Fetch data for each URL
data = {}
for url in urls_dict['course_pages']:
    try:
        print("fetching data from:", url)
        course_data = fetch_course_data(url)
        data[course_data["title"]] = course_data
    except Exception as e:
        data[url] = {"error": str(e)}

# Save data to a JSON file
os.makedirs("app/data", exist_ok=True)
with open("app/data/course_data.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print("Data saved to app/data/course_data.json")

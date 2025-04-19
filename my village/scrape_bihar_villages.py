import requests
from bs4 import BeautifulSoup
import json
import time
import os

def get_district_villages(district_url):
    """Scrape villages from a district page."""
    print(f"Scraping district: {district_url}")
    response = requests.get(district_url)
    if response.status_code != 200:
        print(f"Failed to fetch {district_url}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    villages = []
    
    # Find the table with village data
    table = soup.find('table', {'class': 'table'})
    if not table:
        print(f"No table found in {district_url}")
        return []
    
    # Extract village data
    rows = table.find_all('tr')[1:]  # Skip header row
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            village_name = cols[1].text.strip()
            village_code = cols[0].text.strip()
            villages.append({
                'name': village_name,
                'code': village_code
            })
    
    return villages

def scrape_bihar_villages():
    """Scrape all villages in Bihar from vlist.in."""
    base_url = "https://vlist.in"
    bihar_url = "https://vlist.in/state/10.html"
    
    # Get the Bihar page
    response = requests.get(bihar_url)
    if response.status_code != 200:
        print("Failed to fetch Bihar page")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the district table
    district_table = soup.find('table')
    if not district_table:
        print("No district table found")
        return []
    
    # Extract district data
    districts = []
    rows = district_table.find_all('tr')[1:]  # Skip header row
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            district_link = cols[1].find('a')
            if district_link:
                district_name = district_link.text.strip()
                district_url = base_url + district_link['href']
                total_villages = cols[2].text.strip()
                
                districts.append({
                    'name': district_name,
                    'url': district_url,
                    'total_villages': total_villages,
                    'villages': []
                })
    
    # Scrape villages for each district
    for district in districts:
        district['villages'] = get_district_villages(district['url'])
        time.sleep(1)  # Be nice to the server
    
    return districts

def save_to_json(data, filename):
    """Save data to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    print("Starting to scrape Bihar villages...")
    bihar_data = {
        'state': 'Bihar',
        'state_code': '10',
        'districts': scrape_bihar_villages()
    }
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save to JSON file
    save_to_json(bihar_data, 'data/bihar_villages.json')
    print("Scraping completed!") 
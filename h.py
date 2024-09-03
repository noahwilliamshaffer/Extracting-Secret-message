import requests
from bs4 import BeautifulSoup

def fetch_document(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    return response.text

def extract_table_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the table element
    table = soup.find('table')
    
    coordinates = []
    max_x = max_y = 0
    
    if table:
        # Iterate over rows in the table
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skipping the header row
            cols = row.find_all('td')
            if len(cols) == 3:
                x = int(cols[0].get_text().strip())
                char = cols[1].get_text().strip()
                y = int(cols[2].get_text().strip())
                
                coordinates.append((char, x, y))
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    
    return coordinates, max_x, max_y

def create_grid(coordinates, max_x, max_y):
    # Create a grid of spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    
    for char, x, y in coordinates:
        grid[y][x] = char
    
    return grid

def print_grid(grid):
    for row in grid:
        print("".join(row))

def decode_secret_message(url):
    html_content = fetch_document(url)
    coordinates, max_x, max_y = extract_table_data(html_content)
    grid = create_grid(coordinates, max_x, max_y)
    print_grid(grid)

# Example usage
url = "https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub"
decode_secret_message(url)


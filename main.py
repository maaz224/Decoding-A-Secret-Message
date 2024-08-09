import requests
from bs4 import BeautifulSoup

def retrieve_and_print_grid(url):
    # Step 1: Fetch the Google Doc content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve document: {response.status_code}")
        return
    
    # Step 2: Parse the document content
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.get_text("\n").strip().splitlines()
    
    start_real_data = False
    real_data = []
    for item in data:
        if start_real_data:
            real_data.append(item)
        else:
            if item == 'y-coordinate':
                start_real_data = True
            
    print(real_data)
    
    # Step 3: Create a dictionary to hold the characters and coordinates
    char_positions = {}
    x = 0
    y = 0
    character = ""
    for index, item in enumerate(real_data):
        if index % 3 == 0:
            x = int(item.strip())
        if index % 3 == 1:
            character = item
        if index % 3 == 2:
            y = int(item.strip())
            char_positions[(x, y)] = character
    print(char_positions)
    
    # Step 4: Determine the size of the grid
    max_x = max(pos[0] for pos in char_positions) + 1
    max_y = max(pos[1] for pos in char_positions) + 1
    
    print( max_x, max_y)
    
    # Step 5: Create and fill the grid
    grid = [[' ' for _ in range(max_x)] for _ in range(max_y)]
    
    for (x, y), character in char_positions.items():
        grid[y][x] = character
    
    # Step 6: Print the grid
    for y in range(max_y - 1, -1, -1):  # Reverse the order of rows
        print(''.join(grid[y]))

# Example usage 
doc_url = "https://docs.google.com/document/u/0/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub?pli=1"
# doc_url = "https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub"
retrieve_and_print_grid(doc_url)
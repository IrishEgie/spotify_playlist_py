from bs4 import BeautifulSoup
import requests as rq

response = rq.get("https://www.billboard.com/charts/hot-100/2000-08-12")

soup = BeautifulSoup(response.text, "html.parser")

# Use partial class matching for song titles (adjust based on the exact HTML structure)
titles_soup = soup.find_all("h3", class_="c-title")

# Use partial class matching for chart numbers
num_soup = soup.find_all("span", class_="c-label")

# Extract and clean up the text
title_list = [title.getText().strip() for title in titles_soup]
num_list = [num.getText().strip() for num in num_soup]

# Print the results
print(title_list, num_list)
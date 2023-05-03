import requests
from bs4 import BeautifulSoup
import re
import csv

# List of the top 50 largest digital hedge funds in the US
hedge_funds = ["Bridgewater Associates", "Man Group", "Renaissance Technologies", "Millennium Management, LLC", "Citadel LLC", "D. E. Shaw & Co.", "Two Sigma", "Davidson Kempner Capital Management", "Farallon Capital", "The Children's Investment Fund Management", "Marshall Wace", "Ruffer", "AQR Capital", "Anchorage Capital Group", "Baupost Group", "Point72 Asset Management", "Capula Investment Management", "Wellington Management Company", "Brevan Howard", "PIMCO"]
# Open a CSV file for writing and write the header row
with open('hedge_fund_contacts.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Hedge Fund', 'Website', 'Email', 'Phone'])

    # Loop through each hedge fund and extract its website URL and contact information
    for fund in hedge_funds:
        # Search for the hedge fund's website using Google
        query = fund + ' website'
        url = 'https://www.google.com/search?q=' + query
        
        # Send a GET request to Google and extract the search results
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all('a')
        
        # Loop through the search results and find the hedge fund's website URL
        website_url = ''
        for result in search_results:
            href = result.get('href')
            print(href)
            if href.startswith('http') and 'google' not in href:
                # Found the hedge fund's website URL
                website_url = href
                break
        
        if website_url:
            # Send a GET request to the hedge fund's website and extract the contact information
            response = requests.get(website_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            phone_regex = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
            email = re.findall(email_regex, soup.get_text())
            phone = re.findall(phone_regex, soup.get_text())
            
            # Write the hedge fund's name, website URL, and contact information to the CSV file
            writer.writerow([fund, website_url, ', '.join(email), ', '.join(phone)])
        else:
            # Write the hedge fund's name and an error message to the CSV file
            writer.writerow([fund, 'Website not found', 'Email not found', 'Phone not found'])
    
print('CSV file saved successfully.')
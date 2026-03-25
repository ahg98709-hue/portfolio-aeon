
import requests
import json
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Union
import os
import urllib.parse

# --- Search ---

def search_web(query: str, max_results: int = 5) -> List[Dict]:
    """
    Performs a web search using DuckDuckGo.
    Returns a list of dictionaries with 'title', 'href', 'body'.
    """
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=max_results)]
            if not results:
                return [{"error": "No results found for query: " + query}]
            return results
    except Exception as e:
        return [{"error": f"Search failed: {e}"}]

def search_images(query: str, max_results: int = 5) -> List[Dict]:
    """Search for images."""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.images(query, max_results=max_results)]
            return results
    except Exception as e:
        return [{"error": str(e)}]

def search_news(query: str, max_results: int = 5) -> List[Dict]:
    """Search for news."""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.news(query, max_results=max_results)]
            return results
    except Exception as e:
        return [{"error": str(e)}]

# --- Retrieving Content ---

def get_page_content(url: str) -> str:
    """Fetches the raw HTML content of a page."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error: {e}"

def get_page_text(url: str) -> str:
    """Fetches and extracts visible text from a page."""
    try:
        html = get_page_content(url)
        if html.startswith("Error"):
            return html
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
            
        text = soup.get_text()
        
        # Break into lines and remove leading/trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text
    except Exception as e:
        return f"Error parsing text: {e}"

def get_page_title(url: str) -> str:
    """Fetches the title of a page."""
    try:
        html = get_page_content(url)
        if html.startswith("Error"):
            return "Unknown"
        soup = BeautifulSoup(html, 'html.parser')
        return soup.title.string if soup.title else "No Title"
    except Exception as e:
        return str(e)

# --- API Interaction ---

def api_get(url: str, params: Dict = {}, headers: Dict = {}) -> Union[Dict, str]:
    """Performs a GET request to an API."""
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Error: {e}"

def api_post(url: str, data: Dict = {}, headers: Dict = {}) -> Union[Dict, str]:
    """Performs a POST request to an API."""
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Error: {e}"

def download_file(url: str, output_path: str) -> str:
    """Downloads a file from a URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, stream=True, headers=headers, timeout=30)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return f"Downloaded to {output_path}"
    except Exception as e:
        return str(e)

# --- Utility ---

def get_public_ip() -> str:
    """Returns the public IP address."""
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return "Unknown"

def check_internet_connection() -> bool:
    """Checks for internet connectivity."""
    try:
        requests.get("https://google.com", timeout=3)
        return True
    except:
        return False

def extract_links(url: str) -> List[str]:
    """Extracts all hrefs from a page."""
    try:
        html = get_page_content(url)
        if html.startswith("Error"):
            return []
        soup = BeautifulSoup(html, 'html.parser')
        base_url = "{0.scheme}://{0.netloc}".format(urllib.parse.urlsplit(url))
        links = []
        for a in soup.find_all('a', href=True):
            link = a['href']
            if link.startswith('/'):
                link = urllib.parse.urljoin(base_url, link)
            if link.startswith('http'):
                links.append(link)
        return list(set(links))
    except:
        return []

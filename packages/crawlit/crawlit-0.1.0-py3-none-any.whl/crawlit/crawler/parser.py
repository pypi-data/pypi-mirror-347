#!/usr/bin/env python3
"""
parser.py - HTML parsing and link extraction
"""

import time
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def extract_links(html_content, base_url, delay=0.1):
    """
    Extract links from HTML content from various elements
    
    Args:
        html_content: The HTML content to parse
        base_url: The base URL for resolving relative links
        delay: Delay in seconds to be polite to the server
        
    Returns:
        list: List of absolute URLs found in the HTML
    """
    # Introduce a small delay to be polite to the server
    time.sleep(delay)
    
    soup = BeautifulSoup(html_content, 'lxml')
    links = set()  # Using a set to avoid duplicates
    
    # Dictionary of elements and their attributes that may contain URLs
    elements_to_extract = {
        'a': 'href',
        'img': 'src',
        'script': 'src',
        'link': 'href',
        'iframe': 'src',
        'video': 'src',
        'audio': 'src',
        'source': 'src',
        'form': 'action'
    }
    
    # Extract links from each element type
    for tag_name, attr_name in elements_to_extract.items():
        for tag in soup.find_all(tag_name, {attr_name: True}):
            url = tag[attr_name].strip()
            
            # Process the URL
            processed_url = _process_url(url, base_url)
            if processed_url:
                links.add(processed_url)
    
    return list(links)

def _process_url(url, base_url):
    """
    Process a URL: normalize, filter, and convert to absolute
    
    Args:
        url: The URL to process
        base_url: The base URL for resolving relative links
        
    Returns:
        str: Processed URL or None if URL should be filtered out
    """
    # Skip empty links, javascript links, mailto links, tel links, etc.
    if (not url or 
        url.startswith(('javascript:', 'mailto:', 'tel:', '#', 'data:'))):
        return None
            
    # Convert relative URLs to absolute
    absolute_url = urljoin(base_url, url)
    
    # Parse the URL
    parsed = urlparse(absolute_url)
    
    # Skip non-HTTP URLs
    if parsed.scheme not in ('http', 'https'):
        return None
    
    # Normalize the URL (remove fragments, etc.)
    normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    if parsed.query:
        normalized_url += f"?{parsed.query}"
        
    return normalized_url
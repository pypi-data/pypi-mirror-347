#!/usr/bin/env python3
"""
fetcher.py - HTTP request handling
"""

import logging
import requests

logger = logging.getLogger(__name__)

def fetch_page(url, user_agent="crawlit/1.0", max_retries=3, timeout=10):
    """
    Fetch a web page with retries and proper error handling
    
    Args:
        url: The URL to fetch
        user_agent: User agent string to use in the request
        max_retries: Maximum number of retries on failure
        timeout: Request timeout in seconds
        
    Returns:
        tuple: (success, response_or_error, status_code)
    """
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    retries = 0
    status_code = None
    
    while retries <= max_retries:
        try:
            logger.debug(f"Requesting {url} (attempt {retries + 1}/{max_retries + 1})")
            response = requests.get(
                url, 
                headers=headers,
                timeout=timeout
            )
            status_code = response.status_code
            
            # Check if the request was successful
            if response.status_code == 200:
                return True, response, status_code
            else:
                logger.warning(f"HTTP Error {response.status_code} for {url}")
                return False, f"HTTP Error: {response.status_code}", status_code
                
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout error for {url} (attempt {retries + 1})")
            retries += 1
            status_code = 408  # Request Timeout
            
        except requests.exceptions.ConnectionError:
            logger.warning(f"Connection error for {url} (attempt {retries + 1})")
            retries += 1
            status_code = 503  # Service Unavailable
            
        except requests.exceptions.TooManyRedirects:
            logger.warning(f"Too many redirects for {url}")
            return False, "Too many redirects", 310
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return False, str(e), status_code or 500
    
    return False, f"Max retries ({max_retries}) exceeded", status_code or 429

# Add fetch_url as an alias for fetch_page to make tests pass
# This provides backward compatibility with test code
def fetch_url(url, user_agent="crawlit/1.0", max_retries=3, timeout=10):
    """
    Alias for fetch_page - maintained for backward compatibility with tests
    
    Note: Tests expect this function to return just the response object,
    unlike fetch_page which returns (success, response, status_code)
    """
    success, response_or_error, status_code = fetch_page(url, user_agent, max_retries, timeout)
    
    # Return just the response object as expected by tests
    if success:
        # For success case, tests expect response object
        return response_or_error
    else:
        # For error case, tests expect an exception to be raised
        if isinstance(response_or_error, str) and "HTTP Error" in response_or_error:
            # Extract status code from error message and raise proper exception
            raise requests.exceptions.HTTPError(response_or_error)
        else:
            # For other errors, raise a generic exception
            raise requests.exceptions.RequestException(response_or_error)
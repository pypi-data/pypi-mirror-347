import re
from urllib.parse import urlparse, parse_qs

def parse_youtube_url(url):
    """
    Parses a YouTube URL and extracts the video ID.

    Args:
        url (str): The YouTube URL.

    Returns:
        str: The video ID if found, else None.
    """
    # Match standard YouTube URL patterns
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&]+)',
        r'(?:https?://)?(?:www\.)?youtu\.be/([^?&]+)'
    ]
    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            return match.group(1)
    
    # Handle embedded YouTube URLs
    parsed_url = urlparse(url)
    if 'youtube.com' in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        return query_params.get('v', [None])[0]
    
    return None
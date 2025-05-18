#!/usr/bin/env python3
"""
Earth View Image Parser

This script scrapes the Earth View website to collect image data and metadata.
It saves the results to a JSON file that can be used by the wallpaper changer.
"""

import urllib.request
import json
import os
import argparse
import concurrent.futures
from bs4 import BeautifulSoup
from pathlib import Path

def fetch_earth_view(image_id):
    """Fetch data for a single Earth View image"""
    try:
        print(f"Fetching {image_id} ...")
        url = f'https://earthview.withgoogle.com/{image_id}'
        
        with urllib.request.urlopen(url, timeout=10) as response:
            html = response.read()
            soup = BeautifulSoup(html, "lxml")
            
            region_element = soup.find("div", class_="content__location__region")
            country_element = soup.find("div", class_="content__location__country")
            globe_link = soup.find("a", id="globe", href=True)
            
            region = region_element.text if region_element else ""
            country = country_element.text if country_element else ""
            gmaps_url = globe_link['href'] if globe_link else ""
            
            image_url = f'https://www.gstatic.com/prettyearth/assets/full/{image_id}.jpg'
            
            return {
                'region': region,
                'country': country,
                'map': gmaps_url,
                'image': image_url
            }
    except urllib.error.HTTPError:
        return None
    except Exception as e:
        print(f"Error fetching {image_id}: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Earth View Image Parser')
    parser.add_argument('--start', type=int, default=1000, help='Starting image ID')
    parser.add_argument('--end', type=int, default=7030, help='Ending image ID')
    parser.add_argument('--workers', type=int, default=10, help='Number of worker threads')
    parser.add_argument('--output', type=str, default='earthview.json', help='Output JSON file')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    output_path = Path(args.output)
    output_dir = output_path.parent
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    image_ids = range(args.start, args.end + 1)
    
    # Use thread pool for parallel fetching
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(fetch_earth_view, image_id): image_id for image_id in image_ids}
        
        for future in concurrent.futures.as_completed(futures):
            image_id = futures[future]
            try:
                data = future.result()
                if data:
                    results.append(data)
                    print(f"Added {image_id} - {data['country']}")
            except Exception as e:
                print(f"Error processing {image_id}: {str(e)}")
    
    # Save results to JSON file
    with open(args.output, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)
    
    print(f"Completed! Found {len(results)} images. Data saved to {args.output}")

if __name__ == "__main__":
    main()

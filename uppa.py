"""Fetch photos from Unsplash API, calculate performance scores, display the results."""
import os
import json
import sys
import requests
import numpy as np
import matplotlib.pyplot as plt

# Read ACCESS_KEY and USERNAME from environment variables
ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
USERNAME = os.getenv('UNSPLASH_USERNAME')

# Check if ACCESS_KEY and USERNAME are set
if not ACCESS_KEY or not USERNAME:
    print("Please set the UNSPLASH_ACCESS_KEY and UNSPLASH_USERNAME environment variables.")
    sys.exit(1)

PHOTOS_FILENAME = 'photos.json'


def get_unsplash_photos(username, access_key):
    """Function to get all photos from Unsplash API with pagination"""
    url = f"https://api.unsplash.com/users/{username}/photos"
    all_photos = []
    page = 1
    per_page = 30

    while True:
        params = {
            'client_id': access_key,
            'page': page,
            'per_page': per_page,
            'stats': 'true'
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        photos = response.json()
        if not photos:
            break

        all_photos.extend(photos)
        page += 1

    return all_photos


def save_photos_to_file(photos, filename):
    """Function to save photos to a file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(photos, f, indent=4)


def load_photos_from_file(filename):
    """Function to load photos from a file"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


# Load or fetch photos
if os.path.exists(PHOTOS_FILENAME):
    photos = load_photos_from_file(PHOTOS_FILENAME)
    print("Loaded photos from photos.json")
else:
    photos = get_unsplash_photos(USERNAME, ACCESS_KEY)
    if not photos:
        print("No photos retrieved. Please check your username and access key.")
        sys.exit(1)
    save_photos_to_file(photos, PHOTOS_FILENAME)
    print("Fetched photos from Unsplash API and saved to photos.json")

# Calculate raw performance scores and filter photos
W_V = 1.5
W_D = 0.5
filtered_photos = []

for photo in photos:
    days_online = (np.datetime64(
        'now') - np.datetime64(photo['created_at'])).astype(int) / (24 * 60 * 60)
    if days_online >= 30:
        # Avoid division by zero
        views = photo['statistics']['views']['total'] or 1
        downloads = photo['statistics']['downloads']['total']
        raw_score = (views / days_online) * W_V + (downloads / views) * W_D
        photo['days_online'] = days_online
        photo['raw_score'] = raw_score
        filtered_photos.append(photo)

# Find the upper bound of raw scores using the IQR method
raw_scores = np.array([photo['raw_score'] for photo in filtered_photos])
Q1 = np.percentile(raw_scores, 25)
Q3 = np.percentile(raw_scores, 75)
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR

# Filter out upper bound outliers
filtered_photos = [
    photo for photo in filtered_photos if photo['raw_score'] <= upper_bound]

# Recalculate min and max raw scores after filtering
filtered_raw_scores = np.array([photo['raw_score']
                               for photo in filtered_photos])
min_raw = filtered_raw_scores.min()
max_raw = filtered_raw_scores.max()

# Normalize scores
for photo in filtered_photos:
    photo['normalized_score'] = (
        (photo['raw_score'] - min_raw) / (max_raw - min_raw)) * 100
    photo['days_online'] = int(photo['days_online'])

# Sort photos by normalized score and display the results
sorted_photos = sorted(
    filtered_photos, key=lambda x: x['normalized_score'], reverse=True)
for photo in sorted_photos:
    photo_id = photo['id']
    days_online = photo['days_online']
    views = photo['statistics']['views']['total']
    downloads = photo['statistics']['downloads']['total']
    normalized_score = photo['normalized_score']
    print(f"Photo URL: https://unsplash.com/photos/{photo_id}, Days Online: {days_online}, Views: {views}, Downloads: {downloads}, Normalized Score: {normalized_score:.2f}")

# Generate a bar chart
photo_ids = [photo['id'] for photo in sorted_photos]
normalized_scores = [photo['normalized_score'] for photo in sorted_photos]

plt.figure(figsize=(10, 8))
plt.barh(photo_ids, normalized_scores, color='skyblue')
plt.xlabel('Normalized Score')
plt.ylabel('Photo ID')
plt.title('Normalized Scores of Unsplash Photos')
plt.gca().invert_yaxis()  # Invert y-axis to have the highest score at the top
plt.show()

# UPPA (Unsplash Photo Performance Analyzer)

This script analyzes the performance of your photos on Unsplash. It fetches your photos, calculates performance scores, identifies outliers, filters them, normalizes the scores, and generates a visualization.

## What does this script do?

1. **Fetch Photos from Unsplash**: Retrieves your photos using the Unsplash API.
2. **Calculate Performance Scores**: Computes raw performance scores based on views per day and downloads per view.
3. **Identify Upper Bound Outliers**: Uses the Interquartile Range (IQR) method to calculate the upper bound for outliers.
4. **Filter Upper Bound Outliers**: Removes photos identified as upper bound outliers.
5. **Recalculate Min and Max Scores**: Recalculates the minimum and maximum raw scores after removing outliers.
6. **Normalize Scores**: Normalizes the scores of the remaining photos to a scale of 0 to 100.
7. **Output Results**: Prints the normalized scores, generates a bar chart, and optionally saves the results to a JSON file.

## Prerequisites

- Python 3.x
- `requests` library
- `numpy` library
- `matplotlib` library

You can install the required libraries using pip:

```sh
pip install requests numpy matplotlib
```

## Setup

1. **Unsplash API Access Key**: You need an Unsplash API access key. You can get it by registering as a developer on the Unsplash website.

2. **Environment Variables**: Set the `UNSPLASH_ACCESS_KEY` and `UNSPLASH_USERNAME` environment variables with your Unsplash access key and username.

### Setting Environment Variables

#### On macOS/Linux:

Add the following lines to your `.bashrc` or `.bash_profile`:

```sh
export UNSPLASH_ACCESS_KEY='your_unsplash_access_key'
export UNSPLASH_USERNAME='your_unsplash_username'
```

Then, source the file to apply the changes:

```sh
source ~/.bashrc  # or source ~/.bash_profile
```

#### On Windows:

Set the environment variables using the command line or through the System Properties dialog:

```sh
setx UNSPLASH_ACCESS_KEY "your_unsplash_access_key"
setx UNSPLASH_USERNAME "your_unsplash_username"
```

## Usage

Run the script using Python:

```sh
python uppa.py
```

The script will:

1. Check if `photos.json` exists. If it does, it will load photos from the file.
2. If `photos.json` does not exist, it will fetch photos from Unsplash, save them to `photos.json`, and proceed.
3. Calculate raw performance scores for each photo.
4. Filter out photos with fewer than 30 days online.
5. Identify and filter out upper bound outliers.
6. Recalculate min and max scores and normalize the scores to a range of 0 to 100.
7. Sort the photos by their normalized scores and print the results.
8. Generate a bar chart showing the normalized scores of the photos.

## Example Output

```sh
Photo URL: https://unsplash.com/photos/abc123, Days Online: 45, Views: 1200, Downloads: 150, Normalized Score: 92.50
Photo URL: https://unsplash.com/photos/def456, Days Online: 60, Views: 1500, Downloads: 180, Normalized Score: 85.30
...
```

A bar chart will also be displayed, visualizing the normalized scores of your photos.

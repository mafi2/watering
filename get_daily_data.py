import os
import requests
import pandas as pd

def download_meteoswiss_data(download_dir="data"):
    os.makedirs(download_dir, exist_ok=True)

    files_to_download = {
        "ogd-smn_bas_d_recent.csv": "https://data.geo.admin.ch/ch.meteoschweiz.ogd-smn/bas/ogd-smn_bas_d_recent.csv",
        "ogd-smn_meta_parameters.csv": "https://data.geo.admin.ch/ch.meteoschweiz.ogd-smn/ogd-smn_meta_parameters.csv"
    }

    for filename, url in files_to_download.items():
        file_path = os.path.join(download_dir, filename)
        
        if not os.path.exists(file_path):
            print(f"Downloading {filename}...")
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for HTTP errors
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"Saved to {file_path}")
            except requests.RequestException as e:
                print(f"Failed to download {filename}: {e}")
        else:
            print(f"{filename} already exists. Skipping download.")

# Example usage
download_meteoswiss_data()


def extract_columns_from_bas_d_recent(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"{csv_path} not found")

    # Read CSV (assuming it's ;-separated)
    df = pd.read_csv(csv_path, sep=";")

    # Extract only the two columns
    # From metadata: tre200d0 = Lufttemperatur 2 m ueber Boden; Tagesmittel
    cols = ['reference_timestamp', 'tre200d0']
    if not all(col in df.columns for col in cols):
        missing = [col for col in cols if col not in df.columns]
        raise ValueError(f"Missing columns in CSV: {missing}")

    extracted_df = df[cols]
    return extracted_df

# Example usage:
file_path = "data/ogd-smn_bas_d_recent.csv"
df_extracted = extract_columns_from_bas_d_recent(file_path)
print(df_extracted.head())

# Save as json:
json_path = "data/weather_data.json"

df_extracted.tail(3).to_json(json_path, orient='records', indent=2)
print(f"Last 3 rows saved to {json_path}")
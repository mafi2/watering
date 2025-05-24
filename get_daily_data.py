import os
import requests
import pandas as pd

def download_meteoswiss_data(download_dir="data"):
    os.makedirs(download_dir, exist_ok=True)

    files_to_download = {
        "ogd-smn_bas_d_recent.csv": {
            "url": "https://data.geo.admin.ch/ch.meteoschweiz.ogd-smn/bas/ogd-smn_bas_d_recent.csv",
            "always_download": True
        },
        "ogd-smn_meta_parameters.csv": {
            "url": "https://data.geo.admin.ch/ch.meteoschweiz.ogd-smn/ogd-smn_meta_parameters.csv",
            "always_download": False
        }
    }

    for filename, file_info in files_to_download.items():
        file_path = os.path.join(download_dir, filename)
        should_download = file_info["always_download"] or not os.path.exists(file_path)

        if should_download:
            print(f"Downloading {filename}...")
            try:
                response = requests.get(file_info["url"])
                response.raise_for_status()
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"Saved to {file_path}")
            except requests.RequestException as e:
                print(f"Failed to download {filename}: {e}")
        else:
            print(f"{filename} already exists. Skipping download.")

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

# Download meteoswiss data
download_meteoswiss_data()

# Example usage:
file_path = "data/ogd-smn_bas_d_recent.csv"
df_extracted = extract_columns_from_bas_d_recent(file_path)
print(df_extracted.tail())

# Save as json:
json_path = "data/weather_data.json"

df_extracted.tail(3).to_json(json_path, orient='records', indent=2)
print(f"Last 3 rows saved to {json_path}")
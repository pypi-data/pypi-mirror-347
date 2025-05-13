import os
import urllib.request
import pandas as pd

def _download_file_if_needed(filename: str, url: str, target_dir: str) -> str:
    """
    Download a file from a URL to the target directory if it does not already exist.
    Returns the full local file path.
    """
    os.makedirs(target_dir, exist_ok=True)
    filepath = os.path.join(target_dir, filename)
    if not os.path.exists(filepath):
        print(f"[scRegulate] Downloading {filename} to {filepath}...")
        try:
            urllib.request.urlretrieve(url, filepath)
        except Exception as e:
            raise RuntimeError(f"Failed to download {url}.\nError: {e}")
    return filepath

def collectri_prior(species: str = "human") -> pd.DataFrame:
    """
    Returns the collectri prior dataframe for the given species ("human" or "mouse").
    Downloads the file on first use and caches it under ~/.scregulate/priors/.

    Parameters:
    - species: str = "human" or "mouse"

    Returns:
    - pd.DataFrame with TF-target prior network
    """
    if species not in ["human", "mouse"]:
        raise ValueError("species must be either 'human' or 'mouse'")

    filename = f"collectri_{species}_net.csv"
    base_url = "https://github.com/YDaiLab/scRegulate/raw/main/prior/"
    url = base_url + filename
    target_dir = os.path.expanduser("~/.scregulate/priors")

    local_path = _download_file_if_needed(filename, url, target_dir)
    return pd.read_csv(local_path)

import os
import urllib.request

def download_nedlvs_if_needed():
    url = 'https://ned.ipac.caltech.edu/NED::LVS/fits/Current/'
    destination = os.path.join(os.path.dirname(__file__), 'NEDLVS_20210922_v2.fits')
    if not os.path.exists(destination):
        print(f"Downloading NEDLVS Catalog from {url} ...")
        urllib.request.urlretrieve(url, destination)
        print("Download complete.")
    else:
        print("NEDLVS .fits already exists.")
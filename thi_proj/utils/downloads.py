import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3 import Retry

from thi_proj.resource import resource_path
from thi_proj.utils import logger

LOGGER = logger.get_logger("bilibilib_get_audio", resource_path("../log/thi_proj.log"))


def download_resource(param_url: str, output_path: str, headers: dict):
    # Send an HTTP GET request to the specified URL to start downloading the file
    session = requests.Session()
    retries = Retry(total=5,  # at most retry  times
                    backoff_factor=0.3,  # retry interval time
                    status_forcelist=[500, 502, 503, 504])  # do retry if the status code met

    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("https://", HTTPAdapter(max_retries=retries))

    try:
        with session.get(param_url, headers=headers, stream=True) as l_response:
            l_response.raise_for_status()
            # Get the total file size from the "Content-Length" header
            if l_response.status_code == 200:
                content_length = int(l_response.headers.get("content-length", 0))

                if content_length == 0:
                    LOGGER.info("cant get the resources, content-length: {content_length}")
                    return
                # Open the output file in binary write mode
                with open(output_path, "wb") as file:
                    # Initialize the tqdm progress bar with the total file size
                    with tqdm(total=content_length, unit="B", unit_scale=True, desc=output_path) as proccess_bar:
                        # Iterate over the response content in chunks
                        for data in l_response.iter_content(chunk_size=1024):
                            # Write each chunk to the file
                            file.write(data)
                            # Update the progress bar by the chunk size
                            proccess_bar.update(len(data))
    except requests.exceptions.RequestException as e:
        LOGGER.error(f"download error: {e}")

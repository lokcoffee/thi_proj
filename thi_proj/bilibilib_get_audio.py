import json
from requests.adapters import HTTPAdapter
from urllib3.util import url
from urllib3.util.retry import Retry

import requests
from bs4 import BeautifulSoup, ResultSet
from lxml import etree
from tqdm import tqdm

import utils.logger
from resource import load_yaml, extract_base_url

LOGGER = utils.logger.get_logger("bilibilib_get_audio", "../log/thi_proj.log")

config = load_yaml("../resources/download_items.yml")

download_item = config["download_items"][0]["download_item"]

referer = extract_base_url(download_item["get_title_list_url"])
LOGGER.info(f"referer: {referer}")
# fake request head
def load_headers():
    return {
        "User-Agent": str(download_item["user_agent"]),
        # 防盗链子
        "Referer": referer,
        "Cookie": str(download_item["cookie"])
    }

def download_resource(param_url: str, output_path: str):
    # Send an HTTP GET request to the specified URL to start downloading the file
    session = requests.Session()
    retries = Retry(total=5,  # at most retry  times
                    backoff_factor=0.3,  # retry interval time
                    status_forcelist=[500, 502, 503, 504])  # do retry if the status code met

    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("https://", HTTPAdapter(max_retries=retries))

    try:
        with session.get(param_url, headers=load_headers(), stream=True) as l_response:
            l_response.raise_for_status()
            # Get the total file size from the "Content-Length" header
            if l_response.status_code == 200:
                total_size = int(l_response.headers.get("content-length", 0))

                if total_size == 0:
                    LOGGER.info("cant get the resources")
                    return
                # Open the output file in binary write mode
                with open(output_path, "wb") as file:
                    # Initialize the tqdm progress bar with the total file size
                    with tqdm(total=total_size, unit="B", unit_scale=True, desc=output_path) as proccess_bar:
                        # Iterate over the response content in chunks
                        for data in l_response.iter_content(chunk_size=1024):
                            # Write each chunk to the file
                            file.write(data)
                            # Update the progress bar by the chunk size
                            proccess_bar.update(len(data))
    except requests.exceptions.RequestException as e:
        LOGGER.error(f"download error: {e}")


def extract_play_list(url: str):
    response = requests.get(url, headers=load_headers())
    res_text = response.text
    soup = BeautifulSoup(res_text, "html.parser")
    # extract title
    divs = soup.find_all("div", class_="title-txt")

    lst_title = None
    if isinstance(divs, ResultSet):
        lst_title = [div.get_text() for div in divs]

    return lst_title


def extract_resource_download_url(url: str, title: str):
    response = requests.get(url, headers=load_headers())
    res_text = response.text
    tree = etree.HTML(res_text)

    # extract download url
    base_info = "".join(tree.xpath("/html/head/script[4]/text()"))[20:]

    info_dict = json.loads(base_info)
    video_url = info_dict["data"]["dash"]["video"][0]["baseUrl"]
    audio_url = info_dict["data"]["dash"]["audio"][0]["baseUrl"]

    video_path = "../download/{title}_video.mp4"
    audio_path = "../download/{title}_audio.m4s"

    res_obj = {"video_url": video_url, "audio_url": audio_url, "video_path": video_path.replace("{title}", title),
            "audio_path": audio_path.replace("{title}", title)}
    LOGGER.info(f"extract_resource_download_url {res_obj}")
    return res_obj


if __name__ == "__main__":
    """
    raw -> https://www.bilibili.com/video/BV1vE411d7ht/?spm_id_from=333.788.recommend_more_video.0&vd_source=f230a650621ce31e8709b0bd5a3826fb
    changed to -> https://www.bilibili.com/video/BV1vE411d7ht?spm_id_from=333.788.videopod.episodes&vd_source=f230a650621ce31e8709b0bd5a3826fb
    next -> https://www.bilibili.com/video/BV1vE411d7ht?spm_id_from=333.788.videopod.episodes&vd_source=f230a650621ce31e8709b0bd5a3826fb&p=2
    """

    get_title_list_url = download_item["get_title_list_url"]
    download_url = download_item["download_url"]

    LOGGER.info(f"HEADERS:{load_headers()}")
    lst_play = extract_play_list(get_title_list_url)
    for index, value in enumerate(lst_play, start=1):
        print(f"{index}: {value}")
        resource_url = extract_resource_download_url(f"{download_url}{index}", value)
        download_resource(resource_url["audio_url"], resource_url["audio_path"])
        break

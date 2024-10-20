import json
import os
import sys
import subprocess
import yaml
from urllib.parse import urlparse
from thi_proj.utils import logger


def resource_path(relative_path):
    """获取资源文件的绝对路径，处理 PyInstaller 打包后的情况"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


LOGGER = logger.get_logger("bilibilib_get_audio", resource_path("../log/thi_proj.log"))


def extract_base_url(url: str):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def rename(directory: str, ori_suffix: str, new_suffix: str):
    """
    rename file ext to new_suffix which ext is ori_suffix
    :param directory:
    :param ori_suffix:
    :param new_suffix:
    :return:
    """
    for filename in os.listdir(directory):
        old_file_path = os.path.join(directory, filename)

        if os.path.isfile(old_file_path):
            name, ext = os.path.splitext(filename)
            if ext == ori_suffix:
                new_filename = name + new_suffix
                new_file_path = os.path.join(directory, new_filename)
                os.rename(old_file_path, new_file_path)
                LOGGER.info(f"file {filename} has been renamed to {new_filename}")


def convert_m4s_2_mp3(input_file: str, output_file: str, bitrate: str = "320k"):
    """
    please make sure your local have install the ffmpeg
    if dont, can download it from https://www.gyan.dev/ffmpeg/builds/
    and pay attention convert m4s to mp3, sometimes the output file would be bigger than input_file,
    use the get_audio_birate(file_path) method to check bitrate firstly
    :param input_file:
    :param output_file: if output is empty, then default ${input_file"s file_name}.mp3
    :param bitrate: 128k, 192k, 256k, 320k
    :return:
    """
    command = ["ffmpeg", "-i", input_file, "-b:a", bitrate, output_file]
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + ".mp3"
    if not input_file.endswith(".m4s"):
        LOGGER.warning(f"Failure convert {input_file} to {output_file}, bit rate: {bitrate}")
    try:
        subprocess.run(command, check=True)
        LOGGER.info(f"Successfully convert {input_file} to {output_file}, bit rate: {bitrate}")
    except subprocess.CalledProcessError as e:
        LOGGER.error(f"Failure convert {input_file} to {output_file}, bit rate: {bitrate}, error: {e}")


def get_audio_bitrate(file_path):
    """
    please make sure your local have install the ffmpeg
    if dont, can download it from https://www.gyan.dev/ffmpeg/builds/
    :param file_path:
    :return:
    """
    command = [
        "ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
        "stream=bit_rate", "-of", "json", file_path
    ]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        info = json.loads(result.stdout)
        bitrate = info["streams"][0]["bit_rate"]
        return int(bitrate)
    except (subprocess.CalledProcessError, KeyError, IndexError) as e:
        LOGGER.error(f"Fail to get bitrate: {e}")
        return None


def load_yaml(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config


def ensure_download_directory():
    download_path = resource_path("../download")
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    return download_path

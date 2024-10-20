import os

from resource import convert_m4s_2_mp3, get_audio_bitrate, load_yaml

lst = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

def foreach():
    skip = 5
    for index, value in enumerate(lst, start=1):
        if index <= skip:
            continue
        if index % 10 == 0:
            print("-----------")
        if index <= len(lst):
            print(True)


def rename(directory: str, ori_suffix: str, new_suffix: str):
    for filename in os.listdir(directory):
        old_file_path = os.path.join(directory, filename)

        if os.path.isfile(old_file_path):
            name, ext = os.path.splitext(filename)
            if ext == ori_suffix:
                new_filename = name + new_suffix
                new_file_path = os.path.join(directory, new_filename)
                os.rename(old_file_path, new_file_path)
                print(f"file '{filename}' has been renamed to '{new_filename}'")


rename("D:\\GitHub\\python_proj\\thi_proj\\download", ".mp3", ".m4s")


# convert_m4s_2_mp3("C:\\Users\\fernando\\Desktop\\out\\50.my cousin by daphne du maurier - learn english through story with subtitle_audio.m4s", "C:\\Users\\fernando\\Desktop\\out\\50.my cousin by daphne du maurier - learn english through story with subtitle_audio.mp3")

# read audio file's bitrate
# file_path = "C:\\Users\\fernando\\Desktop\\out\\50.my_cousin_by_daphne_du_maurier_-_learn_english_through_story_with_subtitle_audio.m4s"
# bitrate = get_audio_bitrate(file_path)
# if bitrate:
#     print(f"bitrate: {bitrate / 1000} kbps")


# read yaml

config = load_yaml("../resources/download_items.yml")
print(type(config))
print(config)

def replace_filename(directory: str):
    for filename in os.listdir(directory):
        old_file_path = os.path.join(directory, filename)

        if os.path.isfile(old_file_path):
            name, ext = os.path.splitext(filename)
            filenames = name.split(".")
            new_filename = filenames[0]
            new_filename = f"【{new_filename}】"
            if new_filename == f"【{''.join(filenames)}】":
                continue
            new_filename = f"{new_filename}{''.join(filenames)}{ext}"

            new_file_path = os.path.join(directory, new_filename)
            os.rename(old_file_path, new_file_path)
            print(f"file '{filename}' has been renamed to '{new_filename}'")


# replace_filename("D:\\GitHub\\python_proj\\thi_proj\\download")
# replace_filename("C:\\Users\\fernando\\Desktop\\out")
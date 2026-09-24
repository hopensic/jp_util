from mutagen.mp3 import MP3

def get_mp3_duration(file_path):
    try:
        audio = MP3(file_path)
        return audio.info.length   # 单位：秒
    except Exception as e:
        print(f"读取失败: {file_path}, error: {e}")
        return None
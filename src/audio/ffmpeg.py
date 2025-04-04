# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky
"""
ffmpeg
"""
import subprocess
import os
import platform


def convert_to_wav_16000(audio_path):
    """
    Converts any audio file to WAV format with a sampling rate of 16000Hz.
    The function generates a file with the same name as the input file but with a .wav extension
    in the current script directory.

    Parameters:
    - audio_path (str): Input audio file path.

    Returns:
    - str: Path of the converted audio file (.wav).
    """
    # Ensure the input file exists
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Input file does not exist: {audio_path}")

    # Retrieve file name and target file path
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    output_path = f"{os.path.join(os.path.dirname(audio_path), base_name)}_soywhisky.com.wav"

    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Check the operating system type and set the ffmpeg path
    ffmpeg_filename = "ffmpeg.exe" if platform.system() == "Windows" else "ffmpeg"
    ffmpeg_path = os.path.join(script_dir, "lib", ffmpeg_filename)

    # Check if the ffmpeg executable exists
    if not os.path.isfile(ffmpeg_path):
        raise FileNotFoundError(
            f"'ffmpeg' executable not found: {ffmpeg_path}. "
            f"Please ensure the file exists and is executable."
        )

    command = [
        ffmpeg_path,
        "-i", audio_path,  # 输入文件路径
        "-af", "loudnorm=I=-14:LRA=11:TP=-1.5",  # 使用 loudnorm 滤镜，设置到 YouTube 推荐标准
        "-ar", "16000",  # 采样率 16000Hz
        "-ac", "1",  # 单声道
        "-y",  # 覆盖输出文件
        output_path  # 输出文件路径
    ]

    # Call ffmpeg
    try:
        res = subprocess.run(command, check=True)
        if res.returncode != 0:
            raise RuntimeError(f"ffmpeg returned non-zero exit code: {res.returncode}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to call ffmpeg: {e.stderr.decode('utf-8')}") from e

    # Return the generated file path
    return output_path


# 示例用法
# if __name__ == "__main__":
#     input_audio_path = "F:\OBS_Video\\test.wav"  # 替换为你的音频文件路径
#     try:
#         output = convert_to_wav_16000(input_audio_path)
#         print(f"转换成功！输出文件路径: {output}")
#     except Exception as e:
#         print(f"转换失败: {e}")

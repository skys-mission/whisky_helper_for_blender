import re
from typing import List, Tuple, Dict


def load_cmu_dict(file_path: str) -> Dict[str, List[str]]:
    """
    加载 CMU 字典到内存中。
    :param file_path: CMU 字典文件路径
    :return: 一个字典，键是单词，值是音素列表
    """
    cmu_dict = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 跳过注释行
            if line.startswith(";;;"):
                continue
            # CMU 字典格式：WORD  PH1 PH2 PH3 ...
            parts = line.strip().split("  ")
            if len(parts) < 2:
                continue
            word = parts[0].lower()  # 将单词转为小写
            phonemes = parts[1].split()  # 音素列表
            cmu_dict[word] = phonemes
    return cmu_dict


def align_phonemes_to_timestamps(word_data: Dict, cmu_dict: Dict[str, List[str]]) -> List[Tuple[float, float, str]]:
    """
    将单词的时间戳和音素对齐。
    :param word_data: 包含单词的时间戳数据
    :param cmu_dict: CMU 字典
    :return: 包含时间戳和音素的列表
    """
    aligned_data = []
    for word_info in word_data["result"]:
        word = word_info["word"].lower()  # 单词小写化匹配 CMU 字典
        start_time = word_info["start"]
        end_time = word_info["end"]

        if word in cmu_dict:
            phonemes = cmu_dict[word]
        else:
            phonemes = ["UNKNOWN"]  # 如果单词不在字典中，标记为 UNKNOWN

        # 平均分配时间戳给每个音素
        num_phonemes = len(phonemes)
        time_step = (end_time - start_time) / num_phonemes
        for i, phoneme in enumerate(phonemes):
            phoneme_start = start_time + i * time_step
            phoneme_end = phoneme_start + time_step
            aligned_data.append((phoneme_start, phoneme_end, phoneme))
    return aligned_data


def process_data(input_data: List[Dict], cmu_dict: Dict[str, List[str]]) -> List[Tuple[float, float, str]]:
    """
    处理整个输入数据集，将单词转为音素并对齐时间戳。
    :param input_data: 输入的单词和时间戳数据
    :param cmu_dict: CMU 字典
    :return: 包含时间戳和音素的完整列表
    """
    all_aligned_data = []
    for word_data in input_data:
        aligned_data = align_phonemes_to_timestamps(word_data, cmu_dict)
        all_aligned_data.extend(aligned_data)
    return all_aligned_data


# 示例使用
if __name__ == "__main__":
    # 设置 CMU 字典路径
    cmu_dict_path = "F:\\OBS_Video\\cmudict-0.7b"  # 替换为实际的 CMU 字典文件路径

    # 加载 CMU 字典
    cmu_dict = load_cmu_dict(cmu_dict_path)

    # 示例数据
    input_data = [
        {
            "result": [
                {"conf": 1, "start": 0.84, "end": 1.11, "word": "one"},
                {"conf": 1, "start": 1.11, "end": 1.53, "word": "zero"},
                {"conf": 1, "start": 1.53, "end": 1.95, "word": "zero"},
                {"conf": 1, "start": 1.95, "end": 2.31, "word": "zero"},
                {"conf": 1, "start": 2.31, "end": 2.61, "word": "one"},
            ],
            "text": "one zero zero zero one",
        },
        {
            "result": [
                {"conf": 0.509024, "start": 3.93, "end": 4.11, "word": "nah"},
                {"conf": 0.620121, "start": 4.11, "end": 4.29, "word": "no"},
                {"conf": 0.761823, "start": 4.29, "end": 4.56, "word": "to"},
                {"conf": 0.446183, "start": 4.56, "end": 4.62, "word": "i"},
                {"conf": 0.762531, "start": 4.62, "end": 4.98, "word": "know"},
            ],
            "text": "nah no to i know",
        },
    ]

    # 处理数据
    aligned_phonemes = process_data(input_data, cmu_dict)

    # 输出结果
    for start, end, phoneme in aligned_phonemes:
        print(f"{start:.2f} - {end:.2f}: {phoneme}")
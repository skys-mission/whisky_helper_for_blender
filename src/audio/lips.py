import math

from src.audio.ffmpeg import convert_to_wav_16000
from src.audio.phoneme import phoneme_gen
from src.audio.vosk import run_vosk

# 定义音素到MMD口型的映射规则
phoneme_to_mmd = {
    # 转换为 "a"
    "AA": "a", "AE": "a", "AH": "a", "AY": "a",

    # 转换为 "e"
    "EH": "e", "ER": "e", "R": "e",

    # 转换为 "o"
    "AO": "o", "AW": "o", "OY": "o",

    # 转换为 "i"
    "IY": "i", "IH": "i", "EY": "i",

    # 转换为 "u"
    "UW": "u", "UH": "u", "OW": "u",

    # 转换为 "N"
    "M": "N", "N": "N", "NG": "N",

    # 转换为 "close" (闭嘴)
    "B": "close", "P": "close", "T": "close", "D": "close",
    "K": "close", "G": "close", "F": "close", "V": "close",

    # 转换为 None (静止)
    "TH": None, "DH": None, "S": None, "Z": None, "SH": None,
    "ZH": None, "CH": None, "JH": None, "Y": None, "W": None,
    "L": None, "HH": None,

    # 默认值
    "default": "close"
}

# 微调参数，控制口型幅度
scale = 1.0  # 0.0 ~ 1.0

# 缓冲参数，控制口型边缘的缓冲时间
buffer = 0.04  # 0.0 ~ 0.1

# 平滑参数，控制曲线函数的抖动程度
smoothness = 5  # 0.0 ~ 20.0

# 趋近速度控制参数，控制趋近1的速度
approach_speed = 5  # 0.0 ~ 10.0

# 转换为MMD形态键关键帧格式
mmd_keyframes = []


def clamp(value, min_value, max_value):
    """钳制值在最小值和最大值之间"""
    return max(min(value, max_value), min_value)


def symmetric_sigmoid_transition(t, start, end, peak_value, approach_speed):
    """使用对称的 Sigmoid 函数进行平滑过渡"""
    duration = end - start
    mid_time = (start + end) / 2
    if t < start or t > end:
        return 0.0
    else:
        # 归一化时间 t 到 [0, 1]
        normalized_time = (t - start) / duration
        # 左半部分 (从 0 到 1)
        if normalized_time <= 0.5:
            value = peak_value / (1 + math.exp(-approach_speed * (normalized_time - 0.25) * 4))
        # 右半部分 (从 1 到 0)
        else:
            value = peak_value / (1 + math.exp(-approach_speed * (0.75 - normalized_time) * 4))
        return clamp(value, 0.0, peak_value)


def lips_gen(phoneme_data):
    for start, end, phoneme in phoneme_data:
        # 提取音素的基础部分（去掉音调标记：如 IY1 -> IY）
        base_phoneme = ''.join([c for c in phoneme if not c.isdigit()])

        # 获取对应的MMD口型
        mmd_morph = phoneme_to_mmd.get(base_phoneme, None)
        if mmd_morph:
            # 添加起始关键帧
            mmd_keyframes.append({
                "time": round(start, 3),  # 起始时间
                "morph": mmd_morph,  # MMD口型
                "value": 0.0,  # 起始时关闭口型
                "frame_type": "start",  # 标记为开始帧
            })

            # 添加中间关键帧
            mid_time = (start + end) / 2
            mmd_keyframes.append({
                "time": round(mid_time, 3),  # 中间时间
                "morph": mmd_morph,  # MMD口型
                "value": 1.0,  # 中间时完全打开口型
                "frame_type": "middle",  # 标记为中间帧
            })

            # 添加结束关键帧
            mmd_keyframes.append({
                "time": round(end, 3),  # 结束时间
                "morph": mmd_morph,  # MMD口型
                "value": 0.0,  # 结束时关闭口型
                "frame_type": "end",  # 标记为结束帧
            })

            # 添加缓冲关键帧
            if buffer > 0:
                buffer_start = start + buffer
                buffer_end = end - buffer
                if buffer_start < buffer_end:
                    # 缓冲开始
                    mmd_keyframes.append({
                        "time": round(buffer_start, 3),
                        "morph": mmd_morph,
                        "value": symmetric_sigmoid_transition(buffer_start, start, end, 1.0, approach_speed),
                        "frame_type": "buffer_start",  # 标记为缓冲开始帧
                    })
                    # 缓冲结束
                    mmd_keyframes.append({
                        "time": round(buffer_end, 3),
                        "morph": mmd_morph,
                        "value": symmetric_sigmoid_transition(buffer_end, start, end, 1.0, approach_speed),
                        "frame_type": "buffer_end",  # 标记为缓冲结束帧
                    })

    # 对关键帧按时间排序
    mmd_keyframes.sort(key=lambda x: x["time"])

    return mmd_keyframes



wav_path = convert_to_wav_16000("F:\\OBS_Video\\test.wav")

json_path = run_vosk(wav_path)

phoneme_data = phoneme_gen(json_path)

keyframes=lips_gen(phoneme_data)

for keyframe in keyframes:
    print(
        f"Time: {keyframe['time']},"
        f" Morph: {keyframe['morph']},"
        f" Value: {keyframe['value']},"
        f" FrameType: {keyframe['frame_type']}"
    )


import librosa
import numpy as np

# 加载音频文件
def load_audio(file_path):
    y, sr = librosa.load(file_path, sr=16000)  # 加载音频（采样率 16kHz）
    return y, sr

# 提取共振峰频率
def extract_formants_with_denoise(y, sr, frame_length=512, hop_length=256, db_threshold=-20, rms_threshold=0.01):
    # 分帧和加窗
    frames = librosa.util.frame(y, frame_length=frame_length, hop_length=hop_length)
    formants = []
    timestamps = []
    for i, frame in enumerate(frames.T):
        # 计算帧的分贝值
        frame_db = 10 * np.log10(np.mean(frame**2) + 1e-10)  # 防止log(0)
        frame_rms = np.sqrt(np.mean(frame**2))  # 计算帧的 RMS 值

        # 如果分贝或 RMS 低于阈值，标记为静音
        if frame_db < db_threshold or frame_rms < rms_threshold:
            formants.append((None, None))  # 静音帧，不提取共振峰
            timestamps.append((i * hop_length) / sr)
            continue

        # 计算频谱
        spectrum = np.abs(np.fft.rfft(frame)) ** 2
        freqs = np.fft.rfftfreq(len(frame), 1 / sr)

        # 找到共振峰（简化版）
        peaks = np.argsort(-spectrum)[:2]  # 找到两个最大峰
        f1, f2 = freqs[peaks[0]], freqs[peaks[1]]
        formants.append((f1, f2))

        # 计算时间戳
        timestamp = (i * hop_length) / sr  # 帧的起始时间
        timestamps.append(timestamp)

    return formants, timestamps

# 判断元音类型
def classify_vowel(formants):
    vowels = []
    for f1, f2 in formants:
        # 如果无法提取共振峰，标记为静音
        if f1 is None and f2 is None:
            vowels.append('silence')
            continue

        # 元音分类规则
        if f1 > 700 and 1000 <= f2 <= 1200:
            vowels.append('a')
        elif 500 <= f1 <= 700 and f2 > 1700:
            vowels.append('e')
        elif f1 < 400 and f2 > 2000:
            vowels.append('i')
        elif 400 <= f1 <= 600 and 800 <= f2 <= 1000:
            vowels.append('o')
        elif f1 < 400 and f2 < 1000:
            vowels.append('u')
        else:
            vowels.append('a')  # 未知音素，默认标记为 "unknown"
    return vowels


# 主流程
audio_path = "F:\\OBS_Video\\test2.wav"
y, sr = load_audio(audio_path)

# 提取共振峰并降噪
db_threshold = -20  # 分贝阈值，可根据需要调整
rms_threshold = 0.01  # RMS 阈值，用于更严格的静音过滤
formants, timestamps = extract_formants_with_denoise(y, sr, db_threshold=db_threshold, rms_threshold=rms_threshold)

# 分类元音
vowels = classify_vowel(formants)

# 将元音和时间戳结合
vowel_sequence_with_timestamps = [
    {"vowel": vowel, "timestamp": timestamp}
    for vowel, timestamp in zip(vowels, timestamps)
]

# 打印识别结果
for item in vowel_sequence_with_timestamps:
    if item['vowel']!='silence':
        print(f"时间戳: {item['timestamp']:.3f}s, 元音: {item['vowel']}")
# 定义音素到MMD口型的映射规则
phoneme_to_mmd = {
    # 开口母音
    "AA": "a", "AH": "a", "AE": "a", "AY": "a",
    # 细声母音
    "IY": "i", "IH": "i", "EY": "i",
    # 圆唇母音
    "UW": "u", "UH": "u", "OW": "u",
    # 半开母音
    "EH": "e", "ER": "e", "R": "e",
    # 圆唇开口母音
    "AO": "o", "AW": "o", "OY": "o",
    # 辅音和静音
    "B": None, "P": None, "M": None, "N": None,
    "T": None, "K": None, "G": None,
    # 默认：未知音素处理为静音
}

# 微调参数，控制口型幅度
scale = 1.0  # 0.0 ~ 1.0

# 输入样例数据（时间区间和音素）
phoneme_data = [
    (2.04, 2.13, "IY1"),
    (2.13, 2.22, "R"),
    (2.22, 2.31, "OW0"),
    (2.31, 2.41, "W"),
    (2.41, 2.51, "AH1"),
    (2.51, 2.61, "N"),
    (3.93, 4.02, "N"),
    (4.02, 4.11, "AA1"),
    (4.11, 4.20, "N"),
    (4.20, 4.29, "OW1"),
    (4.29, 4.42, "T"),
    (4.42, 4.56, "UW1"),
    (4.56, 4.62, "AY1"),
    (4.62, 4.80, "N"),
    (4.80, 4.98, "OW1"),
]

# 转换为MMD关键帧格式
mmd_keyframes = []
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
            "value": min(max(1.0 * scale, 0.0), 1.0),  # 钳制值
        })
        # 添加结束关键帧
        mmd_keyframes.append({
            "time": round(end, 3),  # 结束时间
            "morph": mmd_morph,  # MMD口型
            "value": 0.0,  # 结束时关闭口型
        })

# 输出MMD关键帧数据
for keyframe in mmd_keyframes:
    print(f"Time: {keyframe['time']}, Morph: {keyframe['morph']}, Value: {keyframe['value']}")
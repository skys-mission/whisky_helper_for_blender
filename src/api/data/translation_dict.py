# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky
"""
翻译相关
"""


def get_translation_zh_dict(local):
    """
    获取翻译字典

    本函数用于根据指定的本地化参数，返回一个包含翻译映射的字典

    参数:
    local (str): 本地化参数，用于指定需要的翻译语言

    返回:
    dict: 包含翻译映射的字典
    """
    translation_dict = {
        local: translation_zh_map
    }

    return translation_dict


translation_zh_map = {
    ("*", "MMD Lip Gen"): "MMD口型生成",
    ("*", "Audio Path"): "音频文件",
    ("*", "Bilibili cover image"): "B站封面",
    ("*", "382:239 Bilibili cover image"): "382:239 B站封面",
    ("*", "Other"): "其它",
    ("*", "Old Film Standards"): "旧电影标准",
    ("*", "Film Standards"): "电影标准",
    ("*", "2.39:1 Film Standards"): "2.39:1 电影标准",
    ("*", "Standard"): "标准",
    ("*", "Film Standard"): "旧标准",
    ("*", "Landscape"): "横屏",
    ("*", "Portrait"): "竖屏",
    ("*", "Resolution"): "分辨率",
    ("*", "Aspect Ratio"): "宽高比",
    ("*", "Rotate"): "旋转",
    ("*", "ET Helper"): "亦癫助手",
    ("*", "Render Preset"): "渲染预设",
    ("*", "Set Camera"): "设置相机",
    ("*", "Focal Length"): "焦距",
    ("*", "F-Stop"): "光圈",
    ("*", "Depth of Field"): "景深",
    ("*", "Focus on Object"): "聚焦到物体",
    ("*", "Select focus object"): "选择聚焦物体",
    ("*", "Apply settings to the selected camera"): "将设置应用到选定的相机",
    ("*", "14mm ultra-wide field"): "14mm 超广角镜头",
    ("*", "Highlight background"): "突出背景",
    ("*", "24mm wide angle"): "24mm 广角镜头",
    ("*", "scenery, street snap"): "风景摄影，街头抓拍",
    ("*", "50mm human eye perspective"): "50mm 人眼视角镜头",
    ("*", "human eye perspective"): "人眼视角",
    ("*", "85mm classic portrait"): "85mm 经典肖像镜头",
    ("*", "classic portrait, background blur"): "经典肖像，背景虚化",
    ("*", "35mm long-focus"): "35mm 长焦镜头",
    ("*", "long-focus, strong background blur"): "长焦，强烈的背景虚化",
    ("*", "f/1.4 low light env"): "f/1.4 低光环境",
    ("*", "Background blur, portrait/night scene photography"): "背景虚化，适用于人像/夜景摄影",
    ("*", "f/2.8 default"): "f/2.8 默认光圈",
    ("*", "f/4 medium aperture"): "f/4 中等光圈",
    ("*", "Suitable for average lighting conditions"): "适合一般光照条件",
    ("*", "f/8 small aperture"): "f/8 小光圈",
    ("*", "Requires strong lighting"): "需要强光",
    ("*", "f/22 minimum aperture"): "f/22 最小光圈",
    ("*", "Requires a strong light environment"): "需要强光环境",
    ("*", "Slightly Blurred. Suitable for average lighting conditions"): "轻微虚化，适合一般光照条件",
    ("*", "Whisky Helper"): "Whisky助手",
    ("*", "default"): "默认",
    ("*", "Start Frame"): "起始帧",
    ("Operator", "apply camera settings"): "应用相机设置",
    ("Operator", "Gen Lips"): "口型生成",
}

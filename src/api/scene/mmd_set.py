# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky
"""
Blender Scene文件
"""
import bpy  # pylint: disable=import-error

lips_audio_path = bpy.props.StringProperty(
    name="Audio Path",
    description="Path to the Audio file.",
    default="",
    maxlen=512,
    subtype='FILE_PATH',
)

lips_start_frame = bpy.props.IntProperty(name="Start Frame", default=1)

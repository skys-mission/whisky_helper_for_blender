# -*- coding: utf-8 -*-
# Copyright (c) 2025, https://github.com/skys-mission and SoyWhisky
"""
初始化代码
"""
from ..api.bridge import Bridge
from ..api.handler.camera import CameraApplySettingsOperator
from ..api.scene.camera_set_scene import CameraSettingsProperties
from ..api.scene.mmd_set import (lips_audio_path, lips_start_frame, buffer_frame,
                                 approach_speed, db_threshold, \
                                 rms_threshold, max_morph_value,
                                 blink_start_frame, blink_end_frame,
                                 blinking_frequency, blinking_wave_ratio)
from ..api.scene.render_preset_scene import (
    resolution_preset, aspect_ratio_preset, orientation_preset)
from ..api.ui.about import AboutPanel
from ..api.ui.camera_set_panel import CameraSetPanel
from ..api.ui.mmd_blink_panel import RandomBlinkOperator, RandomBlinkPanel
from ..api.ui.mmd_set_panel import MMDHelperPanel, GenLipsOperator
from ..api.ui.render_preset_panel import RenderPresetPanel


class AddonManager:
    """
    插件管理器类。
    负责插件的初始化和卸载。
    """
    _addon_name = "whisky_helper"
    # 定义bl_classes元组，包含所有需要注册的类
    _bl_classes = (
        # 1.Properties(属性定义)
        # 2.Operator(操作器)
        # 3.Menu(菜单)
        # 4.Panel(面板)
        CameraSettingsProperties,
        CameraApplySettingsOperator,
        GenLipsOperator,
        RandomBlinkOperator,
        RenderPresetPanel,
        CameraSetPanel,
        MMDHelperPanel,
        AboutPanel,
        RandomBlinkPanel,
    )

    @staticmethod
    def init_addon():
        """
        初始化插件时调用此函数。
        它负责注册翻译、类和场景属性。
        """

        # 翻译
        Bridge.App.register_translations(
            AddonManager._addon_name
        )

        # Classes
        AddonManager.register_classes()
        # Scene
        AddonManager.register_scene()

    @staticmethod
    def unload_addon():
        """
        卸载插件时调用此函数。
        它负责注销场景属性、类和翻译。
        """

        # Scene
        AddonManager.unregister_scene()
        # Classes
        AddonManager.unregister_classes()
        # 翻译
        Bridge.App.unregister_translations(AddonManager._addon_name)

    @staticmethod
    def register_scene():
        """
        注册场景属性。
        这些属性包括渲染预设、摄像机设置等。
        """
        scene = Bridge.Types.get_scene()
        pp = Bridge.Props.get_pointer_property()

        # Render Preset 相关
        scene.resolution_preset = resolution_preset
        scene.aspect_ratio_preset = aspect_ratio_preset
        scene.orientation_preset = orientation_preset

        # 摄像机预设相关
        scene.camera_settings = pp(type=CameraSettingsProperties)

        # MMD
        scene.lips_audio_path = lips_audio_path
        scene.lips_start_frame = lips_start_frame
        scene.buffer_frame = buffer_frame
        scene.approach_speed = approach_speed
        scene.db_threshold = db_threshold
        scene.rms_threshold = rms_threshold
        scene.max_morph_value = max_morph_value

        # MMD wink
        scene.blink_start_frame = blink_start_frame
        scene.blink_end_frame = blink_end_frame
        scene.blinking_frequency = blinking_frequency
        scene.blinking_wave_ratio = blinking_wave_ratio

    @staticmethod
    def unregister_scene():  # pylint: disable=too-many-branches
        """
        注销场景属性。
        这些属性包括渲染预设、摄像机设置等。
        """
        scene = Bridge.Types.get_scene()

        # 删除Blender Scene
        if hasattr(scene, 'resolution_preset'):
            del scene.resolution_preset
        if hasattr(scene, 'aspect_ratio_preset'):
            del scene.aspect_ratio_preset
        if hasattr(scene, 'orientation_preset'):
            del scene.orientation_preset
        if hasattr(scene, 'camera_settings'):
            del scene.camera_settings
        if hasattr(scene, 'lips_audio_path'):
            del scene.lips_audio_path
        if hasattr(scene, 'lips_start_frame'):
            del scene.lips_start_frame
        if hasattr(scene, 'buffer_frame'):
            del scene.buffer_frame
        if hasattr(scene, 'approach_speed'):
            del scene.approach_speed
        if hasattr(scene, 'db_threshold'):
            del scene.db_threshold
        if hasattr(scene, 'rms_threshold'):
            del scene.rms_threshold
        if hasattr(scene, 'max_morph_value'):
            del scene.max_morph_value
        if hasattr(scene, 'blink_start_frame'):
            del scene.blink_start_frame
        if hasattr(scene, 'blink_end_frame'):
            del scene.blink_end_frame
        if hasattr(scene, 'blinking_frequency'):
            del scene.blinking_frequency
        if hasattr(scene, 'blinking_wave_ratio'):
            del scene.blinking_wave_ratio

    @staticmethod
    def register_classes():
        """
        注册所有bl_classes中的类。
        """
        for cls in AddonManager._bl_classes:
            Bridge.Utils.register_class(cls)

    @staticmethod
    def unregister_classes():
        """
        注销所有bl_classes中的类。
        逆序注销以避免潜在的依赖问题。
        """
        for cls in reversed(AddonManager._bl_classes):
            Bridge.Utils.unregister_class(cls)

    @staticmethod
    def set_addon_name(name):
        """
        ...
        """
        AddonManager._addon_name = name

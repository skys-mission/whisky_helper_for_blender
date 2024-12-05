# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky
"""
MMD面板
"""

import time
import bpy  # pylint: disable=import-error


# 定义一个Blender的面板类，用于在UI中显示渲染预设选项
class MMDHelperPanel(bpy.types.Panel):  # pylint: disable=too-few-public-methods
    """
    渲染预设面板
    """
    # 面板的标题
    bl_label = "MMD Lip Gen"
    # 面板的唯一标识符
    bl_idname = "OBJECT_PT_MMD_Helper"
    # 面板显示的空间类型
    bl_space_type = 'VIEW_3D'
    # 面板显示的区域类型
    bl_region_type = 'UI'
    # 面板显示的类别，用于在UI中分组面板
    bl_category = 'Whisky Helper'
    # 面板的显示顺序
    bl_order = 3

    # 绘制面板中的UI元素
    def draw(self, context):
        """
         在给定的上下文中绘制UI元素。

         参数:
         - context: 当前的上下文对象，包含了关于当前Blender环境的信息。

         此函数负责在UI中添加与场景相关的属性控件，以允许用户编辑场景的属性。
         """
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "lips_audio_path")

        layout.prop(scene, "lips_start_frame")

        layout.operator("mmd.gen_lips")


class GenLipsOperator(bpy.types.Operator):  # pylint: disable=too-few-public-methods
    bl_idname = "mmd.gen_lips"
    bl_label = "Gen Lips"
    bl_description = ""

    def execute(self, context):
        # 开始显示进度条
        context.window_manager.progress_begin(0, 100)

        # 将鼠标指针调整为进度指示器
        context.window.cursor_modal_set('WAIT')

        # 这里可以添加你的处理代码
        # 例如：模拟处理过程
        for i in range(100):
            # 更新进度条
            context.window_manager.progress_update(i)

            # 模拟处理时间
            time.sleep(0.01)

        # 结束进度条
        context.window_manager.progress_end()

        # 恢复鼠标指针
        context.window.cursor_modal_restore()
        return {'FINISHED'}

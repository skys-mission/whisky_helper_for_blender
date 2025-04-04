# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky
# pylint: disable=R0801
"""
MMD面板
"""

import bpy  # pylint: disable=import-error

from ...audio.lips import Lips
from ...util.logger import Log


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

        layout.prop(scene, "db_threshold")

        layout.prop(scene, "rms_threshold")

        layout.prop(scene, "buffer_frame")

        layout.prop(scene, "approach_speed")

        layout.prop(scene, "max_morph_value")

        layout.operator("mmd.gen_lips")


class GenLipsOperator(bpy.types.Operator):  # pylint: disable=too-few-public-methods
    """
    ...
    """
    bl_idname = "mmd.gen_lips"
    bl_label = "Gen Lips"
    bl_description = ""

    def execute(self, context):
        """
        ...
        :param context:
        :return:
        """
        scene = bpy.context.scene
        # 获取当前场景的帧率
        fps = scene.render.fps

        # 开始显示进度条
        context.window_manager.progress_begin(0, 100)

        # 将鼠标指针调整为进度指示器
        context.window.cursor_modal_set('WAIT')
        context.window_manager.progress_update(97)
        try:
            lips = Lips.mmd_lips_gen(
                wav_path=context.scene.lips_audio_path,
                buffer=context.scene.buffer_frame,
                approach_speed=context.scene.approach_speed,
                db_threshold=context.scene.db_threshold,
                rms_threshold=context.scene.rms_threshold,
                max_morph_value=context.scene.max_morph_value,
                start_frame=context.scene.lips_start_frame,
                fps=fps)
            context.window_manager.progress_update(98)
            meshes = find_mesh()
            context.window_manager.progress_update(99)
            for mesh in meshes:
                set_lips_to_mesh(mesh, lips, context.scene.lips_start_frame)

        except Exception as e:  # pylint: disable=broad-exception-caught
            # 结束进度条
            context.window_manager.progress_end()
            # 恢复鼠标指针
            context.window.cursor_modal_restore()
            Log.raise_error(e, Exception)

        # 结束进度条
        context.window_manager.progress_end()

        # 恢复鼠标指针
        context.window.cursor_modal_restore()
        return {'FINISHED'}


def find_shape_keys_with_name(obj, shape_key_name):
    """
    递归查询对象及其子对象中的所有网格体，并查找是否包含指定名称的形态键。

    参数:
        obj (bpy.types.Object): 要查询的对象。
        shape_key_name (str): 要查找的形态键名称。

    返回:
        list: 包含指定名称形态键的对象列表。
    """
    found_objects = []

    # 检查当前对象是否为网格体，并且是否有形态键
    if obj.type == 'MESH' and obj.data.shape_keys:
        for shape_key in obj.data.shape_keys.key_blocks:
            if shape_key.name == shape_key_name:
                found_objects.append(obj)
                break

    # 递归查询子对象
    for child in obj.children:
        found_objects.extend(find_shape_keys_with_name(child, shape_key_name))

    return found_objects


def find_mesh():
    """
    ...
    """
    # 记录包含指定形态键的对象
    found_objects = []

    selected_objects = bpy.context.selected_objects

    if not selected_objects:
        Log.raise_error("Please select an object first.", Exception)
        return found_objects

    # 要查找的形态键名称
    shape_key_name = 'あ'

    for obj in selected_objects:
        found_objects.extend(find_shape_keys_with_name(obj, shape_key_name))

    # 打印结果
    if found_objects:
        Log.info(f"Found  {len(found_objects)} "
                 f"objects containing the shape key '{shape_key_name}'.")
        for obj in found_objects:
            Log.info(f"Object containing the shape key '{shape_key_name}', {obj.name} found.")
    else:
        Log.raise_error(f"No object containing the shape key "
                        f"'{shape_key_name}' was found.", Exception)
    return found_objects


def set_lips_to_mesh(mesh, lips, start_frame):  # pylint: disable=too-many-locals,too-many-branches
    """
    将 lips 数据应用到网格模型上。

    :param mesh: 网格模型对象，用于应用 lips 数据。
    :param lips: 包含 lips 数据的字典，键为形态键名称，值为包含帧信息的列表。
    :param start_frame: 开始应用动画的帧号。
    """
    # 定义口型列表，用于后续的遍历和清理关键帧。
    morph_list = ['あ', 'い', 'う', 'え', 'お']
    # 初始化最大帧数，用于确定动画的结束点。
    max_frame = 0
    # 遍历嘴唇动画数据，找到最大的帧数。
    for _, v in lips.items():
        for m in v:
            max_frame = max(m['frame'], max_frame)

    # 清除所有口型在最大帧范围内的现有关键帧。
    # 修改前的问题代码：
    # for i in range(start_frame, max_frame + 1, 1):

    # 修改后的关键帧清除逻辑：
    # 确保只清除起始帧之后的关键帧
    start = max(start_frame, 1)  # 起始帧最小为1
    end = max(max_frame, start_frame)

    # 获取实际存在的形态键列表
    existing_morphs = [
        k.name for k in mesh.data.shape_keys.key_blocks
    ] if mesh.data.shape_keys else []

    # 修改后的清除逻辑：仅处理存在的形态键
    for morph_key in morph_list:
        if morph_key in existing_morphs:
            for i in range(start, end + 1):
                clear_shape_key_keyframe(mesh, morph_key, i)

    # 强制设置起始帧零值（仅处理存在的形态键）
    for morph in morph_list:
        if morph in existing_morphs:
            # 检查是否已存在起始帧关键帧
            existing_frames = [m['frame'] for m in lips.get(morph, [])]
            if start_frame not in existing_frames:
                set_shape_key_value(mesh, morph, 0.0, start_frame, 'KEYFRAME')

    # 应用关键帧时跳过起始帧
    for morph_key, frames in lips.items():
        if morph_key not in existing_morphs:
            continue

        valid_frames = [m for m in frames if m['frame'] > start_frame]
        for m in valid_frames:
            set_shape_key_value(mesh, morph_key, m['value'], m['frame'], m['frame_type'])

            # 以下行为注释，可能是为了记录或调试目的保留。
            # set_shape_key_value(mesh, morph_key, 0.0, i)

    # 应用 lips 数据到网格模型。
    for k, v in lips.items():
        morph_key = k
        # 查找与当前口型键匹配的形状键。
        for key_block in mesh.data.shape_keys.key_blocks:
            if key_block.name == morph_key:
                break
        else:
            # 如果没有找到匹配的形状键，使用默认的'あ'。
            morph_key = 'あ'

        # 批量处理有效关键帧
        valid_frames = (m for m in v if m['frame'] >= start_frame)

        for m in valid_frames:
            set_shape_key_value(mesh, morph_key, m['value'], m['frame'], m['frame_type'])
            Log.info(f"Set shape key '{morph_key}' with frame {m['frame']} and value {m['value']}")


def set_shape_key_value(obj, shape_key_name, value, frame, f_type):
    """
    设置指定对象的形态键值。

    :param obj: Blender 对象
    :param shape_key_name: 形态键名称
    :param value: 形态键值（0.0 到 1.0）
    :param frame: ...
    :param f_type: ....
    """
    if obj and obj.type == 'MESH':  # pylint: disable=too-many-nested-blocks
        shape_keys = obj.data.shape_keys
        if shape_keys and shape_key_name in shape_keys.key_blocks:
            shape_key = shape_keys.key_blocks[shape_key_name]
            # warming 这是一段特定逻辑，不是通用逻辑，复制复用时需要注意！
            anim_data = shape_key.id_data.animation_data
            sn = False
            if anim_data and anim_data.action:
                # 获取 F-Curve
                for fcu in anim_data.action.fcurves:
                    # 检查是否是这个shape key的F-curve
                    if fcu.data_path == f'key_blocks["{shape_key.name}"].value':
                        # 检查特定帧是否有关键帧
                        for keyframe in fcu.keyframe_points:
                            if keyframe.co[0] == frame:  # co[0]是帧号
                                sn = True
            if round(shape_key.value, 1) == 0.0 and sn:
                return
            if f_type in ("buffer_start", "buffer_end"):
                shape_key.value = max(value, shape_key.value)  # 设置形态键的值
            else:
                shape_key.value = value
            shape_key.keyframe_insert(data_path="value", frame=frame)  # 插入关键帧
        else:
            Log.warning(f"The shape key '{shape_key_name}' does not exist.")
    else:
        Log.warning("The object is not of the mesh type.")


def clear_shape_key_keyframe(obj, shape_key_name, frame):
    """
    清除指定对象的形态键在指定帧的关键帧。

    :param obj: Blender 对象
    :param shape_key_name: 形态键名称
    :param frame: 需要清除关键帧的帧数
    """
    if obj and obj.type == 'MESH':
        shape_keys = obj.data.shape_keys
        if shape_keys and shape_key_name in shape_keys.key_blocks:
            shape_key = shape_keys.key_blocks[shape_key_name]
            try:
                shape_key.keyframe_delete(data_path="value", frame=frame)  # 清除关键帧
            except Exception as e:  # pylint: disable=broad-exception-caught
                Log.info(e)
        else:
            Log.warning(f"The shape key '{shape_key_name}' does not exist.")
    else:
        Log.warning("The object is not of the mesh type.")


def get_shape_key_value(obj, shape_key_name):
    """
    获取指定对象的形态键的值。

    :param obj: Blender 对象
    :param shape_key_name: 形态键名称
    :return: 形态键的值（如果存在），否则返回 None
    """
    if obj and obj.type == 'MESH':
        shape_keys = obj.data.shape_keys
        if shape_keys and shape_key_name in shape_keys.key_blocks:
            shape_key = shape_keys.key_blocks[shape_key_name]
            return shape_key.value  # 返回形态键的值
        Log.warning(f"The shape key '{shape_key_name}' does not exist.")
        return None

    Log.warning("The object is not of the mesh type.")
    return None

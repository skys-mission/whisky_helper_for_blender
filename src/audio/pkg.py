# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky
"""
...
"""
import os
import sys
import bpy  # pylint: disable=import-error




def unload_pkg():
    """
    ...
    """
    addon_dir = os.path.abspath(os.path.dirname(__file__))
    
    # 获取Blender版本
    version = bpy.app.version
    major, minor = version[0], version[1]
    
    # 根据版本选择不同的plib路径
    if major == 3 and minor >= 6 or major == 4 and minor == 0:
        plib_path = os.path.join(addon_dir, 'plib310')
    elif major >= 4 and minor >= 1:
        plib_path = os.path.join(addon_dir, 'plib311')
    else:
        raise ValueError(f"Unsupported Blender version: {major}.{minor}")
        
    if plib_path in sys.path:
        sys.path.remove(plib_path)

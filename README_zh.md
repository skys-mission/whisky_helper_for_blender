# whisky_helper_for_blender

[![Pylint](https://github.com/skys-mission/whisky_helper_for_blender/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/skys-mission/whisky_helper_for_blender/actions/workflows/pylint.yml)
[![CodeQL Advanced](https://github.com/skys-mission/whisky_helper_for_blender/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/skys-mission/whisky_helper_for_blender/actions/workflows/codeql.yml)

其它语言：[English](README.md), (Currently unable to translate more)

一个Blender插件，可以通过vosk模型识别口型动作并生成关键帧，随机眨眼，还有一些我个人常用的小功能。

可以在Github Release页面下载最新版本。因为内嵌一些开源工具。所以目前仅支持Windows平台。

<!-- TOC -->

* [whisky_helper_for_blender](#whisky_helper_for_blender)
    * [Download](#download)
    * [功能](#功能)
        * [MMD口型生成](#mmd口型生成)
            * [使用方法](#使用方法)
            * [参数介绍](#参数介绍)
            * [如何适配其它模型](#如何适配其它模型)
        * [随机眨眼](#随机眨眼)
        * [其它功能](#其它功能)
    * [支持](#支持)
        * [Blender版本适配](#blender版本适配)
        * [操作系统适配](#操作系统适配)
    * [高版本如何安装Blender插件](#高版本如何安装blender插件)
    * [开源引用](#开源引用)

<!-- TOC -->

## Download

https://github.com/skys-mission/whisky_helper_for_blender/releases

## 功能

### MMD口型生成

通过Vosk 音频模型识别出音素口型，添加到MMD标准模型上

本插件识别的MMD模型的口型形态键名：あ，い，う，え，お。除了あ以外没有的全部改到あ上，如果没有あ则报错。

警告：该功能会破坏音频时间范围内的あ，い，う，え，お形态键关键帧

#### 使用方法

![lips_gen2.0f.webp](.img/lips_gen2.0f.webp)

1. 在Audio Path中选择一个音频文件（常规的音频文件大概率都可以用包括mp4）
2. 选中一个mmd模型的任意层父级（注意，如果对象下有多个网格体包含这些形态键，则所有网格体的形态键均会被修改）
3. 建议打开系统控制台观察进度。（Blender菜单栏->windows->Toggle System Console）
4. 设置参数，点击生成（注意当前版本会在音频文件同级目录生成一些可读的缓存文件，不会清除）
5. 等待鼠标指针从数字恢复成正常

#### 参数介绍

![lips3.0.webp](.img/lips3.0.webp)

- Start Frame: 音频从那一帧往后
- DB Threshold: DB降噪，如果识别不准则调高，如果识别不到则调低
- RMS Threshold: RMS降噪，如果识别不准则调高，如果识别不到则调低
- Delayed Opening: 延时张嘴比例
- Speed Up Opening: 识别开始到延时张嘴的曲线速度调整参数
- Max Morph Value: 形态键的最大阈值

#### 如何适配其它模型

比如vrm，你需要找到你的模型或者自己设置A，E，I，O，U的形态键，复制并改为MMD标准形态键名

**至少要拥有あ，才能使用本功能**

- あ = A
- い = I
- う = U
- え = E
- お = O

如果你不会复制，可以参考：[copy_shape_key.md](docs/copy_shape_key.md)

![lip_sync.webp](.img/lip_sync.webp)
模型来源：KissshotSusu

### 随机眨眼

随机眨眼识别的是：まばたき ，这个形态键，如果没有你需要自己转化或制作该形态键

警告：该功能会破坏帧数范围内まばたき形态键关键帧

1. 选中一个mmd模型的任意层父级（注意，如果对象下有多个网格体包含这些形态键，则所有网格体的形态键均会被修改）
2. 建议打开系统控制台观察进度。（Blender菜单栏->windows->Toggle System Console）
3. 设置参数，点击生成
4. 等待鼠标指针从数字恢复成正常

![blink_args.webp](.img/blink_args.webp)

- blink interval: 眨眼间隔，单位秒
- blinking wave ratio: 随机比例0.01-1可调整

### 其它功能

文档编写中...

## 支持

### Blender版本适配

- 主要支持的版本（本人会进行测试）
    - 3.6 ，4.2
- 或许可以运行的版本
    - 大于等于3.6
- 计划支持的版本
    - 下一个Blender LTS版本
- 不计划适配
    - 小于3.6和任何不是LTS的版本

### 操作系统适配

- 当前支持
    - windows-x64
- 暂不考虑适配
    - macos-arm64 (适配难度比我想象中的大，再加上用户群体少，暂不考虑适配)
- 不计划支持
    - linux（除非出现重大变故，否则不计划支持）

## 高版本如何安装Blender插件

参考：https://docs.blender.org/manual/zh-hans/4.2/editors/preferences/addons.html#prefs-extensions-install-legacy-addon

## 开源引用

| 项目                         | 链接                                           | 协议                                     |
|----------------------------|----------------------------------------------|----------------------------------------|
| FFmpeg                     | https://github.com/FFmpeg/FFmpeg             | GPLv3（Releases中内嵌的工具采用协议，仓库中无ffmpeg代码） |
| ~~Vosk-API和Vosk AI Model~~ | ~~https://github.com/alphacep/vosk-api~~     | Apache-2.0                             |
| CMU Dict                   | http://www.speech.cs.cmu.edu/cgi-bin/cmudict | 2-Clause BSD License                   |
| ~~gout-vosk tool~~         | ~~https://github.com/skys-mission/gout~~     | GPLv3                                  |

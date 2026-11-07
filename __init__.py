"""dm_tail_frames —— 取尾帧节点 + 旧节点兼容层

本包注册两个节点：
  1. DMTailFrames        —— 取最后 N 帧（默认 3），推荐用这个
  2. MySplitImageBatch   —— 兼容层：旧工作流里丢失的同名节点，重新注册以消除红叉
"""

import os

from .compat_split import NODE_CLASS_MAPPINGS as _COMPAT_CLASSES
from .compat_split import NODE_DISPLAY_NAME_MAPPINGS as _COMPAT_NAMES
from .tail_frames import NODE_CLASS_MAPPINGS as _TAIL_CLASSES
from .tail_frames import NODE_DISPLAY_NAME_MAPPINGS as _TAIL_NAMES

NODE_CLASS_MAPPINGS = {}
NODE_CLASS_MAPPINGS.update(_TAIL_CLASSES)
NODE_CLASS_MAPPINGS.update(_COMPAT_CLASSES)

NODE_DISPLAY_NAME_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS.update(_TAIL_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(_COMPAT_NAMES)

WEB_DIRECTORY = None

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

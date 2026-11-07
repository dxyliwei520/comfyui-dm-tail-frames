"""兼容层：把已丢失的 `MySplitImageBatch` 重新注册出来。

背景（2026-11-07）：
    用户的工作流 `MiniMax多模态.json` 里有 5 个 `MySplitImageBatch` 节点，
    但原自定义节点包已经不在了（custom_nodes 里搜不到）→ 画布上全是红叉 + UNKNOWN。

做法：
    注册一个同名 `MySplitImageBatch`：
      - 输入：images + 3 个 INT（保持原 3 个控件位，避免连线/布局错乱）
      - 输出：IMAGES + frame_count（与原节点一致，2 个输出）
    语义按"取尾部 N 帧"实现：N = 第二个控件；
      - 若第一个控件 >= 0 且小于总帧数 → 从该位置开始取 N 帧（更像原节点的 start/count/step）
      - 否则 → 直接取最后 N 帧
    这样老工作流不用改连线就能跑，需要精确语义时在画布上调参数即可。
"""

import torch

NODE_NAME = "MySplitImageBatch"


class MySplitImageBatchCompat:
    """兼容旧工作流：取一段 / 取尾部的帧"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "start_or_zero": ("INT", {"default": 0, "min": -100000, "max": 100000, "step": 1,
                                          "tooltip": "起始帧；<=0 或越界时按“取最后 count 帧”处理"}),
                "count": ("INT", {"default": 3, "min": 1, "max": 4096, "step": 1,
                                  "tooltip": "取多少帧；默认 3"}),
                "step": ("INT", {"default": 1, "min": 1, "max": 64, "step": 1,
                                 "tooltip": "步长；1 = 连续帧"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT")
    RETURN_NAMES = ("IMAGES", "frame_count")
    FUNCTION = "run"
    CATEGORY = "DM/Frames"
    DESCRIPTION = "兼容旧工作流的 MySplitImageBatch：按 start/count/step 切帧；start<=0 时取最后 count 帧。"

    def run(self, images, start_or_zero=0, count=3, step=1):
        if images is None:
            return (images, 0)

        n = int(images.shape[0])
        count = max(1, int(count))
        step = max(1, int(step))
        start = int(start_or_zero)

        if n == 0:
            return (images, 0)

        if start <= 0 or start >= n:
            # 取最后 count 帧（最常用的语义）
            lo = max(0, n - count)
            out = images[lo:]
        else:
            out = images[start:start + count]

        if step > 1 and out.shape[0] > 0:
            out = out[::step]

        return (out, n)


NODE_CLASS_MAPPINGS = {NODE_NAME: MySplitImageBatchCompat}
NODE_DISPLAY_NAME_MAPPINGS = {NODE_NAME: "MySplitImageBatch (compat) · 兼容旧节点"}

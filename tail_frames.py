"""DMTailFrames —— 取一批图像的最后 N 帧（默认 3）。

不管总帧数是多少，永远取最后 N 帧；帧数不足时按实际数量返回。
"""

import torch

NODE_NAME = "DMTailFrames"


class DMTailFrames:
    """取 IMAGE 批的最后 N 帧"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "count": ("INT", {"default": 3, "min": 1, "max": 240, "step": 1,
                                  "tooltip": "取最后几帧；默认 3"}),
            },
            "optional": {
                "pad": ("BOOLEAN", {"default": False,
                                    "tooltip": "帧数不足 N 时，是否用最后一帧补齐"}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "run"
    CATEGORY = "DM/Frames"
    DESCRIPTION = "取一批图像的最后 N 帧（默认 3）。与总帧数无关，取不到的按实际数量返回。"

    def run(self, images, count=3, pad=False):
        if images is None:
            return (images,)

        n = int(images.shape[0])
        count = max(1, int(count))
        if n == 0:
            return (images,)

        out = images if n <= count else images[n - count:]

        if pad and out.shape[0] < count:
            need = count - out.shape[0]
            last = out[-1:]
            out = torch.cat([out] + [last] * need, dim=0)

        return (out,)


NODE_CLASS_MAPPINGS = {NODE_NAME: DMTailFrames}
NODE_DISPLAY_NAME_MAPPINGS = {NODE_NAME: "Tail Frames (last N) · 取尾帧"}

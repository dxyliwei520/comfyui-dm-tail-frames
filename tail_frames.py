"""DMTailFrames — take the last N frames of an IMAGE batch (default: 3).

Always returns the trailing N frames regardless of the total frame count.
If the batch has fewer than N frames, the actual count is returned (unless
``pad`` is enabled, in which case the last frame is repeated to fill).
"""

import torch

NODE_NAME = "DMTailFrames"


class DMTailFrames:
    """Take the last N frames of an IMAGE batch."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "count": ("INT", {"default": 3, "min": 1, "max": 240, "step": 1,
                                  "tooltip": "Number of trailing frames to take. Default: 3"}),
            },
            "optional": {
                "pad": ("BOOLEAN", {"default": False,
                                    "tooltip": "Pad with the last frame when the batch has fewer than N frames"}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "run"
    CATEGORY = "DM/Frames"
    DESCRIPTION = ("Take the last N frames of an image batch (default: 3). "
                   "Independent of the total frame count; returns fewer frames if not enough are available.")

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
NODE_DISPLAY_NAME_MAPPINGS = {NODE_NAME: "DM Tail Frames (last N)"}

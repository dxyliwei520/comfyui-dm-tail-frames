"""Compatibility shim that re-registers the lost ``MySplitImageBatch`` node.

Background (2026-11-07):
    A user workflow ("MiniMax multimodal.json") contained 5 ``MySplitImageBatch``
    nodes, but the original custom-node package is gone (not present in
    ``custom_nodes``) — the canvas showed red boxes and UNKNOWN for each of them.

Approach:
    Register a node with the same ``MySplitImageBatch`` name:
      - inputs: images + 3 INT widgets (kept for layout/wiring compatibility)
      - outputs: IMAGES + frame_count (same as the original node: 2 outputs)
    Semantics follow "take the trailing N frames": N = the second widget;
      - if the first widget is >= 0 and smaller than the total frame count,
        take N frames starting at that position (closer to the original
        start/count/step behaviour)
      - otherwise, take the last N frames
    Existing workflows therefore keep working without re-wiring; tweak the
    widgets on the canvas when exact semantics are needed.
"""

import torch

NODE_NAME = "MySplitImageBatch"


class MySplitImageBatchCompat:
    """Compatibility node: take a slice of frames or the trailing frames."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "start_or_zero": ("INT", {"default": 0, "min": -100000, "max": 100000, "step": 1,
                                          "tooltip": "Start frame. If <= 0 or out of range, the last `count` frames are taken"}),
                "count": ("INT", {"default": 3, "min": 1, "max": 4096, "step": 1,
                                  "tooltip": "Number of frames to take. Default: 3"}),
                "step": ("INT", {"default": 1, "min": 1, "max": 64, "step": 1,
                                 "tooltip": "Frame step. 1 = consecutive frames"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT")
    RETURN_NAMES = ("IMAGES", "frame_count")
    FUNCTION = "run"
    CATEGORY = "DM/Frames"
    DESCRIPTION = ("MySplitImageBatch compatibility for legacy workflows: "
                   "slice frames by start/count/step; when start <= 0 the last `count` frames are returned.")

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
            # Take the last `count` frames (the most common use case).
            lo = max(0, n - count)
            out = images[lo:]
        else:
            out = images[start:start + count]

        if step > 1 and out.shape[0] > 0:
            out = out[::step]

        return (out, n)


NODE_CLASS_MAPPINGS = {NODE_NAME: MySplitImageBatchCompat}
NODE_DISPLAY_NAME_MAPPINGS = {NODE_NAME: "MySplitImageBatch (compat)"}

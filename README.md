<div align="center">

# comfyui-dm-tail-frames

**Take the last N frames of an IMAGE batch — by DM 造梦空间**

[![ComfyUI](https://img.shields.io/badge/ComfyUI-custom%20node-4B8BBE)](https://github.com/comfyanonymous/ComfyUI)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Made by DM](https://img.shields.io/badge/made%20by-DM%20%E9%80%A0%E6%A2%A6%E7%A9%BA%E9%97%B4-10b981)](https://www.520xai.com)

🌐 [DM 造梦空间 · 520xai.com](https://www.520xai.com) &nbsp;|&nbsp; [dmllm.cn](https://dmllm.cn)

</div>

---

ComfyUI custom nodes for **taking the last N frames of an IMAGE batch** — built for multi-modal
video segment stitching (e.g. 20 s per segment, feed the last 3 frames into the next segment).

[中文说明](#中文说明)

## Nodes

| Node | Purpose |
|---|---|
| `DMTailFrames` — *Tail Frames (last N) · 取尾帧* | Take the last `count` frames (default 3), regardless of total frames. |
| `MySplitImageBatch` — *compat* | Drop-in replacement for the lost third-party node of the same name, so old workflows stop showing red UNKNOWN nodes. |

## Install

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/dxyliwei520/comfyui-dm-tail-frames.git dm_tail_frames
```

Restart ComfyUI, then search **Tail** or **尾帧** (category `DM/Frames`).

## Behaviour

| input frames | `count=3` output |
|---|---|
| 480 | last 3 |
| 10 | last 3 |
| 3 | 3 |
| 2 | 2 (`pad=true` pads to 3) |
| 0 | unchanged |

## Stitching tip

If the last 3 frames are reused as the first frames of the next segment, they appear twice when
concatenating (a 3-frame stutter). Either drop them on concat, or use overlap nodes
(`ImageBatchExtendWithOverlap`, `ImageBatchJoinWithTransition`).

## Why not the built-in `ImageFromBatch`?

It works (`batch_index=-3, length=3`), but you need two coupled numbers.
This node only needs `count`, and behaves predictably when the batch is shorter than `count`.

---

## 中文说明

**用途**：多模态视频分段拼接 —— 20 秒一段，取最后 3 帧给下一段当接续参考。
**节点**：`DMTailFrames`（取最后 N 帧，默认 3）+ `MySplitImageBatch` 兼容层（救活旧工作流的红叉节点）。
**安装**：`git clone` 到 `ComfyUI/custom_nodes/dm_tail_frames`，重启 ComfyUI，搜 `Tail` 或 `尾帧`。
**回滚**：删除该目录并重启 ComfyUI。

---


> 为「多模态视频分段拼接」场景写的：20 秒一段，取最后 3 帧给下一段当接续参考。
> **不管总帧数是多少，永远取最后 3 帧。**

## 为什么不用自带的 `ImageFromBatch`

自带的 `ImageFromBatch` 要同时给 `batch_index` 和 `length` 两个参数
（取最后 3 帧得写 `batch_index=-3, length=3`），而且 frame 数不够时行为不直观。
这个节点只填一个 `count`，**与总帧数无关**。

## 安装

目录已就位：

```
<ComfyUI>/custom_nodes/dm_tail_frames/__init__.py
```

重启 ComfyUI（或 ComfyUI-Manager → Restart）后生效。

## 用法

节点搜索：**`Tail`** 或 **`尾帧`**

```
分类：DM / Frames
名称：Tail Frames (last N) · 取尾帧
输入：images (IMAGE 批)
      count  (INT，默认 3)
      pad    (可选，不足 N 帧时用最后一帧补齐，默认关)
输出：images (IMAGE 批，最多 N 帧)
```

典型接法：

```
【每段视频解码出来的 IMAGE 批】 → Tail Frames (count=3) → 作为下一段的首帧/参考
```

## 行为

| 输入帧数 | count=3 时输出 |
|---|---|
| 480（20 秒 24fps）| 最后 3 帧 |
| 10 | 最后 3 帧 |
| 3 | 3 帧（原样）|
| 2 | 2 帧（`pad=true` 时补到 3 帧）|
| 0 | 原样返回（不报错）|

## 注意：拼接时别重复

用最后 3 帧接下一段时，这 3 帧会同时出现在上一段结尾与下一段开头，
直接拼会看到 3 帧的重复抖动。两种处理：

1. **接续时丢掉上一段最后 3 帧**（只把它们当参考图喂下一段）—— 推荐
2. 用重叠拼接节点：`ImageBatchExtendWithOverlap` / `ImageBatchJoinWithTransition`

## 回滚

删除 `custom_nodes/dm_tail_frames/` 目录，重启 ComfyUI 即可。
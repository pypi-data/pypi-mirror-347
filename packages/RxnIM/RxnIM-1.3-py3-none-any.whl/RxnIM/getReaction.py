import sys
sys.path.append('./rxn/')
import torch
from reaction import Reaction
import json
from matplotlib import pyplot as plt
import numpy as np
import huggingface_hub
from huggingface_hub import hf_hub_download

ckpt_path = hf_hub_download("CYF200127/rxn", "DETR.ckpt")
model = Reaction(ckpt_path, device=torch.device('cpu'))
device = torch.device('cpu')

def get_reaction(image_path: str) -> list:
    '''Returns a list of reactions extracted from the image.'''
    image_file = image_path
    return json.dumps(model.predict_image_file(image_file))



def generate_combined_image(predictions, image_file):
    """
    将预测的图像整合到一个对称的布局中输出。
    """
    output = model.draw_predictions(predictions, image_file=image_file)
    n_images = len(output)
    # if n_images == 1:
    #     n_cols = 1
    # elif n_images == 2:
    #     n_cols = 2
    # else:
    #     n_cols = 3
    n_cols = 1  # 每行最多显示 3 张图像
    n_rows = (n_images + n_cols - 1) // n_cols  # 计算需要的行数

    # 确保每张图像符合要求
    processed_images = []
    for img in output:
        if len(img.shape) == 2:  # 灰度图像
            img = np.stack([img] * 3, axis=-1)  # 转换为 RGB 格式
        elif img.shape[2] > 3:  # RGBA 图像
            img = img[:, :, :3]  # 只保留 RGB 通道
        if img.dtype == np.float32 or img.dtype == np.float64:
            img = (img * 255).astype(np.uint8)  # 转换为 uint8
        processed_images.append(img)
    output = processed_images

    # 为不足的子图位置添加占位图
    if n_images < n_rows * n_cols:
        blank_image = np.ones_like(output[0]) * 255  # 生成一个白色占位图
        while len(output) < n_rows * n_cols:
            output.append(blank_image)

    # 创建子图画布
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 13 * n_rows))

    # 确保 axes 是一维数组
    if isinstance(axes, np.ndarray):
        axes = axes.flatten()
    else:
        axes = [axes]  # 单个子图的情况

    # 绘制每张图像
    for idx, img in enumerate(output):
        ax = axes[idx]
        ax.imshow(img)
        ax.axis('off')
        if idx < n_images:
            ax.set_title(f"### Reaction {idx + 1} ###", fontsize=42)

    # 删除多余的子图
    for idx in range(n_images, len(axes)):
        fig.delaxes(axes[idx])

    # 保存整合图像
    combined_image_path = "combined_output.png"
    plt.tight_layout()
    plt.savefig(combined_image_path)
    plt.close(fig)
    return combined_image_path

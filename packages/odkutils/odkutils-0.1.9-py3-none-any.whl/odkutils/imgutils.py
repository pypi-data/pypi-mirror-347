
from PIL import Image
from typing import Tuple,Optional
import os
from .odkipfs import crust_upload_file_to_gateway,crust_upload_file

# GIF转为PNG
def gif_to_png(gif_path, output_folder) -> Optional[Exception]:
    # 打开 GIF 文件
    gif = Image.open(gif_path)
    
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 遍历 GIF 的所有帧
    for i in range(gif.n_frames):
        gif.seek(i)  # 切换到第 i 帧
        frame = gif.convert("RGBA")  # 转换为 RGBA 以确保透明度保留
        frame.save(os.path.join(output_folder, f"frame_{i:03d}.png"), format="PNG")

    print("转换完成！")
    return None


# 获取图片cid 
def get_image_cid(image_path) -> Tuple[Optional[str], Optional[Exception]]:
    local_gateway = "http://127.0.0.1:5001"
    try:
        cid, err = crust_upload_file_to_gateway(local_gateway, image_path)
        if err is None:
            return cid, err
        cid,err = crust_upload_file(image_path)
        return cid, err
    except Exception as e:
        return None, e


    
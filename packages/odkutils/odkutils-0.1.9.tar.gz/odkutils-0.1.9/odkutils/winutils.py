from .caj2pdf import CAJParser
import win32clipboard
import win32con
from typing import Optional
from typing import Tuple, List, Optional
import os 
import base64
import io
import tempfile
from PIL import Image,ImageGrab
from .imgutils import get_image_cid
import json
# caj2pdf caj转为pdf 
def convert_caj2pdf(input_file, output_file)-> Optional[Exception]:
    try:
        caj = CAJParser(input_file)
        caj.convert(output_file)
        return None
    except Exception as e:
        return e

# 获取剪切板文件列表
def get_clipboard_file_list()-> Tuple[Optional[List[str]],Optional[Exception]]:
    file_list = []
    try:
        win32clipboard.OpenClipboard()
        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_HDROP):
            file_list = win32clipboard.GetClipboardData(win32con.CF_HDROP)
    except Exception as e:
        return None,e
    finally:
        win32clipboard.CloseClipboard()
    if len(file_list)<1:
        return None,ValueError("剪切板中无文件")
    return file_list,None

# 获取文件后缀
def get_file_extension(file_path) -> Optional[str]:
    _, file_extension = os.path.splitext(file_path)
    return file_extension


# 保存剪切板截图
def save_clipboard_image(save_path) -> Optional[Exception]:
    img = ImageGrab.grabclipboard()
    if isinstance(img, Image.Image):
        img.save(save_path, "PNG")
        return None
    else:
        return ValueError("剪切板中不是图片")

# 获取截图的base64 
def get_clipboard_image_base64() -> Tuple[Optional[str], Optional[Exception]]:
    img = ImageGrab.grabclipboard()
    if isinstance(img, Image.Image):
        # 将图片转换为base64格式
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return base64.b64encode(img_byte_arr).decode('utf-8'), None
    else:
        return None, ValueError("剪切板中无图片")
        

# 获取剪切板中的图片的CID 支持多个
def get_clipboard_image_cids() -> Tuple[Optional[str], Optional[Exception]]:
    cids = []
    img = ImageGrab.grabclipboard()
    if isinstance(img, Image.Image):
        # 获取临时文件路径
        temp_path = tempfile.mktemp(suffix=".png")
        img.save(temp_path, "PNG")
        cid ,err = get_image_cid(temp_path)
        os.remove(temp_path)
        if err is None:
            return [cid], err
        else:
            return None, err
        
    file_list , err = get_clipboard_file_list()
    if err is not None:
        return None, err
    for file_path in file_list:
        file_ext = get_file_extension(file_path)
        if file_ext in [".png",".jpg",".jpeg",".gif"]:
            cid ,err = get_image_cid(file_path)
            if err is None:
                cids.append(cid)
            else:
                return None, err
    return cids, None


# 保存剪切板中图片的CID
def save_clipboard_image_cids(save_path) -> Optional[Exception]:
    cids, err = get_clipboard_image_cids()
    if err is not None:
        return err
    with open(save_path, "w") as f:
        json.dump(cids, f)
    return None
import os
from typing import Optional
import zipfile
from .caj2pdf import CAJParser
import win32clipboard
import win32con
from typing import Tuple, List, Optional
import pandas as pd
# 解压ZIP文件到指定目录
def unzip_file(zip_path: str, extract_to: str) -> Optional[Exception]:
    """
    解压 ZIP 文件到指定目录
    :param zip_path: ZIP 文件路径
    :param extract_to: 解压到的目标目录
    """
    try:
        os.makedirs(extract_to, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 安全解压：校验每个文件路径
            for file_info in zip_ref.infolist():
                # 防御目录遍历攻击
                target_path = os.path.normpath(os.path.join(extract_to, file_info.filename))
                if not os.path.commonprefix([target_path, os.path.abspath(extract_to)]) == os.path.abspath(extract_to):
                    raise ValueError(f"非法文件路径: {file_info.filename}")
                
            # 完成校验后执行解压
            zip_ref.extractall(extract_to)
            return None
    except (zipfile.BadZipFile, FileNotFoundError, ValueError) as e:
        return e
    except Exception as e:
        return e
# 压缩 ZIP文件
def zip_file(source_path: str, zip_path: str) -> Optional[Exception]:
    """
    压缩文件或目录到ZIP格式
    :param source_path: 要压缩的源文件/目录路径
    :param zip_path: 生成的ZIP文件路径
    """
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if os.path.isfile(source_path):
                # 压缩单个文件
                zipf.write(source_path, os.path.basename(source_path))
            else:
                # 递归压缩目录
                for root, dirs, files in os.walk(source_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=source_path)
                        
                        # 安全校验：确保路径在压缩范围内
                        target = os.path.normpath(os.path.join(source_path, arcname))
                        if not os.path.commonprefix([target, source_path]) == source_path:
                            raise ValueError(f"非法文件路径: {file_path}")
                            
                        zipf.write(file_path, arcname)
        return None
    except (FileNotFoundError, ValueError, PermissionError) as e:
        return e
    except Exception as e:
        return e
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

# 删除文件夹
def remove_folder(folder_path)-> Optional[Exception]:
    try:
        # 使用 os.rmdir() 删除文件夹
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                os.remove(file_path)
                print(f"已删除文件: {file_path}")

            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                os.rmdir(dir_path)
                print(f"已删除文件夹: {dir_path}")

        os.rmdir(folder_path)
        print(f"文件夹 '{folder_path}' 已成功删除。")
        return None
    except OSError as e:
        print(f"删除文件夹 '{folder_path}' 时出错: {e}")
        return e
    
# 读csv文件
def read_csv_files_recursively(folder_path)->  Tuple[List[pd.DataFrame],List[str]]:
    csv_dataframes = []
    filenames = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.csv'):
                file_path = os.path.join(root, file_name)
                filenames.append(file_name)
                try:
                    df = pd.read_csv(file_path)
                    csv_dataframes.append(df)
                    print(f"成功读取文件: {file_name}")
                except Exception as e:
                    print(f"读取文件 {file_name} 时出错: {e}")

    return csv_dataframes,filenames
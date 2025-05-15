import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence, pack_padded_sequence, pad_packed_sequence
import os
from typing import Optional
import zipfile
from .caj2pdf import CAJParser
import win32clipboard
import win32con
from typing import Tuple, List, Optional,Dict
import pandas as pd
import random

# 测井数据集定义 将数据集和标签都放在pd.dataframe中 组成一个列表
class WellLogDataset(Dataset):
    def __init__(self, processed_dataframes, input_cols, target_col):
        self.data = []
        for df in processed_dataframes:
            input_data = torch.tensor(df[input_cols].values, dtype=torch.float32)
            target_data = torch.tensor(df[target_col].values, dtype=torch.long)
            self.data.append((input_data, target_data))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]
    
# Collate function for variable-length sequences
def collate_fn(batch):
    inputs, targets = zip(*batch)
    lengths = torch.tensor([len(seq) for seq in inputs])
    sorted_indices = torch.argsort(lengths, descending=True)
    inputs = [inputs[i] for i in sorted_indices]
    targets = [targets[i] for i in sorted_indices]
    lengths = lengths[sorted_indices]
    padded_inputs = pad_sequence(inputs, batch_first=True)
    padded_targets = pad_sequence(targets, batch_first=True)
    return padded_inputs, lengths, padded_targets


# 统计dataframe中列的 最大值最小值 
def get_logdfs_max_min(dataframes: List[pd.DataFrame], columns: List[str]) -> Tuple[Dict[str, Tuple[float, float]], List[pd.DataFrame]]:
    min_max_values = {}
    valid_dataframes = []
    
    # Initialize min/max tracking
    for col in columns:
        min_max_values[col] = {"min": float('inf'), "max": float('-inf')}

    for df in dataframes:
        # Check for required columns
        if not all(col in df.columns for col in columns):
            print(f"Warning: Skipping dataframe with columns {df.columns} due to missing required columns")
            continue
            
        valid = True
        for col in columns:
            try:
                # Filter out invalid values
                clean_series = df[col][df[col] > -9999]
                if len(clean_series) == 0:
                    valid = False
                    break
                
                # Update min/max values
                col_min = clean_series.min()
                col_max = clean_series.max()
                min_max_values[col]["min"] = min(min_max_values[col]["min"], col_min)
                min_max_values[col]["max"] = max(min_max_values[col]["max"], col_max)

            except Exception as e:
                print(f"Error processing column '{col}': {e}")
                valid = False
                break

        if valid:
            valid_dataframes.append(df)

    # Convert to tuple format
    result = {col: (stats["min"], stats["max"]) for col, stats in min_max_values.items()}
    return result, valid_dataframes


# 标准化 dfs , 传入一个dfs 列表和 字典，将字典中的字段值除以value值 
def normalize_dfs(dataframes: List[pd.DataFrame], max_values: Dict[str, float]) -> List[pd.DataFrame]:
    standardized_dataframes = []
    for df in dataframes:
        standardized_df = df.copy()
        for col, max_val in max_values.items():
            standardized_df[col] = df[col]/max_val
        standardized_dataframes.append(standardized_df)
    return standardized_dataframes

# 将列表数据分为测试集和训练集
def ml_split_data(dataframes: List[pd.DataFrame], test_ratio: float = 0.2) -> Tuple[List[pd.DataFrame], List[pd.DataFrame]]:
    random.seed(42)  # Set a seed for reproducibility
    shuffled_indices = list(range(len(dataframes)))
    random.shuffle(shuffled_indices)
    split_index = int(len(dataframes) * (1 - test_ratio))
    train_indices = shuffled_indices[:split_index]
    test_indices = shuffled_indices[split_index:]
    train_dataframes = [dataframes[i] for i in train_indices]
    test_dataframes = [dataframes[i] for i in test_indices]
    return train_dataframes, test_dataframes

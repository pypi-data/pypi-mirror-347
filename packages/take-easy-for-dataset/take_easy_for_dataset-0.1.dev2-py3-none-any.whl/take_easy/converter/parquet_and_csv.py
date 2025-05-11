from typing import List

import loguru
import pyarrow.parquet as pq
import pandas as pd
import pyarrow as pa


def parquet_to_csv(parquet_path, csv_path):
    """
    将 Parquet 文件转换为 CSV 文件。

    参数:
        parquet_path (str): 输入的 Parquet 文件路径
        csv_path (str): 输出的 CSV 文件路径
    """
    table = pq.read_table(parquet_path)
    df = table.to_pandas()
    df.to_csv(csv_path, index=False)
    loguru.logger.success(f"Parquet to CSV conversion successful: {parquet_path} -> {csv_path}")


def csv_to_parquet(csv_path, parquet_path):
    """
    将 CSV 文件转换为 Parquet 文件。

    参数:
        csv_path (str): 输入的 CSV 文件路径
        parquet_path (str): 输出的 Parquet 文件路径
    """
    df = pd.read_csv(csv_path)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, parquet_path)
    loguru.logger.success(f"CSV to Parquet conversion successful: {csv_path} -> {parquet_path}")


def create_csv_template(params: List[str], file_path='template.csv'):
    """
    根据params生成一个平面的csv模板
    :param file_path:
    :param params:
    :return:
    """
    # 创建一个空的 DataFrame
    df = pd.DataFrame(columns=params)

    # 将 DataFrame 保存为 CSV 文件
    df.to_csv(file_path, index=False)
    loguru.logger.success(f"CSV template created at {file_path}")

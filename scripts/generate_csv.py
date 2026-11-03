#!/usr/bin/env python3
"""
DRP CSV生成脚本
用于将药物相关问题分析结果写入CSV文件
支持创建新文件、追加记录和更新现有记录
"""

import csv
import json
import os
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Any

# CSV表头
CSV_HEADERS = [
    "Patient_ID", "Gender", "Age", "Diagnosis",
    "P_Code", "E1_Code", "E2_Code", "C_Code", "I_Code", "A_Code", "O_Code",
    "P_Confidence", "E1_Confidence", "E2_Confidence", "C_Confidence", 
    "I_Confidence", "A_Confidence", "O_Confidence", "Overall_Confidence",
    "Analysis_Notes", "Last_Updated"
]

def calculate_overall_confidence(confidence: Dict[str, float]) -> float:
    """计算总置信度（所有编码置信度的平均值，忽略缺失或非数值项）"""
    if not confidence:
        return 0.0

    values = [v for v in confidence.values()
              if isinstance(v, (int, float)) and not isinstance(v, bool)]
    if not values:
        return 0.0

    return sum(values) / len(values)

def patient_to_row(patient: Dict[str, Any]) -> List[str]:
    """将患者数据转换为CSV行"""
    codes = patient.get("codes", {})
    confidence = patient.get("confidence", {})
    notes = patient.get("notes", "")
    
    # 计算总置信度
    overall_confidence = calculate_overall_confidence(confidence)
    
    # 获取当前时间
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    row = [
        patient.get("id", ""),
        patient.get("gender", ""),
        patient.get("age", ""),
        patient.get("diagnosis", ""),
        codes.get("P", ""),
        codes.get("E1", ""),
        codes.get("E2", ""),
        ";".join(codes.get("C", [])) if isinstance(codes.get("C"), list) else codes.get("C", ""),
        ";".join(codes.get("I", [])) if isinstance(codes.get("I"), list) else codes.get("I", ""),
        codes.get("A", ""),
        codes.get("O", ""),
        str(confidence.get("P", "")),
        str(confidence.get("E1", "")),
        str(confidence.get("E2", "")),
        str(confidence.get("C", "")),
        str(confidence.get("I", "")),
        str(confidence.get("A", "")),
        str(confidence.get("O", "")),
        f"{overall_confidence:.2f}",
        notes,
        last_updated
    ]
    
    return row

def create_csv_file(csv_path: str) -> None:
    """创建新的CSV文件并写入表头"""
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADERS)

def append_patients(csv_path: str, patients: List[Dict[str, Any]]) -> None:
    """追加患者记录到CSV文件"""
    # 如果文件不存在，创建新文件
    if not os.path.exists(csv_path):
        create_csv_file(csv_path)
    
    # 追加记录
    with open(csv_path, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        for patient in patients:
            row = patient_to_row(patient)
            writer.writerow(row)

def update_patient(csv_path: str, patient: Dict[str, Any]) -> bool:
    """更新现有患者记录"""
    if not os.path.exists(csv_path):
        return False
    
    patient_id = patient.get("id")
    if not patient_id:
        return False
    
    # 读取现有数据
    rows = []
    header = None
    updated = False
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                header = row
                rows.append(header)
                continue
            
            if row and row[0] == patient_id:
                # 更新患者数据
                new_row = patient_to_row(patient)
                rows.append(new_row)
                updated = True
            else:
                rows.append(row)
    
    # 写回文件
    if updated:
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
    
    return updated

def main():
    parser = argparse.ArgumentParser(description='DRP CSV生成脚本')
    parser.add_argument('--input', required=True, help='输入JSON文件路径')
    parser.add_argument('--output', required=True, help='输出CSV文件路径')
    parser.add_argument('--mode', choices=['append', 'update'], default='append', 
                       help='操作模式：append（追加）或 update（更新）')
    
    args = parser.parse_args()
    
    # 读取输入JSON
    try:
        with open(args.input, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"错误：找不到输入文件 {args.input}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"错误：输入文件 {args.input} 不是有效的JSON格式")
        sys.exit(1)
    
    patients = data.get("patients", [])
    if not patients:
        print("警告：输入数据中没有患者记录")
        sys.exit(0)
    
    # 执行操作
    if args.mode == 'append':
        append_patients(args.output, patients)
        print(f"成功追加 {len(patients)} 条患者记录到 {args.output}")
    elif args.mode == 'update':
        success_count = 0
        for patient in patients:
            if update_patient(args.output, patient):
                success_count += 1
        
        if success_count > 0:
            print(f"成功更新 {success_count} 条患者记录在 {args.output}")
        else:
            print(f"警告：没有找到需要更新的患者记录")
    
    # 显示统计信息
    if os.path.exists(args.output):
        with open(args.output, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            total_rows = sum(1 for _ in reader) - 1  # 减去表头
        print(f"CSV文件中共有 {total_rows} 条患者记录")

if __name__ == "__main__":
    main()
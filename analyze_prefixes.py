#!/usr/bin/env python3
import os
import re
import json
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# 定义数据目录
BASE_DIR = "/data/wct/FRP-watcher/server_routing"
PROTOCOLS = ["ICMPv6", "TCP80", "TCP443", "UDP53"]

# 定义美观的颜色方案
COLORS = {
    "ICMPv6": "#3b82f6",  # 蓝色
    "TCP80": "#10b981",   # 绿色
    "TCP443": "#f59e0b",  # 橙色
    "UDP53": "#ef4444"    # 红色
}

# 计算BGP路由前缀的地址空间大小（以2^64为单位）
def calculate_prefix_size(prefix):
    try:
        prefix_len = int(prefix.split('/')[1])
        # 地址空间大小 = 2^(128 - prefix_len)
        # 转换为以2^64为单位，便于显示
        size = 2 ** (128 - prefix_len) / (2 ** 64)
        return size
    except:
        return 0

# 分析所有BGP路由前缀文件
def analyze_all_files():
    results = {}
    
    for protocol in PROTOCOLS:
        protocol_dir = os.path.join(BASE_DIR, protocol)
        if not os.path.exists(protocol_dir):
            continue
        
        files = []
        for filename in os.listdir(protocol_dir):
            if filename.endswith('.txt'):
                # 提取日期
                match = re.search(r'\d{8}', filename)
                if match:
                    date_str = match.group(0)
                    try:
                        date = datetime.strptime(date_str, '%Y%m%d')
                        files.append((date, filename))
                    except:
                        pass
        
        # 按日期排序
        files.sort(key=lambda x: x[0])
        
        # 分析每个文件 - 实现去重累计
        protocol_data = []
        seen_prefixes = set()  # 用于去重的集合
        cumulative_size = 0
        
        for date, filename in files:
            file_path = os.path.join(protocol_dir, filename)
            try:
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                
                # 提取BGP路由前缀并去重
                new_prefixes = []
                for line in lines:
                    prefix = line.strip()
                    if prefix and prefix not in seen_prefixes:
                        new_prefixes.append(prefix)
                        seen_prefixes.add(prefix)
                
                # 计算当日新增BGP路由前缀的数量和大小
                count = len(new_prefixes)
                total_size = sum(calculate_prefix_size(prefix) for prefix in new_prefixes)
                cumulative_size += total_size
                
                protocol_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'count': count,  # 当日新增的去重BGP路由前缀数量
                    'size': total_size,  # 当日新增的去重BGP路由前缀大小
                    'cumulative_size': cumulative_size,  # 累计去重BGP路由前缀大小
                    'unique_total': len(seen_prefixes)  # 累计去重BGP路由前缀数量
                })
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        results[protocol] = protocol_data
    
    return results

# 生成BGP路由前缀折线图
def generate_charts(results):
    # 创建输出目录
    output_dir = os.path.join(BASE_DIR, 'analysis')
    os.makedirs(output_dir, exist_ok=True)
    
    # 设置全局样式
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({
        'font.size': 12,
        'font.family': 'Arial',
        'axes.titlesize': 16,
        'axes.labelsize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.figsize': (16, 9),
        'figure.dpi': 300,
        'lines.linewidth': 2,
        'lines.markersize': 5
    })
    
    # 1. BGP路由前缀数量折线图（当日新增）
    plt.figure()
    for protocol, data in results.items():
        dates = [item['date'] for item in data]
        counts = [item['count'] for item in data]
        plt.plot(dates, counts, marker='o', label=protocol, color=COLORS[protocol], alpha=0.8)
    
    plt.title('BGP IPv6 Routing Prefix Count Over Time', fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Number of New BGP Prefixes')
    plt.legend(title='Protocol', loc='upper left', frameon=True, framealpha=0.9)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'prefix_count.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. BGP路由前缀地址空间大小折线图（当日新增）
    plt.figure()
    for protocol, data in results.items():
        dates = [item['date'] for item in data]
        sizes = [item['size'] for item in data]
        plt.plot(dates, sizes, marker='o', label=protocol, color=COLORS[protocol], alpha=0.8)
    
    plt.title('BGP IPv6 Routing Address Space Size Over Time', fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Address Space Size (2^64 units)')
    plt.legend(title='Protocol', loc='upper left', frameon=True, framealpha=0.9)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'address_space.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. 累计BGP路由前缀地址空间大小折线图（去重后）
    plt.figure()
    for protocol, data in results.items():
        dates = [item['date'] for item in data]
        cumulative_sizes = [item['cumulative_size'] for item in data]
        plt.plot(dates, cumulative_sizes, marker='o', label=protocol, color=COLORS[protocol], alpha=0.8)
    
    plt.title('Cumulative BGP IPv6 Routing Address Space Size', fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Address Space Size (2^64 units)')
    plt.legend(title='Protocol', loc='upper left', frameon=True, framealpha=0.9)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cumulative_address_space.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. 累计BGP路由前缀数量折线图（去重后）
    plt.figure()
    for protocol, data in results.items():
        dates = [item['date'] for item in data]
        unique_totals = [item['unique_total'] for item in data]
        plt.plot(dates, unique_totals, marker='o', label=protocol, color=COLORS[protocol], alpha=0.8)
    
    plt.title('Cumulative BGP IPv6 Routing Prefix Count', fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Number of Unique BGP Prefixes')
    plt.legend(title='Protocol', loc='upper left', frameon=True, framealpha=0.9)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cumulative_prefix_count.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. 保存BGP路由前缀分析数据为JSON
    json_path = os.path.join(output_dir, 'analysis_data.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"BGP routing prefix analysis completed. Charts saved to: {output_dir}")

if __name__ == "__main__":
    results = analyze_all_files()
    generate_charts(results)
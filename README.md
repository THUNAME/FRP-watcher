# FRP-watcher

An open-source tool for long-term monitoring of IPv6 Full Response Prefixes (FRP). It performs global IPv6 FRP probing and data collection using mature existing algorithms.

## Analysis Results

### BGP IPv6 Routing Prefix Analysis

We provide comprehensive analysis of BGP-announced IPv6 Fully Responsive Prefixes (FRPs) across different protocols. The following charts show the trends over time:

#### Daily New BGP Prefixes
![BGP IPv6 Routing Prefix Count Over Time](server_routing/analysis/prefix_count.png)

#### Daily New Address Space Size
![BGP IPv6 Routing Address Space Size Over Time](server_routing/analysis/address_space.png)

#### Cumulative Address Space Size (Deduplicated)
![Cumulative BGP IPv6 Routing Address Space Size](server_routing/analysis/cumulative_address_space.png)

#### Cumulative Prefix Count (Deduplicated)
![Cumulative BGP IPv6 Routing Prefix Count](server_routing/analysis/cumulative_prefix_count.png)

### Key Features
- **Deduplicated Analysis**: All cumulative metrics are calculated after removing duplicate prefixes
- **Multi-Protocol Support**: Analysis across ICMPv6, TCP/80, TCP/443, and UDP/53 protocols
- **Daily Updates**: Data is updated daily with new measurements
- **Visual Insights**: Clear, professional charts for easy interpretation

### Folder Structure
```plaintext
FRP-watcher/
├── server_Luori/        # FRP results from Luori server
├── server_gungnir/      # FRP results from Gungnir server
├── server_routing/      # BGP-announced FRP datasets
│   ├── ICMPv6/          # BGP FRPs under ICMPv6 probing
│   ├── TCP80/           # BGP FRPs under TCP/80 probing
│   ├── TCP443/          # BGP FRPs under TCP/443 probing
│   ├── UDP53/           # BGP FRPs under UDP/53 probing
│   └── analysis/        # Generated analysis charts and data
├── all_shortest.txt     # Take the shortest among all accumulated FRPs so far.
├── analyze_prefixes.py  # Script for generating analysis charts
└── README.md            # Project documentation
```

<!-- GUNGNIR_UPDATE_NOTES_START -->
## Latest Gungnir Scanning Update

本次长期检测逻辑更新（Gungnir 代码提交 945c1a4）：

- ICMPv6、TCP80、TCP443、UDP53 的活跃性扫描统一接入双 ZMap worker 流水线，使用共享时间窗配额、按需整数采样和工作 conserving 调度。
- 默认扫描参数调整为全局 5000 pps、每 BGP 平均 10 pps、每批最多 100000 地址、AS 不限速；四协议串行执行，避免协议间叠加速率。
- 本轮活跃性扫描与 Granularity Correction 均使用 75% 响应阈值和提前停止；论文的 16/16（100%）仍是可配置的基准模式。
- trap 继续使用动态初始修正长度 lc（目标前缀长度减 BGP 前缀长度，非正或未匹配回退 8）、规范父网合并、失败步长减半和 /0 边界终止。
- 活跃性扫描直接输出阈值判定集合，不再经过旧提取器的“至少 10 个响应”二次筛选，保持小地址空间的阈值语义一致。
- 本轮复用 2026-11-03 的四协议最新快照，不重新运行模型；输入和 trap 汇总结果均执行最短覆盖筛选，不合并未复验的相邻兄弟网。
- 四协议全部成功后才统一发布并上传，任一阶段失败则不发布不完整结果。

运行标识：frp-refresh-20261106T122801Z
<!-- GUNGNIR_UPDATE_NOTES_END -->

## Citation

If you find this paper useful in your research, please cite this paper.

```
@inproceedings{Wei2025gungnir,
  title = {Gungnir: Autoregressive Model for Unified Generation of IPv6 Fully Responsive Prefixes},
  author = {Wei, Chentian and Liu, Ying and He, Lin and Cheng, Daguo and Zhou, Jiasheng},
  booktitle = {Proceedings of the 33rd IEEE International Conference on Network Protocols (ICNP 2025)},
  year = {2025},
  pages = {},
  doi = {},
  address = {Seoul, South Korea},
  date = {September 22-25},
}
```

```
@INPROCEEDINGS{cheng2024luori,
  author={Cheng, Daguo and He, Lin and Wei, Chentian and Yin, Qilei and Jin, Boran and Wang, Zhaoan and Pan, Xiaoteng and Zhou, Sixu and Liu, Ying and Zhang, Shenglin and Tan, Fuchao and Liu, Wenmao},
  booktitle={2024 IEEE 32nd International Conference on Network Protocols (ICNP)}, 
  title={Luori: Active Probing and Evaluation of Internet-Wide IPv6 Fully Responsive Prefixes}, 
  year={2024},
  volume={},
  number={},
  pages={1-12},
  keywords={Protocols;Current measurement;Reinforcement learning;Transforms;Routing;Optimization;IPv6;fully responsive prefix;active probing},
  doi={10.1109/ICNP61940.2024.10858548}}
```
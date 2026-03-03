# FRP-watcher

An open-source tool for long-term monitoring of IPv6 Full Response Prefixes (FRP). It performs global IPv6 FRP probing and data collection using mature existing algorithms.

### Folder Structure
```plaintext
FRP-watcher/
├── server_Luori/        # FRP results from Luori server
├── server_gungnir/      # FRP results from Gungnir server
├── server_routing/      # BGP-announced FRP datasets
│   ├── ICMPv6/          # BGP FRPs under ICMPv6 probing
│   ├── TCP80/           # BGP FRPs under TCP/80 probing
│   ├── TCP443/          # BGP FRPs under TCP/443 probing
│   └── UDP53/           # BGP FRPs under UDP/53 probing
├── all_shortest.txt     # Take the shortest among all accumulated FRPs so far.
└── README.md            # Project documentation
```





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

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
└── README.md            # Project documentation

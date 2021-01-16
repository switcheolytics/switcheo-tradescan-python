This is currently broken up into 2 sections:

* Tradehub - Decentralized API, can interact with each public validator via this API
* Tradescan - Centralized Switcheo API, only interact with the Switcheo Tradescan API

A python wrapper to interact with the Trade Scan API offered by the Switcheo team and each public validator API endpoint.

This is under active development and may change drastically from each update.

Ideally this gets merged into the switcheo-python project as DeMex and TradeHub progress.

## Getting Started

```
pip install -r requirements.txt
```

### Tradehub

```
from tradehub.utils import validator_crawler_mp
from tradehub.public_client import PublicClient as TradehubPublicClient
import random

validator_dict = validator_crawler_mp(network = 'main')
active_peers = validator_dict["active_peers"]
decentralized_client = TradehubPublicClient(validator_ip=active_peers[random.randint(a=0, b=len(active_peers)-1)])

print(decentralized_client.get_tokens())
```

### Tradescan
```
from tradescan.public_client import PublicClient

tradescan_client = PublicClient()
print(tradescan_client.get_validator_missed_blocks(address="swthvalcons1pqnlj0na6k8u9y27j3elrx584mt3380dal0j9s"))
```

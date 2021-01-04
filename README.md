A python wrapper to interact with the Trade Scan API offered by the Switcheo team.

This is a work in progress and will more than likely get merged into the switcheo-python project as DeMex and TradeHub progress.

## Getting Started

pip install -r requirements.txt

```
from tradescan.public_client import PublicClient

tradescan_client = PublicClient()
print(tradescan_client.get_validator_missed_blocks(address="swthvalcons1pqnlj0na6k8u9y27j3elrx584mt3380dal0j9s"))
```

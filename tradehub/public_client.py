from typing import Union, List, Optional
from tradescan.utils import Request


class PublicClient(object):
    """
    This class allows the user to interact with the TradeScan API including information
    available with validators, tokens, delegators, addresses, and blockchain stats.
    """

    def __init__(self, node_ip: Union[None, str], node_port: Union[None, int] = 5001, uri: Union[None, str] = None):
        """
        Create a public client using IP:Port or URI format.

        Example::
            public_client = PublicClient("127.0.0.1", 5001)

            # or use uri method

            public_client = PublicClient(uri="https://tradehub-api-server.network/")

        :param node_ip: ip address off a tradehub node.
        :param node_port: prt off a tradehub node, default 5001.
        :param uri: URI address off tradehub node.
        """
        if node_ip and uri:
            raise ValueError("Use IP [+Port] or URI, not both!")

        if node_ip and not node_port:
            raise ValueError("Port has to be set if an IP address is provided!")

        self.api_url: str = uri or f"http://{node_ip}:{node_port}"
        self.request: Request = Request(api_url=self.api_url, timeout=30)
        # self.validators = self.get_validator_public_nodes()
        # self.transaction_types = self.get_transaction_types()
        self.tokens: List[dict] = self.get_token_list()


    # def get_address_rewards(self, address):
    #     if address is not None and isinstance(address, str):
    #         return self.request.get(path = '/distribution/delegators/' + address + '/rewards')

    # def get_address_staking(self, address):
    #     if address is not None and isinstance(address, str):
    #         return self.request.get(path = '/staking/delegators/' + address + '/delegations')

    def get_account(self, swth_address: str) -> dict:
        """
        Request account information about swth wallet.

        Example::

            # wallet behind Devel And Co validator
            public_client.get_account("swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl")

        The expected return result for this function is as follows::

            {
              "height": "6102489",
              "result": {
                "type": "cosmos-sdk/Account",
                "value": {
                  "address": "swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl",
                  "coins": [
                    {
                      "denom": "cel1",
                      "amount": "7"
                    },
                    {
                      "denom": "eth1",
                      "amount": "64752601707981"
                    },
                    {
                      "denom": "nex1",
                      "amount": "12289"
                    },
                    {
                      "denom": "nneo2",
                      "amount": "31555"
                    },
                    {
                      "denom": "swth",
                      "amount": "4113439708"
                    },
                    {
                      "denom": "usdc1",
                      "amount": "45376"
                    },
                    {
                      "denom": "wbtc1",
                      "amount": "29"
                    }
                  ],
                  "public_key": {
                    "type": "tendermint/PubKeySecp256k1",
                    "value": "AtCcJkRx1VhzZkOV06yrxKMZ9IvdRxqv5S4gJSQI/aCB"
                  },
                  "account_number": "1756",
                  "sequence": "55"
                }
              }
            }

        :param swth_address: tradehub switcheo address starting with 'swth1' on mainnet and 'tswth1' on testnet.
        :return: json response
        """
        api_params = {
            "account": swth_address,
        }
        return self.request.get(path='/get_account', params=api_params)

    def get_address(self, username: str) -> str:
        """
        Request swth1 tradehub address which is represented by a username.
        Example::

            public_client.get_address("devel484")

        The expected return result for this function is as follows::

            "swth1qlue2pat9cxx2s5xqrv0ashs475n9va963h4hz"

        .. warning:: This endpoint returns only a string if address is found. If no address is found an exception with status code 404 will be raised.

        :param username: Username is lower case
        :return: swth1 address if found
        """
        api_params = {
            "username": username
        }
        return self.request.get(path='/get_address', params=api_params)

    def get_all_validators(self) -> List[dict]:
        """
        Get all validators. This includes active, unbonding and unbonded validators.

        Example::

            public_client.get_all_validators()

        The expected return result for this function is as follows::

            [
                {
                "OperatorAddress":"swthvaloper1vwges9p847l9csj8ehrlgzajhmt4fcq4dmg8x0",
                "ConsPubKey":"swthvalconspub1zcjduepqcufdssqqfycjwz2srp42tytrs7gtdkkry9cpspea3zqsjzqd2tps73pr63",
                "Jailed":false,
                "Status":2,
                "Tokens":"22414566.55131922",
                "DelegatorShares":"22414566.55131922",
                "Description":{
                    "moniker":"Devel \u0026 Co",
                    "identity":"c572aef1818379c38996878357c321398165fcf0",
                    "website":"https://gitlab.com/switcheo-utils",
                    "security_contact":"",
                    "details":"'Devel' @Devel484 25Y (GER) and 'Coco' @colino87 33Y (FR) are two developers from the Switcheo community who have joined forces to develop awesome applications and tools to support the Switcheo Ecosystem. Stay tuned. Telegram: @DevelAndCo"},
                    "UnbondingHeight":0,
                    "UnbondingCompletionTime":"1970-01-01T00:00:00Z",
                    "Commission":{
                        "commission_rates":{
                            "rate":"0.004200000000000000",
                            "max_rate":"0.200000000000000000",
                            "max_change_rate":"0.010000000000000000"
                        },
                        "update_time":"2020-11-27T20:25:33.45991154Z"
                    },
                    "MinSelfDelegation":"1",
                    "ConsAddress":"swthvalcons1pqnlj0na6k8u9y27j3elrx584mt3380dal0j9s",
                    "ConsAddressByte":"0827F93E7DD58FC2915E9473F19A87AED7189DED",
                    "WalletAddress":"swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl",
                    "BondStatus":"bonded"
                },
                ...
            ]

        .. warning:: The response from this endpoint uses different types off name conventions! For example 'UpperCamelCase' and 'snake_case'.
        :return: list with validators
        """
        return self.request.get(path='/get_all_validators')

    def get_balance(self, swth_address: str) -> dict:
        """
        Get balance which includes available, in open orders and open positions.

        Example::

            # wallet behind Devel And Co validator
            public_client.get_balance("swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl")

        The expected return result for this function is as follows::

            {
                "cel1":{
                    "available":"0.0007",
                    "order":"0",
                    "position":"0",
                    "denom":"cel1"
                },
                "eth1":{
                    "available":"0.000064752601707981",
                    "order":"0",
                    "position":"0",
                    "denom":"eth1"
                },
                "nex1":{
                    "available":"0.00012289",
                    "order":"0",
                    "position":"0",
                    "denom":"nex1"
                },
                "nneo2":{
                    "available":"0.00031555",
                    "order":"0",
                    "position":"0",
                    "denom":"nneo2"
                },
                "swth":{
                    "available":"41.13439708",
                    "order":"0",
                    "position":"0",
                    "denom":"swth"
                },
                "usdc1":{
                    "available":"0.045376",
                    "order":"0",
                    "position":"0",
                    "denom":"usdc1"
                },
                "wbtc1":{
                    "available":"0.00000029",
                    "order":"0",
                    "position":"0",
                    "denom":"wbtc1"
                }
            }

        .. note::
            Only non zero balances are returned. Values are already in human readable version.

        :param swth_address: tradehub switcheo address starting with 'swth1' on mainnet and 'tswth1' on testnet.
        :return: dict with currently holding tokens.
        """
        api_params = {
            "account": swth_address
        }
        return self.request.get(path='/get_balance', params=api_params)

    def get_block_time(self) -> str:
        """
        Get the block time in format HH:MM:SS.ZZZZZZ

        Example::

            public_client.get_block_time()

        The expected return result for this function is as follows::

            "00:00:02.190211"

        .. warning:: This endpoint returns only a string.

        :return: block time as string
        """
        return self.request.get(path='/get_block_time')

    def get_blocks(self, before_id: Optional[int] = None, after_id: Optional[int] = None, order_by: Optional[str] = None, swth_valcons: Optional[str] = None, limit: Optional[int] = None) -> List[dict]:
        """
        Get latest blocks or request specific blocks.

        Example::

            public_client.get_blocks()

        The expected return result for this function is as follows::

            [
                {
                    "block_height":"6103923",
                    "time":"2021-01-09T14:15:53.071509+01:00",
                    "count":"1",
                    "proposer_address":"swthvalcons17m2ueqqqt8u0jz4rv5kvk4kg0teel4sckytjlc"
                },
                {
                    "block_height":"6103922",
                    "time":"2021-01-09T14:15:50.824548+01:00",
                    "count":"0",
                    "proposer_address":"swthvalcons1zecfdrf22f6syz8xj4vn8jsvsalxdhwl9tlflk"
                },
                ...
            ]

        .. warning:: This endpoint is not well documented in official documents. The parameters are NOT required.

        :param before_id: Before block height(exclusive)
        :param after_id: After block height(exclusive)
        :param order_by: Not specified yet
        :param swth_valcons: Switcheo tradehub validator consensus starting with 'swthvalcons1' on mainnet and 'tswthvalcons1' on testnet.
        :param limit: Limit the responded result. Values greater than 200 have no effect and a maximum off 200 results are returned.
        :return: List with found blocks matching the requested parameters. Can be empty list []
        """
        api_params = {
            "before_id": before_id,
            "after_id": after_id,
            "order_by": order_by,
            "proposer": swth_valcons,
            "limit": limit
        }

        return self.request.get(path='/get_blocks', params=api_params)

    def get_candlesticks(self, market, granularity, from_epoch, to_epoch):
        api_params = {}
        api_params["market"] = market
        if granularity in ['1', '5', '30', '60', '360', '1440']:
            api_params["resolution"] = granularity
        api_params["from"] = from_epoch
        api_params["to"] = to_epoch
        return self.request.get(path = '/candlesticks', params = api_params)

    def get_delegation_rewards(self, address):
        api_params = {}
        api_params["account"] = address
        return self.request.get(path = '/get_delegation_rewards', params = api_params)

    def get_external_transfers(self, address):
        api_params = {}
        api_params["account"] = address
        return self.request.get(path = '/get_external_transfers', params = api_params)

    def get_insurance_fund_balance(self):
        return self.request.get(path = '/get_insurance_balance')

    def get_leverage(self, address, market):
        '''
            This appears to be dead.
        '''
        api_params = {}
        api_params["account"] = address
        api_params["market"] = market
        return self.request.get(path = '/get_leverage', params = api_params)

    def get_liquidations(self, before_id, after_id, order_by, limit):
        api_params = {}
        api_params["before_id"] = before_id
        api_params["after_id"] = after_id
        api_params["order_by"] = order_by
        api_params["limit"] = limit
        return self.request.get(path = '/get_liquidations', params = api_params)

    def get_market(self, market_symbol):
        api_params = {}
        api_params["market"] = market_symbol
        # if market_symbol is not None and market_symbol in self.markets:
        #     api_params["market_type"] = market_type
        return self.request.get(path = '/get_market', params = api_params)

    def get_market_stats(self, market):
        api_params = {}
        if market is not None: # and market.lower() in self.markets:
            api_params["market"] = market.lower()
        return self.request.get(path = '/get_market_stats', params = api_params)

    def get_markets(self,
                    market_type = None,
                    is_active = None,
                    is_settled = None):
        api_params = {}
        if market_type is not None and market_type in ['futures', 'spot']:
            api_params["market_type"] = market_type
        if is_active is not None and is_active in [True, False]:
            api_params["is_active"] = is_active
        if is_settled is not None and is_settled in [True, False]:
            api_params["is_settled"] = is_settled
        return self.request.get(path = '/get_markets', params = api_params)

    def get_oracle_result(self, oracle_id):
        api_params = {}
        api_params["id"] = oracle_id
        return self.request.get(path = '/get_oracle_result', params = api_params)

    def get_oracle_results(self):
        return self.request.get(path = '/get_oracle_results')

    def get_orderbook(self, market, limit = None):
        api_params = {}
        if market is not None: # and market.lower() in self.markets:
            api_params["market"] = market.lower()
        if limit is not None and limit > 0:
            api_params["limit"] = limit
        return self.request.get(path = '/get_orderbook', params = api_params)

    def get_order(self, order_id):
        api_params = {}
        api_params["order_id"] = order_id
        return self.request.get(path = '/get_order', params = api_params)

    def get_orders(self, address = None):
        '''
            Documentation states that address is required but it looks like you can pass this without and address
            and it will return the last 200 orders. Most likely means you can also pass limit and pagination to this.
        '''
        api_params = {}
        if address is not None:
            api_params["account"] = address
        return self.request.get(path = '/get_orders', params = api_params)

    def get_position(self, address, market):
        '''
            This appears to be dead.
        '''
        api_params = {}
        api_params["account"] = address
        api_params["market"] = market
        return self.request.get(path = '/get_postion', params = api_params)

    def get_positions(self, address):
        '''
            This appears to be dead.
        '''
        api_params = {}
        api_params["account"] = address
        return self.request.get(path = '/get_postions', params = api_params)

    def get_positions_sorted_by_pnl(self, market):
        api_params = {}
        api_params["market"] = market
        return self.request.get(path = '/get_positions_sorted_by_pnl', params = api_params)

    def get_positions_sorted_by_risk(self, market):
        '''
            This appears to be dead.
        '''
        api_params = {}
        api_params["market"] = market
        return self.request.get(path = '/get_positions_sorted_by_risk', params = api_params)

    def get_positions_sorted_by_size(self, market):
        api_params = {}
        api_params["market"] = market
        return self.request.get(path = '/get_positions_sorted_by_size', params = api_params)

    def get_prices(self, market):
        api_params = {}
        if market is not None: # and market.lower() in self.markets:
            api_params["market"] = market.lower()
        return self.request.get(path = '/get_prices', params = api_params)

    def get_profile(self, address):
        api_params = {}
        api_params["account"] = address
        return self.request.get(path = '/get_profile', params = api_params)

    def get_rich_list(self):
        '''
            This does not appear to be working.
        '''
        return self.request.get(path = '/get_rich_list')

    def get_status(self):
        return self.request.get(path = '/get_status')

    def get_transaction(self, hash):
        api_params = {}
        api_params["hash"] = hash
        return self.request.get(path = '/get_transaction', params = api_params)

    def get_transaction_types(self):
        return self.request.get(path = '/get_transaction_types')

    def get_transactions(self, address, msg_type, height, start_block, end_block, before_id, after_id, order_by, limit):
        api_params = {}
        api_params["address"] = address
        api_params["msg_type"] = msg_type
        api_params["height"] = height
        api_params["start_block"] = start_block
        api_params["end_block"] = end_block
        api_params["before_id"] = before_id
        api_params["after_id"] = after_id
        api_params["order_by"] = order_by
        api_params["limit"] = limit
        return self.request.get(path = '/get_transactions', params = api_params)

    def get_token(self, token):
        '''
        This endpoint does not exist on the TradeHub nodes but it does exist in TradeScan.
        This has benn built to mimic what TradeScan returns.
        '''
        if token is not None and token.lower() in self.tokens:
            for get_token in self.get_tokens():
                if get_token["denom"] == token.lower():
                    return get_token

    def get_token_list(self):
        token_list = []
        tokens = self.get_tokens()
        for token in tokens:
            token_list.append(token["denom"])
        return token_list

    def get_tokens(self):
        return self.request.get(path = '/get_tokens')

    def get_top_r_profits(self, market, limit):
        api_params = {}
        api_params["market"] = market
        api_params["limit"] = limit
        return self.request.get(path = '/get_top_r_profits', params = api_params)

    def get_total_balances(self):
        '''
            This doesn't appear to be working.
        '''
        return self.request.get(path = '/get_total_balances')

    def get_trades(self, market, before_id, after_id, order_by, limit):
        api_params = {}
        api_params["market"] = market
        api_params["before_id"] = before_id
        api_params["after_id"] = after_id
        api_params["order_by"] = order_by
        api_params["limit"] = limit
        return self.request.get(path = '/get_trades', params = api_params)

    def get_trades_by_account(self, before_id, after_id, order_by, limit):
        '''
            This appears to be dead.
        '''
        api_params = {}
        api_params["before_id"] = before_id
        api_params["after_id"] = after_id
        api_params["order_by"] = order_by
        api_params["limit"] = limit
        return self.request.get(path = '/get_trades_by_account', params = api_params)

    def get_username_check(self, username):
        api_params = {}
        api_params["username"] = username
        return self.request.get(path = '/username_check', params = api_params)

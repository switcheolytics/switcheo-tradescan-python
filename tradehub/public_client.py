from tradescan.utils import Request

class PublicClient(object):
    """
    This class allows the user to interact with the TradeScan API including information
    available with validators, tokens, delegators, addresses, and blockchain stats.
    """

    def __init__(self, validator_ip):
        """
        :param api_url: The URL for the Switcheo API endpoint.
        :type api_url: str
        """
        self.api_url = "http://{}:5001".format(validator_ip)
        self.request = Request(api_url = self.api_url, timeout = 30)
        # self.validators = self.get_validator_public_nodes()
        # self.transaction_types = self.get_transaction_types()
        self.tokens = self.get_token_list()


    # def get_address_rewards(self, address):
    #     if address is not None and isinstance(address, str):
    #         return self.request.get(path = '/distribution/delegators/' + address + '/rewards')

    # def get_address_staking(self, address):
    #     if address is not None and isinstance(address, str):
    #         return self.request.get(path = '/staking/delegators/' + address + '/delegations')

    def get_account(self, address):
        api_params = {}
        api_params["account"] = address
        return self.request.get(path = '/get_account', params = api_params)

    def get_address(self, username):
        api_params = {}
        api_params["username"] = username
        return self.request.get(path = '/get_address', params = api_params)

    def get_all_validators(self):
        return self.request.get(path = '/get_all_validators')

    def get_balance(self, address):
        api_params = {}
        api_params["account"] = address
        return self.request.get(path = '/get_balance', params = api_params)

    def get_block_time(self):
        return self.request.get(path = '/get_block_time')

    def get_blocks(self, before_id, after_id, order_by, proposer, limit):
        api_params = {}
        api_params["before_id"] = before_id
        api_params["after_id"] = after_id
        api_params["order_by"] = order_by
        api_params["proposer"] = proposer
        api_params["limit"] = limit
        return self.request.get(path = '/get_blocks', params = api_params)

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

    def get_transactions_fees(self):
        gas_fees = self.request.get(path = '/get_txns_fees')
        fees = {}
        for gas_fee in gas_fees["result"]:
            fees[gas_fee["msg_type"]] = gas_fee["fee"]
        return fees

    def get_username_check(self, username):
        api_params = {}
        api_params["username"] = username
        return self.request.get(path = '/username_check', params = api_params)

from tradescan.utils import Request

class PublicClient(object):
    """
    This class allows the user to interact with the TradeScan API including information
    available with validators, tokens, delegators, addresses, and blockchain stats.
    """

    def __init__(self,
                 api_url = 'https://tradescan.switcheo.org'):
        """
        :param api_url: The URL for the Switcheo API endpoint.
        :type api_url: str
        """
        self.request = Request(api_url = api_url, timeout = 30)
        # self.validators = self.get_validator_public_nodes()
        # self.transaction_types = self.get_transaction_types()
        self.tokens = self.get_token_list()


    # def get_address_rewards(self, address):
    #     if address is not None and isinstance(address, str):
    #         return self.request.get(path = '/distribution/delegators/' + address + '/rewards')

    # def get_address_staking(self, address):
    #     if address is not None and isinstance(address, str):
    #         return self.request.get(path = '/staking/delegators/' + address + '/delegations')

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

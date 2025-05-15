from .api import get_post_investment_product_list


class Client:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Client, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, token='', env='prd'):
        if self._initialized:
            return
        self.token = token
        if env == 'prd':
            self.base_url = "https://gw.datayes.com/aladdin_mof"
        elif env == 'qa':
            self.base_url = "https://gw.datayes-stg.com/mom_aladdin_qa"
        elif env == 'stg':
            self.base_url = "https://gw.datayes-stg.com/mom_aladdin_stg"
        else:
            raise ValueError("error env")
        self._initialized = True

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

    def get_post_investment_product_list(self, post_investment_production_id=None):
        return get_post_investment_product_list(self, post_investment_production_id)

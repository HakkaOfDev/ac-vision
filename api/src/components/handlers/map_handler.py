from ..redis.redis_client import rclient


class MapWorkflow:

    def __init__(self):
        self.map = {
            "olts": [],
            "onus": [],
            "edges": []
        }

    def append_olts(self):
        olt_dasan = rclient.json().get('olt-dasan')
        if olt_dasan is not None:
            olt_dasan['id'] = 1
            olt_dasan['model'] = 'olt-dasan'
            self.map['olts'].append(olt_dasan)

    def append_olt_ubiquiti(self):
        olt_ubiquiti = rclient.json().get('olt-ubiquiti')
        olt_ubiquiti['id'] = 3
        olt_ubiquiti['model'] = 'olt-ubiquiti'
        self.map['nodes'].append(olt_ubiquiti)
        self.map['edges'].append({
            'from': 1,
            'to': 3,
            'status': olt_ubiquiti['status']
        })

    def append_onus(self):
        onus_dasan = rclient.json().get('onus-dasan')
        if onus_dasan is not None:
            onu_id = 10
            for onu in onus_dasan:
                onu['id'] = onu_id
                onu['model'] = 'onu-dasan'
                self.map['onus'].append(onu)
                self.map['edges'].append({
                    'id': onu_id,
                    'from': 1,
                    'to': onu_id,
                    'status': onu['status']
                })
                onu_id += 1

    def append_onus_ubiquiti(self):
        onus_ubiquiti = rclient.json().get('onus-ubiquiti')
        onu_id = 100
        for onu in onus_ubiquiti:
            onu['id'] = onu_id
            onu['model'] = 'onu-ubiquiti'
            self.map['nodes'].append(onu)
            self.map['edges'].append({
                'from': 3,
                'to': onu_id,
                'status': onu['status']
            })
            onu_id += 1

    def build(self):
        self.append_olts()
        self.append_onus()

    def get(self):
        if len(self.map['olts'])==0:
            return None
        return self.map

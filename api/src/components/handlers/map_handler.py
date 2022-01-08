from ..redis.redis_client import rclient


class MapWorkflow:

    def __init__(self):
        self.map = {
            'nodes': [],
            'edges': []
        }

    def append_cloud(self):
        cloud = {
            'id': 0,
            'model': 'cloud',
            'displayName': 'Internet'
        }
        self.map['nodes'].append(cloud)

    def append_rt_stack(self):
        rt_stack = rclient.json().get('rt-stack')
        rt_stack['id'] = 1
        rt_stack['model'] = 'rt-stack'
        self.map['nodes'].append(rt_stack)
        self.map['edges'].append({
            'from': 0,
            'to': 1,
            'status': rt_stack['status']
        })

    def append_olt_dasan(self):
        olt_dasan = rclient.json().get('olt-dasan')
        olt_dasan['id'] = 2
        olt_dasan['model'] = 'olt-dasan'
        self.map['nodes'].append(olt_dasan)
        self.map['edges'].append({
            'from': 1,
            'to': 2,
            'status': olt_dasan['status']
        })

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

    def append_onus_dasan(self):
        onus_dasan = rclient.json().get('onus-dasan')
        onu_id = 10
        for onu in onus_dasan:
            onu['id'] = onu_id
            onu['model'] = 'onu-dasan'
            self.map['nodes'].append(onu)
            self.map['edges'].append({
                'from': 2,
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
        self.append_cloud()
        self.append_rt_stack()
        self.append_olt_dasan()
        self.append_olt_ubiquiti()
        self.append_onus_dasan()
        self.append_onus_ubiquiti()

    def get(self):
        return self.map

import socket
from ipwhois import IPWhois
from joblib import Parallel, delayed, cpu_count

class Lookup:
    def __init__(self):
        self.urlip_dict = {}
        self.ip_list = []
        pass

    def whois_lookup(self,ip):
        obj = IPWhois(ip)
        resp = obj.lookup_whois()
        det = resp.get('nets', [])
        if not det:
            return {}
        dmn_details = {
            self.urlip_dict[ip]: {
                'description': det[0].get('description', ''),
                'name': det[0].get('name', ''),
            }
        }
        #print dmn_details
        return dmn_details

    def get_domain_details(self,urls):

        n_jobs = len(self.urlip_dict)
        if n_jobs == 0 : return

        dmn_details  = Parallel(n_jobs=n_jobs, verbose=10)(delayed(self.whois_lookup)(ip) for ip in self.ip_list)
        print dmn_details

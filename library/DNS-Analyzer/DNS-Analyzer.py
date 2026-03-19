import os
import subprocess
import sys
import datetime

def install_package(package_name):
    try:
        __import__(package_name)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
install_package('dns')
import dns.resolver
import dns.reversename
Name = 'DNS Analyzer'
Description = 'Comprehensive DNS reconnaissance tool for IPv4, IPv6, MX, NS, and TXT records.'
EntityType = 'Domain'

def get_domain_info(domain):
    domain = domain.strip().lower()
    results = {'IPv4': [], 'IPv6': [], 'MX_Records': [], 'Name_Servers': [], 'TXT_Records': [], 'TTL': 'N/A'}
    lookup_map = {'A': 'IPv4', 'AAAA': 'IPv6', 'MX': 'MX_Records', 'NS': 'Name_Servers', 'TXT': 'TXT_Records'}
    try:
        for record_type, key in lookup_map.items():
            try:
                answers = dns.resolver.resolve(domain, record_type)
                if results['TTL'] == 'N/A':
                    results['TTL'] = f'{answers.ttl} seconds'
                for rdata in answers:
                    if record_type == 'MX':
                        results[key].append(f'{rdata.exchange} (Priority: {rdata.preference})')
                    else:
                        results[key].append(rdata.to_text())
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                continue
            except Exception:
                results[key] = ['Query Timeout/Error']
        return {'value': domain, 'name': Name, 'icon': os.path.join(os.path.dirname(__file__), 'assets', 'dns.png'), 'type': EntityType, 'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'properties': {'IPv4_Addresses': ' | '.join(results['IPv4']) if results['IPv4'] else 'None', 'IPv6_Addresses': ' | '.join(results['IPv6']) if results['IPv6'] else 'None', 'Mail_Servers': ' | '.join(results['MX_Records']) if results['MX_Records'] else 'None', 'Name_Servers': ' | '.join(results['Name_Servers']) if results['Name_Servers'] else 'None', 'Text_Records': ' '.join(results['TXT_Records']) if results['TXT_Records'] else 'None', 'Time_To_Live': results['TTL'], 'IP_Count': len(results['IPv4']) + len(results['IPv6']), 'Security_SPF': 'Present' if 'v=spf1' in str(results['TXT_Records']) else 'Missing', 'Status': 'Active' if results['IPv4'] else 'No Records Found', 'Description': Description, 'Provider': 'Direct Recursion via dnspython'}}
    except Exception as e:
        return {'value': domain, 'name': Name, 'type': EntityType, 'properties': {'Critical_Error': str(e), 'Status': 'Failed'}}
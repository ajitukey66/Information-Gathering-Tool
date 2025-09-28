
import whois
import dns.resolver
import shodan
import argparse
import requests
import socket

argparse = argparse.ArgumentParser(description="This is a simple information gathering tool", usage="python3 info_gathering.py -d DOMAIN [-s IP]")

argparse.add_argument("-d", "--domain", help="Enter the domain name for footprinting", required=True)
argparse.add_argument("-s", "--shodan", help="Enter the ip address for shodan search")

args = argparse.parse_args()
domain = args.domain
ip = args.shodan

# whois module
print("[+] Getting whois info...")
# using whois library, creating instance
try:
    py = whois.query(domain)
    print("Name: {}".format(py.name))
    print("Registrar: {}".format(py.registrar))
    print("Creation Date: {}".format(py.creation_date))
    print("Expiration Date: {}".format(py.expiration_date))
    print("Registrant: {}".format(py.registrant))
    print("Registration Country: {}".format(py.registrant_country))
except:
    pass

# dns module
print("[+] Getting dns info ...")
# implementing dns.resolver from dnspython
try:
    for a in dns.resolver.resolve(domain, 'A'):
        print("[+] A record: {}".format(a.to_text()))
    for ns in dns.resolver.resolve(domain, 'NS'):
        print("[+] NS record: {}".format(ns.to_text()))
    for mx in dns.resolver.resolve(domain, 'MX'):
        print("[+] MX record: {}".format(mx.to_text()))
    for txt in dns.resolver.resolve(domain, 'TXT'):
        print("[+] TXT record: {}".format(txt.to_text()))
except:
    pass

# Geolocation module
print("[+] Getting geolocation info ...")
# implementing requests library for web request
try:
    response = requests.request('Get', "https://geolocation-db.com/json/" + socket.gethostbyname(domain)).json()
    print("[+] Country: {}".format(response['country_name']))
    print("[+] Latitude: {}".format(response['latitude']))
    print("[+] Longitude: {}".format(response['longitude']))
    print("[+] City: {}".format(response['city']))
    print("[+] state: {}".format(response['state']))
except:
    pass


#shodan module
if ip:
    print("[+] Getting shodan info for IP {}".format(ip))
    #shodan API
    api = shodan.Shodan("___API_KEY___")
    try:
        result = api.search(ip)
        print("[+] Results found: {}".format(results['total']))
        print("[+] IP: {}".format(result['ip_str']))
        print("[+] Data: \n{}".format(result['data']))
        print()
    except:
        print("[-] Shodan search error.")
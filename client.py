#!/usr/bin/env python3
"""This file is not official part of the project, it's just used for testing
purposes:
    $ python3 -m venv .venv
    $ source .venv/lib/activate
    $ pip install dnspython
    $ python client.py --domain=n26.de --proto=udp --host=127.0.0.1 --port=5353
"""
import sys
import argparse

import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query

parser = argparse.ArgumentParser(description='Perform DNS queries')
parser.add_argument('--domain', default='n26.de', help='The domain to resolve')
parser.add_argument('--proto', default='tcp', help='The protocol to use')
parser.add_argument('--host', default='127.0.0.1', help='IP of the DNS server')
parser.add_argument('--port', default='5353', type=int, help='Port of the DNS server')

args = parser.parse_args()


if __name__ == '__main__':
    method = dns.query.udp if args.proto == 'udp' else dns.query.tcp
    qname = dns.name.from_text(args.domain)
    q = dns.message.make_query(qname, dns.rdatatype.NS)
    print('The query is:\n', q)
    print('')
    print('The response is:')

    r = method(q, args.host, port=args.port)
    print(r)
    print('')
    print('The nameservers are:')
    ns_rrset = r.find_rrset(r.answer, qname, dns.rdataclass.IN, dns.rdatatype.NS)
    for rr in ns_rrset:
        print(rr.target)
    print('')

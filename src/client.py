#!/usr/bin/env python3
"""This file is not official part of the project, it's just used for testing
purposes:
    $ python3 -m venv .venv
    $ source .venv/lib/activate
    $ pip install dnspython
    $ python3 client.py google.com udp
"""
import sys

import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query


if __name__ == '__main__':
    domain = 'n26.de'
    if len(sys.argv) > 1:
        domain = sys.argv[1]

    if len(sys.argv) > 2 and sys.argv[2] == 'udp':
        method = dns.query.udp
    else:
        method = dns.query.tcp

    qname = dns.name.from_text(domain)
    q = dns.message.make_query(qname, dns.rdatatype.NS)
    print('The query is:\n', q)
    print('')
    print('The response is:')

    r = method(q, '127.0.0.1', port=5353)
    print(r)
    print('')
    print('The nameservers are:')
    ns_rrset = r.find_rrset(r.answer, qname, dns.rdataclass.IN, dns.rdatatype.NS)
    for rr in ns_rrset:
        print(rr.target)
    print('')

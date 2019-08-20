#!/usr/bin/env python3
import sys

import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query

# This way is just like nslookup/dig:

if __name__ == '__main__':
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

    r = method(q, '127.0.0.1', port=3853)
    print(r)
    # print('r.answer:', r.answer)
    # print('qname:', qname)
    # print('dns.rdataclass.IN:', dns.rdataclass.IN)
    # print('dns.rdatatype.NS:', dns.rdatatype.NS)
    print('')
    print('The nameservers are:')
    ns_rrset = r.find_rrset(r.answer, qname, dns.rdataclass.IN, dns.rdatatype.NS)
    for rr in ns_rrset:
        print(rr.target)
    print('')

# A higher-level way

# import dns.resolver
#
# resolver = dns.resolver.Resolver(configure=False)
# resolver.nameservers = ['127.0.0.1']
# resolver.port = 3853
# answer = resolver.query('amazon.com', 'NS')
# print('The nameservers are:')
# for rr in answer:
#     print(rr.target)

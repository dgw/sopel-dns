# coding=utf8
"""sopel-dns

A DNS lookup plugin for Sopel bots
"""
from __future__ import unicode_literals, absolute_import, division, print_function

import time

import dns.resolver
import requests

from sopel import module

ONELINE_RDTYPES = [
    'A',
    'AAAA',
    'CNAME',
]
MULTILINE_RDTYPES = [
    'TXT',
]
IMPLEMENTED_RDTYPES = ONELINE_RDTYPES + MULTILINE_RDTYPES


@module.commands('dns')
@module.example('.dns domain.tld AAAA', user_help=True)
@module.example('.dns domain.tld', user_help=True)
@module.rate(user=300)
def get_dnsinfo(bot, trigger):
    """Look up DNS information for a domain name."""
    domain = trigger.group(3)
    rdtype = trigger.group(4) or 'A'
    rdtype = rdtype.upper()

    if rdtype not in IMPLEMENTED_RDTYPES:
        bot.reply("I don't know how to show {} records yet.".format(rdtype))
        return module.NOLIMIT

    responses = []

    try:
        answers = dns.resolver.query(domain, rdtype)
        if len(answers) > 0:
            for rdata in answers:
                responses.append(rdata.to_text())
        else:
            bot.reply("Did not find any A records for {}.".format(domain))
            return

    except dns.exception.Timeout:
        bot.reply("DNS lookup timed out for {}.".format(domain))
        return

    except dns.resolver.NXDOMAIN:
        bot.reply("DNS lookup returned NXDOMAIN for {}.".format(domain))
        return

    except dns.resolver.NoNameservers:
        bot.reply("DNS lookup attempted, but no nameservers were available.")
        return

    if rdtype in ONELINE_RDTYPES:
        bot.reply(', '.join([str(x) for x in responses]))
        return

    # Record types that should be handled one response per line
    for x in responses:
        bot.reply(str(x))

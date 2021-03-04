# coding=utf8
"""sopel-dns

A DNS lookup plugin for Sopel IRC bots
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
    'NS',
]
MULTILINE_RDTYPES = [
    'MX',
    'PTR',
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
        if rdtype == 'PTR':
            answers = dns.resolver.resolve_address(domain)
        else:
            answers = dns.resolver.resolve(domain, rdtype)

    except dns.exception.Timeout:
        bot.reply("DNS lookup timed out for {}.".format(domain))
        return module.NOLIMIT
    except dns.resolver.NXDOMAIN:
        bot.reply("DNS lookup returned NXDOMAIN for {}.".format(domain))
        return module.NOLIMIT
    except dns.resolver.NoNameservers:
        bot.reply("DNS lookup attempted, but no nameservers were available.")
        return module.NOLIMIT
    except dns.resolver.NoAnswer:
        bot.reply("No {} records exist for {}.".format(rdtype, domain))
        return module.NOLIMIT
    except dns.exception.SyntaxError:
        if rdtype == 'PTR':
            bot.reply("PTR record lookup is only supported for IP addresses.")
        else:
            bot.reply("That domain name doesn't seem to be valid.")
        return module.NOLIMIT

    if len(answers) > 0:
        for rdata in answers:
            responses.append(rdata.to_text())
    else:
        bot.reply("Did not find any {} records for {}.".format(rdtype, domain))
        return

    if rdtype in ONELINE_RDTYPES:
        bot.reply(', '.join([str(x) for x in responses]))
        return

    # Record types that should be handled one response per line
    for x in responses:
        bot.reply(str(x))

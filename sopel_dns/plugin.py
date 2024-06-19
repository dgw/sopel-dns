"""sopel-dns

A DNS lookup plugin for Sopel IRC bots
"""
from __future__ import unicode_literals, absolute_import, division, print_function

import time

import dns.resolver
import requests

from sopel import plugin

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


@plugin.commands('dns')
@plugin.example('.dns 1.2.3.4 PTR', user_help=True)
@plugin.example('.dns domain.tld AAAA', user_help=True)
@plugin.example('.dns domain.tld', user_help=True)
@plugin.output_prefix('[dns] ')
@plugin.rate(
    user=120,
    message="Please wait {time_left} before attempting another DNS lookup."
)
def get_dnsinfo(bot, trigger):
    """Look up DNS information."""
    domain = trigger.group(3)
    rdtype = trigger.group(4) or 'A'
    rdtype = rdtype.upper()

    if rdtype not in IMPLEMENTED_RDTYPES:
        bot.reply("I don't know how to show {} records yet.".format(rdtype))
        return plugin.NOLIMIT

    responses = []

    try:
        if rdtype == 'PTR':
            answers = dns.resolver.resolve_address(domain)
        else:
            answers = dns.resolver.resolve(domain, rdtype)

    except dns.exception.SyntaxError:
        if rdtype == 'PTR':
            bot.reply("PTR record lookup is only supported for IP addresses.")
        else:
            bot.reply("That domain name doesn't seem to be valid.")
        return plugin.NOLIMIT
    except dns.exception.Timeout:
        bot.say("DNS lookup timed out for {}.".format(domain))
        return plugin.NOLIMIT
    except dns.resolver.NoNameservers:
        bot.say("DNS lookup attempted, but no nameservers were available.")
        return plugin.NOLIMIT
    except dns.resolver.NXDOMAIN:
        bot.say("DNS lookup returned NXDOMAIN for {}.".format(domain))
        return  # do rate-limit, since query succeeded
    except dns.resolver.NoAnswer:
        bot.say("DNS lookup returned no {} records for {}.".format(rdtype, domain))
        return  # do rate-limit, since query succeeded

    if len(answers) > 0:
        for rdata in answers:
            responses.append(rdata.to_text())
    else:
        bot.say("Did not find any {} records for {}.".format(rdtype, domain))
        return

    if rdtype in ONELINE_RDTYPES:
        bot.say(', '.join([str(x) for x in responses]))
        return

    # Record types that should be handled one response per line
    for x in responses:
        bot.say(str(x))

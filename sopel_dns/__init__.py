# coding=utf8
"""sopel-dns

A DNS lookup plugin for Sopel bots
"""
from __future__ import unicode_literals, absolute_import, division, print_function

import time

import dns.resolver
import requests

from sopel import module


@module.commands('dns')
@module.example('.dns domain.tld')
@module.rate(user=300)
def get_dnsinfo(bot, trigger):
    """Look up DNS information for a domain name."""
    domain = trigger.group(2)

    responses = []

    try:
        answers = dns.resolver.query(domain, 'A')
        if len(answers) > 0:
            for rdata in answers:
                responses.append(rdata.to_text())
        else:
            bot.reply("Did not find any A records for {}.".format(domain))
            return

    except dns.exception.Timeout as e:
        bot.reply("DNS lookup timed out for {}.".format(domain))
        return

    except dns.resolver.NXDOMAIN as e:
        bot.reply("DNS lookup returned NXDOMAIN for {}.".format(domain))
        return

    except dns.resolver.NoNameservers:
        bot.reply("DNS lookup attempted, but no nameservers were available.")
        return

    bot.reply(', '.join([str(x) for x in responses]))

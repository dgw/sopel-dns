# sopel-dns

A DNS lookup plugin for Sopel IRC bots


## Usage

Basic usage performs an 'A' record lookup:

```
<user> .dns domain.tld
<bot>  user: 10.10.0.1
```

To look up IPv6 addresses instead, specify the 'AAAA' record type:

```
<user> .dns domain.tld AAAA
<bot>  user: fd12:3456:789a:1::1
```

Other [supported record types](#supported-dns-record-types) output their
results in a similar fashion. Some types, such as `MX` and `TXT`, split the
output across multiple lines to make it easier to read, at the cost of
possible "spam" if there are many records attached to the queried domain.

### Rate limiting

Normal users are rate-limited to one `.dns` command every 5 minutes, both to
control channel flood and to prevent hammering whatever DNS server Sopel's
host system uses to resolve the submitted queries.


## Supported DNS record types

* `A`
* `AAAA`
* `CNAME`
* `MX`
* `NS`
* `PTR`
* `TXT`

If a record type you want isn't listed here, feel free to request it in an
[issue](https://github.com/dgw/sopel-dns/issues/new). Even better: a pull
request enabling that record type, including a demo of the resulting output.

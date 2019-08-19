#!/usr/bin/env python
# coding: utf-8
"""
    ddns.py
    Auto set name.com dns to public IP

"""

import click 
import requests
from namecom import Name

@click.command()
@click.option("--domain",required=True, help="domain name like example.org")
@click.option("--host",required=True, help="host like www, www1")
@click.option("--username",required=True, help="username for name.com")
@click.option("--token",required=True, help="token for name.com")

def ddns(domain=None, host=None, username=None, token=None):
    """Set name.com dns record to public IP."""
    ip = requests.get('https://api.ipify.org').text
    name = Name(username, token)

    data = name.list_records(domain)
    existing_records = [i for i in data["records"] if i.get("host", None) == host]

    if len(existing_records) == 1:
        record = existing_records[0]
        # keep existing record
        if record["type"] == "A" and record["answer"] == ip:
            click.echo("We have found same record there, quit")
            return
        else:
            # update existing record
            click.echo("update existing record")
            name.update_record(domain, record["id"], host, "A", ip)
            return

    click.echo("create record " + host + "." + domain + " to " + ip)
    name.create_record(domain, host, "A", ip)

if __name__ == '__main__':
    ddns()
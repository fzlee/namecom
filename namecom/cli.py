#!/usr/bin/env python
# coding: utf-8
"""
    cli.py
    ~~~~~~~~~~

"""
import os
import sys

import click

from namecom import Name


@click.group()
def cli():
    pass


def get_namecom_client(name, token):
    if not name or not token:
        name = os.environ.get("NAMECOM_NAME", None)
        token = os.environ.get("NAMECOM_TOKEN", None)

    if not name or not token:
        click.echo("name or token are missing", err=True)
        sys.exit(1)

    return Name(name, token)


@cli.command()
@click.option("--domain", help="domain name like example.org")
@click.option("--host", help="host like www, www1")
@click.option("--dns_type", help="DNS record type, like A, cname")
@click.option("--answer", help="127.0.0.1, example.org, etc")
@click.option("--name", help="name for name.com", default="")
@click.option("--token", help="token for name.com", default="")
def create_dns(domain, host, dns_type, answer, name, token):
    client = get_namecom_client(name, token)

    data = client.list_records(domain)
    existing_records = [i for i in data["records"] if i.get("host", None) == host]

    if len(existing_records) == 1:
        record = existing_records[0]
        # keep existing record
        if record["type"] == dns_type and record["answer"] == answer:
            click.echo("We have found same record there, quit")
            return
        else:
            # update existing record
            click.echo("update existing record")
            client.update_record(domain, record["id"], host, dns_type, answer)
            return

    # delete existing records and create new
    for record in existing_records:
        client.delete_record(record["id"])
    client.create_record(domain, host, dns_type, answer)


@cli.command()
@click.option("--domain", help="domain name like example.org")
@click.option("--host", help="host like www, www1")
@click.option("--name", help="name for name.com", default="")
@click.option("--token", help="token for name.com", default="")
def delete_dns(domain, host, name, token):
    client = get_namecom_client(name, token)

    data = client.list_records(domain)
    existing_records = [i for i in data["records"] if i.get("host", None) == host]

    for record in existing_records:
        client.delete_record(domain, record["id"])

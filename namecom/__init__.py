#!/usr/bin/env python
# coding: utf-8
"""
    __init__.py
    ~~~~~~~~~~

"""
import requests

from .helpers import request_error_retry


class DNSMixin():

    def list_records(self, domain_name, **kwargs):
        """
        domain_name: example.org
        kwargs: {
            "page": 1,
            "perPage": 1000
        }
        """
        path = "domains/{}/records".format(domain_name)
        return self.get(
            path,
            params=kwargs
        )

    def get_record(self, domain_name, id_):
        """
        domain_name: example.org
        id: id for record
        """
        path = "domains/{}/records/{}".format(domain_name, id_)
        return self.get(path)

    def create_record(self, domain_name, host, type_, answer, ttl=300, priority=None):
        """
        create_record(
            domain_name="example.org",
            host="www",
            type_="A",
            answer="127.0.0.1"
        )
        """
        path = "domains/{}/records".format(domain_name)
        data = {
            "host": host,
            "type": type_,
            "answer": answer,
            "ttl": ttl
        }

        if type_ in ("MX", "SRV"):
            data["priority"] = priority

        return self.post(path, data)

    def update_record(self, domain_name, id_, host, type_, answer, ttl=300, priority=None):
        """
        parameters are nearly the same as create_record
        """
        path = "domains/{}/records/{}".format(domain_name, id_)
        data = {
            "host": host,
            "type": type_,
            "answer": answer,
            "ttl": ttl
        }

        if type_ in ("MX", "SRV"):
            data["priority"] = priority

        return self.put(path, data)

    def delete_record(self, domain_name, id_):
        path = "domains/{}/records/{}".format(domain_name, id_)
        return self.delete(path)


class DomainMixin():

    def list_domains(self, **kwargs):
        return self.get("domains", params=kwargs)

    def get_domain(self, domain_name):
        return self.get("domains/{}".format(domain_name))

    def check_availability(self, domain_names):
        return self.post(
            "domains:checkAvailability",
            {
                "domainNames": domain_names
            }
        )


class Name(DNSMixin, DomainMixin):
    def __init__(self, name, token, debug=False):
        self.__name = name
        self.__token = token
        self.__debug = debug
        if self.__debug:
            self.__server = "https://api.dev.name.com/v4/"
        else:
            self.__server = "https://api.name.com/v4/"
        self.__client = None

    @property
    def client(self):
        if not self.__client:
            self.__client = requests.Session()
            self.__client.auth = (self.__name, self.__token)
        return self.__client

    @request_error_retry()
    def get(self, path, **kwargs):
        url = self.__server + path
        return self.client.get(url, **kwargs).json()

    @request_error_retry()
    def post(self, path, data):
        url = self.__server + path
        return self.client.post(url, json=data).json()

    @request_error_retry()
    def put(self, path, data):
        url = self.__server + path
        return self.client.put(url, json=data).json()

    @request_error_retry()
    def delete(self, path):
        url = self.__server + path
        return self.client.delete(url).json()

    def hello(self):
        return self.get("hello")

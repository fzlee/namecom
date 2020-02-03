## Python sdk for name.com v4 api


#### Installation
```
pip install namecom --upgrade
``` 


#### Command line guide

If you do not want to append --name and --token to the command every time, run the following command should do some help
```bash
export NAMECOM_NAME=<your namecom username>
export NAMECOM_TOKEN=<your namecom token>
```


To delete a DNS record
```bash
namecli create_dns 
    --domain example.org
    --host www
    --dns-type A
    --answer 127.0.0.1
    --name <your namecom username>
    --token <your namecom token>
```

To delete a DNS record
```bash
namecli delete_dns 
    --domain example.org
    --host www
    --name <your namecom username>
    --token <your namecom token>
```

To create a DDNS record
```bash
namecli ddns 
    --domain example.org
    --host www
    --name <your namecom username>
    --token <your namecom token>
```

#### SDK development

So far, not all name.com api are supported.

Initialization
```python
from namecom import Name
name = Name(name, token)
name.list_records("example.org", page=1, perPage=1000)
name.delete_record("example.org", id_="12345", )
name.create_record("example.org", "www", "A", "127.0.0.1")
```


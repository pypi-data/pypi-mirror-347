# vCenter Bindings
 
vCenter Bindings library contains client bindings for VMware vCenter Automation APIs. This library is part of [vSphere Automation SDK for Python](https://github.com/vmware/vsphere-automation-sdk-python).
 
[Source code](https://github.com/vmware/vsphere-automation-sdk-python/tree/master/lib/src/vcenter-bindings) | [Package (PyPI)](https://pypi.org/project/vcenter-bindings/) | [REST API documentation](https://developer.vmware.com/apis/vsphere-automation/latest/)
 
## Getting started
 
### Prerequisites
 
- Python 3.8+ is required to use this package.
 
### Install the package
 
```bash
pip install vcenter-bindings
```
 
### Connect to a vCenter Server
 
```python
import requests
import urllib3
from vmware.vapi.vsphere.client import create_vsphere_client
session = requests.session()
 
# Disable cert verification for demo purpose.
# This is not recommended in a production environment.
session.verify = False
 
# Disable the secure connection warning for demo purpose.
# This is not recommended in a production environment.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
# Connect to a vCenter Server using username and password
vsphere_client = create_vsphere_client(server='<vc_ip>', username='<vc_username>', password='<vc_password>', session=session)
 
# List all VMs inside the vCenter Server
vsphere_client.vcenter.VM.list()
```
 
Output in a Python Interpreter:
 
```shell
(venv) het-m03:vsphere-automation-sdk-python het$ python
Python 3.9.8 (main, Nov 10 2021, 06:03:50)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import requests
>>> import urllib3
>>> from vmware.vapi.vsphere.client import create_vsphere_client
>>> session = requests.session()
>>> session.verify = False
>>> urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
>>> vsphere_client = create_vsphere_client(server='<vc_ip>', username='<vc_username>', password='<vc_password>', session=session)
>>> vsphere_client.vcenter.VM.list()
[Summary(vm='vm-58', name='standalone-20e4bd3af-esx.0-vm.0', power_state=State(string='POWERED_OFF'), cpu_count=1, memory_size_mib=256),
...]
```
 
**NOTE:** If you are using Bash, be sure to use single quote for username and password to preserve the values. If you use double quote, you will have to escape special characters, such as "$". See [Bash manual](http://www.gnu.org/software/bash/manual/html_node/Double-Quotes.html)

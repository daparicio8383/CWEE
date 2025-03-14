# Injection Attacks

Module that covers XPath Injection, LDAP injection, and HTML injection in PDF generation libraries.

## XPath Injection

[BlindXPathInjection.py](../Injection%20attacks/BlindXPathInjection.py): script to map the whole XML document, in the context of a blind XPath injection (not a time-based exploitation).

### Usage

The script is intended for blind XPath injections that take place in HTTP POST requests. Before executing it, the user will have to do the following:

- Define the request body parameters.
- Copy and paste the exploit url in the “url” variable.
- By default, the script has been configured so that the requests go through a proxy, located at 127.0.0.1:8080.
- For the tests performed, a maximum of **10 child nodes** was set to search from each node found, as well as **a maximum of 50 characters** as for searches performed with **string-length()**. These values can be changed without any problem.
- The payloads will have the following form: '**bbb' or string-length(name(\/\*\[1\]))=1 and '1'='1**, for example. They will arrive at the server only URL-encoded, but the user can change this, if necessary.

```
python BlindXPathInjection.py
```

##### ASCII representation of an XML document.

![alt text](https://github.com/daparicio8383/CWEE/blob/main/Images/BlindXPathInjection.png "ASCII representation of an XML document")

---

## LDAP Injection

[BlindLDAPInjection.py](../Injection%20attacks/BlindLDAPInjection.py): script to determine the value of an attribute, ina LDAP search filter, in the context of a blind LDAP Injection.

### Usage

The script is intended for blind LDAP injections that take place in HTTP POST requests. Before executing it, the user will have to do the following:

- Define the request body parameters.
- Copy and paste the exploit url in the “url” variable.
- By default, the script has been configured so that the requests go through a proxy, located at 127.0.0.1:8080.
- The brute force test will only take place for **one** attribute, that will be defined in the variable **Attribute**. If you want to know the values of more of them, you should change the one in the variable.
- The payloads will assume the search filter has this form: **(&(uid=user))(|(attribute=foo\*)(password=password)))**. Change this, if necessary.

```
python BlindLDAPInjection.py
```

##### ASCII representation of an XML document.

![alt text](https://github.com/daparicio8383/CWEE/blob/main/Images/BlindLDAPInjection.png "Discovering chars of the search filter")


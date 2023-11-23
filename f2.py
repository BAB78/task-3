Traceback (most recent call last):
  File "/home/devasc/.local/lib/python3.8/site-packages/paramiko/channel.py", line 699, in recv
    out = self.in_buffer.read(nbytes, self.timeout)
  File "/home/devasc/.local/lib/python3.8/site-packages/paramiko/buffered_pipe.py", line 164, in read
    raise PipeTimeout()
paramiko.buffered_pipe.PipeTimeout

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/devasc/.local/lib/python3.8/site-packages/netmiko/base_connection.py", line 550, in _read_channel_expect
    new_data = self.remote_conn.recv(MAX_BUFFER)
  File "/home/devasc/.local/lib/python3.8/site-packages/paramiko/channel.py", line 701, in recv
    raise socket.timeout()
socket.timeout

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/devasc/labs/prne/task.py", line 44, in <module>
    net_connect.send_config_set(acl_commands)
  File "/home/devasc/.local/lib/python3.8/site-packages/netmiko/base_connection.py", line 1757, in send_config_set
    new_output = self.read_until_pattern(pattern=re.escape(cmd.strip()))
  File "/home/devasc/.local/lib/python3.8/site-packages/netmiko/base_connection.py", line 627, in read_until_pattern
    return self._read_channel_expect(*args, **kwargs)
  File "/home/devasc/.local/lib/python3.8/site-packages/netmiko/base_connection.py", line 560, in _read_channel_expect
    raise NetmikoTimeoutException(
netmiko.ssh_exception.NetmikoTimeoutException: Timed-out reading channel, data not available.

from netmiko import ConnectHandler

# Define the router details
router = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': 'cisco',
    'password': 'cisco123!',
    'secret': 'class123!',
}

# Connect to the router
net_connect = ConnectHandler(**router)
net_connect.enable()

# i. Configure interfaces with IP addresses
interface_commands = [
    'interface Loopback0',
    'ip address 10.0.0.1 255.255.255.255',
    'interface GigabitEthernet0/0',
    'ip address 192.168.56.101 255.255.255.0',
]

net_connect.send_config_set(interface_commands)

# ii. Configure OSPF
ospf_commands = [
    'router ospf 1',
    'network 10.0.0.0 0.255.255.255 area 0',
    'network 192.168.56.0 0.0.0.255 area 0',
]

net_connect.send_config_set(ospf_commands)

# iii. Configure ACLs
acl_commands = [
    'access-list 101 permit tcp host 192.168.56.101 any eq www',
    'access-list 101 permit ip any host 192.168.56.30',
    'interface GigabitEthernet0/0',
    'ip access-group 101 in',
    'ip access-group 101 out',
]

net_connect.send_config_set(acl_commands)

# iv. Configure IPSec
ipsec_commands = [
    'crypto isakmp policy 1',
    'encryption aes',
    'authentication pre-share',
    'group 2',
    'crypto isakmp key your_shared_key address 0.0.0.0',
    'crypto ipsec transform-set myset esp-aes esp-sha-hmac',
    'crypto map mymap 10 ipsec-isakmp',
    'set peer 192.168.56.30',
    'set transform-set myset',
    'match address 101',  # Use the ACL number defined in acl_commands
    'interface GigabitEthernet0/0',
    'crypto map mymap',
]

net_connect.send_config_set(ipsec_commands)

# Disconnect from the router
net_connect.disconnect()

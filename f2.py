from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException, NetmikoAuthenticationException

# Define the router details
router = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': 'cisco',
    'password': 'cisco123!',
}

try:
    # Connect to the router
    print("Connecting to the router...")
    net_connect = ConnectHandler(**router)
    net_connect.enable()
    print("Connection established!")

    # i. Configure Loopback and an additional interface with IP addresses
    interface_commands = [
        'interface Loopback0',
        'ip address 10.0.0.1 255.255.255.255',
        'interface GigabitEthernet0/1',
        'ip address 192.168.56.101 255.255.255.0',
    ]

    print("Configuring interfaces...")
    output = net_connect.send_config_set(interface_commands)
    print("Interfaces configured!")

    # ii. Configure OSPF
    ospf_commands = [
        'router ospf 1',
        'network 10.0.0.1 0.0.0.0 area 0',
        'network 192.168.56.0 0.0.0.255 area 0',
    ]

    print("Configuring OSPF...")
    output = net_connect.send_config_set(ospf_commands)
    print("OSPF configured!")

    # iii. Print Loopback configuration
    print("Configured Loopback0 with IP address 10.0.0.1/32")

    # Disconnect from the router
    print("Disconnecting from the router...")
    net_connect.disconnect()
    print("Disconnected!")

except NetmikoAuthenticationException as auth_error:
    print(f"Authentication failed: {auth_error}")

except NetmikoTimeoutException as timeout_error:
    print(f"Connection to device timed out: {timeout_error}")

except Exception as e:
    print(f"An error occurred: {str(e)}")

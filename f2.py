from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException, NetmikoAuthenticationException
import time

router = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': 'cisco',
    'password': 'cisco123!',
}

max_retries = 3  # Define the maximum number of connection retries
retry = 0

while retry < max_retries:
    try:
        print(f"Connection attempt {retry + 1}...")
        net_connect = ConnectHandler(**router)
        net_connect.enable()

        interface_commands = [
            'interface Loopback0',
            'ip address 10.0.0.1 255.255.255.255',
            'interface GigabitEthernet0/1',
            'ip address 192.168.56.101 255.255.255.0',
        ]
        print("Configuring interfaces...")
        net_connect.send_config_set(interface_commands)

        # Configure OSPF
        ospf_commands = [
            'router ospf 1',
            'network 10.0.0.1 0.0.0.0 area 0',
            'network 192.168.56.0 0.0.0.255 area 0',
        ]
        print("Configuring OSPF...")
        net_connect.send_config_set(ospf_commands)

        print("Configured Loopback0 with IP address 10.0.0.1/32")

        print("Disconnecting from the router...")
        net_connect.disconnect()
        print("Disconnected!")

        break  # Connection succeeded, exit loop

    except NetmikoAuthenticationException as auth_error:
        print(f"Authentication failed: {auth_error}")
        break  # Break the loop, as authentication issue won't resolve with retries

    except NetmikoTimeoutException as timeout_error:
        print(f"Attempt {retry + 1} timed out: {timeout_error}")
        retry += 1
        if retry == max_retries:
            print("Maximum retries exceeded. Script ending.")
        else:
            print("Retrying...")
            time.sleep(5)  # Wait for a while before retrying

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        break  # Break the loop for other unhandled exceptions

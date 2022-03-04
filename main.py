#!/user/bin/env python3

# importing relevant modules.
# subprocess helps to take and give cmd to shell via terminal.
import re
import subprocess
# optparse helps in parsing the data taken by making it a process.
import optparse


# To get the interface and the new MAC address from the user.
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    # Checks and handles the error if the user input is null
    if not options.interface:
        parser.error("[-] Please enter an interface, use '-i' or '--interface' | use '-h' or '--help' for more info.")
    elif not options.new_mac:
        parser.error("[-] Please enter an MAC address, use '-m' or '--mac' | use '-h' or '--help' for more info.")
    return options


# To change the MAC address.
def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + str(interface))
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def find_mac(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface], universal_newlines=True)
    mac_check = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig)
    mac = mac_check.group(0)
    if mac:
        return mac
    else:
        print("[-] Could not read MAC address")


option = get_arguments()
old_mac = find_mac(option.interface)
change_mac(option.interface, option.new_mac)
changed_mac = find_mac(option.interface)
print("[+] Current MAC address: " + str(old_mac))

if old_mac == changed_mac:
    print("[-] The MAC is same as before and therefore didn't change.")
elif changed_mac == option.new_mac:
    print("[+] Successfully changed the MAC address to " + str(changed_mac))

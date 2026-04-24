#!/usr/bin/env python3
"""
topo.py - Creates the Mininet network topology

TOPOLOGY:
    h1 (10.0.0.1) ─┐
    h2 (10.0.0.2) ──── s1 (switch) ──── POX Controller
    h3 (10.0.0.3) ─┘

WHY THIS TOPOLOGY:
    Simple 3-host single-switch topology is ideal for demonstrating
    SDN concepts clearly - blocking between specific hosts and QoS
    without unnecessary complexity.
"""

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def create_topology():
    """
    Creates and starts the network.
    RemoteController means Mininet will connect to our POX controller
    that is already running on port 6633.
    """

    info("*** Creating network\n")

    # Create the network object
    # RemoteController = our POX controller running separately
    # OVSSwitch = Open vSwitch (the virtual switch)
    net = Mininet(
        controller=RemoteController,
        switch=OVSSwitch,
        autoSetMacs=True    # Auto-assign MAC addresses
    )

    # Add the remote controller (POX running on localhost)
    info("*** Adding controller\n")
    c0 = net.addController(
        'c0',
        ip='127.0.0.1',   # localhost
        port=6633          # default OpenFlow port
    )

    # Add one switch
    info("*** Adding switch\n")
    s1 = net.addSwitch('s1')

    # Add 3 hosts with fixed IP addresses
    info("*** Adding hosts\n")
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')

    # Connect all hosts to the switch with virtual links
    info("*** Adding links\n")
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)

    # Start the network (boots everything up)
    info("*** Starting network\n")
    net.start()

    # Print useful info
    info("\n*** Network ready!\n")
    info("*** Hosts: h1=10.0.0.1, h2=10.0.0.2, h3=10.0.0.3\n")
    info("*** Try these commands:\n")
    info("    pingall          - test all connections\n")
    info("    h1 ping h2       - ping from h1 to h2\n")
    info("    h2 iperf -s &    - start iperf server on h2\n")
    info("    h1 iperf -c 10.0.0.2 - test speed\n")
    info("    h2 bash /home/$USER/qos_project/run_qos.sh - apply QoS\n")

    # Open interactive CLI so you can type commands
    CLI(net)

    # When you type 'exit' in CLI, this runs:
    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    # Set log level to info so we see what's happening
    setLogLevel('info')
    create_topology()

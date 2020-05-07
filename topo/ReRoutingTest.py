#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, Host
from mininet.cli import CLI
from mininet.link import TCLink, Intf
from mininet.log import setLogLevel, info
from subprocess import call
'''
h1---h2---h4
     |  /
     h3

'''

def myNetwork():

    net = Mininet(topo=None,
                       build=False,
                       ipBase='10.0.0.0/24')

    info( '*** Adding controller\n' )
    c0 = net.addController(name='c0',
                           controller=Controller,
                           protocol='tcp',
                           port=6633)

    info( '*** Add switches/APs\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)

    info( '*** Add hosts/stations\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(s1, h2)
    net.addLink(h2, s2)
    net.addLink(h2, s3)
    net.addLink(s2, h3)
    net.addLink(s3, h4)
    net.addLink(h3, s4)
    net.addLink(s4, h4)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches/APs\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])

    info( '*** Post configure nodes\n')

    h2.cmd("ifconfig h2-eth1 10.0.1.2/24")
    h2.cmd("ifconfig h2-eth2 10.0.2.2/24")
    h3.cmd("ifconfig h3-eth0 10.0.1.3/24")
    h3.cmd("ifconfig h3-eth1 10.0.3.3/24")
    h4.cmd("ifconfig h4-eth0 10.0.2.4/24")
    h4.cmd("ifconfig h4-eth1 10.0.3.4/24")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()


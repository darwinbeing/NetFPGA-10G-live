#!/usr/bin/python

from NFTest import *
import random
from RegressRouterLib import *

from reg_defines_reference_router import *


phy2loop0 = ('../connections/2phy', [])

nftest_init(sim_loop = [], hw_config = [phy2loop0])
nftest_start()

# asserting the reset_counter to 1 for clearing the registers
nftest_regwrite(XPAR_NF10_ROUTER_OUTPUT_PORT_LOOKUP_0_BAR0_RESET_CNTRS_OFFSET(), 0x1)

# asseting the reset_counter to 0 for enable the counters to increment
nftest_regwrite(XPAR_NF10_ROUTER_OUTPUT_PORT_LOOKUP_0_BAR0_RESET_CNTRS_OFFSET(), 0x0)


routerMAC = ["00:ca:fe:00:00:01", "00:ca:fe:00:00:02", "00:ca:fe:00:00:03", "00:ca:fe:00:00:04"]
routerIP = ["192.168.0.40", "192.168.1.40", "192.168.2.40", "192.168.3.40"]

# Clear all tables in a hardware test (not needed in software)
if isHW():
    nftest_invalidate_all_tables()

# Write the mac and IP addresses
for port in range(4):
    nftest_add_dst_ip_filter_entry (port, routerIP[port])
    nftest_set_router_MAC ('nf%d'%port, routerMAC[port])

# add an entry in the routing table:
subnetIP = ["192.168.2.0", "192.168.1.0"]
subnetMask = ["255.255.255.0", "255.255.255.0"]
nextHopIP = ["192.168.1.54", "192.168.3.12"]
outPort = [0x1, 0x4]
nextHopMAC = "dd:55:dd:66:dd:77"

for i in range(2):
    nftest_add_LPM_table_entry (i, subnetIP[i], subnetMask[i], nextHopIP[i], outPort[i])
    nftest_add_ARP_table_entry (i, nextHopIP[i], nextHopMAC)

#clear the num pkts forwarded reg
nftest_regwrite(XPAR_NF10_ROUTER_OUTPUT_PORT_LOOKUP_0_BAR0_PKT_FORWARDED_OFFSET(), 0)

nftest_barrier()

precreated = [[], []]
precreated_exp = [[], []]
# loop for 20 packets from eth1 to eth2
for port in range(2):
    for i in range(20):
        # set parameters
        DA = routerMAC[port]
        SA = "aa:bb:cc:dd:ee:ff"
        DST_IP = "192.168.%d.1"%(port + 1)
        SRC_IP = "192.168.0.1"
        length = 100
        nextHopMAC = "dd:55:dd:66:dd:77"

        sent_pkt = make_IP_pkt(dst_MAC=DA, src_MAC=SA, dst_IP=DST_IP,
                               src_IP=SRC_IP, pkt_len=length)
        exp_pkt = make_IP_pkt(dst_MAC=nextHopMAC, src_MAC=routerMAC[1 - port],
                              TTL = 63, dst_IP=DST_IP, src_IP=SRC_IP)
        exp_pkt[scapy.Raw].load = sent_pkt[scapy.Raw].load

        # send packet out of eth1->nf0
        nftest_send_phy('nf%d'%port, sent_pkt);
        nftest_expect_phy('nf%d'%(1-port), exp_pkt);

nftest_barrier()

rres1=nftest_regread_expect(XPAR_NF10_ROUTER_OUTPUT_PORT_LOOKUP_0_BAR0_PKT_FORWARDED_OFFSET(), 40);
mres=[rres1]
nftest_finish(mres)

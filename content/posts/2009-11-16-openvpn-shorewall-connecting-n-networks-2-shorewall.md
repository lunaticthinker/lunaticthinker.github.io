---
title: "OpenVPN / Shorewall – connecting N networks [#2 Shorewall]"
author: dragos
type: post
date: 2009-11-16T19:22:11+00:00
url: /openvpn-shorewall-connecting-n-networks-2-shorewall/
featured_image: /media/2010/12/openvpn.jpg
categories:
  - Linux in a Box
  - Linux Services
---

To continue my previous article about Virtual Networks, today its time to write the firewall configuration part, which, is a lot more simple than you have imagined.

**/etc/shorewal/interfaces**

###############################################################################

#ZONE   INTERFACE       BROADCAST       OPTIONS

net     eth1            detect          dhcp,tcpflags,routefilter,nosmurfs

loc     eth0            detect          tcpflags,detectnets,nosmurfs

loc    tun+            detect          –

**/etc/shorewall/rules**

#ACTION SOURCE          DEST            PROTO   DEST    SOURCE          ORIGINAL        RATE            USER/   MARK

#                                               PORT    PORT(S)         DEST            LIMIT           GROUP

#SECTION ESTABLISHED

#SECTION RELATED

ACCEPT          fw              net             udp     10000

ACCEPT          net             fw              udp     10000

ACCEPT          fw              loc             udp     10000

ACCEPT          loc             fw              udp     10000

\# PING

Ping/ACCEPT     loc             $FW

Ping/ACCEPT:warn:PING   loc:tun0        loc:eth1

Ping/ACCEPT     net             $FW

#LAST LINE — ADD YOUR ENTRIES BEFORE THIS ONE — DO NOT REMOVE

I did have to write a special rule for the PING port, but in rest everythig worked perfectly. Please note that this specific rule must be duplicated for each tun interface regarding to the interface it must redirect the messages.

The interface file mentions the third interface (for tunneling in this case) on which openVPN sends the messages.

The rules files enables the port used by openVPN (in this case 10000) and adds the ping rule mentioned above.

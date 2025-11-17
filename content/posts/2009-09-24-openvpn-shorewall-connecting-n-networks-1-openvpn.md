---
title: "OpenVPN / Shorewall – connecting N networks [#1 OpenVPN]"
author: dragos
type: post
date: 2009-09-24T11:43:25+00:00
url: /openvpn-shorewall-connecting-n-networks-1-openvpn/
featured_image: /media/2010/12/openvpn.jpg
categories:
  - Linux in a Box
  - Linux Services
---

OK… We all know what virtual private networks are… Problem for me was how to connect 3 separate networks located in 3 separate locations around my hometown into a one and only virtual private network. Heard about OpenVPN from a friend of mine and decided to give it a try.

To make a connect two networks into a virtual private network is easy… You just go on the client – server way of thinking and using the “[how to][1]” example from OpenVPN website, you can manage to do it pretty fast. If that”s hard… I”m sure you can find out, on <a title="Google Search" href="http://www.google.ro/search?q=openvpn+connect+networks" target="_blank" rel="noopener noreferrer">Google</a>, tons of tutorials where from to inspire yourself (here is [one][2] I liked).

When talking about connection more than two networks, the problem is a lot more complex. And the more the number of network grows, the more the problem is more complicated. Of course we can still use the server – client architecture, where you can connect dozens of clients to the server. Problem is, after connecting all the clients, the package routing between all those clumsy mad clients who may want or not to communicate between themselves.

Another option is… creating for N networks a set of N-1 VPNs, going again for the server – client architecture for each VPN. I”ll give here an example of 3 networks connected through 3 VPNs.

Let”s say that the servers of those 3 networks are **C1**, **C2** and **C3**. We will connect **C3** and **C2** to **C1** via **VPN1** and **C3** with **C2** via **VPN2** considering as vpn servers the C1 and C3 servers. The result will look smth like this:

VPN1 = ( C1 <–> C2 & C1 <–> C3) | VPN2 = ( C3 <–> C2 )

Further more I”ll name S1 and S3 the OpenVPN software servers and C12, C13, C32 the OpenVPN sofware clients. Connection the three networks via S1 in VPN1 it”s not enough because C3 will never be able to connect with C2. Thus, instead of routing all the C3 to C2 traffic through S1, we add another VPN network which will handle this connection.

In this way… for N networks we will have N-1 OpenVPN servers which will have each from 1 to N-1 clients ( S1 – 1 client -> Sn-1 -> N-1 clients), which is a sum of (N-1)(N-2)/2  OpenVPN clients.

I”m not saying this version is better than routing all the packages through a **unique** OpenVPN server, but for a small number of networks it may work better. Hell it should work a lot better if we have even 1000 networks to connect, but… there is always the problem of the resources… Even more… there is always a way to simplify the problem.

**3 Networks Example**

I will give now the config files for the 3 networks connection I made, leaving you space to study and modify upon what I did. The entire system was simulated on a virtual machine:

_Server/Network 1_ _([openvpn configs – 10.10.1.1][3])_ \_\_

External IP: 192.168.223.134

Internal IP/Network: 10.10.1.1/24

_Server/Network 2_ _([openvpn configs – 10.10.2.1][4])_

External IP: 192.168.223.133

Internal IP/Network: 10.10.2.1/24

_Server/Network 3_ _\_\_([openvpn configs – 10.10.3.1][5])_

External IP: 192.168.223.132

Internal IP/Network 10.10.3.1/24

**Note**

Please note that the routing problem cannot be solved only by OpenVPN software… This is only a part of the problem. The part above solves only the communication between the networks” servers. In order to be able to see the other networks from wherever inside one of your networks you will need some **iptables** rules. This can be done according to the “how to” example given by OpenVPN or using a firewall like **Shorewall**… But I will discuss the **Shorewall** part in another thread… and later…

\*\*

\*\*

[1]: http://openvpn.net/open-source/documentation/howto.html
[2]: https://forum.openwrt.org/viewtopic.php?id=12979 "OpenWRT forums / OpenVPN network"
[3]: http://dragosc.itmcd.ro/wp-content/uploads/2009/09/openvpn101011.tgz
[4]: http://dragosc.itmcd.ro/wp-content/uploads/2009/09/openvpn101021.tgz
[5]: http://dragosc.itmcd.ro/wp-content/uploads/2009/09/openvpn101031.tgz

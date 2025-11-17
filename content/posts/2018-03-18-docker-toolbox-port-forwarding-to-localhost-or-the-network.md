---
title: Docker Toolbox port forwarding to localhost or the network
author: dragos
date: 2018-03-18T00:28:08+00:00
url: /docker-toolbox-port-forwarding-to-localhost-or-the-network/
featured_image: /media/2018/03/docker-banner2.jpg
eltd_hide_background_image_meta:
  - no
eltd_video_type_meta:
  - social
eltd_disable_footer_meta:
  - no
eltd_featured_post_meta:
  - no
categories:
  - "Coder's Grave"
  - Home Page
  - Linux in a Box
  - Linux Services
  - Other OSs
tags:
  - docker
  - docker toolbox
  - windows home
---

For a long time we avoided using [Docker Toolkbox][1] because we didn’t understand how to allow the containers created within the docker Virtual Box machine by using local host and not the virtual machine’s ip (usually 192.168.99.100).

 

This recently changed when one of my employees was forced to work for a while from within a client’s network, and even more, work under Windows while the application was to be accessed under network designated domains only. Long story short, the application had to be run on docker, however accessed on a domain like ‘myapp.domain.foo’, which also made it accessible not only to my developer as well as the rest of the group.

This can be easily achieved under Windows Pro hence HyperV and [Docker for Windows][2] tool have a different setup which allow us to use the container port publish under ‘localhost’ directly. So I had my doubts again whether to upgrade his OS or not.

 

I think it is obvious that we were not the only ones confronting with this problem, and hence we first encountered this issue the docker community evolved. So back to Google again, where we found a [post][3] by [Dmytro Nemoga][4] mentioning about a command named **netsh** which could port redirect localhost or any other network interface from the computer to the network interface used by the Docker virtual machine.

 

So here it comes, part one of the solution. Using **Windows Powershell** or the old **cmd**, you can port forward your localhost port to the ip of the virtual machine.

    netsh interface portproxy add v4tov4 listenaddress=127.0.0.1 listenport=80 connectaddress=192.168.99.100 connectport=80

List all forwards:

    netsh interface portproxy show v4tov4

And delete the ones you don’t need anymore:

    netsh interface portproxy delete v4tov4 listenaddress=127.0.0.1 listenport=80

But, as explained, this is not all. For **localhost** works like a charm, however, if you wish to make the docker container accessible from within the network, Windows Operating System will give you yet another pain in the back.

First of all, you will need to make a port redirect not from localhost, but from your external network interface. So, find out what IP you are using in that specific network, make sure that it is static or the router remembers the IP it allocated you and use the rule above (replace YOUR_NETWORK_IP with your network IP, duh!):

    netsh interface portproxy add v4tov4 listenaddress=YOUR_NETWORK_IP listenport=80 connectaddress=192.168.99.100 connectport=80

Second of all, most Windows OSs are not accessible for ping anymore, so you will need to launch the **Windows Defender Firewall with Advanced Security** tool and, for **Inbound Rules** activate the **File and Printer Sharing (Echo Request ICMPv4-in)** option.

And third of all, you will need to add a new inbound rule, enabling the ports you need to make public. For that,

- select the **New Rule…** option,
- then in the new window select **Port** _(Rule that controls connections for a TCP or UDP port)_,
- then select port type: **TCP/UDP** and mention the ports you want to publish; like 8**0, 8080, 3000** or any other port you need,
- then select **Allow the Connection** _(This includes connections that are protected with IPsec_ as well as those _are not)_,
- then, in the next tab (Profile) leave everything selected,
- and in the last tab mention a rule name, i.e. **CUSTOM RULE HTTP** and a description for the rule.

This will allow you to access the container not only from localhost but from the network you’re connected to as well.

 

Well… that’s all folks. Hope this will help you 🙂

[1]: https://docs.docker.com/toolbox/toolbox_install_windows/
[2]: https://docs.docker.com/docker-for-windows/install/
[3]: https://github.com/moby/moby/issues/15740#issuecomment-200409378
[4]: https://github.com/dnemoga

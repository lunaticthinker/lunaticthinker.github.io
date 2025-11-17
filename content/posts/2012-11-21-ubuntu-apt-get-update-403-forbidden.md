---
title: Ubuntu apt-get update 403 Forbidden
author: dragos
type: post
date: 2012-11-21T09:44:34+00:00
url: /ubuntu-apt-get-update-403-forbidden/
featured_image: /media/2012/11/ubuntu-blue-1440x900.jpg
categories:
  - Linux in a Box
---

After running apt-get update, today I obtained a lot of 403 errors in the command log.

<pre class="prettyprint">W: Failed to fetch http://ro.archive.ubuntu.com/ubuntu/dists/precise-backports/restricted/binary-amd64/Packages  403  Forbidden
W: Failed to fetch http://ro.archive.ubuntu.com/ubuntu/dists/precise-backports/universe/binary-amd64/Packages  403  Forbidden
W: Failed to fetch http://ro.archive.ubuntu.com/ubuntu/dists/precise-backports/multiverse/binary-amd64/Packages  403  Forbidden
W: Failed to fetch http://ro.archive.ubuntu.com/ubuntu/dists/precise-backports/main/binary-i386/Packages  403  Forbidden
W: Failed to fetch http://ro.archive.ubuntu.com/ubuntu/dists/precise-backports/restricted/binary-i386/Packages  403  Forbidden
W: Failed to fetch http://ro.archive.ubuntu.com/ubuntu/dists/precise-backports/universe/binary-i386/Packages  403  Forbidden
W: Failed to fetch http://ro.archive.ubuntu.com/ubuntu/dists/precise-backports/multiverse/binary-i386/Packages  403  Forbidden</pre>

Lucky me, one of my friends got this before me and already had the fix.

<pre class="prettyprint">sudo apt-cache clean
sudo apt-get clean
cd /var/lib/apt
sudo rm -Rf lists.old/lists
sudo mv lists lists.old
sudo mkdir -p lists/partial
sudo apt-get clean
sudo apt-get update
sudo apt-get upgrade</pre>

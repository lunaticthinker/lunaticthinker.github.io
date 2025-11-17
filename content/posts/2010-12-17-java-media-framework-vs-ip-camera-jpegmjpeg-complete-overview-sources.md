---
title: Java Media Framework vs IP Camera JPEG/MJPEG – reviewed
author: dragos
type: post
date: 2010-12-17T11:00:43+00:00
url: /java-media-framework-vs-ip-camera-jpegmjpeg-complete-overview-sources/
featured_image: /media/2010/12/Java_logo-5.jpg
categories:
  - "Coder's Grave"
  - Home Page
  - Java
---

**NOTE:**

- I will try not to re-write again all the informations I already wrote in “<a href="http://dragosc.itmcd.ro/it-stuff/java-media-framework-vs-ip-camera-jpegmjpeg/" target="_blank" rel="noopener noreferrer">Java Media Framwork vs IP Camera JPEG/MJPEG</a>” a few years ago. This article is only a review of what I wrote back then, plus more info about my implementation of DataSource for JPEG/MJPEG IP Cameras.
- Another note is, that this project of mine, has been attached to my own company which I founded a few years ago and I’m still trying to grow it. Project licence will be LGPL.

OK… Since Oracle bought SUN a few years ago, but their website still doesn’t reflect all info about Java Media Framework, it’s still best do <a href="http://www.google.ro/search?aq=f&sourceid=chrome&ie=UTF-8&q=java+media+framework" target="_blank" rel="noopener noreferrer">Google</a> after the info about JMF, than give you a specific link.

The article that belongs to [Chris Adamson][1], <a href="http://www.onjava.com/pub/a/onjava/2002/12/23/jmf.html" target="_blank" rel="noopener noreferrer">Java Media Development with QuickTime for Java</a>, still exists and, believe me it’s pretty useful. It explains how to create a new JMF plugin using the Java lib for Quick Time, released by Apple. Only wish I had access to them, but that’s another problem.

Even though at first I kinda disliked working with JMF due to it’s huge lack of documentation (some would say, it has such thing, I would say: NO), I discovered in time that it’s not that complicated. The principles are pretty simple, and even though the library hasn’t seen another update since 2001, its extendability is pretty high. We’ve already seen a plugin from mr. Adamson for qt-java, and from what I’ve known there are other plugins there on the web.

The main idea in Chris Adamson’s article is to create two classes, one to extend **DataSource** and one to extend **PushBufferStream** or **PullBufferStream** from JMF.

The _DataSource_ class is needed by JMF Players to read the info you need to display, while the _BufferStream_ is actually the reader of the “video” stream.

In our case, we can say the _BufferStream_ class is a bit more complicated, but as we look closer it is not. We do have to check two cases though.

1. Cameras that do have a fully MJPEG stream.
2. Cameras that only have JPEG ‘streams’. In this case, it’s not a real stream actually, and we have to simulate one by re-reading the source in a loop.

The only problem we couldn’t solve in a nice manner was creating a handler class, so we sticked to this:

<pre class="prettyprint">package org.itmc.ipcamera.media.content.unknown;

public class Handler extends com.sun.media.content.unknown.Handler
{}</pre>

If you download the sources, you’ll discover that each class has a static function for testing, also including an example for how to use it.

You can download the latest sources from:

[http://svn.itmcd.ro/trunk/jmf/ipcamera][2]

user & pass: anonymous

We’re looking for help to improve our code, and make from “ipcamera” an API worth to use for all types of streaming used by ip cameras, so if you think you’re smart enough and want to help, or if you used this API in your application and want to share with us some of your code, please contact us. Leave us a comment to this post, and we will contact u ASAP. (The comment will not be published unless you request so.)

Also, if you think our code has helped you, please try and donate us a few coins. This is free LGPL work, but in order to continue our research, we do need some funds there.

[paypal-donation]

[1]: http://www.onjava.com/pub/au/1045
[2]: http://svn.itmcd.ro/trunk/jmf/ipcamera/

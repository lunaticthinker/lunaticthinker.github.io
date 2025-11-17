---
title: Railo / ColdFusion – Writing Image to Outpout Stream
author: dragos
type: post
date: 2014-06-03T10:37:35+00:00
url: /railo-coldfusion-writing-image-to-outpout-stream/
featured_image: /media/2015/11/dna-structure.jpg
categories:
  - "Coder's Grave"
  - ColdFusion
  - Home Page
---

Hello guys,

Needed to do this for a project my team is maintaining, but I could only find the solution for ColdFusion, which looks like this:

<pre class="prettyprint">JavaImport = structNew();

JavaImport.io = structNew();
JavaImport.io.File = CreateObject('java', 'java.io.File');

JavaxImport = StructNew();

JavaxImport.imageio = StructNew();
JavaxImport.imageio.ImageIO = CreateObject('java', 'javax.imageio.ImageIO');

imageBuffer = JavaxImport.imageio.ImageIO.read(JavaImport.io.File.Init(imagePath));

response = getPageContext().getFusionContext().getResponse();
response.setHeader('Content-Type', 'image/png');
response.setHeader('Cache-Control', 'max-age=604800, public');
JavaxImport.imageio.ImageIO.write(imageBuffer, "png", response.getResponse().getOutputStream() );</pre>

After consulting Railo documentation on [GetPageContext][1] method, we’ve come to the following result:

<pre class="prettyprint">JavaImport = structNew();

JavaImport.io = structNew();
JavaImport.io.File = CreateObject('java', 'java.io.File');

JavaxImport = StructNew();

JavaxImport.imageio = StructNew();
JavaxImport.imageio.ImageIO = CreateObject('java', 'javax.imageio.ImageIO');

imageBuffer = JavaxImport.imageio.ImageIO.read(JavaImport.io.File.Init(imagePath));

response = getPageContext();
response.setHeader('Content-Type', 'image/png');
response.setHeader('Cache-Control', 'max-age=604800, public');
JavaxImport.imageio.ImageIO.write(imageBuffer, "png", response.getResponseStream() );</pre>

How it will be useful to you as well.

[1]: http://www.getrailo.org/javadoc-4-0/railo/runtime/functions/other/GetPageContext.html

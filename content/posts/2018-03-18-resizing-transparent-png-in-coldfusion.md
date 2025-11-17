---
title: Resizing Transparent PNG in ColdFusion
author: dragos
type: post
date: 2018-03-18T01:03:15+00:00
url: /resizing-transparent-png-in-coldfusion/
featured_image: /media/2014/03/dna-structure-cfml.png
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
  - ColdFusion
  - Home Page
---

Hello guys,

Needed to do this for a project my team is maintaining, but I could only find the solution for ColdFusion, which looks like this:

    JavaImport = structNew();

    JavaImport.io = structNew();
    JavaImport.io.File = CreateObject('java', 'java.io.File');

    JavaxImport = StructNew();

    JavaxImport.imageio = StructNew();
    JavaxImport.imageio.ImageIO = CreateObject('java', 'javax.imageio.ImageIO');

    imageBuffer = JavaxImport.imageio.ImageIO.read(JavaImport.io.File.Init(imagePath));

    response = getPageContext().getFusionContext().getResponse();
    response.setHeader('Content-Type', 'image/png');
    response.setHeader('Cache-Control', 'max-age=604800, public');
    JavaxImport.imageio.ImageIO.write(imageBuffer, "png", response.getResponse().getOutputStream() );

After consulting Railo documentation on [GetPageContext][1] method, we’ve come to the following result:

    JavaImport = structNew();

    JavaImport.io = structNew();
    JavaImport.io.File = CreateObject('java', 'java.io.File');

    JavaxImport = StructNew();

    JavaxImport.imageio = StructNew();
    JavaxImport.imageio.ImageIO = CreateObject('java', 'javax.imageio.ImageIO');

    imageBuffer = JavaxImport.imageio.ImageIO.read(JavaImport.io.File.Init(imagePath));

    response = getPageContext();
    response.setHeader('Content-Type', 'image/png');
    response.setHeader('Cache-Control', 'max-age=604800, public');
    JavaxImport.imageio.ImageIO.write(imageBuffer, "png", response.getResponseStream() );

How it will be useful to you as well.

[1]: http://www.getrailo.org/javadoc-4-0/railo/runtime/functions/other/GetPageContext.html

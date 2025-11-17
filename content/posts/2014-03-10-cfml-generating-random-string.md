---
title: CFML Generating Random String
author: dragos
date: 2014-03-10T10:27:40+00:00
url: /cfml-generating-random-string/
featured_image: /media/2014/03/dna-structure-cfml.png
categories:
  - "Coder's Grave"
  - ColdFusion
  - Home Page
---

While working on one of my client’s projects, I’ve encountered the need of generating RANDOM strings. Since, as almost, any other language, Cold Fusion does not have any type of support for this functionality, I had to create a function of my own.

Hope you find it useful.

<pre class="prettyprint"><cfscript>
    function RandomString(length, chars="ABCDEFGHIJKLMNOPQRST0123456789-") {
        var i = 0;
        var theString = "";
        for (i = 0; i < length; i++) {
            theString &= Mid(chars, RandRange(1, len(chars), "SHA1PRNG"), 1);
        }
        return theString;
    }
</cfscript></pre>

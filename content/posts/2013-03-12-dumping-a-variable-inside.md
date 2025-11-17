---
title: Dumping object inside cfscript tag
author: dragos
type: post
date: 2013-03-12T10:35:03+00:00
url: /dumping-a-variable-inside/
featured_image: /media/2014/03/dna-structure-cfml.png
categories:
  - "Coder's Grave"
  - ColdFusion
  - Home Page
---

I’ve been looking for this a few times now, until now i’ve found two interesting options.

One is creating a cffunction of your own, and using it inside a cfscript afterwards:

<pre class="prettyprint"><CFFUNCTION NAME="MyDump">
    <CFARGUMENT NAME="OBJ" Required="TRUE">
    <CFDUMP VAR="#Obj#">
</CFFUNCTION></pre>

The other one is using a 100% cfscript approach, which can also be placed in a function of your own:

<pre class="prettyprint">createObject("component", "cfide.adminapi.base").dump(var);</pre>

Also, starting ColdFusion 9, you can use the **writeDump** function.

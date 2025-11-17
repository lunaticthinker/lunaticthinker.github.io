---
title: 3DES Encryption with PHP
author: dragos
type: post
date: 2015-11-25T14:21:37+00:00
url: /3des-encryption-with-php/
featured_image: /media/2015/11/dna-structure.jpg
categories:
  - Uncategorized
tags:
  - 3des
  - php
---

An if I started with 3DES encryption, I thought… why stop?

Here is the PHP Version as well.

<pre class="lang:php decode:true " title="3DES Encryption with PHP" >function encrypt3DES($key,$iv,$text_enc){
     $block = mcrypt_get_block_size('tripledes', 'cbc');
     $pad = $block - (strlen($text_enc) % $block);
     $text_enc .= str_repeat(chr($pad), $pad);
     $text_enc = mcrypt_encrypt(MCRYPT_3DES, $key, $text_enc, MCRYPT_MODE_CBC, $iv);
     $text_enc = base64_encode ($text_enc);
     return $text_enc;
 }
 
 echo "\n";
 
 echo encrypt3DES("62v01fVsCWHfRcW\0\0\0\0\0\0\0\0\0", "\0\0\0\0\0\0\0\0", "66866996699") . "\n";</pre>

---
title: 3DES Encryption with CFSCRIPT
author: dragos
type: post
date: 2015-11-25T13:26:40+00:00
url: /3des-encryption-with-cfscript/
featured_image: /media/2014/03/dna-structure-cfml.png
categories:
  - "Coder's Grave"
  - ColdFusion
  - Home Page
---

Won’t comment much about it. We needed it, you may need it, so here it is:

<pre class="lang:cfml decode:true " ><cfscript>

    key = '62v01fVsCWHfRcW';
    text = '66866996699';
    iv = BinaryDecode("0000000000000000","hex");

    function extendKey(key, size = 24, c = "0") {
        var i = 0;
        for (i = len(key); i lt size; i = i + 1) {
            key = key & c;
        }
        return key;
    }
    
    function extendText(text, c = "0") {
        var i = 0;
        for (i = len(text) % 8; i lt 8; i = i + 1) {
            text = text & c;
        }
        return text;
    }
    
    function encrypt3desCbcCF(text, key, iv) {
        return encrypt(
            text, 
            toBase64(extendKey(key, 24, urlDecode('%00'))), 
            'DESEDE/CBC/PKCS5Padding', 
            'Base64', 
            iv
        );
    }
    
    function javaCreateObject(obj) {
        return createObject('java', obj);
    }
    
    function encrypt3desCbcJava(text, key, iv) {
        var Cipher          = javaCreateObject('javax.crypto.Cipher');
        var IvParameterSpec = javaCreateObject('javax.crypto.spec.IvParameterSpec');
        var SecretKeySpec   = javaCreateObject('javax.crypto.spec.SecretKeySpec');
    
        var jkey = SecretKeySpec.init(
            extendKey(key, 24, urlDecode('%00')).getBytes(), 
            "DESede"
        );

        var jiv = IvParameterSpec.init(iv);

        var jcipher = Cipher.getInstance("DESede/CBC/PKCS5Padding");
        jcipher.init(Cipher.ENCRYPT_MODE, jkey, jiv);
        
            
        return toBase64(jcipher.doFinal(
            text.getBytes()
        ));
    }

</cfscript>

<cfdump var="#extendKey(key, 24, 'A')#" /><br />
<cfdump var="#extendText(text, 'A')#" /><br />
<cfdump var="#encrypt3desCbcCF(text, key, iv)#" /><br />
<cfdump var="#encrypt3desCbcJava(text, key, iv)#" /><br /></pre>

Check also as an example here [on trycf.com][1]

[1]: http://trycf.com/gist/6c6d9bad3c4ae2838137/acf11?theme=monokai

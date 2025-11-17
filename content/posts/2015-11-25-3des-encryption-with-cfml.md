---
title: 3DES Encryption with CFML
author: dragos
type: post
date: 2015-11-25T14:13:21+00:00
url: /3des-encryption-with-cfml/
featured_image: /media/2014/03/dna-structure-cfml.png
categories:
  - Uncategorized
tags:
  - 3des
  - cf
  - cfml
  - coldfusion
---

Here’s a CFML version for the 3DES [encription script][1] I presented earlier (CFScript only).

<pre class="lang:cfml decode:true " ><cffunction access="public" name="prepare3DESKey" returntype="string" output="false" hint="Prepare 3DES key for encryption.">
	<cfargument name="key" type="string" default="" />
	<cfif len(key) eq 0>
		<cfset key = generateSecretKey('DESEDE') />
	<cfelse>
		<!--- if key is lower than 24 bytes; fill the empty bytes with NULL --->
		<cfloop from="#len(key)#" to="23" index="i">
			

<!--- do NOT use chr(0). in CF it does not work --->
			<cfset key = key & urlDecode('%00') />
		</cfloop>
	</cfif>
	<cfreturn key />
</cffunction>

<cfset key="#prepare3DESKey('62v01fVsCWHfRcW')#" />
<cfdump var="#len(key)#" />
<cfdump var="#key#" />

<cffunction access="public" name="encrypt3DESCBC" returntype="string" output="false" hint="Encrypts a string based on a given key and initialization vector, using CF methods.">
	<cfargument name="encrypting" type="string" required="true" />
	<cfargument name="key"        type="string" default="" />
	<cfargument name="iv"         type="string" default="0000000000000000" />

	<cfreturn encrypt(
		encrypting,
		toBase64(prepare3DESKey(key)),
		'DESEDE/CBC/PKCS5Padding', 
        'Base64', 
        BinaryDecode(iv, 'Hex')
	) />
</cffunction>

<cffunction access="public" name="encrypt3DESCBC_Java" returntype="string" output="false" hint="Encrypts a string based on a given key and initialization vector, using Java functionality.">
	<cfargument name="encrypting" type="string" required="true" />
	<cfargument name="key"        type="string" default="" />
	<cfargument name="iv"         type="string" default="0000000000000000" />
	
	<cfset iv = BinaryDecode(iv, 'Hex') />

	<cfset Cipher          = createObject('java', 'javax.crypto.Cipher') />
	<cfset jcipher = Cipher.getInstance("DESede/CBC/PKCS5Padding") />
	
    <cfset IvParameterSpec = createObject('java', 'javax.crypto.spec.IvParameterSpec') />
    <cfset jiv = IvParameterSpec.init(iv) />
    
    <cfset SecretKeySpec   = createObject('java', 'javax.crypto.spec.SecretKeySpec') />
    <cfset jkey = SecretKeySpec.init(
        prepare3DESKey(key).getBytes(), 
        "DESede"
    ) />

    <cfset jcipher.init(Cipher.ENCRYPT_MODE, jkey, jiv) />
                
    <cfreturn toBase64(jcipher.doFinal(
        encrypting.getBytes()
    )) />
    
    <cfreturn "test" />
</cffunction>

<cfdump var="#encrypt3DESCBC('66866996699', '62v01fVsCWHfRcW')#" /></pre>

And here’s a test script [on trycf.com][2] also.

[1]: /coders-grave/web-develop/coldfusion/3des-encryption-with-cfscript/
[2]: http://trycf.com/gist/36a929d67b1a95897667/acf11?theme=monokai

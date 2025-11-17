---
title: Cross Programming Language Encryption – CSharp, Part 1
author: dragos
date: 2020-05-05T08:04:07+00:00
url: /cross-programming-language-encryption-csharp-part-1/
featured_image: /media/2020/05/dna-structure-csharp.jpg
eltd_featured_post_meta:
  - no
eltd_disable_footer_meta:
  - no
eltd_video_type_meta:
  - social
eltd_hide_background_image_meta:
  - no
categories:
  - "Coder's Grave"
  - Home Page
---

[![GitHub stars][1]][2] [![GitHub followers][3]][4]  
See a demo at [Github][2]

---

One of our challenges at work, lately, was to send encrypted messages between multiple applications, written in different programming languages: [C#][5], [Go][6] and [JavaScript][7]{.aioseop-link}.

In our case, it was more like [TypeScript][8]{.aioseop-link}, but from this point of view, it is safe to talk about JavaScript from two simple reasons:

- TypeScript compiles to JavaScript
- The library used for cryptography was written with JavaScript.

Our team debated between two encryption algorithms for this job: AES and RSA.

### AES

_The _**_Advanced Encryption Standard_**_ (_**_AES_**_), also known by its original name _**_Rijndael_**_ (Dutch pronunciation: _[_[ˈrɛindaːl]_][9]_), is a specification for the _[_encryption_][10]_ of electronic data established by the U.S. _[_National Institute of Standards and Technology_][11]_ (NIST) in 2001._

_AES is a subset of the Rijndael _[_block cipher_][12]_ developed by two _[_Belgian_][13]_ cryptographers, _[_Vincent Rijmen_][14]_ and _[_Joan Daemen_][15]_, who submitted a proposal_<sup><a href="https://en.wikipedia.org/wiki/Advanced_Encryption_Standard#cite_note-Rijndaelv2-7"><em>[5]</em></a></sup>_ to NIST during the _[_AES selection process_][16]_._<sup><a href="https://en.wikipedia.org/wiki/Advanced_Encryption_Standard#cite_note-8"><em>[6]</em></a></sup>_ Rijndael is a family of ciphers with different key and block sizes._

_For AES, NIST selected three members of the Rijndael family, each with a block size of 128 bits, but three different key lengths: 128, 192 and 256 bits._

_AES has been adopted by the _[_U.S. government_][17]_ and is now used worldwide. It supersedes the _[_Data Encryption Standard_][18]_ (DES), which was published in 1977. The algorithm described by AES is a _[_symmetric-key algorithm_][19]_, meaning the same key is used for both encrypting and decrypting the data._

### RSA

**_RSA_**_ (_**_Rivest–Shamir–Adleman_**_) is one of the first _[_public-key cryptosystems_][20]_ and is widely used for secure data transmission. In such a _[_cryptosystem_][21]_, the _[_encryption key_][22]_ is public and distinct from the _[_decryption key_][23]_ which is kept secret (private). In RSA, this asymmetry is based on the practical difficulty of _[_factoring_][24]_ the product of two large _[_prime numbers_][25]_, the “_[_factoring problem_][26]_“. The _[_acronym_][27]_ RSA is the initial letters of the surnames of _[_Ron Rivest_][28]_, _[_Adi Shamir_][29]_, and _[_Leonard Adleman_][30]_, who publicly described the algorithm in 1977. _[_Clifford Cocks_][31]_, an English mathematician working for the British intelligence agency _[_Government Communications Headquarters_][32]_ (GCHQ), had developed an equivalent system in 1973, which was not _[_declassified_][33]_ until 1997._

_A user of RSA creates and then publishes a public key based on two large _[_prime numbers_][25]_, along with an auxiliary value. The prime numbers must be kept secret. Anyone can use the public key to encrypt a message, but only someone with knowledge of the prime numbers can decode the message. Breaking RSA _[_encryption_][10]_ is known as the _[_RSA problem_][34]_. Whether it is as difficult as the _[_factoring problem_][26]_ is an open question. There are no published methods to defeat the system if a large enough key is used._

_RSA is a relatively slow algorithm, and because of this, it is less commonly used to directly encrypt user data. More often, RSA passes encrypted shared keys for _[_symmetric key_][19]_ cryptography which in turn can perform bulk encryption-decryption operations at much higher speed._

### Coding AES With C#

Please note that AES has three different key lengths: 128, 192 and 256 bits, which I have tried to simplify here by using as key a **Hash** string who’s length can only be 16, 24 or 32 bytes.

In C#, the AES class is represented through the [System.Security.Cryptography.Rijandel][35]{.aioseop-link} class, however I chose to use the [Managed][36]{.aioseop-link} class.

As we’ve already read, AES will require key of 128, 192 or 256 bits, which translated into 16, 24 or 32 bytes and an Initialization Vector (IV) of 16 bytes.

For my demo, I have chosen to define a class receiving a **Hash** parameter, which will later become our **Key**, while our **IV** will be randomly generated.

<pre class="wp-block-code"><code lang="csharp" class="language-csharp">using System.Security.Cryptography;
using System.Collections.Generic;

class AesEncrypt
{

  private RijndaelManaged aes;

  public AesEncrypt(String Hash)
  {

    if (Hash.Length != 16 && Hash.Length != 24 && Hash.Length != 32)
    {
      throw new Exception("Invalid hash length. Must be 16, 24 or 32.");
    }

    aes = new RijndaelManaged();
    aes.KeySize = Hash.Length * 8;
    aes.Mode = CipherMode.CFB;
    aes.Padding = PaddingMode.None;</code></pre>

One of the things you will need to check and make sure it is supported by each language will be the [Block Cipher Mode][37]{.aioseop-link}. Another one will be the [Padding][38]{.aioseop-link} hence, as you will find out, some Cipher modes do require certain padding values.

<pre class="wp-block-code"><code lang="csharp" class="language-csharp">    aes.Key = Encoding.UTF8.GetBytes(Hash);
    aes.GenerateIV();
  }</code></pre>

Since our IV is randomly generated, when encrypting our content, we will have to send the IV as well. Otherwise, the other party will be missing a part of the decryption information. A common thing would be to concatenate our IV in front or at the end of the encrypted content.

<pre class="wp-block-code"><code lang="csharp" class="language-csharp">  /**
   * Encrypt will encrypt a string password using AES algorithm, returning a Base64 for of the encrypt result
   */
  public string Encrypt(String password)
  {
    byte[] data = Encoding.UTF8.GetBytes(password);

    using (var encryptor = this.aes.CreateEncryptor())
    using (var msEncrypt = new MemoryStream())
    using (var csEncrypt = new CryptoStream(msEncrypt, encryptor, CryptoStreamMode.Write))
    using (var bw = new BinaryWriter(csEncrypt, Encoding.UTF8))
    {
      bw.Write(data);
      bw.Close();

      List<byte> list = new List<byte>();
      list.AddRange(this.aes.IV);
      list.AddRange(msEncrypt.ToArray());</code></pre>

Another common practice is to encode everything in an easy to read, easy to transmit mode, to prevent wrong data conversions. The easiest way to do this is to convert our encrypted result to Base64.

<pre class="wp-block-code"><code lang="csharp" class="language-csharp">      return Convert.ToBase64String(list.ToArray());
    }
  }</code></pre>

Now, the decryption part will have to handle the things, in the opposite way. When encrypted, we have 1st initialized our Rijandel class using our Key and IV, encrypted our content then appended our IV and nevertheless encoded our result in an easy to transmit way by using Base64.

When decrypting, we will first need to decode our data from Base64, then separate our IV and encrypted content.

<pre class="wp-block-code"><code lang="csharp" class="language-csharp">  /**
   * Decrypt will decrypt a string password using AES algorithm, expecting a Base64 form of the encrypted password
   */
  public String Decrypt(String ciphertext)
  {
    byte[] data = Convert.FromBase64String(ciphertext);

    Array.Copy(data, 0, this.aes.IV, 0, 16);

    byte[] cryptedData = new byte[data.Length - 16];
    Array.Copy(data, 16, cryptedData, 0, data.Length - 16);</code></pre>

When this is done, we will have all the elements needed to decrypt our content. Please keep in mind the Key will be known for both parties, being used to both encrypt and decrypt the content, while the IV is transported along with the encrypted content.

<pre class="wp-block-code"><code lang="csharp" class="language-csharp">    using (var decrytpor = this.aes.CreateDecryptor())
    using (var msEncrypt = new MemoryStream())
    using (var csEncrypt = new CryptoStream(msEncrypt, decrytpor, CryptoStreamMode.Write))
    using (var bw = new BinaryWriter(csEncrypt, Encoding.UTF8))
    {
      bw.Write(cryptedData);
      bw.Close();

      return Encoding.UTF8.GetString(msEncrypt.ToArray());
    }
  }
}</code></pre>

Nevertheless, in the end, we should be able to obtain the same content we have encrypted.

### Coding RSA With C#

Using RSA, as we will see, is a bit less complicated, however, RSA will require generating a certificate, which can be easily done using the [OpenSSL][39]{.aioseop-link} set of tools.

<pre class="wp-block-code"><code lang="bash" class="language-bash">openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem
openssl pkcs12 -export -out cert.pfx -inkey key.pem -in cert.pem</code></pre>

In order to be to use RSA encryption, we will be using the [System.Security.Cryptography.X509Certificates.X509Certificate2][40]{.aioseop-link} class, which will allow us to load our generated certificate, and used it for both encryption and decryption.

<pre class="wp-block-code"><code lang="csharp" class="language-csharp">using System.Security.Cryptography.X509Certificates;
using System.Security.Cryptography;

class RsaEncrypt
{

  private X509Certificate2 Cert;

  public RsaEncrypt(String CertPath)
  {
    Cert = new X509Certificate2(CertPath);
  }

  /**
   * Encrypt will encrypt a string password using an SSL certificate, returning a Base64 for of the encrypt result
   */
  public String Encrypt(String Password)
  {
    using (RSA Rsa = Cert.GetRSAPublicKey())
    {
      byte[] PasswordBytes = Encoding.Default.GetBytes(Password);
      byte[] EncryptedPassword = Rsa.Encrypt(PasswordBytes, RSAEncryptionPadding.OaepSHA512);

      return Convert.ToBase64String(EncryptedPassword);
    }
  }

  /**
   * Decrypt will decrypt a string password using an SSL certificate, expecting a Base64 form of the encrypted password
   */
  public String Decrypt(String Password)
  {
    using (RSA Rsa = Cert.GetRSAPrivateKey())
    {
      byte[] PasswordBytes = Convert.FromBase64String(Password);
      byte[] DecryptedPassword = Rsa.Decrypt(PasswordBytes, RSAEncryptionPadding.OaepSHA512);

      return Encoding.Default.GetString(DecryptedPassword);
    }
  }

}</code></pre>

### Conclusion

Of course one of the wonders we had, was which encryption algorithm is more powerful. The answer to this question is **both and none**. It depends a lot on the design of your application and the purpose of the encryption.

RSA and AES are algorithms of two different cryptographic types. Former is a public key algorithm while later is a symmetric key algorithm. The encryption and decryption keys of RSA are different while that of AES are same. Hence AES key has to be shared between the parties securely before encryption.

Given Alice and Bob, RSA can be used by Alice and Bob even if they have never met before but Bob’s authentic public key is available to Alice. Alice uses Bob’s public key to encrypt a message. Bob uses his private key to decrypt the message. Only Bob can decrypt and no other person amounts to confidentiality without having exchanged a key.

What we can definitely tell you and recommend is: RSA is more computationally intensive than AES, and much slower. It’s normally used to encrypt only small amounts of data.

As for our problem of **Cross Programming Language Encryption**, I have only presented **C#** so far. Stay tuned.

### References

- [Wikipedia / RSA\_(cryptosystem)][41]{.aioseop-link}
- [Wikipedia / Advanced Encryption Standard][42]{.aioseop-link}
- [Wikipedia / Block Cipher Mode][37]{.aioseop-link}
- [Encryption – should I be using RSA or AES?][43]{.aioseop-link}
- [AES vs RSA – Which is stronger given two scenarios?][44]
- [AES vs. RSA to encrypt large size of data][45]
- [MSDN / System.Security.Cryptography Namespace][46]{.aioseop-link}
- [MSDN / RijndaelManaged][36]{.aioseop-link}
- [MSDN / X509Certificate2][47]{.aioseop-link}

### Related Articles

- [Cross Programming Language Encryption – C# VS GO, Part 2][48]{.aioseop-link}
- [Cross Programming Language Encryption – NodeJs vs Go, Part 3][49]
- [Cross Programming Language Encryption – C# vs NodeJs vs Go, Part 4][50]

[1]: https://img.shields.io/github/stars/lunaticthinker-me/demo-cross-lang-encryption-cs?style=social
[2]: https://github.com/lunaticthinker-me/demo-cross-lang-encryption-cs
[3]: https://img.shields.io/github/followers/dragoscirjan?style=social
[4]: https://github.com/dragoscirjan
[5]: https://docs.microsoft.com/en-us/dotnet/csharp/
[6]: https://golang.org/
[7]: https://www.ecma-international.org/
[8]: https://www.typescriptlang.org/
[9]: https://en.wikipedia.org/wiki/Help:IPA/Dutch
[10]: https://en.wikipedia.org/wiki/Encryption
[11]: https://en.wikipedia.org/wiki/National_Institute_of_Standards_and_Technology
[12]: https://en.wikipedia.org/wiki/Block_cipher
[13]: https://en.wikipedia.org/wiki/Belgium
[14]: https://en.wikipedia.org/wiki/Vincent_Rijmen
[15]: https://en.wikipedia.org/wiki/Joan_Daemen
[16]: https://en.wikipedia.org/wiki/Advanced_Encryption_Standard_process
[17]: https://en.wikipedia.org/wiki/Federal_government_of_the_United_States
[18]: https://en.wikipedia.org/wiki/Data_Encryption_Standard
[19]: https://en.wikipedia.org/wiki/Symmetric-key_algorithm
[20]: https://en.wikipedia.org/wiki/Public-key_cryptography
[21]: https://en.wikipedia.org/wiki/Cryptosystem
[22]: https://en.wikipedia.org/wiki/Encryption_key
[23]: https://en.wikipedia.org/wiki/Decryption_key
[24]: https://en.wikipedia.org/wiki/Factorization
[25]: https://en.wikipedia.org/wiki/Prime_number
[26]: https://en.wikipedia.org/wiki/Factoring_problem
[27]: https://en.wikipedia.org/wiki/Acronym
[28]: https://en.wikipedia.org/wiki/Ron_Rivest
[29]: https://en.wikipedia.org/wiki/Adi_Shamir
[30]: https://en.wikipedia.org/wiki/Leonard_Adleman
[31]: https://en.wikipedia.org/wiki/Clifford_Cocks
[32]: https://en.wikipedia.org/wiki/Government_Communications_Headquarters
[33]: https://en.wikipedia.org/wiki/Classified_information
[34]: https://en.wikipedia.org/wiki/RSA_problem
[35]: https://docs.microsoft.com/en-us/dotnet/api/system.security.cryptography.rijndael?view=netcore-3.1
[36]: https://docs.microsoft.com/en-us/dotnet/api/system.security.cryptography.rijndaelmanaged?view=netcore-3.1
[37]: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation
[38]: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Padding
[39]: https://www.openssl.org/
[40]: https://docs.microsoft.com/en-us/dotnet/api/system.security.cryptography.x509certificates.x509certificate2?view=netframework-4.6.1
[41]: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
[42]: https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
[43]: https://security.stackexchange.com/questions/10949/encryption-should-i-be-using-rsa-or-aes
[44]: https://crypto.stackexchange.com/questions/47991/aes-vs-rsa-which-is-stronger-given-two-scenarios
[45]: https://stackoverflow.com/questions/13238674/aes-vs-rsa-to-encrypt-large-size-of-data
[46]: https://docs.microsoft.com/en-us/dotnet/api/system.security.cryptography?view=dotnet-plat-ext-3.1
[47]: https://docs.microsoft.com/en-us/dotnet/api/system.security.cryptography.x509certificates.x509certificate2?view=netcore-3.1
[48]: /cross-programming-language-encryption-csharp-vs-go-part-2/
[49]: https://lunaticthinker.me/cross-programming-language-encryption-javascript-vs-go-part-3/
[50]: /cross-programming-language-encryption-c-vs-javascript-vs-go-part-4/

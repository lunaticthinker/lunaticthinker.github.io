---
title: Cross Programming Language Encryption – NodeJs vs Go, Part 3
author: admin
date: 2020-06-07T02:12:19+00:00
url: /cross-programming-language-encryption-javascript-vs-go-part-3/
featured_image: /media/2020/06/dna-structure-node.jpg
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
  - JavaScript
---

[![GitHub stars][1]][2] [![GitHub followers][3]][4]  
See a demo at [Github][5]

---

Previous parts of this article treated encryption from the point of view of C# and GoLang programming languages.

What I did not mention, was the full architecture of our application, which I should probably not and which eventually would also imply a module that will also need to send encrypted content from a **NodeJs** module, towards our **Go Lang** module.

This also gave me the chance to extend a bit my research and try to make a 3 programming languages implementation of the same two crypto algorithms that I have started with: AES and RSA.

When it comes to NodeJs, there are a few modules that claim they do encrypt stuff, however, the best choice is to use the native NodeJs [crypto][6]{.aioseop-link} library.

### NodeJs Buffer and Base64

Both encryption algorithms described below, will be implementing [Buffer][7]{.aioseop-link}s. However, for a few versions now, NodeJs will tell you: **don’t use `var buffer = new Buffer()` because it’s deprecated, use `var buffer = Buffer.alloc()`.** But then, I’ll ask you: How can I convert a Base64 string to a decoded buffer, because obviously, when I would try to do smth like `Buffer.alloc(base64str.length, base64str, 'base64')`, the length is not quite correct.

In order to solve this correctly, we need to know how to calculate the length of a string decoded from Base64. Luckily, I found pretty fast a small article called [Get original length from a Base 64 string][8]{.aioseop-link}, which helped me to write the following function (**note to all, all the code below is written in TypeScript and not JavaScript**):

<pre class="wp-block-code"><code lang="typescript" class="language-typescript">  protected base64Length(password: string): number {
    return Math.floor((3 * password.length) / 4) - password.replace(/[^=]/gi, '').length;
  }</code></pre>

Having this discovered, and covered, let’s discuss now about AES and RSA under NodeJs.

### Coding AES with NodeJs

Incredible or not (after doing this in, now, 3 programming languages) AES is always harder to implement in comparison to RSA. Not necessarily by the number of lines of code, but by the strange ways, each programming language chooses to implement it.

In NodeJs, it is enough to know that AES cipher along with all  [Cipher Modes][9]{.aioseop-link} will be represented in strings: **aes-<size>-<cipher-mode>**. I will not comment on why, nor ask, but it seems one of the dullest ways of implementing it.

So, the first step would be initializing our encryption class, providing a hash as the key, and, based on the hash length, choose the algorithm and set your cipher mode (in my case: ‘cfb’).

Now, if you would ask me what cipher modes are supported by NodeJs, my first answer would be: _I have no freakin’ idea, I know CFB works…_; but after a short Google search I could confirm: CBC, CCM, CFB, GCM, OCB. If you wish for more, I advise you to research.

<pre class="wp-block-code"><code lang="typescript" class="language-typescript">export class AesCrypt {
  protected algorithm: string;

  constructor(private hash: string) {
    switch (hash.length) {
      case 16:
        // 'aes-128-<abbr>'
        this.algorithm = 'aes-128-cfb';
        break;
      case 24:
        this.algorithm = 'aes-192-cfb';
        break;
      case 32:
        this.algorithm = 'aes-256-cfb';
        break;
      default:
        throw new Error('invalid hash length. must be 16, 24 or 32');
    }
  }</code></pre>

One problem with NodeJs, is… **asynchronicity**. Yes, people… the shock for NodeJs was that you cannot do smth like `createCiper().encrypt()`, but you actually need to feed your content to a cipher and deal with an asynchronous method which eventually will calculate your encrypted content.

As a result, the AES encrypt and decrypt method, will be async.

<pre class="wp-block-code"><code lang="typescript" class="language-typescript">  async encrypt(password: string): Promise<string> {
    return new Promise((resolve) => {
      let encrypted: Buffer;

      const key = this.hash;
      const iv = crypto.randomBytes(16);

      const cipher = crypto.createCipheriv(this.algorithm, key, iv);
      cipher.on('readable', () => {
        let chunk;
        while (null !== (chunk = cipher.read())) {
          encrypted = encrypted ? Buffer.concat([encrypted, chunk]) : chunk;
        }
      });
      cipher.on('end', () => {
        const buffer = Buffer.concat([iv, encrypted]);
        resolve(buffer.toString('base64'));
      });
      cipher.write(password);
      cipher.end();
    });
  }
}</code></pre>

The amount of Buffer.concat in the function above (and also below) is determined by two things. As I’ve mentioned above, we’re working with Buffers, not strings, so we cannot actually write: `c = a + b`.

<pre class="wp-block-code"><code lang="typescript" class="language-typescript">
  async decrypt(password: string): Promise<string> {
    return new Promise((resolve) => {
      const key = this.hash;

      const buffer = Buffer.alloc(this.base64Length(password), password, 'base64');
      const iv = Buffer.alloc(16, 0);
      buffer.copy(iv, 0, 0, 16);

      const encrypted = Buffer.alloc(buffer.length - 16, 0);
      buffer.copy(encrypted, 0, 16, buffer.length);

      const decipher = crypto.createDecipheriv(this.algorithm, key, iv);
      let decrypted: Buffer;
      decipher.on('readable', () => {
        let chunk;
        while (null !== (chunk = decipher.read())) {
          decrypted = decrypted ? Buffer.concat([decrypted, chunk]) : chunk;
        }
      });
      decipher.on('end', () => {
        resolve(decrypted.toString('utf-8'));
      });
      decipher.write(encrypted);
      decipher.end();
    });
  }</code></pre>

### Coding RSA with NodeJs

As also discovered in Go Lang, and seems it’s similar under NodeJs, encrypting using an RSA certificate, will be done, by using a private and a public key, which first we need to load.

<pre class="wp-block-code"><code lang="typescript" class="language-typescript">export class RsaCrypt {
  protected prvKey: string;
  protected pubKey: string;

  protected options: Partial<crypto.RsaPrivateKey> = {
    oaepHash: 'sha512',
    padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
  };

  constructor(prvPath: string, pubPath: string) {
    this.prvKey = fs.readFileSync(prvPath).toString('utf-8');
    this.pubKey = fs.readFileSync(pubPath).toString('utf-8');
  }</code></pre>

Another step in RSA encryption would be, setting the padding (as decided in my previous parts of this articles, it will be OAEP), and also the hash type if needed.

<pre class="wp-block-code"><code lang="typescript" class="language-typescript">  encrypt(password: string): string {
    const buffer = new util.TextEncoder().encode(password);
    const encrypted = crypto.publicEncrypt(
      {
        ...this.options,
        key: this.prvKey,
      },
      buffer,
    );
    return encrypted.toString('base64');
  }</code></pre>

Except for that, the simplicity for writing encrypt and decrypt methods, is almost astonishing.

<pre class="wp-block-code"><code lang="typescript" class="language-typescript">  decrypt(password: string): string {
    // const buffer = new Buffer(password, 'base64');
    const buffer = Buffer.alloc(this.base64Length(password), password, 'base64');
    const decrypted = crypto.privateDecrypt(
      {
        ...this.options,
        key: this.prvKey,
      },
      buffer,
    );
    return decrypted.toString('utf-8');
  }
}</code></pre>

### References

- [Wikipedia / RSA\_(cryptosystem)][10]
- [Wikipedia / Advanced Encryption Standard][11]{.aioseop-link}
- [NodeJs][12]{.aioseop-link} [crypto][6]{.aioseop-link}

### Related Articles

- [Cross Programming Language Encryption – CSharp, Part 1][13]{.aioseop-link}
- [Cross Programming Language Encryption – C# VS GO, Part 2][14]
- [Cross Programming Language Encryption – C# vs NodeJs vs Go, Part 4][15]

[1]: https://img.shields.io/github/stars/lunaticthinker-me/demo-cross-lang-encryption-js?style=social
[2]: https://github.com/lunaticthinker-me/demo-cross-lang-encryption-cs
[3]: https://img.shields.io/github/followers/dragoscirjan?style=social
[4]: https://github.com/dragoscirjan
[5]: https://github.com/lunaticthinker-me/demo-cross-lang-encryption-js
[6]: https://nodejs.org/api/crypto.html
[7]: https://nodejs.org/api/buffer.html
[8]: https://blog.aaronlenoir.com/2017/11/10/get-original-length-from-base-64-string/
[9]: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation
[10]: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
[11]: https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
[12]: https://golang.org/pkg/crypto/
[13]: /cross-programming-language-encryption-csharp-part-1/
[14]: https://lunaticthinker.me/cross-programming-language-encryption-csharp-vs-go-part-2/
[15]: /cross-programming-language-encryption-c-vs-javascript-vs-go-part-4/

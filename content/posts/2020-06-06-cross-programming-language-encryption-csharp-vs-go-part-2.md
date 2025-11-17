---
title: Cross Programming Language Encryption – CSharp vs Go, Part 2
author: dragos
type: post
date: 2020-06-06T20:00:42+00:00
url: /cross-programming-language-encryption-csharp-vs-go-part-2/
featured_image: /media/2020/06/dna-structure-go.jpg
eltd_featured_post_meta:
  - no
eltd_disable_footer_meta:
  - no
eltd_video_type_meta:
  - social
eltd_hide_background_image_meta:
  - no
categories:
  - GO
  - Home Page
  - Uncategorized
---

[![GitHub stars][1]][2] [![GitHub followers][3]][4]  
See a demo at [Github][5]

---

[The first part of this article][6]{.aioseop-link}, discussed Encryption coding at C# level. It introduced you in the world of [AES][7]{.aioseop-link} and [RSA][8]{.aioseop-link} encryption algorithms. But the role of this story is not only to introduce you to some encryption algorithms but also show you how to code them under some programming languages.

As mentioned before, our team goal was to encrypt messages from a module written in **C#**, and decrypt them in a module written in [**Go lang**][9]{.aioseop-link}.

### Coding AES with Go

For this purpose, I have chosen to define a structure holding the Key and the Initialization Vector (IV). As explained in the previous article, we will use a private Hash which will be shared between encryptor and decryptor, while the IV will be attached to the encrypted content.

<pre class="wp-block-code"><code lang="go" class="language-go">
// AESCrypt -
type AESCrypt struct {
	Key []byte
	IV  []byte
}

// NewAESCrypt -
func NewAESCrypt(Hash string) (*AESCrypt, error) {
	enc := AESCrypt{}

	if len(Hash) != 16 && len(Hash) != 24 && len(Hash) != 32 {
		return nil, fmt.Errorf("invalid hash length. must be 16, 24 or 32")
	}

	enc.Key = []byte(Hash)
	enc.IV = make([]byte, 16)
	if _, err := io.ReadFull(rand.Reader, enc.IV); err != nil {
		return nil, fmt.Errorf("unable to generate IV: %s", err.Error())
	}

	return &enc, nil
}</code></pre>

Next step, considering our C# experience, is picking our [Block Cipher Mode][10]{.aioseop-link}. From this point of view, Go’s [crypt/cipher][11]{.aioseop-link} library contains a different list of ciphers (CBC, CFB, CTR, GCM, OFB), unlike C# (which contains CBC, CFB, CTS, ECB, OFB), but, as you can see, a few of them are common ground.

Also, considering I picked a cipher that requires no padding, you’ll see that, in Go, we won’t have to mention the idea of padding.

<pre class="wp-block-code"><code lang="go" class="language-go">// Encrypt will encrypt a string password using AES algorithm, returning a Base64 for of the encrypt result
func (enc AESCrypt) Encrypt(password string) (string, error) {
	block, err := aes.NewCipher(enc.Key)
	if err != nil {
		return "", err
	}

	stream := cipher.NewCFBEncrypter(block, enc.IV)

	encPassword := make([]byte, len([]byte(password)))

	stream.XORKeyStream(encPassword, []byte(password))

	return base64.StdEncoding.EncodeToString(append(enc.IV, encPassword...)), nil
}</code></pre>

For the decryption method, all has been said in the C# section of this article, only mention again, being that it will be a mirror function of the **encrypt** one.

<pre class="wp-block-code"><code lang="go" class="language-go">// Decrypt will decrypt a string password using AES algorithm, expecting a Base64 form of the encrypted password
func (enc AESCrypt) Decrypt(password string) (string, error) {

	encPassword, err := base64.StdEncoding.DecodeString(password)
	if err != nil {
		return "", err
	}

	block, err := aes.NewCipher(enc.Key)
	if err != nil {
		return "", err
	}

	enc.IV = encPassword[0:16]

	stream := cipher.NewCFBDecrypter(block, enc.IV)

	encPassword = encPassword[16:]

	decPassword := make([]byte, len(encPassword))

	stream.XORKeyStream(decPassword, encPassword)

	return string(decPassword), nil
}
</code></pre>

### Coding RSA with Go

The form of my RSA struct in Go, is not far from the AES one, the only difference being that we will need two variables, one for the public key, and the second for the private key.

<pre class="wp-block-code"><code lang="go" class="language-go">// RsaCrypt -
type RsaCrypt struct {
	PubKey  *rsa.PublicKey
	PrivKey *rsa.PrivateKey
}

// NewSSLCrypt -
func NewRSACrypt(PubKeyPath string, PrivKeyPath string) (*RsaCrypt, error) {
	encTool := &SslCrypt{}

	if err := encTool.ReadPublicKey(PubKeyPath); err != nil {
		return nil, err
	}
	if err := encTool.ReadPrivateKey(PrivKeyPath); err != nil {
		return nil, err
	}

	return encTool, nil
}</code></pre>

Then, for the purpose of writing beautiful code, we would have to write methods to read our public and private key, since the way things work in go are not that “beautiful” as they are in C#.

<pre class="wp-block-code"><code lang="go" class="language-go">// ReadPublicKey -
func (enc *RsaCrypt) ReadPublicKey(path string) error {
	data, err := ioutil.ReadFile(path)
	if err != nil {
		return fmt.Errorf("could not read public key file: %s", err.Error())
	}

	block, _ := pem.Decode(data)
	if block.Type != "CERTIFICATE" {
		return fmt.Errorf("invalid block type: %s", block.Type)
	}

	cert, err := x509.ParseCertificate(block.Bytes)
	if err != nil {
		return err
	}

	enc.PubKey = cert.PublicKey.(*rsa.PublicKey)

	return nil
}

// ReadPrivateKey -
func (enc *RsaCrypt) ReadPrivateKey(path string) error {
	data, err := ioutil.ReadFile(path)
	if err != nil {
		return fmt.Errorf("could not read private key file: %s", err.Error())
	}

	block, _ := pem.Decode(data)
	if block.Type != "PRIVATE KEY" {
		return fmt.Errorf("invalid block type: %s", block.Type)
	}

	if key, err := x509.ParsePKCS1PrivateKey(block.Bytes); err == nil {
		enc.PrivKey = key
		return nil
	}

	if key, err := x509.ParsePKCS8PrivateKey(block.Bytes); err == nil {
		switch key := key.(type) {
		case *rsa.PrivateKey:
			enc.PrivKey = key
			return nil
		case *ecdsa.PrivateKey:
			return fmt.Errorf("found ecdsa private key type in PKCS#8 wrapping; aiming for rsa")
		default:
			return fmt.Errorf("found unknown private key type in PKCS#8 wrapping")
		}
	}

	if _, err := x509.ParseECPrivateKey(block.Bytes); err == nil {
		// enc.PrivKey = key
		// return nil
		return fmt.Errorf("found ecdsa private key type in PKCS#8 wrapping; aiming for rsa")
	}

	return fmt.Errorf("failed to parse private key")
}</code></pre>

And then writing the encrypt and decrypt method.

What I did not mention in the C# part of this article, is that RSA uses a [padding scheme][12] also, and, as far as I identified them we can use two types: [OAEP or][13]{.aioseop-link} [PKCS1.][14]{.aioseop-link}

Again you will see that our encryption result will be encoded using Base64, for the simple reason of preventing data loss because of possible different encoding issues present on different operating systems.

<pre class="wp-block-code"><code lang="go" class="language-go">// Encrypt will encrypt a string password using an RSA certificate,
// returning a Base64 for of the encrypt result
func (enc *RsaCrypt) Encrypt(password string) (string, error) {
	hash := sha512.New()

	ciphertext, err := rsa.EncryptOAEP(hash, rand.Reader, enc.PubKey, []byte(password), nil)
	if err != nil {
		return "", err
	}

	return base64.StdEncoding.EncodeToString(ciphertext), nil
}

// Decrypt will decrypt a string password using an RSA certificate,
// expecting a Base64 form of the encrypted password
func (enc *RsaCrypt) Decrypt(password string) (string, error) {
	hash := sha512.New()

	bytes, err := base64.StdEncoding.DecodeString(password)
	if err != nil {
		return "", err
	}

	ciphertext, err := rsa.DecryptOAEP(hash, rand.Reader, enc.PrivKey, bytes, nil)
	if err != nil {
		return "", err
	}

	return string(ciphertext), nil
}
</code></pre>

### References

- [Wikipedia / RSA\_(cryptosystem)][8]
- [Wikipedia / Advanced Encryption Standard][7]{.aioseop-link}
- [Wikipedia / Block Cipher Mode][10]{.aioseop-link}
- [Wikipedia / Optimal asymmetric encryption padding][13]{.aioseop-link}
- [Wikipedia / PKCS1][14]{.aioseop-link}
- [Golang crypto][15]{.aioseop-link}

### Related Articles

- [Cross Programming Language Encryption – CSharp, Part 1][6]{.aioseop-link}
- [Cross Programming Language Encryption – NodeJs vs Go, Part 3][16]
- [Cross Programming Language Encryption – C# vs NodeJs vs Go, Part 4][17]

[1]: https://img.shields.io/github/stars/lunaticthinker-me/demo-cross-lang-encryption-go?style=social
[2]: https://github.com/lunaticthinker-me/demo-cross-lang-encryption-cs
[3]: https://img.shields.io/github/followers/dragoscirjan?style=social
[4]: https://github.com/dragoscirjan
[5]: https://github.com/lunaticthinker-me/demo-cross-lang-encryption-go
[6]: /cross-programming-language-encryption-csharp-part-1/
[7]: https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
[8]: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
[9]: https://golang.org/
[10]: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation
[11]: https://golang.org/pkg/crypto/cipher
[12]: https://en.wikipedia.org/wiki/Padding_(cryptography)
[13]: https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding
[14]: https://en.wikipedia.org/wiki/PKCS_1
[15]: https://golang.org/pkg/crypto/
[16]: https://lunaticthinker.me/cross-programming-language-encryption-javascript-vs-go-part-3/
[17]: /cross-programming-language-encryption-c-vs-javascript-vs-go-part-4/

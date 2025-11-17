---
title: Convert camelCase to Underscores Using sed
author: dragos
type: post
date: 2009-11-24T16:33:18+00:00
url: /convert-camelcase-to-underscores-using-sed/
categories:
  - Linux in a Box
  - Uncategorized
---

This short post deals with converting strings of the form camelCase or CamelCase into camel_case, and vice versa. These are three different popular naming conventions for variable/function/class names.

Convert CamelCase or camelCase to camel_case:

```bash
sed -e 's/([A-Z])/_\l\1/g' file.txt
echo "camelCase" | sed -e 's/([A-Z])/_\l\1/g'
```

Convert camel_case to camelCase

```bash
sed -e 's/_([a-z])/\u\1/g' file.txt
echo "camel_case" | sed -e 's/_([a-z])/\u\1/g'
```

Convert camel_case to CamelCase:

```bash
sed -e 's/_([a-z])/\u\1/g' -e 's/^([a-z])/\u\1/g' file.txt
echo "camel_case" | sed -e 's/_([a-z])/\u\1/g' -e 's/^([a-z])/\u\1/g'
```

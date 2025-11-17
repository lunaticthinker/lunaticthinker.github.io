---
title: Zend framework 2 generating route url with domain name
author: dragos
type: post
date: 2013-10-25T08:55:40+00:00
url: /zend-framework-2-generating-route-url-with-domain-name/
featured_image: /media/2013/10/Top-7-Tools-for-Analyzing-and-Parsing-Your-PHP-Code.jpg
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
  - Home Page
  - PHP
---

Nothing more than this little line of code:

<pre class="prettyprint">$homeUrl = $this->url(
    'youRouteName',
    array(/* your route params */),
    array('force_canonical' => true)
);</pre>

Of course, you need to call it within a code zone where you can invoke the URL helper. What you see above, assumes that you are in a .phtml file invoked by a controller’s action.

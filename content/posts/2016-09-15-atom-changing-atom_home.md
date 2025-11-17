---
title: Atom – Changing ATOM_HOME
author: dragos
date: 2016-09-15T08:41:57+00:00
url: /atom-changing-atom_home/
featured_image: /media/2016/05/atom.jpg
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
  - IDE
---

How many of you didn’t try to make a propert IDE from [Atom][1] by now. Let me tell you. From many many many many (I forgot how many) points of view, it’s one of the best **text editors** out there. And yes, with a little work, the right plugins and a lot of think through, it can be transformed into a proper IDE.

Not what I’m gonna talk abut today though… Gonna talk about a bugging issue, that always bothererd me because (at least in it’s early days (and I mean versions 1.5 to 1.8)) I experienced it A LOT. While not on SSD, but on **old good and latent HDD**, if Atom had a lot of plugins installed (let’s be serious, **npm** doesn’t do a great job with package management and neither does **apm**), from time to time, Atom was crashing. It was refusing to load properly, couldn’t index either the project nor the plugin list and had to [reset it (read here how)][2]. Not saying it was Atom’s fault. I had like at least 100 plugins installed. Any of those could be the black sheep. But remember, I had Atom installed on both Win and Linux on SSDs drives, and never ever ever had this problem.

So I began a new quest (please keep in mind I’m just an Atom user, not a developer). A quest to find out whether I could change the home path for Atom. I asked again for an SSD (only a multinational company manager could ignore our requests for SSDs in a time of upgrade and buy us HDDs because they’re plain cheaper), after proving my point that the HDD is TOO SLOW to load my tools, and finally got one, but couldn’t reinstall OS. SO I had to, somehow, move my Atom home folder to another partition. So here it is (for Windows, obviously, but you could adapt it to any OS, I guess):

**[the .bat version][3]**

<pre>. $HOME/bin/path.sh

set ATOM_HOME=F:\path\to\new_atom_home\.atom
start C:\path\to\atom\Update.exe --processStart atom.exe
echo ATOM_HOME currently at %ATOM_HOME%
echo.
pause
</pre>

**[the .sh version][4]** in case you’re using git bash

<pre>#! /bin/bash

export ATOM_HOME="/path/to/new_atom_home/.atom" && /c/path/to/atom/Update.exe --processStart atom.exe
echo ATOM_HOME currently at $ATOM_HOME
</pre>

**Note:** If you wish to use the .sh version, your atom shortcut exec path should look like:

<pre>C:\path\to\git\git-bash.exe C:\path\to\atom.sh
</pre>

**Note:** If you wish to download my scripts, feel free to, but don’t forget to adapt it to your own paths.

[1]: https://atom.io/
[2]: /coders-grave/resetting-atom-ide/
[3]: /wp-content/uploads/2016/09/atom.bat_.txt
[4]: /wp-content/uploads/2016/09/atom.sh_.txt

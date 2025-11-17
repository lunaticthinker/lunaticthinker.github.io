---
title: 90 Days Windows Extending Evaluation Period
author: dragos
type: post
date: 2013-11-23T16:39:44+00:00
url: /90-days-windows-extending-evaluation-period/
categories:
  - Other OSs
---

Searched a lot for this, but eventually [Microsoft][1] gave me the answer: http://support.microsoft.com/kb/948472

1. Click Start, and then click Command Prompt.

2. Type slmgr.vbs -dli, and then press ENTER to check the current status of your evaluation period.

3. To reset the evaluation period, type slmgr.vbs –rearm, and then press ENTER.

4. Restart the computer.

[1]: http://www.microsoft.com/

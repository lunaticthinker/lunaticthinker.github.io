---
title: Java Media Framework vs IP Camera JPEG/MJPEG
author: dragos
type: post
date: 2008-04-22T23:12:25+00:00
url: /java-media-framework-vs-ip-camera-jpegmjpeg/
featured_image: /media/2010/12/Java_logo-5.jpg
categories:
  - "Coder's Grave"
  - Home Page
  - Java
---

**NOTE:**

- This article is pretty deprecated. I do not say that the info here is false, but I would like to write a new article about this. Please leave me comments with what you want to know, and I will try do add more info to the article. And ofcourse, more sources.
- A Romanian translation for this article is found [here][1].

I really don”t think I”m either the first or the last to try and obtain images from and ip camera and than use them with <a title="Java Media Framework" href="http://www.google.ro/url?sa=t&ct=res&cd=1&url=http%3A%2F%2Fjava.sun.com%2Fproducts%2Fjava-media%2Fjmf%2F&ei=kbcHSNCXGJygmwPmwKyCBQ&usg=AFQjCNHFWA3xDh0qc9PpUvRQB83F9rl9sw&sig2=oaN-RciWsAPLPXVf8C3E8w" target="_blank" rel="noopener noreferrer">JMF</a>. So… after a few days of reading and trying to understand how JMF works, as I already had a JPEG/MJPEG grabber, here is my solutions:

As [Chris Adamson][2] explains in his article, <a href="http://www.onjava.com/pub/a/onjava/2002/12/23/jmf.html" target="_blank" rel="noopener noreferrer"><em>Java Media Development with QuickTime for Java</em></a>, to create a new JMF plugin you need to create two classes, one to extend [DataSource][3] and one to extend [PushBufferStream][4] or [PullBufferStream][5] from JMF. For DataSource I used [PushBufferDataSource][6], which implements the parent class: DataSource.

The most important element is the fact that Datasource must be placed int a package named smth like this: _name1.name2.someothername.media.protocol.numeprotocol_ (i.e. com.sun.media.protocol.http, com.sun.media.protocol.rtp, com.ibm.media.protocol.file).

For the DataSource class I used the example given by SUN in their [ScreenGrabber][7], and I only modified the streaming class name. I won”t reveal the image grabing class, as SUN forum is allready filled with such examples, but I will reveal the streaming class under a surogated protocol I called _htmjpeg_. I”m sure it won”t take long to you to understant that the protocol is just a simple name, and can be easily changed in my example:

[JMF MJPEG Plugin][8] (for Download)

[[wppald_inposts|Donation for JMF Work]]

<pre class="prettyprint">package com.itmc.media.protocol.htmjpeg;

import com.itmc.ipcamera.mjpeg.grabber.mjpegGrabber;
import java.awt.*;
import java.awt.image.BufferedImage;
import javax.media.*;
import javax.media.format.*;
import javax.media.protocol.*;
import java.io.IOException;

public class mjpegStream extends mjpegGrabber implements PushBufferStream, Runnable {

    protected ContentDescriptor cd = new ContentDescriptor(ContentDescriptor.RAW);
    protected int maxDataLength;
    protected int [] data;
    protected Dimension size;
    protected RGBFormat rgbFormat;
    protected boolean started;
    protected Thread thread;
    protected float frameRate = 7.0f;
    protected BufferTransferHandler transferHandler;
    protected Control [] controls = new Control[0];
    protected int x, y, width, height;

    protected Robot robot = null;
    protected BufferedImage im = null;
    protected boolean mjpeg = false;

    public mjpegStream(MediaLocator locator) {
        super("http:" + locator.getRemainder());
        System.out.println("http://" + locator.getRemainder());
        try {
            super.connect();
            im = super.readJPEG();
            super.disconnect();
        } catch(Exception e) {
        }
        if (im == null) {
            try {
                super.connect();
                im = super.readMJPEG();
                mjpeg = true;
                super.disconnect();
            } catch(Exception e) {
            }
        }

	size = new Dimension(im.getWidth(), im.getHeight());
//        im = new BufferedImage(100, 100, BufferedImage.TYPE_INT_ARGB);
//        size = new Dimension(100, 100);
	maxDataLength = size.width * size.height * 3;
	rgbFormat = new RGBFormat(
            size, maxDataLength,
            Format.intArray,
            frameRate,
            32,
            0xFF0000, 0xFF00, 0xFF,
            1, size.width,
            VideoFormat.FALSE,
            Format.NOT_SPECIFIED
        );

        System.out.println(rgbFormat.getFrameRate());

	// generate the data
	data = new int[maxDataLength];
	thread = new Thread(this, "Htmjpeg Grabber");
    }

    /***************************************************************************
     * SourceStream
     ***************************************************************************/

    public ContentDescriptor getContentDescriptor() {
	return cd;
    }

    public long getContentLength() {
	return LENGTH_UNKNOWN;
    }

    public boolean endOfStream() {
	return false;
    }

    /***************************************************************************
     * PushBufferStream
     ***************************************************************************/

    int seqNo = 0;

    public Format getFormat() {
	return rgbFormat;
    }

    public void read(Buffer buffer) throws IOException {
	synchronized (this) {
            super.connect();
	    Object outdata = buffer.getData();
	    if (outdata == null || !(outdata.getClass() == Format.intArray) ||
		((int[])outdata).length < maxDataLength) {
		outdata = new int[maxDataLength];
		buffer.setData(outdata);
	    }
	    buffer.setFormat( rgbFormat );
	    buffer.setTimeStamp( (long) (seqNo * (1000 / frameRate) * 1000000) );
	    BufferedImage bi = mjpeg?super.readMJPEG():super.readJPEG();
	    bi.getRGB(0, 0, size.width, size.height, (int[])outdata, 0, size.width);
	    buffer.setSequenceNumber( seqNo );
	    buffer.setLength(maxDataLength);
	    buffer.setFlags(Buffer.FLAG_KEY_FRAME);
	    buffer.setHeader( null );
	    seqNo++;
            if (!mjpeg) super.disconnect();
	}
    }

    public void setTransferHandler(BufferTransferHandler transferHandler) {
	synchronized (this) {
	    this.transferHandler = transferHandler;
	    notifyAll();
	}
    }

    void start(boolean started) {
	synchronized ( this ) {
	    this.started = started;
	    if (started && !thread.isAlive()) {
		thread = new Thread(this);
		thread.start();
	    }
	    notifyAll();
	}
    }

    /***************************************************************************
     * Runnable
     ***************************************************************************/

    public void run() {
	while (started) {
	    synchronized (this) {
		while (transferHandler == null && started) {
		    try {
			wait(1000);
		    } catch (InterruptedException ie) {
		    }
		} // while
	    }

	    if (started && transferHandler != null) {
		transferHandler.transferData(this);
		try {
		    Thread.currentThread().sleep( 10 );
		} catch (InterruptedException ise) {
		}
	    }
	} // while (started)
    } // run

    // Controls

    public Object [] getControls() {
	return controls;
    }

    public Object getControl(String controlType) {
       try {
          Class  cls = Class.forName(controlType);
          Object cs[] = getControls();
          for (int i = 0; i < cs.length; i++) {
             if (cls.isInstance(cs[i]))
                return cs[i];
          }
          return null;

       } catch (Exception e) {   // no such controlType or such control
         return null;
       }
    }
}</pre>

[1]: http://dragosc.itmcd.ro/it-stuff/java-media-framework-vs-ip-camera-jpegmjpeg-ro " Java Media Framework vs IP Camera JPEG/MJPEG"
[2]: http://www.onjava.com/pub/au/1045
[3]: http://java.sun.com/products/java-media/jmf/2.1.1/apidocs/javax/media/protocol/DataSource.html
[4]: http://java.sun.com/products/java-media/jmf/2.1.1/apidocs/javax/media/protocol/PushSourceStream.html
[5]: http://java.sun.com/products/java-media/jmf/2.1.1/apidocs/javax/media/protocol/PullBufferStream.html
[6]: http://java.sun.com/products/java-media/jmf/2.1.1/apidocs/javax/media/protocol/PushBufferDataSource.html
[7]: http://java.sun.com/products/java-media/jmf/2.1.1/solutions/ScreenGrabber.html
[8]: http://dor.homelinux.com/wp-content/uploads/2008/04/mjpegstream.java "JMF MJPEG Plugin"

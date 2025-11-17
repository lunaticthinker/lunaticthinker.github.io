---
title: Where to store uploaded files? File System versus Database storage.
type: post
date: 2020-07-23T16:43:42+00:00
url: /where-to-store-uploaded-files-file-system-versus-database-storage/
featured_image: /media/2015/11/dna-structure.jpg
categories:
  - "Coder's Grave"
  - Home Page
  - Linux in a Box
---

The purpose of this research, as described in the title, comparing the idea of storing files using either a Database or the mere FileSystem of the operating system by studying the experience of other people’s or companies’ and learning as much as possible from their experience.

Almost all analyses and discussions present on different speciality websites, as well as dedicated database companies, present almost the same answer, and the same principles in storing uploaded files.

But before that, let’s see some pros and cons for using each type of file storage (also, with additional comments, explaining or negating some of the affirmations):

#### **Pros of the File system:**

- Performance can be better than doing it in DB. To justify this, If you store large files in DB then it may slow down the performance because a simple query to retrieve the list of files or filename will also load the file data if you used Select \* in your query. While Files system accessing a file is quite simple and lightweight.
  _This comment is partially true. No DB architect in his right mind would put the file blob in the same table with the file’s metadata, however, writing and reading from a database is tributary to SQL queries, which may become intensive over time._
- Saving the files and downloading them in the file system is much simpler than database since a simple Save as function will help you out. Downloading can be done by addressing an URL with the location of the saved file.
- Migrating the data is an easy process here. You can just copy and paste the folder to your desired destination while ensuring that write permissions are provided to your destination.
- Cost-effective as It is Economical in most of the cases to expand your web server rather than paying for certain Databases.
- Easy to migrate it to Cloud storage like Amazon S3 or CDNs etc in the future.

#### **Cons of the File system:**

- Loosely packed. No ACID (Atomicity, Consistency, Isolation, Durability) operations relational mapping which mean there is no guarantee. Consider a scenario if your files are deleted from the location manually or by some hacking dudes, you might not know whether the file exists or not. Painful right?
  _This is indeed true. Not even involving the idea of hacking, the disk (thus the file) can be corrupted, files can be deleted “by mistake”, but this is a loop in the system’s design and not a problem for the Fyle System itself. If we talk about database backup and replication/synchronization when it comes to databases, why shouldn’t we apply the same principles here as well?_
- Low Security. Since your files can be saved in a folder where you should have provided write permissions, it is prone to safety issues and invites troubles like hacking. So it is best to avoid saving in fs if you cannot afford to compromise in terms of security.
  _This is completely false. If the hacker gains access to your application or your application’s OS, there are very big changes he will get access to the database as well._

#### **When is it most preferred:**

- If your application is liable to handle Large files of size more than 5MB and the massive number say thousands of file uploads.
  _This is also confirmed by a Microsoft study on their own Database & File System (MSSQL vs NTFS) which concludes that for files bigger than 264kb, the best approach is storing the files on a File System and not in a Database._
- If your application can land you on cloud nine, I mean your application will have a large number of users.

#### **Best way to do:**

Though File System comes with some cost and certain cons, a good Internal Folder Structure and choosing a folder location which may be a little difficult to access by others, but I will talk about this, in a section.

#### **Pros of Database:**

- ACID consistency which includes a rollback of an update that is complicated when the files are stored outside the database.
  _This is indeed a plus of Database storage. Performing the same actions on a File System required serious scripts and a lot more headaches just by taking into consideration the mere complexity of your storage implementation._
- Files will be in sync with the database so cannot be orphaned from it which gives you an upper hand in tracking transactions.
- Backups automatically include file binaries.
- More Secure than saving in a File System.
  _Incorrect. Security, if necessary, should be done by encryption, and not by DB/FS storage. The reasons are explained in a comment above._

#### **Cons of Database:**

- You may have to convert the files to a **blob** type in order to store it in DB.
- Database Backups will become more hefty and heavy.
- Memory ineffective. To add more, often RDBMS’s are RAM driven. So all data has to go to RAM first. Yeah, that’s right. Had you ever thought about what happens when an RDBMS has to find and sort data? RDBMS tracks each data page even the lowest amount of data read/written, and it has to track if it’s in memory or if it’s on disk if it’s indexed or sorted physically etc.

#### **When is it most preferred:**

- If your user’s file needs to be more tightly coupled, secured and confidential.   
- If your application will not demand a large number of files from a large number of users.

#### **Best way to do:**

- Be cautious with your Select query, Avoid Unwanted Select \* queries which may frequently retrieve the file data unnecessarily.
- Caching the file data can pave a way to reduce memory and database usage.
- If you are using SQL Server 2008 or higher version, make use of FILESTREAM.

As another note here, so far, I have taken into consideration only SQL databases. If for SQL databases the only solutions I would probably recommend as storage systems (and only for files of very small size) are Microsoft SQL and Oracle SQL (which are also very costly), there is also the NoSQL side with implementations of databases who appear to behave better as file storage, but also, under certain limitations.

You can find [here][1] a list of NoSQL database with document storage capabilities, out of which I would highlight [CouchDB][2] which is used by NpmJS (yet in a very complex system that also involves this specific DB), and to which I would also add [MongoDB][3] (of which I have learned, that their storage approach is [to split the stored files into chunks of 255kb][4] (see the Microsoft DB vs FS article to explain more probably).

In the end, the conclusion is not necessarily about which solution is better, but

- What are the capabilities and the costs of your hardware
- What is the use of your written software and how many users should it serve which also determines
- What is the number and average size of the files you need to store and also
- How intensive is the file operations service in your application

As a developer who relies on open-source software, considering the solutions above, I would probably never recommend SQL solutions because a “good” SQL solution is very pricey in this case, and also because it will require pricey hardware.

#### **First choice – FS storage**

The first solution I would probably choose to develop since it’s probably the most cost-effective would be the File System storage implementation, but even this solution would come with some rules or questions

- First of all, you need to learn the capabilities of your partitioning system or find a partitioning system that would behave best.
  - \_In a response I read on ServerFault, someone decided to run a test over an XFS partition of 500Gb. He wrote a script that generated 50-100k files and placed them in nested directories 1/2/3/4/5/6/7/8 (5-8 levels deep) and let it run for I think 1 week. It filled up the disk and ended up having about 25 million files or so. Access to any file with a known path was instant. Listing any directory with a known path was instant.
    Getting a count of the list of files, however (via find) took 68 hours.
    He also ran a test putting a lot of files in one directory. He got up to about 3.7 million files in one directory before he stopped. Listing the directory to get a count took about 5 minutes. Deleting all the files in that directory took 20 hours.
    But lookup and access to any file were instant.\_
  - Another example would be that EXT2 partition type, only supports about 256 subfolders in a folder. 
- Secondary, as described in the XFS example above, a very good ratio of folders/subfolders/files need to be tested in order to offer the File System a chance to behave properly.
  This doesn’t necessarily need to be a priority, writing a good path determining wrapper, would help to perform migrations whenever is needed.
  Furthermore, instant access of a huge list of files, listing or tree-ing a directory was never our job. We are not talking about storing files and their metadata on the FS, we’re only talking about storing files on the FS. Metadata and any other data can always stay where their place is: in a database.

For modelling a file system storage I recommend two solutions:

- Use an incremental numeric system; start with, i.e., 1.jpg and increment the file name further, pad the name with a character or with 0 (zero), revert it and then split the name in a few chunks which will represent the server.

<pre class="wp-block-code"><code lang="javascript" class="language-javascript">export const pathWrap = id => {
    id = ('' + 19).padStart(19, '0');
    return [id.split('').slice(-2).join('\\'), id].join('\\')
}</code></pre>

- Use a GUID/UUID ID system (don’t use hashes like MD4 or SHA since they’re not unique), and then apply the same principle above, maybe without the reverting part.

<pre class="wp-block-code"><code lang="javascript" class="language-javascript">export const pathWrap = (id) => [
    id.replace(/-/ig, '').split('').slice(0, 4).join(''),
    id.replace(/-/ig, '').split('').slice(4, 8).join(''),
    id
].join('\\')</code></pre>

For example, taking a numeric approach with a max padding of 19 digits (size in digits of MAX_INT under both SQLite and PGSQL) servers, and splitting it in chunks of 3 letters, we would reach a number of \(\sum\limits\_{k = 0}^6 ({C(10,3))^k} = \sum\limits\_{k = 0}^6 {160^k}\) total of folders, which may not be necessary for your application storage.

Furthermore, given the UUID example, and following the same principle, you would get a number of folders of  \(\sum\limits\_{k = 0}^{16} {(C(16,3))^k} = \sum\limits\_{k = 0}^{16} {560^k}\) , a number of folders which is completely unnecessary.

To summarize, to know exactly how many folders we may create, for taken a digit/character naming system, using _n_ characters/digits, having _l_ as ID length, and splitting the name into chunks of _m_ characters to form a path, the total number of directories should be  \(\sum\limits*{k = 0}^{l \mod m} {(C(n,m))^k}\), where \_n mod m* is the maximum amount of chunks that can be created with _m_ characters length. 

Given the two methods examples above, though we could obtain a smaller number of files which would fit a small application’s requirements without any problem.

#### **Second Choice – NoSQL Db**

A second would be to research the capabilities of a NoSQL database like MongoDB or CouchDB. 

**MongoDB’s** document size has an upper limit of 16MB, the idea of chunking is to allow streaming, i.e. allow users to download (or stream) a file without having the server to store the whole thing in RAM.

This mechanism is heavily used in streaming videos, image movies of 2 GB HD quality loaded in server’s RAM, that’d be really a waste of precious resources. The default chunk size of GridFS is 256kB which is supposedly a good compromise of overhead (more queries to the database) and little memory use, but it can be configured.

Streaming hardly makes sense for small images and delivering those images will require at least two to three round-trips to the database instead of one: One to find the fs.files document, and two to get the chunks. Even if we increased the chunk size, we’d still need two round-trips before we can even start to deliver the file.

So to sum it up storing files in mongo provides all the features of mongo like backup/replication/sharding/HA etc. But adds the extra overhead of querying one or more collections to retrieve a single chunk.

Even though I am more reluctant in talking about CouchDB, of which I barely know more than its name, I feel like I need to since it’s the DB behind the NPMJS architecture. However, if you read the implementation details, a single CouchDB solution is pretty much not acceptable. I found posts who would describe the relation to CouchDB pretty much as…

_We tried using CouchDB for image storage because the images logically “belonged” to some data entities that were in Couch._ _The benefit was that if you deleted an entity, the images would be deleted too, but the drawbacks were far greater than the benefits. The most important one was that the database grew so large that syncing it took so long that it wasn’t practical any more. The CouchDB sync protocol just isn’t geared towards moving a very large number of binaries quickly._

_To illustrate how unwieldy it can become, imagine replacing the CouchDB component with a tar.gz-server that can read and write to a single_ _tar.gz-archive. You really don’t gain anything apart from having bottlenecks in odd places. _

#### **In conclusion**

Every research that I did, would point me in using an FS storage for files (maybe except Mongo which could be the wonder child) probably direct myself in using the first 2-3 characters for the file’s ID into forming a set of 2-3 directories, then, as the project and data grow, maybe develop a more complex path-ing solution.

In addition to this, depending on the type of project, a set of reliable scripts/tools for database maintenance, migration and recovery should be created before putting the application in production, and not while starting to encounter issues with it.

#### Documentation

- <https://habiletechnologies.com/blog/better-saving-files-database-file-system/>
- <https://serverfault.com/questions/95444/storing-a-million-images-in-the-filesystem>
- <https://softwareengineering.stackexchange.com/questions/150669/is-it-a-bad-practice-to-store-large-files-10-mb-in-a-database>
- <https://www.microsoft.com/en-us/research/wp-content/uploads/2006/04/tr-2006-45.pdf>
- <https://dzone.com/articles/which-is-better-saving-files-in-database-or-in-fil>
- <https://www.8bitmen.com/instagram-architecture-how-does-it-store-search-billions-of-images/>
- <https://instagram-engineering.com/what-powers-instagram-hundreds-of-instances-dozens-of-technologies-adf2e22da2ad>
- <https://engineering.fb.com/core-data/needle-in-a-haystack-efficient-storage-of-billions-of-photos/>
- <https://groups.google.com/forum/#!topic/couchdb-user-archive/3GIBx0s2G5M>
- <https://stackoverflow.com/questions/13869162/mongodb-couchdb-for-storing-files-replication>
- <https://blog.npmjs.org/post/71267056460/fastly-manta-loggly-and-couchdb-attachments>
- <https://blog.npmjs.org/post/75707294465/new-npm-registry-architecture>
- <https://medium.com/@vaibhav0109/should-i-use-db-to-store-file-410ee22268c7>
- <https://www.predictiveanalyticstoday.com/top-nosql-document-databases/>

[1]: https://www.predictiveanalyticstoday.com/top-nosql-document-databases
[2]: https://couchdb.apache.org/
[3]: https://www.mongodb.com/
[4]: https://docs.mongodb.com/manual/core/gridfs/

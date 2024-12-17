URL Splitting
=============
The WWW has taught the world that the URL is a compact and easy-to-use
unique locator for a resource. As a string, its got a fixed format, it's
easy to parse, it contains structured info about domain names, port
numbers, filepaths and more.  Given that Atomese Nodes are also strings,
its a natural fit to store a file location as a URL.

However, it is also nice to extract the pieces-parts from the URL: the
domain name, the filepath, the filename itself. How should this be done?

The conventional answer is blunt: just do it. This is python. Just import
some URL-splitting python module, read the documentation, use it. Done.

### resources

[info](http://horothesia.blogspot.com/2014/07/hacking-on-apache-log-files-with-python.html)

---

- find type of log...

        -bash-3.2$
        -bash-3.2$ grep CustomLog ./httpd.conf
        ...
        CustomLog /path/a/access_log combined
        CustomLog /path/b/access_log combined
        CustomLog /path/c/access_log combined
        CustomLog /path/d/pike_access_log combined
        -bash-3.2$

- ok, type is 'combined'; find the log-format...

        -bash-3.2$
        -bash-3.2$ grep combined ./httpd.conf
        LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
        ...
        -bash-3.2$


---

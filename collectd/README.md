I created this collectd plugin to allow me to test my internet connection speed at home throughout the day.  It uses the Python 
`speedtest` library to run a speedtest every 15 minutes.  It collects ping and download/upload speeds, both for individual 
servers and in aggregate.  You can specify a test location or let it choose the test server automatically.  For consistency I 
specify a server.

![bandwidth](https://github.com/evandhoffman/detritus/raw/master/collectd/graph-1.png)

![latency](https://github.com/evandhoffman/detritus/raw/master/collectd/graph.png)

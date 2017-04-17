#!/usr/bin/python

import collectd
import speedtest
import signal

def restore_sigchld():
        signal.signal(signal.SIGCHLD, signal.SIG_DFL)


def read_callback(data=None):
    print "I'm in the read_callback now bruh"

    servers = []
    # If you want to test against a specific server
    # servers = [1234]

    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download()
    s.upload()
    s.results.share()

    results_dict = s.results.dict()

    # Ping
    ping = collectd.Values()
    ping.plugin = 'speedtest'
#    ping.interval = 300
    ping.type = 'ping'
    ping.type_instance = 'ping'
    ping.values = [ results_dict['ping'] ]
    ping.dispatch()

    # Download
    dl = collectd.Values()
    dl.plugin = 'speedtest'
    dl.type = 'gauge'
#    dl.interval = 300
    dl.type_instance = 'download'
    dl.values = [ results_dict['download'] ]
    dl.dispatch()

    # Upload
    ul = collectd.Values()
    ul.plugin = 'speedtest'
    ul.type = 'gauge'
#    ul.interval = 300
    ul.type_instance = 'upload'
    ul.values = [ results_dict['upload'] ]
    ul.dispatch()

    print "download speed was %s" % results_dict['download']

collectd.register_init(restore_sigchld)
collectd.register_read(read_callback, 900)


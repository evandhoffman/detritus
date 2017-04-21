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

    server = results_dict['server']

    # Ping
    ping = collectd.Values()
    ping.plugin = 'speedtest'
#    ping.interval = 300
    ping.type = 'ping'
    ping.type_instance = 'Ping (%s, %s)' % ( server['name'], server['sponsor'] )
    ping.values = [ results_dict['ping'] ]
    ping.dispatch()

    ping.type_instance = 'Ping (aggr)'
    ping.dispatch()

    # Download
    dl = collectd.Values()
    dl.plugin = 'speedtest'
    dl.type = 'gauge'
#    dl.interval = 300
    dl.type_instance = 'Download (%s, %s)' % ( server['name'], server['sponsor'] )
    dl.values = [ results_dict['download'] ]
    dl.dispatch()

    dl.type_instance = 'Download (aggr)'
    dl.dispatch()

    # Upload
    ul = collectd.Values()
    ul.plugin = 'speedtest'
    ul.type = 'gauge'
#    ul.interval = 300
    ul.type_instance = 'Upload (%s, %s)' % ( server['name'], server['sponsor'] )
    ul.values = [ results_dict['upload'] ]
    ul.dispatch()

    ul.type_instance = 'Upload (aggr)'
    ul.dispatch()

    print "download speed was %s" % results_dict['download']

collectd.register_init(restore_sigchld)
collectd.register_read(read_callback, 900)


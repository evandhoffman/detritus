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
    ping.type_instance = '%s, %s' % ( server['name'], server['sponsor'] )
    ping.values = [ results_dict['ping'] ]
    ping.dispatch()

    ping.type_instance = 'Aggregated'
    ping.dispatch()
    print "ping time was %s ms" % results_dict['ping']

    dl = collectd.Values()
    dl.plugin = 'speedtest'
    dl.type = 'speedtest'
    dl.type_instance = '%s, %s' % ( server['name'], server['sponsor'] )
    dl.values = [ results_dict['download'] , results_dict['upload']]
    dl.dispatch()
    print "Download: %s Mb/s, Upload: %s Mb/s. Server: %s, Sponsor: %s" % (results_dict['download'] / 1e9, results_dict['upload'] / 1e9, server['name'], server['sponsor'])

    dl.type_instance = 'Aggregated'
    dl.dispatch()



collectd.register_init(restore_sigchld)
collectd.register_read(read_callback, 120)


#!/usr/bin/python

import requests
from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup
import json
import rrdtool
import os 

def get_stats(router_addr, statname):
	stat_urls = { 'status' : 'cgi-bin/VmRouterStatusStatusCfgCgi',
	'downstream' : 'cgi-bin/VmRouterStatusDownstreamCfgCgi',
	'upstream' : 'cgi-bin/VmRouterStatusUpstreamCfgCgi',
	'upstream_burst': 'cgi-bin/VmRouterStatusBurstCfgCgi',
	}
	if statname not in stat_urls:
		print "DORK"
		return
	req = requests.get('http://%s/%s' % (router_addr, stat_urls[statname]))
	soup = BeautifulSoup(req.text)
	table = soup.find("table")
	head_items = table.find('thead').findAll('th')
	stats = {}
	entries = []
	for item in head_items:
		if (item.text != u"&nbsp;"):
			stats[item.text] = {}
			entries.append(item.text)
	statrows = table.findAll('tr')
	for row in statrows:
		cells = row.findAll('td')
		if len(cells) > 0:
			heading = cells[0]
			for index,item_stat in enumerate(cells[1:]):
				# print "%s : %s" % (entries[index], item_stat.text)
				value = "U" if item_stat.text=="N/A" else item_stat.text
				stats[entries[index]][heading.text] = value
	return stats

def log_upstream(stats, param, key):
	upstream_sources = [
		'DS:US-1:GAUGE:300:U:U',
		'DS:US-2:GAUGE:300:U:U',
		'DS:US-3:GAUGE:300:U:U',
		'DS:US-4:GAUGE:300:U:U']
	upstream_archives = [
		'RRA:AVERAGE:0.5:1:604800', # 7 days worth of full res, every 30 seconds
		'RRA:AVERAGE:0.5:10:2419200', # 28 days of every 5 minutes
		'RRA:AVERAGE:0.5:120:8760' # 1 year's worth of every hour
	]
	if not os.path.exists('rrds/upstream_%s.rrd' % param):
		rrdtool.create('rrds/upstream_%s.rrd' % param,'--step','30',upstream_sources, upstream_archives)
	upstream_update = 	"N:%s:%s:%s:%s" %  (
		str(stats['upstream']['US-1'][key]),
		str(stats['upstream']['US-2'][key]),
		str(stats['upstream']['US-3'][key]),
		str(stats['upstream']['US-4'][key]) )

	rrdtool.update('rrds/upstream_%s.rrd' % param, upstream_update)
	print "Upstream: [%s] %s" % (key, upstream_update)

def log_upstream_counter(stats, param, key):
	upstream_sources = [
		'DS:US-1:COUNTER:300:U:U',
		'DS:US-2:COUNTER:300:U:U',
		'DS:US-3:COUNTER:300:U:U',
		'DS:US-4:COUNTER:300:U:U']
	upstream_archives = [
		'RRA:AVERAGE:0.5:1:604800', # 7 days worth of full res, every 30 seconds
		'RRA:AVERAGE:0.5:10:2419200', # 28 days of every 5 minutes
		'RRA:AVERAGE:0.5:120:8760' # 1 year's worth of every hour
	]
	if not os.path.exists('rrds/upstream_%s.rrd' % param):
		rrdtool.create('rrds/upstream_%s.rrd' % param,'--step','30',upstream_sources, upstream_archives)
	upstream_update = 	"N:%s:%s:%s:%s" %  (
		str(stats['upstream']['US-1'][key]),
		str(stats['upstream']['US-2'][key]),
		str(stats['upstream']['US-3'][key]),
		str(stats['upstream']['US-4'][key]) )

	rrdtool.update('rrds/upstream_%s.rrd' % param, upstream_update)
	print "Upstream: [%s] %s" % (key, upstream_update)

def log_downstream(stats, param, key):
	downstream_sources = [
		'DS:DS-1:GAUGE:300:U:U',
		'DS:DS-2:GAUGE:300:U:U',
		'DS:DS-3:GAUGE:300:U:U',
		'DS:DS-4:GAUGE:300:U:U',
		'DS:DS-5:GAUGE:300:U:U',
		'DS:DS-6:GAUGE:300:U:U',
		'DS:DS-7:GAUGE:300:U:U',
		'DS:DS-8:GAUGE:300:U:U']
	downstream_archives = [
		'RRA:AVERAGE:0.5:1:604800', # 7 days worth of full res, every 30 seconds
		'RRA:AVERAGE:0.5:10:2419200', # 28 days of every 5 minutes
		'RRA:AVERAGE:0.5:120:8760' # 1 year's worth of every hour
	]

	if not os.path.exists('rrds/downstream_%s.rrd' % param):
		rrdtool.create('rrds/downstream_%s.rrd' % param,'--step','30',downstream_sources, downstream_archives)
	downstream_update = 	"N:%s:%s:%s:%s:%s:%s:%s:%s" %  (
		str(stats['downstream']['DS-1'][key]) ,
		str(stats['downstream']['DS-2'][key]),
		str(stats['downstream']['DS-3'][key]),
		str(stats['downstream']['DS-4'][key]),
		str(stats['downstream']['DS-5'][key]),
		str(stats['downstream']['DS-6'][key]),
		str(stats['downstream']['DS-7'][key]),
		str(stats['downstream']['DS-8'][key]))
	print "Downstream: [%s] %s" % (key, downstream_update)
	rrdtool.update('rrds/downstream_%s.rrd' % param, downstream_update)


def log_downstream_counter(stats, param, key):
	downstream_sources = [
		'DS:DS-1:COUNTER:300:U:U',
		'DS:DS-2:COUNTER:300:U:U',
		'DS:DS-3:COUNTER:300:U:U',
		'DS:DS-4:COUNTER:300:U:U',
		'DS:DS-5:COUNTER:300:U:U',
		'DS:DS-6:COUNTER:300:U:U',
		'DS:DS-7:COUNTER:300:U:U',
		'DS:DS-8:COUNTER:300:U:U']
	downstream_archives = [
		'RRA:AVERAGE:0.5:1:604800', # 7 days worth of full res, every 30 seconds
		'RRA:AVERAGE:0.5:10:2419200', # 28 days of every 5 minutes
		'RRA:AVERAGE:0.5:120:8760' # 1 year's worth of every hour
	]

	if not os.path.exists('rrds/downstream_%s.rrd' % param):
		rrdtool.create('rrds/downstream_%s.rrd' % param,'--step','30',downstream_sources, downstream_archives)
	downstream_update = 	"N:%s:%s:%s:%s:%s:%s:%s:%s" %  (
		str(abs(int(stats['downstream']['DS-1'][key]))) ,
		str(abs(int(stats['downstream']['DS-2'][key]))),
		str(abs(int(stats['downstream']['DS-3'][key]))),
		str(abs(int(stats['downstream']['DS-4'][key]))),
		str(abs(int(stats['downstream']['DS-5'][key]))),
		str(abs(int(stats['downstream']['DS-6'][key]))),
		str(abs(int(stats['downstream']['DS-7'][key]))),
		str(abs(int(stats['downstream']['DS-8'][key]))))
	print "Downstream{counter}: [%s] %s" % (key, downstream_update)
	rrdtool.update('rrds/downstream_%s.rrd' % param, downstream_update)



if __name__=='__main__':
	upstream = get_stats('192.168.0.1', 'upstream')
	downstream = get_stats('192.168.0.1', 'downstream')
	stats = {'upstream': upstream, 'downstream': downstream}

	log_downstream(stats, 'power', 'Power Level (dBmV)')
	log_downstream(stats, 'snr', 'RxMER (dB)')
	log_downstream(stats, 'freq', 'Frequency (Hz)')
	log_downstream_counter(stats, 'prerserr', 'Pre RS Errors')
	log_downstream_counter(stats, 'postrserr', 'Post RS Errors')
	log_upstream(stats, 'power', 'Power Level (dBmV)')
	log_upstream(stats, 'sym_rate', 'Symbol Rate (Sym/sec)')
	log_upstream(stats, 'freq', 'Frequency (Hz)')
	log_upstream_counter(stats, 't1', 'T1 Timeouts')
	log_upstream_counter(stats, 't2', 'T2 Timeouts')
	log_upstream_counter(stats, 't3', 'T3 Timeouts')
	log_upstream_counter(stats, 't4', 'T4 Timeouts')
	print "Done updating"

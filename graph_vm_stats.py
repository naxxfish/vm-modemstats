#!/usr/bin/python
import rrdtool

colours = [ 'FF0000', 'FF7F00', 'FFFF00', '00FF00', '0000FF', '4B0082', '8F00FF', '9000FF' ] # now including Ultraviolet!

def graph_stat(updown, param, start, caption, units, extraopts=[], tracetype="LINE"):
	rrdfile = "rrds/%s_%s.rrd" % (updown, param)
	down_channels = [ 'DS-1', 'DS-2', 'DS-3', 'DS-4', 'DS-5', 'DS-6', 'DS-7', 'DS-8' ]
	up_channels = ['US-1', 'US-2', 'US-3', 'US-4' ]
	channels = []
	if updown == 'upstream':
		channels = up_channels
	elif updown == 'downstream':
		channels = down_channels
	defs = []
	for channel in channels:
		defs = defs + [ 'DEF:%s=%s:%s:AVERAGE' % ( channel, rrdfile, channel ) ]
	lines = []
	i=0
	for channel in channels:
		lines = lines + ["LINE:%s#%s:%s (%s)" % (channel, colours[i], caption, channel)]
		i=i+1
	print lines
	rrdtool.graph('graphs/%s_%s_%s.png' % (updown, param, start), 
		defs, 
		lines, 
		'--vertical-label', units, 
		'--title', ("%s %s" % (updown, caption)).title(), 
		'--start', start,
		'--width', '1024',
		'--height', '512', 
		'--units-length', '3',
		'--alt-y-grid',
		'--alt-autoscale',
		'--color', 'BACK#111111',
		'--color', 'CANVAS#ffffff00',
		'--color', 'FONT#ffffff',
		'--color', 'GRID#666666',
		'--color', 'MGRID#883333',
		extraopts)

if __name__ == '__main__':
	graph_stat('downstream', 'power', 'end-1h', 'Power', 'dBmV')
	graph_stat('upstream', 'power', 'end-1h', 'Power', 'dBmV')
	graph_stat('downstream', 'snr', 'end-1h', 'Signal to Noise', 'dB')
	graph_stat('downstream', 'freq', 'end-1h', 'Frequency', 'Hz')
	graph_stat('upstream', 'freq', 'end-1h', 'Frequency', 'Hz')
	graph_stat('upstream', 't3', 'end-1h', 'T3 Timeouts', 'timeout/sec')
	graph_stat('downstream', 'prerserr', 'end-1h', 'Pre-RS Errors', 'errors/sec', extraopts=['--logarithmic'])
	graph_stat('downstream', 'postrserr', 'end-1h', 'Post-RS Errors', 'errors/sec', extraopts=['--logarithmic'])

	graph_stat('downstream', 'power', 'end-24h', 'Power', 'dBmV')
	graph_stat('upstream', 'power', 'end-24h', 'Power', 'dBmV')
	graph_stat('downstream', 'snr', 'end-24h', 'Signal to Noise', 'dB')
	graph_stat('downstream', 'freq', 'end-24h', 'Frequency', 'Hz')
	graph_stat('upstream', 'freq', 'end-24h', 'Frequency', 'Hz')
	graph_stat('upstream', 't3', 'end-24h', 'T3 Timeouts', 'timeout/sec')
	graph_stat('downstream', 'prerserr', 'end-24h', 'Pre-RS Errors', 'errors/sec', extraopts = ['--logarithmic'])
	graph_stat('downstream', 'postrserr', 'end-24h', 'Post-RS Errors', 'errors/sec', extraopts = ['--logarithmic'])

	graph_stat('upstream', 'power', '-604800', 'Power', 'dBmV')
	graph_stat('downstream', 'power', '-604800', 'Power', 'dBmV')
	graph_stat('downstream', 'snr', '-604800', 'Signal to Noise', 'dB')
	graph_stat('downstream', 'freq', '-604800', 'Frequency', 'Hz')
	graph_stat('upstream', 'freq', '-604800', 'Frequency', 'Hz')
	graph_stat('upstream', 't3', '-604800', 'T3 Timeouts', 'timeout/sec')
	graph_stat('downstream', 'prerserr', '-604800', 'Pre-RS Errors', 'errors/sec', extraopts = ['--logarithmic'])
	graph_stat('downstream', 'postrserr', '-604800', 'Post-RS Errors', 'errors/sec', extraopts = ['--logarithmic'])

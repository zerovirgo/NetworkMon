import re
msg = '[0].data = [[Date.UTC(2016,3,12,00,05,29), 0.102884],'
m = re.search('(\(.*\))',msg)
print m.group(1)
print type(m.group(1))
mm = m.group(1)
print mm.strip('(').strip(')')
print '-'.join( mm.strip('(').strip(')').split(','))
print msg.split('), ')[-1].split('],')[0]

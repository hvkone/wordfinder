from corpy.udpipe import Model
from corpy.udpipe import pprint


m = Model(".//corpus//udpipemodel//chinese.udpipe")

sents = list(m.process(".//corpus//chinese//23825-0.txt"))
pprint(sents)
import gevent
from gevent import monkey

from baidu import *

monkey.patch_all()

jobs = []
for i in range(1, 501):
    jobs.append(i)
print(jobs)

job = [gevent.spawn(parserJS, range1) for range1 in jobs]
gevent.joinall(job)
import os
import profile
import pstats

from fib_seq import fib_seq  # noqa

# Create 5 set of stats
base_filename = os.path.dirname(os.path.realpath(__file__))
filenames = []
for i in range(5):
    filename = 'fib_dump_%d.stats' % i
    profile.run('fib_seq(20)',
                os.path.join(base_filename, filename))

# Read all 5 stats files into a single object
stats = pstats.Stats(os.path.join(base_filename, 'fib_dump_0.stats'))
for i in range(1, 5):
    stats.add(os.path.join(base_filename, 'fib_dump_%d.stats' % i))

fname = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'fib_dump.stats',
)

stats.dump_stats(fname)

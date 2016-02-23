import profile
import pstats
import os

from fib_seq import fib_seq  # noqa

# Create 5 set of stats
base_filename = os.path.dirname(os.path.realpath(__file__))
filenames = []
for i in range(5):
    filename = 'profile_stats_%d.stats' % i
    profile.run('print %d, fib_seq(20)' % i,
                os.path.join(base_filename, filename))

# Read all 5 stats files into a single object
stats = pstats.Stats(os.path.join(base_filename, 'profile_stats_0.stats'))
for i in range(1, 5):
    stats.add(os.path.join(base_filename, 'profile_stats_%d.stats' % i))

fname = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'fib_dump.stats',
)

stats.dump_stats(fname)

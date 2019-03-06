# coding: utf-8

from __future__ import (unicode_literals, print_function,
        division)

from seqgentools.sequence import Sequence, Chain, INF

# IDEA
# - index of an element is an extendable tuple
# - When new dimension is discovered, add an additional index in the tuple
# - Each index has an attribute of length, which is also changable
# - When an range is dicovered as null, do not include it to the space
# - Previous searched index is preserved eventhough new dimension is added
#   by assuming all new dimensions are indexed as zero
# - If a dimension is not valid in ranges, it is assumed that there is only one element
# - ?? support a tuple is an index of another search tuple?

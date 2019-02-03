seqgentools
==============

Sequence Generation Tools

Motivation
=============

Python itertools_ package provides users with useful tools that helps to create iterators for efficient loopings." Tools in the package can define a large multi-dimensional arrays succinctly.

For example, following code snippets generate a 3-dimensional space that has 1,000 data points:

.. code-block:: python

    >>> for x,y,z in itertools.product(range(10), repeat=3):
    >>>     # DO work on each "point of (x,y,z)"

However, itertools_ has one critical drawback to be used as a search space generator for Machine-learning techniques: Its element should be accessed sequentially. For example, to access to the last point of (9,9,9) in previous code example, you need to go through all 999 elements from (0,0,0) to (9,9,8). It is because Python iterator does not support indexing. Next code examples shows that iterator can not be index.

.. code-block:: python

    >>> space = itertools.product(range(10), repeat=3)
    >>> space[999]
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: 'itertools.product' object is not subscriptable

"seqgentools" takes core capability of "itertools_" and adds indexing capability. 

.. code-block:: python

    >>> import seqgentools as sgt
    >>> space = sgt.Product(range(10), repeat=3)
    >>> space[999]
    (9, 9, 9)


Installation
=============

Best way to install "seqgentools" is using "pip" as shown below.

.. code-block:: bash

    >>> pip install seqgentools --user

To access the latest version, please download from this site using git.

.. code-block:: bash

    >>> git clone https://github.com/NCAR/seqgentools.git

Getting-started
=================

Whenever possible, "seqgentools" follows conventions of using "itertools_" so that user can leverage of their knowledge. One obvious difference between "seqgentools" and "itertools_" is that seqgentools allows indexing using brackets of "[" and "]". The other notable difference is that, in "seqgentools", the name of sequence genrators starts with a capital letter while "itertools_" starts with a lower-cases. This is to emphasize that sequence generators are genrated from class, not from function.

As of this version, "seqgentools" implemented follwoing sequence generators.

    * Count: generates a sequence of, possibily infinite, numbers 
    * Cycle: generates a cyclic sequence of another sequence
    * Repeat: generates a repeating sequece of object
    * Chain: generate a chained seqnece of another sequences
    * Product: generate a sequence of mathematical product of another sequences
    * Permutations: generate a permuted sequence of another sequence
    * Combinations: generate a combinated sequence of another sequence
    * PermutationRange: generate a chained sequence of series of permuted sequence ranging r=0 to r=n of another sequence
    * CombinationRange: generate a chained sequence of series of combinated sequence ranging r=0 to r=n of another sequence
    * Wrapper: genearte a sequence from Python sequece data types

[seqgentools examples]

.. code-block:: python

    >>> import seqgentools as sgt
    >>>
    >>> ###### Count #######
    >>>
    >>> seq.Count(10)[10]
    20
    >>>
    >>> ###### Cycle #######
    >>>
    >>> seq.Cycle((1,2,3))[10]
    2
    >>>
    >>> ###### Repeat #######
    >>>
    >>> seq.Repeat(1)[10]
    1
    >>>
    >>> ###### Chain #######
    >>>
    >>> list(seq.Chain(range(3), range(4)))
    [0, 1, 2, 0, 1, 2, 3]
    >>>
    >>> ###### Product #######
    >>>
    >>> prod = seq.Product(range(2), range(2))
    >>> list(prod)
    [(0, 0), (0, 1), (1, 0), (1, 1)]
    >>> prod[3]
    (1, 1)
    >>>
    >>> ###### Permutations #######
    >>>
    >>> perm = seq.Permutations("ABC", 2)
    >>> list(perm)
    [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'),
        ('C', 'B')]
    >>> perm[3]
    ('B', 'C')
    >>>
    >>> ###### Combinations #######
    >>>
    >>> comb = seq.Combinations("ABC", 2)
    >>> list(comb)
    [('A', 'B'), ('A', 'C'), ('B', 'C')]
    >>> comb[2]
    ('B', 'C')
    >>>
    >>> ###### PermutationRange #######
    >>>
    >>> permrange = seq.PermutationRange("ABC")
    >>> list(permrange)
    [(), ('A',), ('B',), ('C',), ('A', 'B'), ('A', 'C'), ('B', 'A'),
        ('B', 'C'), ('C', 'A'), ('C', 'B'), ('A', 'B', 'C'), ('A', 'C', 'B'),
        ('B', 'A', 'C'), ('B', 'C', 'A'), ('C', 'A', 'B'), ('C', 'B', 'A')]
    >>> permrange[3]
    ('C',)
    >>>
    >>> ###### CombinationRange #######
    >>>
    >>> combrange = seq.CombinationRange("ABC")
    >>> list(combrange)
    [(), ('A',), ('B',), ('C',), ('A', 'B'), ('A', 'C'), ('B', 'C'),
        ('A', 'B', 'C')]
    >>> combrange[2]
    ('B',)

NOTE: "seqgentools" support infinite sequence in, not all, but most of sequence generators.

NOTE: testing codes in "tests" subdirectory could be a good place to investigate furtuer.

NOTE: "Wrapper" sequence generator wraps Python sequence data types such as list, tuple, dictionary, string, set, etc.

.. _itertools: https://docs.python.org/3/library/itertools.html

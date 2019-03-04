seqgentools
==============

Python combinatorics library that generates indexible sequences through combinations, permutations, and/or products of another sequences. It creates the sequences without actually allocating memory so that a sequence having a large, possibly infinite, number of elements can be used in many applications such as an optimal solution searching problem.

Motivation
=============

Python itertools_ package provides users with capability of creating "iterators for efficient loopings". From the prospective of "optimization problems", "itertools" could be a convinient tool to succinctly define a, possibly large, search space without actually allocating memory for the instance of the space.

For example, following code snippet generates a 3-dimensional space that has 1,000 data points:

.. code-block:: python

    >>> for x,y,z in itertools.product(range(10), repeat=3):
    >>>     # DO work on each "point of (x,y,z)"

However, itertools_ has one critical drawback to be used as a search space generator for search algorithms: Its element should be accessed sequentially. For example, to access to the last point of (9,9,9) in previous code example, you need to go through all 999 elements from (0,0,0) to (9,9,8). It is because Python iterator does not support indexing. Next code example shows that iterator can not be indexed.

.. code-block:: python

    >>> space = itertools.product(range(10), repeat=3)
    >>> space[999]
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: 'itertools.product' object is not subscriptable

"seqgentools" takes the core capabilities of "itertools_" and adds randomly-accessible indexing capability to them. 

.. code-block:: python

    >>> import seqgentools as seq
    >>> space = seq.Product(range(10), repeat=3)
    >>> space[999]
    (9, 9, 9)


Installation
=============

"seqgentools" can be easily installed using "pip" as shown below.

.. code-block:: bash

    >>> pip install seqgentools --user

To access the latest features, please download from this repository using git.

.. code-block:: bash

    >>> git clone https://github.com/NCAR/seqgentools.git

Getting-started
=================

Whenever possible, "seqgentools" follows conventions of using "itertools_" so that user can leverage of their knowledge about "itertools_". If you are not familiar with "itertools_", I believe, it is worth of investing a couple of miniutes to see what it can do for you.

Doing is believing: please follow examples shown below to get an idea of how "seqgentools" works.

.. code-block:: python

    >>> import seqgentools as seq
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
    >>> ###### Combinations_with_replacement #######
    >>>
    >>> combr = seq.Combinations_with_replacement("ABC", 2)
    >>> list(combr)
    [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]
    >>> combr[2]
    ('A', 'C')
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

Search-space Generator
=======================

"seqgentools" contains a hierachical search space generator that can dramatically reduce
  the total size of search space compared to naive products of each search dimensions.

API Documentation
=================

Under development.

Until API documentation is ready, please see "itertools_" API documentation as "seqgentools", whenever possible, follows "itertools_" API.

As of this version, "seqgentools" implemented follwoing sequence generators.

    * Count:            generates a sequence of, possibily infinite, evenly spaced numbers 
    * Cycle:            generates a cyclic chain of another sequence
    * Repeat:           generates a repeating sequece of object
    * Chain:            generates a chained sequence of another sequences
    * Product:          generates a sequence of mathematical product of another sequences
    * Permutations:     generates a permuted sequence of another sequence
    * Combinations:     generates a combinated sequence of another sequence
    * Combinations_with_replacement: generates a combinated sequence of another sequence with replacement
    * PermutationRange: generates a chained sequence of series of permuted sequence
                        ranging r=0 to r=n of another sequence
    * CombinationRange: generates a chained sequence of series of combinated sequence
                        ranging r=0 to r=n of another sequence
    * Wrapper:          generates a sequence from Python sequece data types
    * Fibonacci:        generates an random-accesible Fibonacci sequence

[NOTES]

    * "seqgentools" supports randomly accessible indexing of infinite sequences.
    * "Product", "Permutations", "Combinations", "Combinations_with_replacement", "PermutationRange",
      and "CombinationRange" do not accept infinite sequence as their input(s).
    * test codes in "tests" subdirectory could be a good place to start further investigation.
    * "Wrapper" sequence generator wraps Python sequence data types such as list, tuple, dictionary, string, set, etc.
    * The name of sequence generators in "seqgentools" starts with a capital letter while "itertools_"
      starts with a lower-case. This is to emphasize that sequence generators are instantiated from class, not from function.

.. _itertools: https://docs.python.org/3/library/itertools.html

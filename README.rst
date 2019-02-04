seqgentools
==============

Sequence Generation Tools

Motivation
=============

Python itertools_ package provides users with capability of creating "iterators for efficient loopings". From the prospectives of machine-learning techniques, "itertools" could be a good tool to define a large multi-dimensional arrays succinctly without actually allocating memory for the arrays.

For example, following code snippet generates a 3-dimensional space that has 1,000 data points:

.. code-block:: python

    >>> for x,y,z in itertools.product(range(10), repeat=3):
    >>>     # DO work on each "point of (x,y,z)"

However, itertools_ has one critical drawback to be used as a search space generator for Machine-learning techniques: Its element should be accessed sequentially. For example, to access to the last point of (9,9,9) in previous code example, you need to go through all 999 elements from (0,0,0) to (9,9,8). It is because Python iterator does not support indexing. Next code example shows that iterator can not be indexed.

.. code-block:: python

    >>> space = itertools.product(range(10), repeat=3)
    >>> space[999]
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: 'itertools.product' object is not subscriptable

"seqgentools" takes the core capabilities of "itertools_" and adds indexing capability to them. 

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

Whenever possible, "seqgentools" follows conventions of using "itertools_" so that user can leverage of their knowledge about "itertools_". If you are not familiar with "_itertools_", I believe, it is worth of investing a couple of miniutes to see what it can do for you.

Doing is believing: please follow examples shown below to get an idea of how "seqgentools" works.

.. code-block:: python

    >>> import seqgentools as seq
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

As of this version, "seqgentools" implemented follwoing sequence generators.

    * Count:            generates a sequence of, possibily infinite, evenly spaced numbers 
    * Cycle:            generates a cyclic chain of another sequence
    * Repeat:           generates a repeating sequece of object
    * Chain:            generates a chained sequence of another sequences
    * Product:          generates a sequence of mathematical product of another sequences
    * Permutations:     generates a permuted sequence of another sequence
    * Combinations:     generates a combinated sequence of another sequence
    * PermutationRange: generates a chained sequence of series of permuted sequence
                        ranging r=0 to r=n of another sequence
    * CombinationRange: generates a chained sequence of series of combinated sequence
                        ranging r=0 to r=n of another sequence
    * Wrapper:          generates a sequence from Python sequece data types

[NOTES]

    * "seqgentools" supports indexing of infinite sequences.
    * "Product", "Permutations", "Combinations", "PermutationRange", and "CombinationRange" do not
      accept infinite sequence as their input(s).
    * test codes in "tests" subdirectory could be a good place to start further investigation.
    * "Wrapper" sequence generator wraps Python sequence data types such as list, tuple, dictionary, string, set, etc.
    * The name of sequence generators in "seqgentools" starts with a capital letter while "itertools_"
      starts with a lower-case. This is to emphasize that sequence generators are instantiated from class, not from function.

.. _itertools: https://docs.python.org/3/library/itertools.html

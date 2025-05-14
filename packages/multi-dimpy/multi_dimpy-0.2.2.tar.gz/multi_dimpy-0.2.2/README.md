# Overview
Everyone knows you can't add apples and oranges.<br>
Most people also know you can't add meters and seconds.<br>
But sometimes people do—accidentally, when it's hidden in code or in matrix computations.

Models and algorithms with dimensional inconsistencies might still yield decent results, but they don't make physical sense, and a change of units results in a change to the output, when units shouldn't make a difference.

Software packages for managing dimensions already exist, but they lack the ability to do **dimensioned linear algebra**—they mostly just work with scalar values.
So as a first go and a proof-of-concept, this package wraps NumPy and tracks physical dimensions of $n$-dimensional arrays using theory developed in the book *Multidimensional Analysis* (see citation below).

(Hart, G. W. (1995). Multidimensional Analysis: Algebras and Systems for Science and Engineering. Springer-Verlag.)

# Contributing

This package is in its very early stages.
I'll update this section with more information soon (hopefully), but in the meantime feel free to get acquainted with dimensioned linear algebra, perhaps by perusing *Multidimensional Analysis* (cited in the [Overview](#overview)), or adding to the [Discussion](https://github.com/schilln/multi-dimpy/discussions).

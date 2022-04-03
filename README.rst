About
=====

Make terminal graphics fun and easy! :P

.. warning::

   This project is far from useful yet! Stay tuned!

Examples
========

Command line
------------

.. code-block:: text

   $ terminal_graphics show examples/lenna.png
   $ terminal_graphics info
   $ terminal_graphics show $(fzf)

Scripting
---------

.. code-block:: python

   from terminal_graphics import write_file

   write_file('examples/lenna.png')

Adding Items
============

General Structure
-----------------

ILMO uses a model of ``Books`` and ``BookInstances`` or `Material`` and ``MaterialInstances``.
A book contains general information about a book

.. code::

    Book:
        title: string, required
        author: Author object, required
        genre: Genre object
        summary: String
        isbn: String
        language: Language object

As you can see there are some objects that refer to other models like ``Author``.
To create a book you need to create these first (or add them later, not recommended).

The physical books that are in the library are then represented in ``BookInstance``. It has the following properties

.. code::

    BookInstance:
        label: String, required
        book: Author object, required
        loan_status: available | maintenance | On Loan | Reserved, required
        imprint: String

Add Books
---------

ILMO currently only supports adding books via the admin interface.


ID System
^^^^^^^^^

As most libraries do often have multiple copies of the same book an identification
system is proposed that accounts for that. Feel free to use your own, this is just an inspiration!

For books the ID format therefore consists of a ``stem`` of category and 
number and a ``numbering`` with characters of copies.

.. code::

   CC[number] [ii]
   
   "CH42 c"    # Titel 42 in category Chemistry, copy number 3

   "XY132 af"  # Titel 132 in category XY, copy number 33

   "a16792 c"  # bad example as categories should be two capital letters and the
               # titel number should be ascending

- CC: 
   Category abbreviation e. ``CH`` for chemistry. It is advised to use
   a two letter abbreviation, but there is no technical limit.
- Number: 
   Indicates which title the book has. The number is ascending incremented for every title
   added to the category.
- ii: 
   index of the copy. For the first copy the index is ``a`` for the second 
   it is ``b`` and for the 27th copy it is ``aa``.



Add material
------------

ILMO currently only supports adding material via the admin interface.

ID System
^^^^^^^^^

Material has a different ID system. It consists of an abbreviation and an index.

.. code::

   AA [index]
   
   "LC 42"           # Labcoat number 42
   "SG 132"          # Safety glasses number 132

   "Labcoat 16792"   # bad example as abbreviation should be two capital letters and index
                     # number should be ascending

- AA:
   Abbreviation of the items name
- Index:
   Ascending number. The highest index of an item is the number of items of this name.


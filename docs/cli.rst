Commandline Usage
==================


.. programm:: bmst

.. options:: -s <store>, --store <store>

  required, tells the primary data store

.. option:: --serve

  serve the primary datastore via http

.. option:: --backup source

  create blob+metadata based backup of the files in source

.. option:: --show

  print a listing of the metadata items

.. option --ls <key>

  print the metadata of the item refered by key

.. option:: --archive <key> <target>

  creatr an compressed archive (tarball/zip) from the items of the metadata item refered by key

.. option:: --extract <key> <target>

  restore the items refered by the metadata of `key` as files below target

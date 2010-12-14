Design of the Store
====================



On Disk
========

The on Disk Format is designed for simplicity and rsync-support


There are 2 kinds of object, thus 2 subdirectories.

* blobs store binary items, they are below blobs using a finename sheme of
  root/'blob'/sha[:2]/sha[2:]

* metadata items store compressed json objects below 'meta'
  the metadata files should be pretty-printed json, using the indent of 2 spaces


Smart rest fontend
==================

The web fontend exposes 2 resource collections for blobs and meta items

on get requests they will serve as is, put requests may only contain full content

PUT of meta items that refer unknown blobs will be refused telling the missing blobs

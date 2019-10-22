----
status: raw
----

# Flexible Content Storage Layering


## Core Storage

Content Addressed Value Storage
: a store for opaque binary values and addresses them by a content hash and the hash type

Default Hash Type
: blake2b-512

Linked Metadata Store:
: layered on top of the content store
  uses msgpack serialization
  uses msgpack extension types to do content references


Root
: a  single reference value put at the hash id 0000
0 wit the invalid hash type root



Reference:references are encoded within a extension type



### Aiases Mechanism



* Roots
* Content
* Abstract Content/Stand in



# data tracking


* blobs
* metadata


# data roots

* manifests
* stand-ins




## Content Storage

## Blob Storage


## Rich Data Storage

rich data storage MUST use EITHER of:

* json: pretty printed with an indent of 2 and sorted keys
* cbor: self identified
* msgpack:

rich data must refer a named schema



# Content References

* reference types:
  * strong (traverse in gc)
  * weak (traversal in gc, transfer belonging elements to weak/unnneeded)
  * informal (no gc traversal)


# Data Roots
# Manifest for the Root Object

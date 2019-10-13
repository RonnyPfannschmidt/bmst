## Content Storage


All content stored MUST be addressed by content hash.
Content hashes MUST use either the `hash:algorith` form or the `hash` form
If the Algorithm is not given, blake2b must be assumed.
If the Algorithm is give, it SHOULD follow the naming in the python stdlib.



## Blob Storage

Blobs MUST be stored as is

## Rich Data Storage

rich data storage MUST use EITHER of:

* json: pretty printed with an indent of 2
* cbor: self identified
* msgpack


# Content References in Rich Data

TODO: reference types


# Content Stand Ins


(enable expressing larger blobs as concat of smaller blobs & co)



# Data Roots


# Manifest for the Root Object

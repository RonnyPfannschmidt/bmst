import apipkg
apipkg.initpkg(__name__, {
    'FileStore': '.store:FileStore',
    'MappingStore': '.store:MappingStore',
    'MetaStore': '.metastore:MetaStore',
})

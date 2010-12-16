import apipkg
apipkg.initpkg(__name__, {
    'FileStore': '.store:FileStore',
    'MappingStore': '.store:MappingStore',
    'Httplib2Store': '.store:Httplib2Store',
    'MetaStore': '.metastore:MetaStore',
})

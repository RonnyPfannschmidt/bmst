import apipkg
apipkg.initpkg(__name__, {
    'FileStore': '.store:FileStore',
    'Httplib2Store': '.store:Httplib2Store',
    'MetaStore': '.metastore:MetaStore',
})

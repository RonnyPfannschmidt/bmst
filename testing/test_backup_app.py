from bmst.backup_app import load_tree, fullmeta, make_backup
from bmst.managed import  BMST
import bz2


def test_load(tmpdir):
    assert load_tree(tmpdir) == {}

    tmpdir.ensure('a/b').write('test\n')

    assert load_tree(tmpdir) == {
        'a/b': ('4e1243bd22c66e76c2ba9eddc1f91394e57f9f83', 'test\n'),
    }


def test_fullmeta(tmpdir):
    root = tmpdir.ensure('root', dir=1)
    root.join('test').write('test\n')
    meta, blobs = fullmeta(root)
    assert meta == {
        'project': 'root',
        'tags': ['backup'],
        'items': {
            'test': '4e1243bd22c66e76c2ba9eddc1f91394e57f9f83',
        },
    }

    assert blobs == {
        '4e1243bd22c66e76c2ba9eddc1f91394e57f9f83': 'test\n',
    }


def test_makebackup(tmpdir):
    test_fullmeta(tmpdir)
    bmst = BMST(blobs={}, meta={})
    make_backup(tmpdir.join('root'), bmst)
    assert bmst.blobs == {
        '4e1243bd22c66e76c2ba9eddc1f91394e57f9f83':
            'BZh91AY&SY\xcc\xc3q\xd4\x00\x00\x02A\x80\x00\x10\x02\x00\x0c\x00'
            ' \x00!\x9ah3M\x19\x97\x8b\xb9"\x9c(Hfa\xb8\xea\x00',
    }
    assert bmst.meta == {
        '675857289b324a4f65e1fc5ead1a97d75a248945':
            'BZh91AY&SY(\xe2\xd0f\x00\x00?\xdb\x80@\x10P\x04?\xf0\x00\n?\xba'
            '\xde\n \x00t"\x9az\x02z\x9a1\x03\xd4h\x0c\x83S\xd2CC \xd0\x1ah\r'
            '\x04\x17z\x10N\x1e\x81\x80\x80\xc5)\xe8\t$\x9e\x9d%\x91 \xe5\x80'
            '~lt\xda8&F:\x0bX\xd6\x19\x89\xcc%\xc5\xae\x00\x88L3zY\x12K\x89'
            '\xaa\xb7\x10_p Das\xfe\x91P\x06\xaa\xdd\x1e\xd5\x8b\x9b\x97DT'
            '\xf9G\x9f\x8b\xb9"\x9c(H\x14qh3\x00',
    }

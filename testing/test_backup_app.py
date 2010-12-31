from bmst.backup_app import load_tree


def test_load(tmpdir):
    assert load_tree(tmpdir) == {}

    tmpdir.ensure('a/b').write('test\n')

    assert load_tree(tmpdir) == {
        'a/b': ('4e1243bd22c66e76c2ba9eddc1f91394e57f9f83', 'test\n'),
    }

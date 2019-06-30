from distutils.core import setup


setup(
    name="bmst",
    description="a simple experimet in backup stores",
    use_scm_version=True,
    setup_requires=["setuptools_scm>3"],
    install_requires=["httplib2", "werkzeug", "py"],
)

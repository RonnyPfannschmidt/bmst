from distutils.core import setup
from hgdistver import get_version

setup(
    name="bmst",
    description="a simple experimet in backup stores",
    version=get_version(),
    install_requires=["httplib2", "werkzeug", "py"],
)

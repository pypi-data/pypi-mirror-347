from setuptools import setup, find_packages

setup(
    name="dummy-conda-plugin",
    version="0.1.0rc1",
    entry_points={"conda": ["dataflow-conda-plugin = plugin.plugin"]},
    packages=find_packages(include=["plugin"]),
    package_data={'plugin': ['scripts/*.sh']},
)
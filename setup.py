from setuptools import find_packages, setup

setup(
    name="surl",
    version="0.2.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask==1.1.2", "flask-restful==0.3.8"],
)

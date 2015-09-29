try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="luigi-monitor",
    version="0.2.1",
    description="Send summary messages of your Luigi jobs to Slack.",
    url="https://github.com/hudl/luigi-monitor",
    author="Hudl",
    author_email="alex.debrie@hudl.com",
    license="MIT",
    packages=['luigi_monitor'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7"
    ],
    keywords="luigi",
    install_requires=["requests", "luigi"]
)

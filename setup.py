try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="luigi-monitor",
    version="0.1.0",
    description="Send summary messages of your Luigi jobs to Slack.",
    url="https://github.com/hudl/luigi-monitor",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7"
    ],
    keywords="luigi",
    install_requires=["requests", "luigi"]
)

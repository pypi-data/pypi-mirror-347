from setuptools import setup, find_packages

setup(
    name="smtp_webtester",  # harus unik di PyPI
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",  # dan semua dependen lainnya
    ],
    entry_points={
        'console_scripts': [
            'smtp-webtester=smtp_webtester.main:main',  # command line entry
        ],
    },
    author="Mrv3n0m666",
    author_email="testceklow123@hotmail.com", 
    description="SMTP Web Tester Bot via Flask",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Mrv3n0m666/Smtp-Webtester",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

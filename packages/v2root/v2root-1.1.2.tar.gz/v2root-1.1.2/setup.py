from setuptools import setup, find_packages

setup(
    name="v2root",
    version="1.1.2",
    author="Project V2Root, Sepehr0Day",
    author_email="sphrz2324@gmail.com",
    description="A Python package to manage v2ray with native extensions",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/V2RayRoot/V2Root",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "v2root": [
            "lib/*.so",
            "lib/*.o",
            "lib/*.dll",
            "lib/src/*.c",
            "lib/src/*.h",
            "lib/v2ray",
            "lib/v2ray.exe",
            "lib/Makefile.linux",
            "lib/Makefile.win",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Operating System :: POSIX :: Linux"
    ],
    python_requires=">=3.6",
    license="MIT",
    install_requires=[
        "colorama>=0.4.6",  
    ],
)
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    lng_description = fh.read()

setuptools.setup(
    name="PyPasta",
    version="0.1",
    author="Deep",
    author_email="asyncpy@proton.me",
    license="MIT",
    description="Upload and retrieve pastes from Pastebin via Python EASLY .",
    long_description=lng_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    url="https://github.com/DevZ44d/PyPasta",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)

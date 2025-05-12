from setuptools import setup, find_packages

setup(
    name="mepybase",
    version="1.0",
    author="mellon",
    author_email="mellon.email@example.com",
    description="Mellon self py base utils",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mellon/mepybase/",  # 确保 URL 是正确的
    packages=find_packages(),
    install_requires=[
        "colorama",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

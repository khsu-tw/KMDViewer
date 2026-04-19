from setuptools import setup, find_packages

setup(
    name="KMDViewer",
    version="1.0",
    description="A Markdown Viewer with PDF export capability",
    author="Hsu, Kai-Chun",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "PyQt5>=5.15.0",
        "markdown-it-py>=3.0.0",
        "mdit-py-plugins>=0.4.0",
        "pygments>=2.17.0",
        "weasyprint>=60.0",
        "Pillow>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "kmdviewer=src.main:main",
        ],
    },
    include_package_data=True,
)

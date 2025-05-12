from setuptools import setup, find_packages

setup(
    name="imagefrompdf",
    version="1.0.2",
    long_description=open("README.md").read(),
    packages=find_packages(),
    long_description_content_type="text/markdown",
    url="https://github.com/jedahee/imagefrompdf",
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'imagefrompdf=imagefrompdf.__main__:pdf_to_images',  # Comando para la CLI
        ],
    },
    install_requires=[
        'pdf2image',
        'Pillow',
        'click',
    ],
    extras_require={
        'dev': [
            'pytest',
            'tox',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

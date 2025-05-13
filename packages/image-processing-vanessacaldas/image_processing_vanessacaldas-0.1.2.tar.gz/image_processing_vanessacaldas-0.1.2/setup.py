from setuptools import setup, find_packages

setup(
    name="image_processing-vanessacaldas",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "Pillow"
    ],
    author="Vanessa de Souza Caldas",
    author_email="vanessacaldaszootecnista@gmail.com",
    description="Um pacote simples de processamento de imagens.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="http://github.com/vanessacaldas/image-processing-package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)

import setuptools

# Читаем долгое описание из README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gemini-translator",
    version="0.1.0",
    author="Ivan Khomich",
    author_email="ivan.khomich@gmail.com",
    description="Python library for translation (Gemini Translator)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=["requests>=2.0"],
)

from setuptools import setup, find_packages

setup(
    name="Axalense",
    version="1.2.87",
    description="Axalense is a framework developed at Axamine ai for image analysis and various other Vision langauge task its  tool built with Groq technology. It enables developers to easily analyze and moderate images using intelligent visual recognition and natural language prompts.",
    author="Henilsinh Raj",
    author_email="henilsinhrajraj@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "groq",
        "Pillow"
        
    ],
    python_requires='>=3.7',
    include_package_data=True,
    license="MIT",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    data_files=[("", ["LICENSE"])],)

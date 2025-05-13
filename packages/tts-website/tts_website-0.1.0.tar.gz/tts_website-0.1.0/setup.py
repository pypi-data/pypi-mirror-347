from setuptools import setup, find_packages

setup(
    name="tts-website",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Text-to-Speech converter website",
    packages=find_packages(),
    install_requires=[
        "gTTS",  # Example: Google's Text-to-Speech library
        "Flask", # Example: If your website uses Flask
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

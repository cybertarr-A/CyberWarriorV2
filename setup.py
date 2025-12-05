from setuptools import setup, find_packages

setup(
    name="cyberwarrior",
    version="2.0.0",
    description="AI-powered vulnerability detection tool",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "gitpython",
        "transformers",
        "torch",
        "rich",
        "tqdm",
        "huggingface_hub",
    ],
)

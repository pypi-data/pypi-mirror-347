from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="local-ai-utils-assist",
    version="0.2.3",
    packages=['assist'],
    package_dir={"assist": "assist"},
    entry_points={
        'console_scripts': [
            'assist=assist.cli:main',
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'typing_extensions',
        'openai',
        'fire',
        'pyyaml',
        'mcp-agent',
        'local-ai-utils-core',
    ],
)
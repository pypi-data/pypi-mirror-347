from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="local-ai-utils-core",
    version="0.2.5",
    package_dir={'local_ai_utils_core': 'core'},
    packages=['local_ai_utils_core', 'local_ai_utils_core.ui'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'openai',
        'pyyaml',
        'pytest',
        'desktop_notifier'
    ],
)
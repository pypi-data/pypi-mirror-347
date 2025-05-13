from setuptools import setup, find_packages

setup(
    name="local-ai-utils-core",
    version="0.2.4",
    package_dir={'local_ai_utils_core': 'core'},
    packages=['local_ai_utils_core', 'local_ai_utils_core.ui'],
    install_requires=[
        'openai',
        'pyyaml',
        'pytest',
        'desktop_notifier'
    ],
)
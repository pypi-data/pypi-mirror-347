from setuptools import setup
import os, shutil

# package name
package = "rgroq"

# update package readme
latest_readme = os.path.join("README.md") # github repository readme
package_readme = os.path.join(package, "README.md") # package readme
shutil.copy(latest_readme, package_readme)
with open(package_readme, "r", encoding="utf-8") as fileObj:
    long_description = fileObj.read()

# get required packages
install_requires = []
with open(os.path.join(package, "requirements.txt"), "r") as fileObj:
    for line in fileObj.readlines():
        mod = line.strip()
        if mod:
            install_requires.append(mod)

# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
setup(
    name=package,
    version="1.3.0",
    python_requires=">=3.8",
    description="A terminal chatbot, powered by Groq Cloud API (Windows / macOS / Linux)",
    long_description=long_description,
    author="Ruben Phagura",
    author_email="contact@rubenphagura.com",
    packages=[
        package,
        f"{package}.utils",
        f"{package}.audio",
        f"{package}.temp",
    ],
    package_data={
        package: ["*.*"],
        f"{package}.utils": ["*.*"],
        f"{package}.audio": ["*.*"],
        f"{package}.temp": ["*.*"],
    },
    license="GNU General Public License (GPL)",
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            f"rgroq={package}.main:main",
        ],
    },
    keywords="ai google gemini palm codey vertex api multimodal vision",
    project_urls={
        "Source": "https://github.com/ruben2163/groqchat",
        "Tracker": "https://github.com/ruben2163/groqchat/issues",
        "Documentation": "https://github.com/ruben2163/groqchat/wiki",
    },
    classifiers=[
        # Reference: https://pypi.org/classifiers/

        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
from setuptools import setup, find_packages

setup(
    name='mcp_rdkit',
    version='0.1.5',
    author='Shashank Shekhar Shukla',
    author_email='shukla20shashankshekhar@gmail.com',
    description='A package for RDKit integration with MCP',
    long_description="""
MCP RDKit is a Python package that integrates the RDKit cheminformatics toolkit with the Model Context Protocol (MCP) framework. It provides tools for molecular visualization, descriptor calculation, and seamless communication with MCP servers for advanced chemical informatics workflows.
""",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    install_requires=[
        "rdkit",
        "mcp"
    ],
    project_urls={
        "Documentation": "https://github.com/s20ss/mcp_rdkit#readme",
        "Source": "https://github.com/s20ss/mcp_rdkit",
        "Issues": "https://github.com/s20ss/mcp_rdkit/issues"
    },
)
from setuptools import setup, find_packages

# Open README.md with UTF-8 encoding to avoid encoding issues
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='MeetingAssistant',  # Name of your package
    version='0.1.1',            # Version of your package
    packages=find_packages(), # Automatically find your packages in the directory
    install_requires=[
        'PySimpleGUI',
        'openai',
        'faiss-cpu',
        'python-telegram-bot',
        'python-dotenv',
        'sentence-transformers',
        'scikit-learn',
        'torch',
        'tqdm',
    ],
    author='Samruddhi Tiwari',  # Your name
    author_email='samruddhitiwari003@gmail.com',  # Your email
    description='A conversational meeting assistant',  # Short description
    long_description=long_description,  # Long description from README.md
    long_description_content_type='text/markdown',  # Format of long description
    url='https://github.com/samruddhitiwari/MeetingAssistant',  # Your project URL
    classifiers=[
        'Programming Language :: Python :: 3',  # Python version
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',  # OS compatibility
    ],
    python_requires='>=3.6',  # Specify the Python version
)

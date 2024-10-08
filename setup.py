from setuptools import setup, find_packages

setup(
    name='wechatmsg',
    version='1.0.1',
    packages=find_packages(include=['.', 'app', 'app.*']),  
    py_modules=['wechatmsg'],  
    install_requires=[
        'PyQt5',
        'psutil',
        'pycryptodomex',
        'pywin32',
        'pymem',
        'silk-python',
        'pyaudio',
        'fuzzywuzzy',
        'python-Levenshtein',
        'requests',
        'flask==3.0.0',
        'pyecharts==2.0.1',
        'jieba==0.42.1',
        'google==3.0.0',
        'protobuf==4.25.1',
        'soupsieve==2.5',
        'lz4==4.3.2',
        'pilk==0.2.4',
        'python-docx==1.1.0',
        'docxcompose==1.4.0',
    ],
)

from setuptools import setup, find_packages

setup(
    name='sheet-task-uploader',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'gspread',
        'google-api-python-client',
        'oauth2client'
    ],
    description='Google Sheets için otomatik görev listesi, checkbox ve renklendirme modülü',
    author='İrfan Gedik',
    author_email='irfangedik@gmail.com',
    url='https://github.com/irfangedik/sheet-task-uploader',
    keywords=['google sheets', 'automation', 'task tracker', 'checkbox', 'gspread'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
from setuptools import setup, find_packages

setup(
    name="eth-gas-tracker-gui",            
    version="0.1.0",                       
    packages=find_packages(),              
    install_requires=[                     
        "requests",                         
        "tkinter",                          
    ],
    entry_points={                         
        'console_scripts': [
            'eth-gas-tracker=gas_tracker_gui:main',   
        ],
    },
    include_package_data=True,             
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",  
    author="Gendis Nanaya",                    
    author_email="gendisnanaya@gmail.com",  
    description="A simple tool to track Ethereum gas prices with a GUI",  
    license="MIT",                         
    url="https://github.com/gendisnanaya/ETH-Gas-Tracker-GUI",  
    classifiers=[                           
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
)

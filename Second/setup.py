from distutils.core import setup

setup(name="SecondPkg", 
    version="1.0", 
    description="Second module", 
    author="dongGe", 
    py_modules=['subA.aa', 'subA.bb', 'subB.cc','subB.dd']) 
    # py_modules 需指明所需包含的py文件
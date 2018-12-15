import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='pyqsys',  
     version='0.0',
     author="HanCheng Liu",
     author_email="buaa_cnlhc@buaa.edu.cn",
     description="Altera Quartus Platform Designer (QSys) Helper",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/CNLHC/pyqsys",
     packages=setuptools.find_packages(),
 )

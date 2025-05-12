from setuptools import setup,find_packages

setup(
    name='NetHyTech-Stt_aditya_s',
    version='0.1',
    author='Aditya Sharma',
    author_email='aadityasharma38535@gmail.com',
    description='this is speech to text package created by aditya sharma',
)
packages = find_packages(),
install_requirements = [
    'selenium',
    'webdriver_manager'
]





from setuptools import setup, find_packages

setup(
    name='fashiondata00',
    version='0.1.2',  # 이전보다 높은 버전으로 반드시 설정!
    author='KWON KI YONG',
    author_email='fashiondata00@inu.ac.kr',
    description='Excel-style conditional aggregation with AND/OR logic for pandas',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['pandas'],
    python_requires='>=3.13',
)
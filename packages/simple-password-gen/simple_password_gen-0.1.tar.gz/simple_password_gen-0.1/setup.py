from setuptools import setup, find_packages

setup(
    name='simple_password-gen',
    version='0.1',
    packages=find_packages(),
    description='کتابخانه‌ای ساده برای تولید پسورد تصادفی در پایتون',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/simple_password',  # تغییر بده در صورت نیاز
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)

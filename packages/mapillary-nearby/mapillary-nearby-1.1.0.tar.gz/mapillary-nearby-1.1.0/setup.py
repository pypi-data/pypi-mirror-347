import setuptools
import distutils.core

setuptools.setup(
    name='mapillary-nearby',
    version="1.1.0",
    author='@readwithai',
    long_description_content_type='text/markdown',
    author_email='talwrii@gmail.com',
    description='Get pictures near an location using mapillary suitable for use as wallpaper.',
    license='MIT',
    keywords='mapilliary,wallpaper,background,nearby',
    url='https://github.com/talwrii/mapillary-nearby',
    packages=["mapillary_nearby"],
    long_description=open('README.md').read(),
    install_requires=["mapillary"],
    entry_points={
        'console_scripts': ['mapillary-nearby=mapillary_nearby.main:main']
    }
)

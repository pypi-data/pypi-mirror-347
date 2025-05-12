from setuptools import setup, find_packages

setup(
    name='monkez_video_input',
    version='0.1.1',
    author='Monkez',
    author_email='tiendelai@gmail.com',
    description='A Python class for streaming video from a camera or a video file. It supports frame resizing, FPS control, and automatic restart of the video stream in case of errors.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['opencv-python'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

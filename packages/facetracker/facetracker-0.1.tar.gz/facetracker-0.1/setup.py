from setuptools import setup, find_packages

setup(
    name="facetracker",
    version="0.1",
    description="Real-time face recognition with live state export.",
    author="Handicate Labs",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "face_recognition",
        "opencv-python",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'facetracker=facetracker.tracker:start_recognition'
        ]
    }
)

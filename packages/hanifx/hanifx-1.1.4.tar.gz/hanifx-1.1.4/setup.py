from setuptools import setup, find_packages

setup(
    name="hanifx",  # প্যাকেজের নাম
    version="1.1.4",  # প্যাকেজের ভার্সন
    description="A Python package for detecting and preventing harmful code execution.",  # প্যাকেজের সংক্ষিপ্ত বর্ণনা
    long_description="""\
        hanifx is a Python package designed for cybersecurity tasks. It provides functionalities for detecting 
        harmful code execution and includes a custom hashing algorithm. The module helps in identifying malicious 
        scripts and preventing potential security threats in Python code. It also includes features specifically 
        for white-hat hacking and provides detailed reports on detected threats, making it a useful tool for developers 
        and security researchers.
    """,  # বিস্তারিত বর্ণনা
    long_description_content_type="text/plain",  # বিস্তারিত বর্ণনা কনটেন্ট টাইপ
    author="Hanif",  # তোমার নাম
    author_email="sajim4653@gmail.com",  # তোমার ইমেইল
    packages=find_packages(),  # প্যাকেজের তালিকা
    install_requires=[  # প্যাকেজের নির্ভরতাগুলি
        # এখানে যদি কোন নির্ভরশীল প্যাকেজ থাকে, তা লিখতে পারো
    ],
    classifiers=[  # প্যাকেজের শ্রেণী
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Python এর মিনিমাম ভার্সন
)

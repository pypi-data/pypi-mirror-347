from setuptools import setup, find_packages

setup(
    name="textbasic",  # 패키지 이름 (pip install 시 사용될 이름)
    version="0.1.3",    # 버전
    packages=find_packages(),  # textbasic 폴더 내 모든 패키지 포함
    include_package_data=True,  # 이 설정을 통해 패키지 내 데이터 파일을 포함시킬 수 있음
    package_data={
        "textbasic.basic": ["dictionary.json"],  # 서브 모듈 안의 JSON 파일을 포함
    },
    install_requires=[ # 패키지 설치 시 같이 설치되도록 설정
        "pandas>=2.2.0",
        "konlpy>=0.6.0",
        "emoji>=2.14.1",
        "pyarrow>=19.0.1"
    ],
    author="Kimyh",
    author_email="kim_yh663927@naver.com",
    description="Text preprocessing package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/Kim-YoonHyun/my_package",  # 깃허브 주소 등
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # 최소 지원할 파이썬 버전
)

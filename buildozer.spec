name: Build Android APK

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.9'

    - name: Install buildozer
      run: |
        pip install --upgrade pip
        pip install buildozer cython

    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y \
          openjdk-17-jdk \
          autoconf \
          libtool \
          pkg-config \
          zlib1g-dev \
          libncurses5-dev \
          libncursesw5-dev \
          libtinfo5 \
          cmake \
          libffi-dev \
          libssl-dev

    - name: Build APK
      run: buildozer android debug

    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: KarCul
        path: bin/*.apk
        retention-days: 30
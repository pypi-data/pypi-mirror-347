from setuptools import setup, find_packages

setup(
    name='lstm_reader',
    version='0.1.1',
    description='LSTM-based station passenger flow training and prediction',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'numpy', 'pandas', 'torch', 'scikit-learn'
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'lstm-train=lstm_reader.core:read_train',
            'lstm-predict=lstm_reader.core:read_predict',
        ],
    },
)

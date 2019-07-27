from distutils.core import setup
setup(
  name = 'baghchal',  
  packages = ['baghchal'],
  version = '0.1',
  license='MIT',
  description = 'baghchal is a pure Python Bagh Chal library that supports game import, move generation, move validation and board image rendering. It also comes with a simple engine based on minimax algorithm and alpha-beta pruning.',
  author = 'Soyuj Jung Basnet',
  author_email = 'bsoyuj@gmail.com',
  url = 'https://github.com/basnetsoyuj/baghchal',
  download_url = 'https://github.com/basnetsoyuj/baghchal/archive/v_0.1.tar.gz',
  keywords = ['Bagh Chal', 'game environment', 'board game'],
  install_requires=[
          'numpy',
          'Pillow',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',

  ],
)
from setuptools import setup

setup(
      name="itunes_to_spotify",
      version="0.1",
      author_email="samryan@seas.upenn.edu",
      packages=['itunes_to_spotify_package'],
      install_requires=[
        'spotipy',
        'Click'
      ],
      entry_points={
        'console_scripts':
        ['itunes_to_spotify = itunes_to_spotify_package.main:main']
      }
)

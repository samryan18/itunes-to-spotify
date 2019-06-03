from setuptools import setup

setup(
      name="itunes_to_spotify",
      version="0.1",
      author_email="samuelryan18@gmail.com",
      packages=['itunes_to_spotify_package'],
      python_requires='>=3.4',
      install_requires=[
        'spotipy @ git+https://github.com/plamere/spotipy.git#egg=spotipy',
        'Click',
      ],
      entry_points={
        'console_scripts':
        ['itunes_to_spotify = itunes_to_spotify_package.main:main_overwrite',
        'itunes_to_spotify_new = itunes_to_spotify_package.main:main_new_playlist']
      }
)

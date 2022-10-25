# About this project
A collection of scripts that can:
- Generate data for complex functions
- Plot them in 3D using domain coloring
- Create animations of rotating the resulting 3D graph around different axes

## Example output using the Riemann-Zeta function (default function in this project)

<p align="center">
  <img src="./readme_images/riemann_zeta.gif" width="500" />
</p>

## :hammer_and_wrench: Setup/ Preparation
```bash
pipenv install --ignore-pipfile --skip-lock --python 3.8
pipenv shell
```
If faced by `UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.`
```bash
sudo apt-get install python3.8-tk
```
Make sure `ffmpeg` is installed to be able to create animated 3D plots

## :hammer_and_wrench: Config file
You can edit `config.ini` as necessary to specify different configurations such as function input intervals, whether to plot data in polar form or not..

## :rocket: Usage examples:
#### Run everything as a pipeline
```bash
python run_pipeline.py
```
#### Generate plot data only
```bash
python generate_complex_function_data.py
```
#### Plot or generate frames for already available data
```bash
python plot_complex_function_data.py
```
#### Create animation from already available frame data
```bash
python ffmpeg_create_video.py
```

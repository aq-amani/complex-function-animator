import generate_complex_function_data as data
import plot_complex_function_data as plotter

import configparser

header = """
+-----------------------------+
| (c) 2022 Amani AbuQdais     |
| https://github.com/aq-amani |
+-----------------------------+
"""

def main():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    create_frames = config.getboolean('PLOTTER', 'CREATE_FRAMES')

    print(header)
    print('Running pipeline according to config.ini settings..')
    if create_frames:
        print('Will generate complex function data and create a rotation animation video..')
    else:
        print('Will generate complex function data and view the plot..')

    data.generate_complex_data()
    plotter.plot_complex_data()

    if create_frames:
        import ffmpeg_create_video as video
        video.main()

if __name__ == '__main__':
    main()

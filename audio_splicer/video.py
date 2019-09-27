import ffmpeg

in_file = ffmpeg.input('input.mp4')
(
    ffmpeg
    .concat(
        in_file.trim(start=0, end=1),
        in_file.trim(start=100, end=101),
    )
    .output('out.mp4')
    .run()
)



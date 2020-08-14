"""
Example of using ImageMagick to create a collage out of 9 images.
"""

import os
import subprocess as sp

this_path = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(this_path, "example_collage_images")
output_path = os.path.join(this_path, "example_output")

images = [
    image_filename
    for image_filename in os.listdir(image_path)
    if not image_filename[0] == "."
    and not os.path.isdir(os.path.join(image_path, image_filename))
]

for col in range(3):
    sp.call(
        ["convert"]
        + [
            os.path.join(image_path, image_filename)
            for image_filename in images[3 * col : 3 + 3 * col]
        ]
        + ["-append", os.path.join(output_path, f"col_{col}.png")]
    )

sp.call(
    ["convert"]
    + [os.path.join(output_path, f"col_{col}.png") for col in range(3)]
    + ["+append", os.path.join(output_path, "collage.png")]
)

#!/usr/bin/env python

import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

class RunText:
    def __init__(self, rows=32, cols=64, pwm_lsb_nanoseconds=50, gpio_slowdown=2, color="255,255,0", speed=0.009, brightness=0.5):
        self.options = RGBMatrixOptions()
        self.options.rows = rows
        self.options.cols = cols
        self.options.pwm_lsb_nanoseconds = pwm_lsb_nanoseconds
        self.options.gpio_slowdown = gpio_slowdown
        
        # Add the pixel mapper option to rotate the display by 180 degrees
        self.options.pixel_mapper_config = "Rotate:180"

        self.matrix = RGBMatrix(options=self.options)
        
        # Adjust the brightness of the color
        self.color = tuple(int(c * brightness) for c in map(int, color.split(',')))
        self.speed = speed

    def render_text(self, text):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("fonts/spleen-16x32.bdf")
        text_color = graphics.Color(*self.color)

        pos = offscreen_canvas.width
        while True:
            offscreen_canvas.Clear()
            length = graphics.DrawText(offscreen_canvas, font, pos, 23, text_color, text)
            pos -= 1
            if (pos + length < 0):
                break
            time.sleep(self.speed)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Display text on an RGB matrix.')
    parser.add_argument('text', type=str, help='Text to display on the matrix')
    parser.add_argument('--brightness', type=float, default=0.5, help='Set text brightness (0.0 to 1.0)')
    args = parser.parse_args()

    run_text = RunText(brightness=args.brightness)
    run_text.render_text(args.text)

if __name__ == "__main__":
    main()

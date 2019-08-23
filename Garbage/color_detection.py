from numpy import array
from PIL import Image
from urllib.request import urlopen


class ColorFind():
    link = None
    colors = dict()

    def __init__(self, link):
        self.link = link
        self.build_color_dict()
        pass

    def build_color_dict(self):
        self.colors['black'] = [0, 0, 0]
        self.colors['white'] = [255, 255, 255]
        self.colors['red'] = [255, 0, 0]
        self.colors['blue'] = [0, 0, 255]
        self.colors['yellow'] = [255, 255, 0]
        self.colors['maroon'] = [128, 0, 0]
        self.colors['olive'] = [128, 128, 0]
        self.colors['green'] = [0, 128, 0]
        self.colors['purple'] = [128, 0, 128]
        self.colors['navy'] = [0, 0, 128]

    def doFind(self):
        img = Image.open(urlopen(self.link))
        # img = Image.open('im9.jpg')
        # img.show()
        print(img.format, img.size, img.mode)
        imarray = array(img)
        r_sum = 0
        g_sum = 0
        b_sum = 0
        cnt = 0
        for px_row in imarray:
            for px in px_row:
                # print(px)
                cnt+= 1
                r_sum += px[0]
                g_sum += px[1]
                b_sum += px[2]

        height = img.size[0]
        width = img.size[1]
        rgb_sum = height*width

        # r_avg = r_sum / rgb_sum
        # g_avg = g_sum / rgb_sum
        # b_avg = b_sum / rgb_sum

        r_avg = r_sum - int(r_sum/255) * 255
        g_avg = g_sum - int(g_sum/255) * 255
        b_avg = b_sum - int(b_sum/255) * 255

        print(r_avg, g_avg, b_avg)
        mn_dif = float('inf')
        its_color = None
        for clr in self.colors:
            r, g, b = self.colors[clr]
            r = r - int(r / 255) * 255
            g = g - int(g / 255) * 255
            b = b - int(b / 255) * 255

            # rgb = r + g+ b
            # if rgb > 0:
            #     r /= rgb
            #     g /= rgb
            #     b /= rgb
            # print(r, g, b, ' : '+ clr)
            df = (r_avg - r)**2 + (g_avg - g)**2 + (b_avg - b)**2
            if mn_dif > df:
                its_color = clr
                mn_dif = df

        return its_color


if __name__ == '__main__':
    cf = ColorFind('https://lh3.googleusercontent.com/-W1OKM2eVj4s/XV6PoqTZG2I/AAAAAAAAGaw/syznzrw7Hl4inGNoY1h7gf3QfFPUWPaxACK8BGAs/s0/2019-08-22.jpg?fbclid=IwAR04NoroADCNi9EB0q5b-7HGteZHzBfXdXYNLFzWSksveUJeRiCLXT87_4I').doFind()
    print(cf)
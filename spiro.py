import argparse
import math
import random
import turtle
from datetime import datetime
from PIL import Image
import sys


class Spiro:
    def __init__(self, xc, yc, col, R, r, l):
        print("Spiro Constructor")
        self.t = turtle.Turtle()
        self.t.shape('turtle')
        self.step = 5
        self.drawingComplete = False
        self.setparams(xc, yc, col, R, r, l)
        self.restart()

    def setparams(self, xc, yc, col, R, r, l):
        print("Spiro Setparams")
        self.xc = xc
        self.yc = yc
        self.col = col
        self.R = int(R)
        self.r = int(r)
        self.l = l
        gcdVal = math.gcd(self.r, self.R)
        self.nRot = self.r//gcdVal
        self.k = r/float(R)
        self.t.color(*col)
        self.a = 0

    def restart(self):
        print("Spiro Restart")
        self.drawingComplete = False

        self.t.showturtle()
        self.t.up()
        R,k,l = self.R, self.k, self.l
        a = 0.0
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()


    def draw(self):
        print("Spiro draw")
        R,k,l = self.R, self.k, self.l
        for i in range(0, 360*self.nRot + 1, self.step):
            a = math.radians(i)
            x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
            y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
            self.t.setpos(self.xc + x, self.yc + y)
        self.t.hideturtle()

    def update(self):
        print("Spiro Update")
        if self.drawingComplete:
            return
        self.a += self.step
        R, k, l = self.R, self.k, self.l
        a = math.radians(self.a)
        x = self.R*((1-k) * math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = self.R*((1-k) * math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        if self.a >= 360*self.nRot:
            self.drawingComplete = True
            self.t.hideturtle()

    def clear(self):
        self.t.clear()

class SpiroAnimator:
    def __init__(self, N):
        self.deltaT = 10
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        self.spiros = []
        for i in range(N):
            print("SpiroAnimator Constructor")
            rparams = self.genRandomParams()
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)
        turtle.ontimer(self.update, self.deltaT)

    def genRandomParams(self):
        width,height = self.width, self.height
        R = random.randint(50, min(width, height)//2)
        r = random.randint(10, 9*R//10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width//2, width//2)
        yc = random.randint(-height//2, height//2)
        col = (random.random(),
               random.random(),
               random.random())
        print("SpiroAnimator getRandom", (xc, yc, col, R, r, l))
        return (xc, yc, col, R, r, l)

    def restart(self):
        print("SpiroAnimator Restart")
        for spiro in self.spiros:
            spiro.clear()
            rparams = self.genRandomParams()
            spiro.setparams(*rparams)
            spiro.restart()

    def update(self):
        print("SpiroAnimator Update")
        nComplete = 0
        for spiro in self.spiros:
            spiro.update()
            if spiro.drawingComplete:
                nComplete += 1
        if nComplete == len(self.spiros):
            self.restart()
        turtle.ontimer(self.update, self.deltaT)

    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()

def saveDrawing():
    turtle.hideturtle()
    dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
    fileName = 'spiro-' + dateStr
    print('saving drawing to %s.eps/png' % fileName)
    canvas = turtle.getcanvas()
    canvas.postscript(file = fileName + '.eps')
    img = Image.open(fileName + '.eps')
    img.save(fileName + '.png', 'png')
    turtle.showturtle()

def main():
    print('genrating spirography...')
    descStr = """This program draws Spirographs using the Turtle module.
    When run with no arguments, this program draws randow Sporographs.
    
    Terminology:
    
    R: radius of outer circle
    r: radius of inner circle
    l: ratio of hole distance to r
    """
    parser = argparse.ArgumentParser(description=descStr)

    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False,
                        help="The three arguments in sparams: R, r, l.")

    args = parser.parse_args()

    turtle.setup(width=0.8)
    turtle.shape('turtle')
    turtle.title('Spirographs!')
    turtle.onkey(saveDrawing, "s")
    turtle.listen()
    turtle.hideturtle()

    if args.sparams:
        params = [float(x) for x in args.sparams]
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0,0,col, *params)
        spiro.draw()
    else:
        spiroAnim = SpiroAnimator(4)
        turtle.onkey(spiroAnim.toggleTurtles, "t")
        turtle.onkey(spiroAnim.restart, "space")

    turtle.mainloop()

if __name__ == '__main__':
    main()

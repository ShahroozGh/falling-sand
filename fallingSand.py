import tkinter as tk

class MainWindow:
	def __init__(self, root):
		self.root = root
		#root = tk.Tk()

		self.PIXEL_SIZE = 10
		self.WINDOW_SIZE = 700

		self.world = World(self.WINDOW_SIZE, self.PIXEL_SIZE) #Contains particles and does physics calcs (Pysics does not neet to worry about graphics)

		self.initGui()
		

		self.gameLoop(root)#Will run on seperate thread(Not really), after meathod will decide when called
		self.root.mainloop()#Tkinter event loop

	#Initialize tkinter widgets and components
	def initGui(self):
		self.frame = tk.Frame(bg="white")
		self.frame.pack()

		self.canvas = tk.Canvas(self.frame, bg="black", width = self.WINDOW_SIZE, height = self.WINDOW_SIZE)
		self.canvas.pack()

		#Bind button listners to respond to clicks on canvas
		self.canvas.bind("<Button-1>", self.canvasClicked)
		self.canvas.bind("<B1-Motion>", self.canvasClicked)

	def gameLoop(self, root):
		print("Loop")
		self.world.updateWorld() #Maybe update and paint at the same time so iteration only has to be don once
		self.paint(self.world)
		self.job = self.root.after(100, self.gameLoop, root)

	def paint(self, world):
		print("Paint")
		self.canvas.delete(tk.ALL)
		#get array from world and iterate
			#if blah paint blah at xy
		for x in range(int(self.WINDOW_SIZE/self.PIXEL_SIZE)):
			for y in range(int(self.WINDOW_SIZE/self.PIXEL_SIZE)):
				if world.particleArray[x][y].pType == 1:
					self.canvas.create_rectangle(x * self.PIXEL_SIZE, y * self.PIXEL_SIZE, x * self.PIXEL_SIZE + self.PIXEL_SIZE, y * self.PIXEL_SIZE + self.PIXEL_SIZE, fill = "brown")

	def canvasClicked(self, event):
		print("CLick: " + str(event.x) + ", " + str(event.y))
		xTile = (event.x - (event.x % 10)) / 10
		yTile = (event.y - (event.y % 10)) / 10

class World:
	def __init__(self, WINDOW_SIZE, PIXEL_SIZE):
		self.WINDOW_SIZE = WINDOW_SIZE
		self.PIXEL_SIZE = PIXEL_SIZE

		self.particleArray = [[Particle(x,y,0) for y in range(int(WINDOW_SIZE/PIXEL_SIZE))] for x in range(int(WINDOW_SIZE/PIXEL_SIZE))]

	#Simulate next step
	def updateWorld():
		print("Update")
		#iterate through particles
		#move particles

class Particle:
	#Dont use ints and strings, use smaller, maybe bitmask?
	#may not need x, y (determined by position in 2d array)
	def __init__(self, x = 0, y = 0, pType = 0, movedFlag = False):
		self.x = x
		self.y = y
		self.pType = pType
		self.movedFlag = False

#Entry point
def main():
	root = tk.Tk()
	app = MainWindow(root)

if __name__ == "__main__":main()

import tkinter as tk
import random
import time

class MainWindow:
	def __init__(self, root):
		self.root = root
		#root = tk.Tk()

		self.frameCount = 0
		self.frameRate = 0

		self.PIXEL_SIZE = 5
		self.WINDOW_SIZE = 700

		self.selectedElement = 0

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

		self.elementSbox = tk.Spinbox(self.frame, from_ = 0, to = 4, repeatdelay = 100, repeatinterval = 100, command = self.newElementSelected)
		self.elementSbox.pack()

		self.frameRateL = tk.Label(self.frame, text = "0", font = ("Helvetica", 10))
		self.frameRateL.pack(side = tk.LEFT)

		#Bind button listners to respond to clicks on canvas
		self.canvas.bind("<Button-1>", self.canvasClicked)
		self.canvas.bind("<B1-Motion>", self.canvasClicked)

	def gameLoop(self, root):
		print("Loop")
		t0 = time.clock()
		self.world.updateWorld() #Maybe update and paint at the same time so iteration only has to be don once
		self.paint(self.world)
		t1 = time.clock()
		self.frameCount += 1

		self.frameRate = 1.0/(t1 - t0 + 0.01)
		self.frameRateL.config(text = "FPS:" + str(self.frameRate))
		self.job = self.root.after(10, self.gameLoop, root)

	def paint(self, world):
		print("Paint")
		self.canvas.delete(tk.ALL)
		#get array from world and iterate
			#if blah paint blah at xy
		for x in range(int(self.WINDOW_SIZE/self.PIXEL_SIZE)):
			for y in range(int(self.WINDOW_SIZE/self.PIXEL_SIZE)):
				if world.particleArray[x][y].pType == 1:
					self.canvas.create_rectangle(x * self.PIXEL_SIZE, y * self.PIXEL_SIZE, x * self.PIXEL_SIZE + self.PIXEL_SIZE, y * self.PIXEL_SIZE + self.PIXEL_SIZE, fill = "orange")
				elif world.particleArray[x][y].pType == 64:
					self.canvas.create_rectangle(x * self.PIXEL_SIZE, y * self.PIXEL_SIZE, x * self.PIXEL_SIZE + self.PIXEL_SIZE, y * self.PIXEL_SIZE + self.PIXEL_SIZE, fill = "white")
				elif world.particleArray[x][y].pType == 2:
					self.canvas.create_rectangle(x * self.PIXEL_SIZE, y * self.PIXEL_SIZE, x * self.PIXEL_SIZE + self.PIXEL_SIZE, y * self.PIXEL_SIZE + self.PIXEL_SIZE, fill = "grey")
				elif world.particleArray[x][y].pType == 3:
					self.canvas.create_rectangle(x * self.PIXEL_SIZE, y * self.PIXEL_SIZE, x * self.PIXEL_SIZE + self.PIXEL_SIZE, y * self.PIXEL_SIZE + self.PIXEL_SIZE, fill = "blue")
				elif world.particleArray[x][y].pType == 4:
					self.canvas.create_rectangle(x * self.PIXEL_SIZE, y * self.PIXEL_SIZE, x * self.PIXEL_SIZE + self.PIXEL_SIZE, y * self.PIXEL_SIZE + self.PIXEL_SIZE, fill = "brown")


	def canvasClicked(self, event):
		print("CLick: " + str(event.x) + ", " + str(event.y))

		#convert window pixel coord to tile coord (Determine which tile was clicked)
		xTile = (event.x - (event.x % self.PIXEL_SIZE)) / self.PIXEL_SIZE
		yTile = (event.y - (event.y % self.PIXEL_SIZE)) / self.PIXEL_SIZE

		self.world.addParticle(int(xTile), int(yTile), int(self.selectedElement))

	def newElementSelected(self):
		self.selectedElement = int(self.elementSbox.get())


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class World:
	def __init__(self, WINDOW_SIZE, PIXEL_SIZE):

		#Stores classes to be instantiated (Use to get correct Particle sublclass given pType #)
		self.Elements = [Air,Sand,Stone,Water,Oil]

		self.WINDOW_SIZE = WINDOW_SIZE
		self.PIXEL_SIZE = PIXEL_SIZE

		self.particleArray = [[self.Elements[0](x,y,0) for y in range(int(WINDOW_SIZE/PIXEL_SIZE))] for x in range(int(WINDOW_SIZE/PIXEL_SIZE))]

		#Fill bottom with stone so elements dont fall out of bouds (need logic to make out of bounds particles dissapear)
		for x in range(int(WINDOW_SIZE/PIXEL_SIZE)):
			self.particleArray[x][int(WINDOW_SIZE/PIXEL_SIZE) - 1] = self.Elements[2](x,int(WINDOW_SIZE/PIXEL_SIZE) - 1,64)#64 as type so that its not printed as stone

	#Simulate next step
	def updateWorld(self):
		print("Update")
		#iterate through particles
		#move particles
		#maybe have particles determine movement (pass in array?)

		for x in range(int(self.WINDOW_SIZE/self.PIXEL_SIZE)):
			for y in range(int(self.WINDOW_SIZE/self.PIXEL_SIZE)): #Just call update, no need for check, or 
				if self.particleArray[x][y].pType != 0 and self.particleArray[x][y].pType != 64 and self.particleArray[x][y].movedFlag is False:
					self.particleArray[x][y].update(self.particleArray, self.surroundingParticles(x,y))
		
		for x in range(int(self.WINDOW_SIZE/self.PIXEL_SIZE)):
			for y in range(int(self.WINDOW_SIZE/self.PIXEL_SIZE)):
				self.particleArray[x][y].movedFlag = False

	def addParticle(self, x, y, selectedElement):
		print("Add")
		self.particleArray[x][y] = self.Elements[selectedElement](x, y)

	#move this to particle maybe
	def surroundingParticles(self, x, y):
		particleList = []

		particleList.append(self.particleArray[x-1][y-1])
		particleList.append(self.particleArray[x][y-1])
		particleList.append(self.particleArray[x+1][y-1])

		particleList.append(self.particleArray[x-1][y])
		particleList.append(self.particleArray[x+1][y])

		particleList.append(self.particleArray[x-1][y+1])
		particleList.append(self.particleArray[x][y+1])
		particleList.append(self.particleArray[x+1][y+1])

		# [0,1,2,3,4,5,6,7]
		#
		# 0 1 2
		# 3 X 4
		# 5 6 7
		#
		
		return particleList


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Particle:
	#Dont use ints and strings, use smaller, maybe bitmask?
	#may not need x, y (determined by position in 2d array)
	def __init__(self, x = 0, y = 0, pType = 0, movedFlag = False):
		self.x = x
		self.y = y
		self.pType = pType
		self.movedFlag = False

		
		#Default Properties
		self.gravity = 1 #1 for normal gravity, -1 for floating, 0 for immovable
		self.isSolid = False #For immovable objects such as stone
		self.isPowder = False #Powders have infinite density, sink below all liquids, stack with other powders
		self.isLiquid = False #Liquids like powders but have varying densities(can float), stacking depends on density
		self.density = 1.0 #Density of liquid, with 1 being a powder, always sinks


	def update(self, particleArray, neighbourList):
		#if air below
		if neighbourList[6].pType == 0:
			self.swap(self.x, self.y, neighbourList[6].x, neighbourList[6].y, particleArray)
		elif neighbourList[6].pType == 63:
			self.replaceWithAir()
			#if opaque
		elif neighbourList[6].pType == 64 or neighbourList[6].pType == 1:
			
			if neighbourList[5].pType == 0 and neighbourList[5].pType == 0:
				if random.randint(0,1) == 1:
					self.swap(self.x, self.y, neighbourList[5].x, neighbourList[5].y, particleArray)
				else:
					self.swap(self.x, self.y, neighbourList[7].x, neighbourList[7].y, particleArray)

			if neighbourList[5].pType == 0:
					self.swap(self.x, self.y, neighbourList[5].x, neighbourList[5].y, particleArray)
			if neighbourList[7].pType == 0:
					self.swap(self.x, self.y, neighbourList[7].x, neighbourList[7].y, particleArray)





	def swap(self, initX, initY, finX, finY, particleArray):
		self.movedFlag = True
		particleArray[finX][finY].movedFlag = True


		tempX = particleArray[finX][finY].x
		particleArray[finX][finY].x = self.x
		self.x = tempX

		tempY = particleArray[finX][finY].y
		particleArray[finX][finY].y = self.y
		self.y = tempY

		temp = particleArray[finX][finY]
		particleArray[finX][finY] = particleArray[initX][initY]
		particleArray[initX][initY] = temp

	def replaceWithAir(self):
		self.pType = 0

#-----------------------------------------------------------------------------------------------------
#maybe have a liquid and powder class (extended from particle) which respective elements extend,
class Air(Particle):
	def __init__(self, x, y, pType = 0, movedFlag = False):
		Particle.__init__(self, x, y, pType, movedFlag)
		self.gravity = 0 
		self.isSolid = False 
		self.isPowder = False 
		self.isLiquid = False 
		self.density = 0.0 

	def update(self, particleArray, neighbourList):
		pass

class Sand(Particle):
	def __init__(self, x, y, pType = 1, movedFlag = False):
		Particle.__init__(self, x, y, pType, movedFlag)
		self.gravity = 0 
		self.isSolid = False 
		self.isPowder = True 
		self.isLiquid = False 
		self.density = 1.0 

	def update(self, particleArray, neighbourList): #Maybe move gravity logic up to Particle in own method, will be used alot
		#Gravity logic
		#if air below
		if neighbourList[6].pType == 0 or neighbourList[6].isLiquid:
			self.swap(self.x, self.y, neighbourList[6].x, neighbourList[6].y, particleArray)
		#if Out of bounds (doesnt exist now, using 64 for stone, will change 64 to oob later)
		elif neighbourList[6].pType == 63:
			self.replaceWithAir()
		#if powder below
		elif neighbourList[6].isPowder or neighbourList[6].isSolid:
			#check if left or right is open and move if so
			if neighbourList[5].pType == 0 and neighbourList[7].pType == 0:
				if random.randint(0,1) == 1:
					self.swap(self.x, self.y, neighbourList[5].x, neighbourList[5].y, particleArray)
				else:
					self.swap(self.x, self.y, neighbourList[7].x, neighbourList[7].y, particleArray)

			elif neighbourList[5].pType == 0:
					self.swap(self.x, self.y, neighbourList[5].x, neighbourList[5].y, particleArray)
			elif neighbourList[7].pType == 0:
					self.swap(self.x, self.y, neighbourList[7].x, neighbourList[7].y, particleArray)

class Stone(Particle):
	def __init__(self, x, y, pType = 2, movedFlag = False):
		Particle.__init__(self, x, y, pType, movedFlag)
		self.gravity = 0
		self.isSolid = True
		self.isPowder = False
		self.isLiquid = False

	def update(self, particleArray, neighbourList):
		pass

class Water(Particle):
	def __init__(self, x, y, pType = 3, movedFlag = False):
		Particle.__init__(self, x, y, pType, movedFlag)
		self.gravity = 1 
		self.isSolid = False 
		self.isPowder = False 
		self.isLiquid = True 
		self.density = 0.5 

	def update(self, particleArray, neighbourList):
		#Gravity logic
		#if air below or less dense liquid
		if neighbourList[6].pType == 0 or neighbourList[6].density < self.density:
			self.swap(self.x, self.y, neighbourList[6].x, neighbourList[6].y, particleArray)
		#if Out of bounds (doesnt exist now, using 64 for stone, will change 64 to oob later)
		elif neighbourList[6].pType == 63:
			self.replaceWithAir()

		#if powder below or solid, or more dense (if more dense treat as solid)
		elif neighbourList[6].isPowder or neighbourList[6].isSolid or neighbourList[6].density >= self.density:
			#check if left or right is open and move if so (Checks for air in text space, should check density instead? This way it will work if a liquid is in another less dense liquid
			if neighbourList[5].density < self.density and neighbourList[7].density < self.density:
				if random.randint(0,1) == 1:
					self.swap(self.x, self.y, neighbourList[5].x, neighbourList[5].y, particleArray)
				else:
					self.swap(self.x, self.y, neighbourList[7].x, neighbourList[7].y, particleArray)

			elif neighbourList[5].density < self.density:
					self.swap(self.x, self.y, neighbourList[5].x, neighbourList[5].y, particleArray)
			elif neighbourList[7].density < self.density:
					self.swap(self.x, self.y, neighbourList[7].x, neighbourList[7].y, particleArray)

class Oil(Particle):
	def __init__(self, x, y, pType = 4, movedFlag = False):
		Particle.__init__(self, x, y, pType, movedFlag)
		self.gravity = 1 
		self.isSolid = False 
		self.isPowder = False 
		self.isLiquid = True 
		self.density = 0.1 

	def update(self, particleArray, neighbourList):
		#Gravity logic
		#if air below or less dense liquid
		if neighbourList[6].pType == 0 or neighbourList[6].density < self.density:
			self.swap(self.x, self.y, neighbourList[6].x, neighbourList[6].y, particleArray)
		#if Out of bounds (doesnt exist now, using 64 for stone, will change 64 to oob later)
		elif neighbourList[6].pType == 63:
			self.replaceWithAir()

		#if powder below or solid, or more dense (if more dense treat as solid)
		elif neighbourList[6].isPowder or neighbourList[6].isSolid or neighbourList[6].density >= self.density:
			#check if left or right is open and move if so (Checks for air in text space, should check density instead? This way it will work if a liquid is in another less dense liquid
			if neighbourList[5].density < self.density and neighbourList[7].density < self.density:
				if random.randint(0,1) == 1:
					self.swap(self.x, self.y, neighbourList[5].x, neighbourList[5].y, particleArray)
				else:
					self.swap(self.x, self.y, neighbourList[7].x, neighbourList[7].y, particleArray)

			elif neighbourList[5].pType == 0:
					self.swap(self.x, self.y, neighbourList[5].x, neighbourList[5].y, particleArray)
			elif neighbourList[7].pType == 0:
					self.swap(self.x, self.y, neighbourList[7].x, neighbourList[7].y, particleArray)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Entry point
def main():
	root = tk.Tk()
	app = MainWindow(root)

if __name__ == "__main__":main()

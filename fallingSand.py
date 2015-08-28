import tkinter as tk
import random
import time

class MainWindow:
	def __init__(self, root):
		self.root = root
		#root = tk.Tk()

		self.frameCount = 0
		self.frameRate = 0
		self.physicsTime = 0
		self.paintTime = 0
		self.totalProcessTime = 0

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

		self.elementSbox = tk.Spinbox(self.frame, from_ = 0, to = 6, repeatdelay = 100, repeatinterval = 100, command = self.newElementSelected)
		self.elementSbox.pack()

		self.frameRateL = tk.Label(self.frame, text = "0", font = ("Helvetica", 10), anchor = "nw")
		self.frameRateL.pack(side = tk.LEFT)

		self.initCanvasTiles(self.WINDOW_SIZE, self.PIXEL_SIZE)

		#Bind button listners to respond to clicks on canvas
		self.canvas.bind("<Button-1>", self.canvasClicked)
		self.canvas.bind("<B1-Motion>", self.canvasClicked)

	def gameLoop(self, root):
		print("Loop")
		
		tt0 = time.clock()#Start total timer

		pht0 = time.clock()#time physics calcs
		self.world.updateWorld() #Maybe update and paint at the same time so iteration only has to be don once
		pht1 = time.clock()

		pt0 = time.clock()#time paint calcs
		self.paint(self.world)
		pt1 = time.clock()

		tt1 = time.clock()
		self.frameCount += 1

		self.physicsTime = pht1 - pht0
		self.paintTime = pt1 - pt0
		self.totalProcessTime = tt1 - tt0

		self.frameRate = 1.0/(self.totalProcessTime + 0.01)
		self.frameRateL.config(text = "FPS:" + str(self.frameRate) + "\n" + "Phys Time:" + str(self.physicsTime*1000) + "\n" + "Paint Time:" + str(self.paintTime*1000) + "\n" + "Total Time:" + str(self.totalProcessTime*1000))
		self.job = self.root.after(10, self.gameLoop, root)

	def initCanvasTiles(self, WINDOW_SIZE, PIXEL_SIZE):
		self.canvasTiles = [[self.canvas.create_rectangle(x * self.PIXEL_SIZE, y * self.PIXEL_SIZE, x * self.PIXEL_SIZE + self.PIXEL_SIZE, y * self.PIXEL_SIZE + self.PIXEL_SIZE, fill = "black") for y in range(int(WINDOW_SIZE/PIXEL_SIZE))] for x in range(int(WINDOW_SIZE/PIXEL_SIZE))]

	def paint(self, world):
		print("Paint")
		# self.canvas.delete(tk.ALL)
		# #get array from world and iterate
		# 	#if blah paint blah at xy
		# for x in range(int(self.WINDOW_SIZE/self.PIXEL_SIZE)):
		# 	for y in range(int(self.WINDOW_SIZE/self.PIXEL_SIZE)):
		# 		if world.particleArray[x][y].pType == 1:
		# 			self.canvas.create_rectangle(x * self.PIXEL_SIZE, y * self.PIXEL_SIZE, x * self.PIXEL_SIZE + self.PIXEL_SIZE, y * self.PIXEL_SIZE + self.PIXEL_SIZE, fill = "#F0C002")
		# 		elif world.particleArray[x][y].pType == 64:
		# 			self.canvas.create_rectangle(x * self.PIXEL_SIZE, y * self.PIXEL_SIZE, x * self.PIXEL_SIZE + self.PIXEL_SIZE, y * self.PIXEL_SIZE + self.PIXEL_SIZE, fill = "white")
		# 		elif world.particleArray[x][y].pType == 2:
		# 			self.canvas.create_rectangle(x * self.PIXEL_SIZE, y * self.PIXEL_SIZE, x * self.PIXEL_SIZE + self.PIXEL_SIZE, y * self.PIXEL_SIZE + self.PIXEL_SIZE, fill = "grey")
		# 		elif world.particleArray[x][y].pType == 3:
		# 			self.canvas.create_rectangle(x * self.PIXEL_SIZE, y * self.PIXEL_SIZE, x * self.PIXEL_SIZE + self.PIXEL_SIZE, y * self.PIXEL_SIZE + self.PIXEL_SIZE, fill = "blue")
		# 		elif world.particleArray[x][y].pType == 4:
		# 			self.canvas.create_rectangle(x * self.PIXEL_SIZE, y * self.PIXEL_SIZE, x * self.PIXEL_SIZE + self.PIXEL_SIZE, y * self.PIXEL_SIZE + self.PIXEL_SIZE, fill = "#8C3A00")
		# 		elif world.particleArray[x][y].pType == 5:
		# 			self.canvas.create_rectangle(x * self.PIXEL_SIZE, y * self.PIXEL_SIZE, x * self.PIXEL_SIZE + self.PIXEL_SIZE, y * self.PIXEL_SIZE + self.PIXEL_SIZE, fill = "#BDEEFF") #Light bluish grey 
		# 		elif world.particleArray[x][y].pType == 6:
		# 			self.canvas.create_rectangle(x * self.PIXEL_SIZE, y * self.PIXEL_SIZE, x * self.PIXEL_SIZE + self.PIXEL_SIZE, y * self.PIXEL_SIZE + self.PIXEL_SIZE, fill = "#2BA6CF")

		for x in range(int(self.WINDOW_SIZE/self.PIXEL_SIZE)):
			for y in range(int(self.WINDOW_SIZE/self.PIXEL_SIZE)):
				if world.particleArray[x][y].pType == 1:
					self.canvas.itemconfig(self.canvasTiles[x][y], fill = "#F0C002")
				elif world.particleArray[x][y].pType == 64:
					self.canvas.itemconfig(self.canvasTiles[x][y], fill = "white")
				elif world.particleArray[x][y].pType == 2:
					self.canvas.itemconfig(self.canvasTiles[x][y], fill = "grey")
				elif world.particleArray[x][y].pType == 3:
					self.canvas.itemconfig(self.canvasTiles[x][y], fill = "blue")
				elif world.particleArray[x][y].pType == 4:
					self.canvas.itemconfig(self.canvasTiles[x][y], fill = "#8C3A00")
				elif world.particleArray[x][y].pType == 5:
					self.canvas.itemconfig(self.canvasTiles[x][y], fill = "#BDEEFF")#Light bluish grey 
				elif world.particleArray[x][y].pType == 6:
					self.canvas.itemconfig(self.canvasTiles[x][y], fill = "#2BA6CF")
				elif world.particleArray[x][y].pType == 0:
					self.canvas.itemconfig(self.canvasTiles[x][y], fill = "black")


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
		self.Elements = [Air,Sand,Stone,Water,Oil,Ice,Spout]

		self.WINDOW_SIZE = WINDOW_SIZE
		self.PIXEL_SIZE = PIXEL_SIZE

		self.particleArray = [[self.Elements[0](x,y,0) for y in range(int(WINDOW_SIZE/PIXEL_SIZE))] for x in range(int(WINDOW_SIZE/PIXEL_SIZE))]

		#Fill boundary with stone so elements dont fall out of bouds (need logic to make out of bounds particles dissapear)
		for x in range(int(WINDOW_SIZE/PIXEL_SIZE)):
			self.particleArray[x][int(WINDOW_SIZE/PIXEL_SIZE) - 1] = Boundary(x,int(WINDOW_SIZE/PIXEL_SIZE) - 1,64)#64 as type so that its not printed as stone
			self.particleArray[x][0] = Boundary(x,0,64)#64 as type so that its not printed as stone
		for y in range(int(WINDOW_SIZE/PIXEL_SIZE)):
			self.particleArray[int(WINDOW_SIZE/PIXEL_SIZE) - 1][y] = Boundary(int(WINDOW_SIZE/PIXEL_SIZE) - 1, y,64)#64 as type so that its not printed as stone
			self.particleArray[0][y] = Boundary(0, y,64)#64 as type so that its not printed as stone

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
		self.particleArray[x][y] = self.Elements[selectedElement](x, y, selectedElement)

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


		#Pass this in instead from world
		self.Elements = [Air,Sand,Stone,Water,Oil,Ice,Spout]

		
		#Default Properties
		self.gravity = 1 #1 for normal gravity, -1 for floating, 0 for immovable
		self.isSolid = False #For immovable objects such as stone
		self.isPowder = False #Powders have infinite density, sink below all liquids, stack with other powders
		self.isLiquid = False #Liquids like powders but have varying densities(can float), stacking depends on density
		self.density = 1.0 #Density of liquid, with 1 being a powder, always sinks


	def update(self, particleArray, neighbourList):
		if self.gravity != 0:
			self.updateGravity(particleArray, neighbourList)

		self.particleLogic(particleArray, neighbourList)
		

	def updateGravity(self, particleArray, neighbourList):
		#Gravity logic
		#If boundary below
		if neighbourList[6].pType == 64:
			pass
		#if air below or less dense liquid
		elif neighbourList[6].pType == 0 or neighbourList[6].density < self.density:
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

	#Override to implement custom logic
	def particleLogic(self, particleArray, neighbourList):
		pass



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

	def addParticle(self, x, y, pType, particleArray):
		particleArray[x][y] = self.Elements[pType](x,y,pType)

	#Dont use, only chenges type not class
	def replaceWithAir(self):
		self.pType = 0

#-----------------------------------------------------------------------------------------------------
#maybe have a liquid and powder class (extended from particle) which respective elements extend,
class Air(Particle):
	def __init__(self, x, y, pType = 0, movedFlag = False):
		Particle.__init__(self, x, y, pType, movedFlag)
		#Overridden property variables
		self.gravity = 0 
		self.isSolid = False 
		self.isPowder = False 
		self.isLiquid = False 
		self.density = 0.0 

	#No need to use update function for air so just ovveride
	def update(self, particleArray, neighbourList):
		pass


class Sand(Particle):
	def __init__(self, x, y, pType = 1, movedFlag = False):
		Particle.__init__(self, x, y, pType, movedFlag)
		#Overridden property variables
		self.gravity = 1 
		self.isSolid = False 
		self.isPowder = True 
		self.isLiquid = False 
		self.density = 1.0

	

class Stone(Particle):
	def __init__(self, x, y, pType = 2, movedFlag = False):
		Particle.__init__(self, x, y, pType, movedFlag)
		#Overridden property variables
		self.gravity = 0
		self.isSolid = True
		self.isPowder = False
		self.isLiquid = False



class Water(Particle):
	def __init__(self, x, y, pType = 3, movedFlag = False):
		Particle.__init__(self, x, y, pType, movedFlag)
		#Overridden property variables
		self.gravity = 1 
		self.isSolid = False 
		self.isPowder = False 
		self.isLiquid = True 
		self.density = 0.5

	# def particleLogic(self, particleArray, neighbourList):
	# 	if neighbourList[3].pType == 3 and neighbourList[4].pType == 0:
	# 		self.swap(self.x, self.y, neighbourList[4].x, neighbourList[4].y, particleArray)
	# 	elif neighbourList[4].pType == 3 and neighbourList[3].pType == 0:
	# 		self.swap(self.x, self.y, neighbourList[3].x, neighbourList[3].y, particleArray)


	

class Oil(Particle):
	def __init__(self, x, y, pType = 4, movedFlag = False):
		Particle.__init__(self, x, y, pType, movedFlag)
		#Overridden property variables
		self.gravity = 1 
		self.isSolid = False 
		self.isPowder = False 
		self.isLiquid = True 
		self.density = 0.1

class Ice(Particle):
	def __init__(self, x, y, pType = 5, movedFlag = False):
		Particle.__init__(self, x, y, pType, movedFlag)
		#Overridden property variables
		self.gravity = 0
		self.isSolid = True 
		self.isPowder = False 
		self.isLiquid = False 
		self.density = 1.0

	def particleLogic(self, particleArray, neighbourList):
		
		for particle in neighbourList:
			if particle.pType == 3:
				if random.randint(0,100) == 0:
					self.addParticle(particle.x, particle.y, 5, particleArray)

class Spout(Particle):
	def __init__(self, x, y, pType = 6, movedFlag = False):
		Particle.__init__(self, x, y, pType, movedFlag)
		#Overridden property variables
		self.gravity = 0
		self.isSolid = True 
		self.isPowder = False 
		self.isLiquid = False 
		self.density = 1.0

	def particleLogic(self, particleArray, neighbourList):

		if neighbourList[6].pType == 0:
			if random.randint(0,10) == 0:
				self.addParticle(self.x, self.y + 1, 3, particleArray)
			




class Boundary(Particle):
	def __init__(self, x, y, pType = 64, movedFlag = False):
		Particle.__init__(self, x, y, pType, movedFlag)
		#Overridden property variables
		self.gravity = 0 
		self.isSolid = False 
		self.isPowder = False 
		self.isLiquid = False 
		self.density = 1.0

	#No need to use update function for air so just ovveride
	def update(self, particleArray, neighbourList):
		pass



	
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Entry point
def main():
	root = tk.Tk()
	app = MainWindow(root)

if __name__ == "__main__":main()

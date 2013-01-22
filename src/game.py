#Terrain Editor 1.3

#import statements
import pygame,sys,os
from pygame.locals import *
class Display:
	def __init__(self):
		#map variables
		self.map=pygame.Rect(0,0,800,416)
		self.DIMENSION=32
		self.XLEN=25;self.YLEN=13
		self.squareVIEWX=0;self.squareVIEWY=0
		self.COLORS=[(170,242,170),(178,124,79),(0,102,0),(177,177,177),(144,175,214),(0,102,0),(177,177,177),(144,175,214)] #setup colors
		(self.xmax,self.ymax)=(40,40)

		#self.tile_set variable
		self.tile_set_=open('../tile/tile.txt').readlines()
		for i in range(len(self.tile_set_)):
			self.tile_set_[i]=self.tile_set_[i].strip()
		
		self.tile_set={}
		for i in self.tile_set_:
			self.tile_set[i]=open('../tile/'+i+'/tile.txt').readlines()
			for j in range(len(self.tile_set[i])):
				self.tile_set[i][j]=self.tile_set[i][j].strip()
		for i in self.tile_set:
			for j in range(len(self.tile_set[i])):
				self.tile_set[i][j]=pygame.image.load('../tile/'+i+'/'+self.tile_set[i][j])
		
		#frame variables
		self.minimap_NW=(7,451)
		self.minimap_dimensions=(161,142)

		#self.board
		self.board=[[],[]]
		for i in range(self.xmax):
			self.board[0].append([])
			self.board[1].append([])
			for j in range(self.ymax):
				self.board[0][i].append(0)
				self.board[1][i].append(0)
				

		#pygame setup
		pygame.init()
		mainClock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((800,600))

		#frame setup
		self.frameimage=pygame.image.load('..\\frame\\frame.png')
		self.minimapBack=pygame.Rect(self.minimap_NW[0], self.minimap_NW[1], self.minimap_dimensions[0], self.minimap_dimensions[1])
		self.minimap_front_coor=((self.minimap_dimensions[0]-self.xmax*2)/2+self.minimap_NW[0],(self.minimap_dimensions[1]-self.ymax*2)/2+self.minimap_NW[1])
		self.minimapFront=pygame.Rect(self.minimap_front_coor[0],self.minimap_front_coor[1],self.xmax*2,self.ymax*2)

		while True:
			if True: #display
				pygame.display.set_caption(str(pygame.mouse.get_pos()[0])+' '+str(pygame.mouse.get_pos()[1]))
				#frame display
				self.screen.blit(self.frameimage,(0,0))
				#minimap display
				pygame.draw.rect(self.screen,(0,0,0),self.minimapBack)
				pygame.draw.rect(self.screen,(209,234,211),self.minimapFront)
				#map tiles display
				for i in range(self.YLEN):
					for j in range(self.XLEN):
						self.screen.blit(self.tile_set[self.tile_set_[self.board[0][j+self.squareVIEWX][i+self.squareVIEWY]]][self.board[1][j+self.squareVIEWX][i+self.squareVIEWY]],(j*32,i*32))
				#minimap display
				for i in range(self.xmax):
					for j in range(self.ymax):
						color=self.COLORS[self.board[0][i][j]]
						pixel=pygame.Rect(self.minimap_front_coor[0]+i*2,self.minimap_front_coor[1]+j*2,3,3)
						pygame.draw.rect(self.screen,color,pixel)
				#minimap viewbox
				viewbox={}
				viewbox['top']=pygame.Rect(self.minimap_front_coor[0]+self.squareVIEWX*2, self.minimap_front_coor[1]+self.squareVIEWY*2-1, self.XLEN*2, 2)
				viewbox['bottom']=pygame.Rect(self.minimap_front_coor[0]+self.squareVIEWX*2, self.minimap_front_coor[1]+self.YLEN*2+self.squareVIEWY*2, self.XLEN*2, 2)
				viewbox['left']=pygame.Rect(self.minimap_front_coor[0]+self.squareVIEWX*2, self.minimap_front_coor[1]+self.squareVIEWY*2, 1, self.YLEN*2)
				viewbox['right']=pygame.Rect(self.minimap_front_coor[0]+self.XLEN*2+self.squareVIEWX*2, self.minimap_front_coor[1]+self.squareVIEWY*2, 1, self.YLEN*2)
				for i in viewbox:
					pygame.draw.rect(self.screen, (255,255,255), viewbox[i])
				#update Display
				pygame.display.flip()
			if True: #events process
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit();sys.exit()
					if event.type == MOUSEBUTTONDOWN:
						if True: #save clicked position
							temp=pygame.mouse.get_pos()
							position=(int(temp[0]),int(temp[1]))
							del temp
						
						#clicks map and selects square
						if self.map.collidepoint(position):
							x1=(int((pygame.mouse.get_pos()[0])/self.DIMENSION))
							y1=(int((pygame.mouse.get_pos()[1])/self.DIMENSION))
							if event.button == 1 or event.button == 4 or event.button == 5:
								self.board[0][x1+self.squareVIEWX][y1+self.squareVIEWY]=(self.board[0][x1+self.squareVIEWX][y1+self.squareVIEWY]+1)%len(self.tile_set)
								self.board[1][x1+self.squareVIEWX][y1+self.squareVIEWY]=0
							elif event.button == 3:
								self.board[1][x1+self.squareVIEWX][y1+self.squareVIEWY]=(self.board[1][x1+self.squareVIEWX][y1+self.squareVIEWY]+1)%len(self.tile_set[self.tile_set_[self.board[0][x1+self.squareVIEWX][y1+self.squareVIEWY]]])
								#print(self.board[1][x1+self.squareVIEWX][y1+self.squareVIEWY])
							del x1, y1
						
						#### Change viewbox and Move Map ###
						if position[0]>self.minimap_front_coor[0] and position[0]<self.minimap_front_coor[0]+self.xmax*2 and position[1]>self.minimap_front_coor[1] and position[1]<self.minimap_front_coor[1]+self.ymax*2:
							if int((position[0]-self.minimap_front_coor[0])/2)<self.XLEN/2:
								self.squareVIEWX=0
							elif int((position[0]-self.minimap_front_coor[0])/2)>self.xmax-int(self.XLEN/2)-1:
								self.squareVIEWX=self.xmax-self.XLEN
								#print(self.squareVIEWX)
							else:
								self.squareVIEWX=int((position[0]-self.minimap_front_coor[0])/2)-int(self.XLEN/2)
								#print(self.squareVIEWX)
							if int((position[1]-self.minimap_front_coor[1])/2)<self.YLEN/2:
								self.squareVIEWY=0
							elif int((position[1]-self.minimap_front_coor[1])/2)>self.ymax-int(self.YLEN/2):
								self.squareVIEWY=self.ymax-self.YLEN
							else:
								self.squareVIEWY=int((position[1]-self.minimap_front_coor[1])/2)-int(self.YLEN/2)-1
						
					if event.type == KEYDOWN:
						#### Move map ######################
						if event.key == K_UP:
							if self.squareVIEWY>0:
								self.squareVIEWY-=1
						elif event.key == K_DOWN:
							if self.squareVIEWY<self.ymax-self.YLEN:
								self.squareVIEWY+=1
						elif event.key == K_LEFT:
							if self.squareVIEWX>0:
								self.squareVIEWX-=1
						elif event.key == K_RIGHT:
							if self.squareVIEWX<self.xmax-self.XLEN:
								self.squareVIEWX+=1
Display()
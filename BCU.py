import enum
try:
    import Queue as queue
except ImportError:
    # Python 3
    import queue

class Color( enum.Enum ):
	BLACK = 0 	#Sin descubrir
	GREY  = 1 	#Descubierto (Fue visto por alguno de sus vecinos)
	WHITE = 2 	#Expandido (Que ha descubierto a todos sus vecinos)

	def colorToString( self ):
		if( self == Color.BLACK ):
			return "BLACK"
		if( self == Color.GREY ):
			return "GREY"
		if( self == Color.WHITE ):
			return "WHITE"

class Vertex:
	def __init__( self, name, neighborsList, neighborDistanceList, color, distancePredecessor, predecessorVertex, place ):
		self.name = name 						#Str nombre
		self.neighborsList = []					#Lista de tipo vertex
		self.neighborDistanceList = []			#Lista distacia entre vecinos con mismo orden que la lista de vecinos
		self.color = Color.BLACK 				#Color de busqueda
		self.distancePredecessor = 0 			#Distancia acumulada para busqueda
		self.predecessorVertex = None 			#Vertice predecesor en el arbol de busqueda
		self.place = 0

	def setColor( self, color ):
		self.color = color

	def setDistance( self, distancePredecessor ):
		self.distancePredecessor = distancePredecessor

	def setPredecesor( self, predecessorVertex ):
		self.predecessorVertex = predecessorVertex

	def setPlace( self, place ):
		self.place = place

	def getNamePredecesor( vertex ):
		if( vertex != None ):
			return vertex.name
		else:
			return "without predecessor"

	def printNeighborList( self ):
		print( "Neighbors:  ", end=" " )
		for neighbor  in self.neighborsList:
			print( neighbor.name, end=" " )

	def printVertex( self ):
		print( "Name:        " + self.name )
		self.printNeighborList()
		print( "\nDistance:   ", end=" " )
		for nDistnace  in self.neighborDistanceList:
			print( str( nDistnace ), end=" " )

		print( "\nColor:       " + Color.colorToString( self.color ) )
		print( "Distance:    " + str( self.distancePredecessor ) )
		print( "Predecessor: " + Vertex.getNamePredecesor( self.predecessorVertex ) )
		print( "Place:       " + str( self.place ))
		print( "==============" )

	def isOnNeighborList( self, neighborName ):
		flag = False
		for neighbor in self.neighborsList:
			if( neighbor.name == neighborName ):
				flag = True		
		return flag

	def allGreyNeighbors( self ):
		flag = False
		for n in self.neighborsList:
			if n.color != Color.GREY: 
				return flag
		return True

	def addNeighbor( self, vertex, distance ):
		if( self.isOnNeighborList( vertex.name ) != True ):
			self.neighborsList.append( vertex )
			self.neighborDistanceList.append( distance )
			return True
		else:
			return False

	def discoverVertex( self, predecessorVertex, distance ):
		self.setColor( Color.GREY )
		self.setPredecesor( predecessorVertex )
		self.setDistance( distance )

	def expandVertex( self ):
		self.setColor( Color.WHITE)

class Graph:
	def __init__( self, vertexList ):
		self.vertexList = []

	def isOnVertexList( self, vertexName ):
		flag = False
		for v in self.vertexList:
			if v.name == vertexName : 
				flag = True
		
		return flag

	def findVertex( self, vertexName ):
		vertex = None
		for v in self.vertexList:
			if v.name == vertexName :
				vertex = v

		return vertex

	def addVertex( self, vertexName ):
		if self.isOnVertexList( vertexName ) != True :
			self.vertexList.append( Vertex( vertexName, None, None, None, None, None, None ) )
			return True
		else:
			return False

	def addAxis( self, vName, uName, distance ):
		v = self.findVertex( vName )
		u = self.findVertex( uName )
		#Verificar que ambos vertices estan dentro del grafo
		if ( v != None ) and ( u != None ) :
			if ( v.isOnNeighborList( uName ) != True ) and ( u.isOnNeighborList( vName ) != True  ):
				v.addNeighbor( u, distance )
				u.addNeighbor( v, distance )
				return True

		return False

	def printGraph( self ):
		for v in self.vertexList:
			v.printVertex()

	def bubbleSort( queue ):
		lst = []
		while queue.empty() != True:
				lst.append( queue.get() )

		done = False

		i = 0
		while i < len( lst ) - 1 and done == False :
			done = True
			j = len( lst ) - 1
			while j > i:
				if lst[ j-1 ].distancePredecessor > lst[ j ].distancePredecessor :
					tmpV = lst[ j-1 ]
					lst[ j-1 ] = lst[ j ]
					lst[ j ] = tmpV
				j -= 1
			i += 1

		return lst

	def printRout( self, startVertex, endVertex ):
		print( "*****MEJOR RUTA*****" )
		print( "INICIO: ", startVertex.name )
		print( "FIN:    ", endVertex.name )

		tmpVertexList = []
		tmpVertex = endVertex
		while tmpVertex != None:
			tmpVertexList.append( tmpVertex )
			tmpVertex = tmpVertex.predecessorVertex

		i = len( tmpVertexList ) - 1 
		while i != -1 :
			v = tmpVertexList[ i ]
			v.printVertex()
			i -= 1

	def UCS( self, startVertexName, endVertexName ):
		assert self.isOnVertexList( startVertexName )
		assert self.isOnVertexList( endVertexName )

		startVertex = self.findVertex( startVertexName )
		endVertex	= self.findVertex( endVertexName )

		place = 0
		q1 = queue.Queue( 120 )

		q1.put( startVertex )
		startVertex.discoverVertex( None, 0 )

		while q1.empty() != True:

			#Lista para nodos de nivel
			tmpLevelList = []

			#Vaciar todos los nodos de nivel de la cola 1
			while q1.empty() != True:
				tmpLevelList.append( q1.get() )

			for vertex in tmpLevelList:
				for neighbor in vertex.neighborsList:				
					tmpIndex = vertex.neighborsList.index( neighbor )

					#Si no ha sido descubierto se pone predecesor y su distancia con respecto a este
					if neighbor.color == Color.BLACK :
						distance = vertex.distancePredecessor + vertex.neighborDistanceList[ tmpIndex ]
						neighbor.discoverVertex( vertex, distance )
						q1.put( neighbor )

					#Si ya se descubrió y hay otra coincidencia, revisar cual tiene menor distnacia
					if neighbor.color == Color.GREY :
						distance = vertex.distancePredecessor + vertex.neighborDistanceList[ tmpIndex ]
						if neighbor.distancePredecessor > distance :
							neighbor.discoverVertex( vertex, distance )

			#Ordenar cola de mayor a menor
			sortLst = Graph.bubbleSort( q1 )

			while q1.empty() != True:
				q1.get() 

			for v in sortLst:
				q1.put( v )

		self.printRout( startVertex, endVertex )
		return True

	def createRomaniaGraph( self ):

		assert self.addVertex( "Ara" )
		assert self.addVertex( "Buc" )
		assert self.addVertex( "Cra" )
		assert self.addVertex( "Dro" )
		assert self.addVertex( "Efo" )
		assert self.addVertex( "Fag" )
		assert self.addVertex( "Giu" )
		assert self.addVertex( "Hir" )
		assert self.addVertex( "Ias" )
		assert self.addVertex( "Lug" )
		assert self.addVertex( "Meh" )
		assert self.addVertex( "Nea" )
		assert self.addVertex( "Ora" )
		assert self.addVertex( "Pit" )
		assert self.addVertex( "Rim" )
		assert self.addVertex( "Sib" )
		assert self.addVertex( "Tim" )
		assert self.addVertex( "Urz" )
		assert self.addVertex( "Vas" )
		assert self.addVertex( "Zer" )
		
		assert self.addAxis( "Ora", "Sib", 151 )
		assert self.addAxis( "Ora", "Zer", 71  )
		assert self.addAxis( "Zer", "Ara", 75  )
		assert self.addAxis( "Ara", "Tim", 118 )
		assert self.addAxis( "Ara", "Sib", 140 )
		assert self.addAxis( "Tim", "Lug", 111 )
		assert self.addAxis( "Lug", "Meh", 70  )
		assert self.addAxis( "Meh", "Dro", 75  )
		assert self.addAxis( "Dro", "Cra", 120 )
		assert self.addAxis( "Cra", "Rim", 146 )
		assert self.addAxis( "Cra", "Pit", 138 )
		assert self.addAxis( "Sib", "Rim", 80  )
		assert self.addAxis( "Sib", "Fag", 99  )
		assert self.addAxis( "Rim", "Pit", 97  )
		assert self.addAxis( "Fag", "Buc", 211 )
		assert self.addAxis( "Pit", "Buc", 101 )
		assert self.addAxis( "Buc", "Giu", 90  )
		assert self.addAxis( "Buc", "Urz", 85  )
		assert self.addAxis( "Urz", "Hir", 98  )
		assert self.addAxis( "Hir", "Efo", 86  )
		assert self.addAxis( "Urz", "Vas", 142 )
		assert self.addAxis( "Vas", "Ias", 92  )
		assert self.addAxis( "Ias", "Nea", 87  )

		return True


#################################################
##				DRIVER PROGRAM				   ##
#################################################
def main():
	graph = Graph( None )
	graph.createRomaniaGraph()

	#Ejemplo 9
	print("-------Ejemplo 9------------")
	graph.UCS( "Zer", "Hir" )

	#Ejmplo 10
	##print("-------Ejemplo 10------------")
	##graph.UCS( "Ara", "Buc" )




if __name__ == "__main__":
    main()
		
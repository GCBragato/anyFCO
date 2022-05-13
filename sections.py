from math import pi, pow

class Polygon():
    """Properties of a polygon defined by the coordinates of its
    vertices. Input the list  of vertices in counter-clockwise fashion.\n

    Properties:
    List of X coordinates: .coorsX[]
    List of Y coordinates: .coorsY[]
    Area: .area
    Center of Gravity: .cgX and .cgY
    List of offset vertices coordinates for the CG to be the origin: .XY_cg[]
    List of offset X coordinates: .coorsCgX[]
    List of offset Y coordinates: .coorsCgY[]
    Inertia X to (0,0): .Ix_origin
    Inertia Y to (0,0): .Iy_origin
    Inertia XY to (0,0): .Ixy_origin
    Inertia X to CG: .Ix
    Inertia Y to CG: .Iy
    Inertia XY to CG: .Ixy
    """

    def __init__(self, XY:str):
        self.XY = XY
        self.coorsX, self.coorsY = self.partXY(XY)
        self.area, self.cgX, self.cgY = self.area_F(self.coorsX, self.coorsY)
        self.coorsCgX, self.coorsCgY = self.coorsCgXY(self.coorsX, self.coorsY, self.cgX, self.cgY)
        self.XY_cg = self.join_XY(self.coorsCgX, self.coorsCgY)
        self.Iy_origin,self.Ix_origin,self.Ixy_origin = self.inertia(self.coorsX, self.coorsY)
        self.Iy,self.Ix,self.Ixy = self.inertia(self.coorsCgX, self.coorsCgY)

    def partXY(self, XY):
        #Separa as coordenadas de lista X,Y inserida
        coorsX = []
        coorsY = []
        for XY in XY:
            coorsX.append(float(XY.partition(',')[0]))
            coorsY.append(float(XY.partition(',')[2]))
        return coorsX, coorsY
    
    def area_F(self, coorsX, coorsY):
        #Calcula a área e o centroide
        sArea = 0.0
        cgX = 0
        cgY = 0
        for i in range(len(coorsX)):
            sArea += (coorsX[i-1]+coorsX[i])*(coorsY[i-1]-coorsY[i])
            cgX += (coorsX[i-1]+coorsX[i])*(coorsX[i-1]*coorsY[i]-coorsX[i]*coorsY[i-1])
            cgY += (coorsY[i-1]+coorsY[i])*(coorsX[i-1]*coorsY[i]-coorsX[i]*coorsY[i-1])
        sArea = abs(sArea/2)
        cgX = cgX/(6*sArea)
        cgY = cgY/(6*sArea)
        return sArea, cgX, cgY

    def coorsCgXY(self, coorsX, coorsY, cgX, cgY):
        #Desloca o formato para que o centróide seja a origem (0,0)
        #Retorna lista de novos X e Y
        coorsCgX = []
        coorsCgY = []
        for i in range(len(coorsX)):
            coorsCgX.append(coorsX[i]-cgX)
            coorsCgY.append(coorsY[i]-cgY)
        return coorsCgX, coorsCgY

    def join_XY(self, X, Y):
        #Une as coordanadas deslocadas para uma lista com X,Y
        newXY = []
        for i in range(len(X)):
            newXY.append(str(X[i])+','+str(Y[i]))
        return newXY

    def inertia(self, X, Y):
        #Retorna momento de inércia
        Iy = 0
        Ix = 0
        Ixy = 0
        for i in range(len(X)):
            Iy += (X[i-1]*Y[i]-X[i]*Y[i-1])*(X[i-1]**2+X[i-1]*X[i]+X[i]**2)
            Ix += (X[i-1]*Y[i]-X[i]*Y[i-1])*(Y[i-1]**2+Y[i-1]*Y[i]+Y[i]**2)
            Ixy += (X[i-1]*Y[i]-X[i]*Y[i-1])*(X[i-1]*Y[i]+2*X[i-1]*Y[i-1]+2*X[i]*Y[i]+X[i]*Y[i-1])
        return Iy/12, Ix/12, Ixy/24

class Circle():
    """Properties of a circle defined by its radius
    
    Properties:
    Area: .area
    Inertia X or Y to CG: .I
    Inertia XY to CG: .Ixy
    """

    def __init__(self, r:float):
        self.area = pi*r**2
        self.I = pi*pow(r,4)/4
        self.Ixy = pi*pow(r,4)/2

class Rectangle():
    """Properties of a rectangle defined by its sides
    
    Properties:
    Area: .area
    Inertia X to CG: .Ix
    Inertia Y to CG: .Iy
    Inertia XY to CG: .Ixy
    """

    def __init__(self, b:float, h:float):
        self.area = b*h
        self.Ix = b*pow(h,3)/12
        self.Iy = h*pow(b,3)/12
        self.Ixy = 0
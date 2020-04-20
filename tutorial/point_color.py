import vtk
import random

#Create the geometry of a point (the coordinate)
points = vtk.vtkPoints()
p = [1.0, 2.0, 3.0]
q = [2.0, 1.0, 1.0]
r = [3.0, 2.0, 4.0]
s = [2.0, 0.0, 5.0]
pointLists= [p, q, r, s]

#Create the topology of the point (a vertex)
vertices = vtk.vtkCellArray()

#Set up colors
Colors = vtk.vtkUnsignedCharArray()
Colors.SetNumberOfComponents(3)
Colors.SetName("Colors")

for idx in range(len(pointLists)):

    id = points.InsertNextPoint(pointLists[idx])
    vertices.InsertNextCell(1)
    vertices.InsertCellPoint(id)

    cl1 = random.randrange(0,256)
    cl2 = random.randrange(0,256)
    cl3 = random.randrange(0,256)
    Colors.InsertNextTuple([cl1, cl2, cl3])



#Create polydata
polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.SetVerts(vertices)
polydata.GetPointData().SetScalars(Colors)
polydata.Modified()

#Visualize
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(polydata)

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(10)
# actor.GetProperty().SetColor(colors.GetColor3d("Yellow"))
# actor.GetProperty().SetColor(color_list[i])

renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

renderer.AddActor(actor)

renderWindow.Render()
renderWindowInteractor.Start()

    

import vtk

#Create the geometry of a point (the coordinate)
points = vtk.vtkPoints()
p = [1.0, 2.0, 3.0]
q = [2.0, 1.0, 1.0]
r = [3.0, 2.0, 4.0]
s = [2.0, 0.0, 5.0]
pointLists= [p, q, r, s]

#Create the topology of the point (a vertex)
vertices = vtk.vtkCellArray()

for idx in range(len(pointLists)):

    id = points.InsertNextPoint(pointLists[idx])
    vertices.InsertNextCell(1)
    vertices.InsertCellPoint(id)


#Create polydata
polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.SetVerts(vertices)
polydata.Modified()

#Visualize
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(polydata)

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(10)
#How to color points?

renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

renderer.AddActor(actor)

renderWindow.Render()
renderWindowInteractor.Start()

    

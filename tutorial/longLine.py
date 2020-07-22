import vtk

def make_actor(polydata):
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor

origin = [0,0,0]
p0 = [1,0,0]
p1 = [0,1,0]
p2 = [0,1,2]
p3 = [1,2,3]

points = vtk.vtkPoints()
points.InsertNextPoint(origin)
points.InsertNextPoint(p0)
points.InsertNextPoint(p1)
points.InsertNextPoint(p2)
points.InsertNextPoint(p3)

lines = vtk.vtkCellArray()

for i in range(3):
    line = vtk.vtkLine()
    line.GetPointIds().SetId(0,i)
    line.GetPointIds().SetId(1, i+1)
    lines.InsertNextCell(line)

    
linesPolydata = vtk.vtkPolyData()
linesPolydata.SetPoints(points)
linesPolydata.SetLines(lines)

actor = make_actor(linesPolydata)
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize(1000, 1000)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindow.Render()
renderWindowInteractor.Start()


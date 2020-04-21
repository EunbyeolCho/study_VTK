import vtk



#Basic line
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)


def make_actor(polydata):
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(Colors.GetColor3d("Cyan"))
    #Make seperation by wire(line)
    actor.GetProperty().SetRepresentationToWireframe()

    return actor


if __name__=="__main__":
        
    Colors = vtk.vtkNamedColors()
    #Colors can be used for actor and renderer
    Points = vtk.vtkPoints()
    Points.InsertNextPoint(0,0,0)
    Points.InsertNextPoint(0,1,0)
    Points.InsertNextPoint(1,0,0)
    Points.InsertNextPoint(1.5,1,0)

    traingleStrip = vtk.vtkTriangleStrip()
    traingleStrip.GetPointIds().SetNumberOfIds(4)
    traingleStrip.GetPointIds().SetId(0,0)
    traingleStrip.GetPointIds().SetId(1,1)
    traingleStrip.GetPointIds().SetId(2,2)
    traingleStrip.GetPointIds().SetId(3,3)


    cells = vtk.vtkCellArray()
    cells.InsertNextCell(traingleStrip)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(Points)
    polydata.SetStrips(cells)

    actor = make_actor(polydata)


    #Visualize
    ren.AddActor(actor)
    ren.SetBackground(Colors.GetColor3d("DarkGreen"))
    ren.ResetCamera()

    iren.Initialize()
    renWin.Render()
    iren.Start()

import vtk


#Basic line
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)


if __name__ == "__main__":

    colors = vtk.vtkNamedColors()

    points = vtk.vtkPoints()

    points.InsertNextPoint(0.0, 0.0, 0.0)
    points.InsertNextPoint(1.0, 0.0, 0.0)
    points.InsertNextPoint(1.0, 1.0, 0.0)
    points.InsertNextPoint(0.0, 1.0, 0.0)


    
    #Create a triangle on the three points in the polydata
    #The first input is the index of the polygon vertex
    #The second input is the index into the point (geometry) array

    tri1 = vtk.vtkTriangle()
    tri1.GetPointIds().SetId(0, 0)
    tri1.GetPointIds().SetId(1, 1)
    tri1.GetPointIds().SetId(2, 2)

    tri2 = vtk.vtkTriangle()
    tri2.GetPointIds().SetId(0, 2)
    tri2.GetPointIds().SetId(1, 3)
    tri2.GetPointIds().SetId(2, 0)


    #Add the triangles to the list of triangles(in this case there is only 2 triangles)
    triangles = vtk.vtkCellArray()
    triangles.InsertNextCell(tri1)
    triangles.InsertNextCell(tri2)

    #Create a PolyData, add the geometry and topology to the polydatas
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    polyData.SetPolys(triangles)
    polyData.Modified()

    #Set the cell color
    cellColor = vtk.vtkUnsignedCharArray()
    cellColor.SetNumberOfComponents(1)
    cellColor.SetNumberOfTuples(polyData.GetNumberOfCells())
    cellColor.SetName("gt")

    #Modified polydata
    polyData.GetCellData().SetScalars(cellColor)
    polyData.Modified()


    #Visualzie
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    # actor.GetProperty().SetColor(colors.GetColor3d("Yellow"))

    ren.AddActor(actor)
    ren.ResetCamera()

    iren.Initialize()
    renWin.Render()
    iren.Start()

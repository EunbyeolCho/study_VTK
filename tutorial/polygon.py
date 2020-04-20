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


    #Create the polygon
    #The first input is the index of the polygon vertex
    #The second input is the index into the point (geometry) array
    polygon = vtk.vtkPolygon()
    polygon.GetPointIds().SetNumberOfIds(4) #make a quad
    polygon.GetPointIds().SetId(0, 0)
    polygon.GetPointIds().SetId(1, 1)
    polygon.GetPointIds().SetId(2, 2)
    polygon.GetPointIds().SetId(3, 3)


    #Add the polygon to a list of polygons(in this case there is only 1)
    polygons = vtk.vtkCellArray()
    polygons.InsertNextCell(polygon)

    #Create a PolyData, add the geometry and topology to the polydatas
    polygonPolyData = vtk.vtkPolyData()
    polygonPolyData.SetPoints(points)
    polygonPolyData.SetPolys(polygons)



    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polygonPolyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d("Yellow"))

    ren.AddActor(actor)
    ren.ResetCamera()

    iren.Initialize()
    renWin.Render()
    iren.Start()

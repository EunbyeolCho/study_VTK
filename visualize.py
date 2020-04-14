import vtk



if __name__=="__main__":


    #Color mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)        
    
    mapper.SetColorModeToMapScalars()
    mapper.GetLookupTable().SetUseBelowRangeColor(True)
    mapper.GetLookupTable().SetBelowRangeColor(1.0, 1.0, 1.0, 1.0)
    mapper.SetScalarRange([1.0, 15.0])

    #Color actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    # actor.GetProperty().SetColor(1,0,0)
    # renderer.AddActor(actor)
    
    #Make AxesActor
    axesActor = vtk.vtkAxesActor()
    axesActor.SetTotalLength(5, 5, 5)
    axesActor.AxisLabelsOff()
    renderer.AddActor(axesActor)


    renderer.SetBackground(.1, .2, .3)
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(1000, 1000)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindow.Render()
    renderWindowInteractor.Start()

import vtk

sphereSource1 = vtk.vtkSphereSource()
sphereSource1.Update()

delaunay1 = vtk.vtkDelaunay3D()
delaunay1.SetInputConnection(sphereSource1.GetOutputPort())
delaunay1.Update()

sphereSource2 = vtk.vtkSphereSource()
sphereSource2.SetCenter(5,0,0)
sphereSource2.Update()


delaunay2 = vtk.vtkDelaunay3D()
delaunay2.SetInputConnection(sphereSource2.GetOutputPort())
delaunay2.Update()


appendFilter = vtk.vtkAppendFilter()
appendFilter.AddInputConnection(delaunay1.GetOutputPort())
appendFilter.AddInputConnection(delaunay2.GetOutputPort())
appendFilter.Update()


# connectivityFilter = vtk.vtkConnectivityFilter()
# connectivityFilter.SetInputConnection(appendFilter.GetOutputPort())
# connectivityFilter.SetExtractionModeToAllRegions()
# connectivityFilter.ColorRegionsOn()
# connectivityFilter.Update()

#######################
mapper = vtk.vtkDataSetMapper()
mapper.SetInputConnection(appendFilter.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)


renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
renWin.SetSize(1500, 1500)
renWin.Render()


iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())


iren.Initialize()
iren.Start()


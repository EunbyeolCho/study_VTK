import vtk

sphereSource = vtk.vtkSphereSource()
sphereSource.Update()


pointPicker = vtk.vtkPointPicker()
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(sphereSource.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)


renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
renWin.SetSize(1500, 1500)
iren = vtk.vtkRenderWindowInteractor()

iren.SetPicker(pointPicker)
iren.SetRenderWindow(renWin)
iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())



renWin.Render()
iren.Start()

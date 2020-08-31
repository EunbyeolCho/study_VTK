"""
https://vtk.org/doc/nightly/html/classvtkSelectPolyData.html
"""

import vtk
import random

renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
renWin.SetSize(1500, 1500)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())



#Make Control Point
landmark = vtk.vtkPoints()
landmark.InsertNextPoint([random.randrange(0, 10)/10, random.randrange(0, 10)/10, 0.0])
landmark.InsertNextPoint([random.randrange(0, 10)/10, random.randrange(0, 10)/10, 0.0])
landmark.InsertNextPoint([random.randrange(0, 10)/10, random.randrange(0, 10)/10, 0.0])
# landmark.InsertNextPoint([random.randrange(0, 10)/10, random.randrange(0, 10)/10, 0.0])
# landmark.InsertNextPoint([random.randrange(0, 10)/10, random.randrange(0, 10)/10, 0.0])
# landmark.InsertNextPoint([random.randrange(0, 10)/10, random.randrange(0, 10)/10, 0.0])
landmarkActor = vtk.vtkActor()
pickedPoint = -1

target = vtk.vtkPolyData()
targetActor = vtk.vtkActor()

scalarBar = vtk.vtkScalarBarActor()

def LeftButtonPressed(obj, ev):


    pos = obj.GetEventPosition()

    picker = vtk.vtkPointPicker()
    picker.PickFromListOn()
    picker.AddPickList(landmarkActor)
    
    picker.Pick(pos[0], pos[1], 0, renderer)


    global pickedPoint
    pickedPoint = picker.GetPointId()    


def MouseMove(obj, ev):
    if pickedPoint == -1 : return
    
    pos = obj.GetEventPosition()

    picker = vtk.vtkCellPicker()
    picker.Pick(pos[0], pos[1], 0, renderer)

    landmark.SetPoint(pickedPoint, picker.GetPickPosition())
    landmark.Modified()
    

def LeftButtonRelease(obj, ev):

    global pickedPoint
    pickedPoint = -1


    #Select Polydata
    loop = vtk.vtkSelectPolyData()
    loop.SetInputData(target)
    loop.SetLoop(landmark)
    loop.GenerateSelectionScalarsOn()
    # loop.SetSelectionModeToLargestRegion()
    loop.SetSelectionModeToSmallestRegion()
    loop.Update()


    outputScalar = loop.GetOutput().GetPointData().GetScalars() 

    #Add
    if outputScalar == None:

        for i in range(landmark.GetNumberOfPoints()):
            print(landmark.GetPoint(i), end=" ")
        print()
        # return 
    


    target.GetPointData().SetScalars(outputScalar)
    target.GetPointData().Modified()

    targetActor.GetMapper().SetScalarRange(outputScalar.GetRange())
    ##### error!
    # AttributeError: 'NoneType' object has no attribute 'GetRange'




if __name__ == "__main__":
    planeSource = vtk.vtkPlaneSource()
    planeSource.SetResolution(10, 10)
    planeSource.Update()


    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName("./sample1.vtp")
    reader.Update()


    polyData = planeSource.GetOutput()
    polyData.GetPointData().RemoveArray("Normals")
    triangleFilter = vtk.vtkTriangleFilter()
    triangleFilter.SetInputData(polyData)
    triangleFilter.Update()
    
    target = reader.GetOutput()
    # target = triangleFilter.GetOutput()



    numPoints = target.GetNumberOfPoints()    
    array = vtk.vtkFloatArray()
    array.SetNumberOfTuples(numPoints)
    for idx in range(numPoints):
        array.SetTuple(idx, [0])

    target.GetPointData().SetScalars(array)


    mapper = vtk.vtkPolyDataMapper()
    mapper.SetScalarRange(target.GetPointData().GetScalars().GetRange())
    mapper.SetInputData(target)

    targetActor = vtk.vtkActor()
    targetActor.SetMapper(mapper)
    
    renderer.AddActor(targetActor)


    #Show Landmark
    numLandmarks = landmark.GetNumberOfPoints()
 
    #Add Closed Lines
    lines = vtk.vtkCellArray()
    lines.InsertNextCell(numLandmarks+1)
    for idx in range(numLandmarks):
        lines.InsertCellPoint(idx)          
    lines.InsertCellPoint(0)

 

    #Make Landmark Polydata
    landmarkPoly = vtk.vtkPolyData()
    landmarkPoly.SetPoints(landmark)
    landmarkPoly.SetLines(lines)


    landmarkMapper = vtk.vtkOpenGLSphereMapper()
    landmarkMapper.SetInputData(landmarkPoly)
    landmarkMapper.SetRadius(.1)

    # landmarkActor = vtk.vtkActor()
    landmarkActor.SetMapper(landmarkMapper)

    lineMapper = vtk.vtkPolyDataMapper()
    lineMapper.SetInputData(landmarkPoly)

    lineActor = vtk.vtkActor()
    lineActor.SetMapper(lineMapper)

    renderer.AddActor(lineActor)
    renderer.AddActor(landmarkActor)



    #Add ScalarBar Actor
    scalarBar = vtk.vtkScalarBarActor()
    scalarBar.SetLookupTable(targetActor.GetMapper().GetLookupTable())
    renderer.AddActor2D(scalarBar)
    renderer.SetBackground(0.0, 0.0, 0.0)
    renderer.SetBackground2(0.5, 0.5, 0.5)
    renderer.SetGradientBackground(True)

    renWin.Render()


    #Add Interactor
    iren.AddObserver("LeftButtonPressEvent", LeftButtonPressed)
    iren.AddObserver("InteractionEvent", MouseMove)
    iren.AddObserver("EndInteractionEvent", LeftButtonRelease)

    iren.Initialize()
    iren.Start()
    
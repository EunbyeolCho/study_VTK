import vtk
import os 

def read_vtp(filename):

    vtpReader = vtk.vtkXMLPolyDataReader()
    vtpReader.SetFileName(filename)
    vtpReader.Update()
    polydata = vtpReader.GetOutput()

    return polydata


def DownsamplePointCloud(polydata):
    """
    https://lorensen.github.io/VTKExamples/site/Cxx/PolyData/DownsamplePointCloud/
    """

    cleanPolydata = vtk.vtkCleanPolyData()
    cleanPolydata.SetInputData(polydata)
    cleanPolydata.SetTolerance(0.1)
    cleanPolydata.Update()

    return cleanPolydata

def reorder_polyline(edgeData):

    #Reorder polyline
    stripper = vtk.vtkStripper()
    stripper.SetInputData(edgeData)
    stripper.JoinContiguousSegmentsOn()
    # stripper.Update()

    cleanPoly = vtk.vtkCleanPolyData()
    cleanPoly.SetInputConnection(stripper.GetOutputPort())
    # cleanPoly.Update()

    stripper2 = vtk.vtkStripper()
    stripper2.SetInputConnection(cleanPoly.GetOutputPort())
    stripper2.JoinContiguousSegmentsOn()
    # stripper2.Update()

    cleanPoly2 = vtk.vtkCleanPolyData()
    cleanPoly2.SetInputConnection(stripper2.GetOutputPort())
    cleanPoly2.Update()

    return cleanPoly2.GetOutput()


def generate_landmarks(polydata):

    #Extract Boundary Edges
    # https://lorensen.github.io/VTKExamples/site/Cxx/Meshes/BoundaryEdges/
    featureEdges = vtk.vtkFeatureEdges()
    featureEdges.SetInputData(polydata)
    featureEdges.BoundaryEdgesOn()
    featureEdges.FeatureEdgesOff()
    featureEdges.ManifoldEdgesOff()
    featureEdges.NonManifoldEdgesOff()
    featureEdges.Update()
    edgeData = featureEdges.GetOutput()

    
    
    
    edgeData = reorder_polyline(edgeData)


    #Make spline curve - dunno if it is necessary
    spline = vtk.vtkParametricSpline()
    spline.SetPoints(edgeData.GetPoints())
    spline.ParameterizeByLengthOff()
    spline.ClosedOn()
    numResolution = 10 * edgeData.GetNumberOfPoints()
    functionSource = vtk.vtkParametricFunctionSource()
    functionSource.SetParametricFunction(spline)
    functionSource.SetUResolution(numResolution)
    functionSource.SetVResolution(numResolution)
    functionSource.SetWResolution(numResolution)
    functionSource.Update()
    cleanFilter = vtk.vtkCleanPolyData()
    cleanFilter.SetInputData(functionSource.GetOutput())
    cleanFilter.Update()
    curvePoly = cleanFilter.GetOutput()

    return curvePoly


if __name__ == '__main__':



    root_dir = './data/'
    file_list = os.listdir(root_dir)

    reader = vtk.vtkSTLReader()
    reader.SetFileName(os.path.join(root_dir, file_list[7]))
    reader.Update()
    polydata = reader.GetOutput()


    curvePoly = generate_landmarks(polydata)
    cleanPolydata = DownsamplePointCloud(curvePoly)
    cleanPoints = cleanPolydata.GetOutput().GetPoints()
    pointData = cleanPoints.GetData()
    
    
    newPoints = vtk.vtkPoints()
    newVertices = vtk.vtkCellArray()
    
    for idx in range(pointData.GetNumberOfTuples()):

        id = newPoints.InsertNextPoint(pointData.GetTuple(idx))
        newVertices.InsertNextCell(1)
        newVertices.InsertCellPoint(id)
        
    new_polydata = vtk.vtkPolyData()
    new_polydata.SetVerts(newVertices)
    new_polydata.SetPoints(newPoints)
    new_polydata.Modified()


    cleanMapper = vtk.vtkPolyDataMapper()
    # cleanMapper = vtk.vtkOpenGLSphereMapper()
    # cleanMapper.SetInputConnection(cleanPolydata.GetOutputPort())
    cleanMapper.SetInputData(new_polydata)
    cleanActor = vtk.vtkActor()
    cleanActor.SetMapper(cleanMapper)
    cleanActor.GetProperty().SetPointSize(10)
    cleanActor.GetProperty().SetColor(1.0, 0.0, 0.0)

    inputMapper = vtk.vtkPolyDataMapper()
    inputMapper.SetInputData(polydata)
    inputActor = vtk.vtkActor()
    inputActor.SetMapper(inputMapper)


    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(600,600)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    style = vtk.vtkInteractorStyleTrackballCamera()
    interactor.SetInteractorStyle(style)

    leftRenderer  = vtk.vtkRenderer()
    renderWindow.AddRenderer(leftRenderer)
    leftRenderer.AddActor(cleanActor)
    leftRenderer.AddActor(inputActor)


    renderWindow.Render()
    interactor.Start()








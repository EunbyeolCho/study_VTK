import vtk
import numpy as np
import random

#If data type is polydata
def random_poly_rotation(input_poly):

    transform = vtk.vtkTransform()
    transform.RotateX(random.randrange(-30, 30))
    transform.RotateY(random.randrange(-30, 30))
    transform.RotateZ(random.randrange(-30, 30))
    transform.Update()

    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputData(input_poly)
    transformFilter.SetTransform(transform)
    transformFilter.Update()
    output_poly = transformFilter.GetOutput()

    return output_poly


def random_poly_scaling(input_poly):


    transform = vtk.vtkTransform()
    scale_rate = random.uniform(0.8, 1.2)
    # scale_rate=2
    transform.Scale(scale_rate, scale_rate, scale_rate)
    transform.Update()

    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputData(input_poly)
    transformFilter.SetTransform(transform)
    transformFilter.Update()
    output_poly = transformFilter.GetOutput()
    

    return output_poly



#If data type is list
def random_rotation(input_batch):
    transform = vtk.vtkTransform()
    # anlge = random.randrange(-180, 180)
    transform.RotateX(random.randrange(-180, 180))
    transform.RotateY(random.randrange(-180, 180))
    transform.RotateZ(random.randrange(-180, 180))
    transform.Update()
    result_batch = np.array([*map(transform.TransformPoint, input_batch)])


    return result_batch

def random_scaling(input_batch):
    transform = vtk.vtkTransform()
    scale_rate = random.uniform(0.8, 1.2)

    transform.Scale(scale_rate, scale_rate, scale_rate)
    transform.Update()

    result_batch = []
    for batch in input_batch :
        batch = np.array(batch)
        result = np.array([*map(transform.TransformPoint, batch)])
        result_batch.append(result)

    return result_batch




def mesh_transform(polydata, rotate_axis, angle=180):

    transform = vtk.vtkTransform()
    if rotate_axis == 'X':
        transform.RotateX(angle)
    elif rotate_axis == 'Y':
        transform.RotateY(angle)
    elif rotate_axis == 'Z':
        transform.RotateZ(angle)
    else:
        print("you have to choose X or Y or Z")

    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputData(polydata)
    transformFilter.SetTransform(transform)
    transformFilter.Update()  
    polydata = transformFilter.GetOutput()   

    return polydata


def CenterPolyData(polydata):

    center = polydata.GetCenter()
    transform = vtk.vtkTransform()
    transform.Translate(-center[0], -center[1], -center[2])
    transform.Update()

    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputData(polydata)
    transformFilter.SetTransform(transform)
    transformFilter.Update()
    polydata = transformFilter.GetOutput()
    
    ##Normalize
    num_points = polydata.GetNumberOfPoints()
    boundingBox = polydata.GetBounds()
    
    xRange = boundingBox[1] - boundingBox[0]
    yRange = boundingBox[3] - boundingBox[2]
    zRange = boundingBox[5] - boundingBox[4]

    
    normalizeRange = np.max([xRange, yRange, zRange])


    for idx in range(num_points):
        position = polydata.GetPoint(idx)
        position_normalized = [position[0] / normalizeRange, position[1] / normalizeRange, position[2] / normalizeRange]
        polydata.GetPoints().SetPoint(idx, position_normalized)
    polydata.GetPoints().Modified()

    return polydata
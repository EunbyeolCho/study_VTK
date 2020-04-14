import vtk
import numpy as np
import random
import os
import glob
import math


def CenterPolyData(polydata):

    center = polydata.GetCenter()
    transform = vtk.vtkTransform()
    transform.Translate(-center[0], -center[1], -center[2])
    transform.Update()

    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputData(polydata)
    transformFilter.SetTransform(transform)
    transformFilter.Update()
    center_polydata = transformFilter.GetOutput()

    return center_polydata


def get_normal(polydata):
    
    normalGenerator = vtk.vtkPolyDataNormals()
    normalGenerator.SetInputData(polydata)
    # normalGenerator.SetInputConnection(polydata)
    normalGenerator.ComputePointNormalsOff()
    normalGenerator.ComputeCellNormalsOn() # On????
    normalGenerator.Update()
    polydata = normalGenerator.GetOutput()

    normalDataDouble = polydata.GetCellData().GetArray("Normals")
    nc = normalDataDouble.GetNumberOfTuples()
    normals  = polydata.GetCellData().GetNormals()
    
    normal_vectors = []
    normal_vectors = [0,0,0]

    for i in range(nc):
        normal_vectors[0] += normals.GetTuple(i,)[0]
        normal_vectors[1] += normals.GetTuple(i,)[1]
        normal_vectors[2] += normals.GetTuple(i,)[2]
    
    # print(normal_vectors)
    sum_vector = normal_vectors
    return sum_vector


def apply_pca(input_poly):


    result_input = []
    pointCloud = input_poly.GetPoints()
    numPoints = pointCloud.GetNumberOfPoints()

    for idx in range(numPoints):
        pos = pointCloud.GetPoint(idx)
        result_input.append(pos)

    #Apply pca
    data = np.array(result_input).transpose()
    cov_mtx = np.cov(data)

    eVec, eVal, _ = np.linalg.svd(cov_mtx, full_matrices=True)
    result_temp = np.matmul(np.transpose(eVec), data)
    result = result_temp.transpose() #(54149, 3)

    #Update points of polydata
    for i in range(len(result)):
        input_poly.GetPoints().SetPoint(i, result[i])
    input_poly.GetPoints().Modified()
    output_poly = CenterPolyData(input_poly)

    return output_poly

def align_polydata(original_polydata):


    original_boundingBox = original_polydata.GetBounds()
    origin_z_idx = np.argmin([original_boundingBox[1]-original_boundingBox[0], original_boundingBox[3]-original_boundingBox[2], original_boundingBox[5]-original_boundingBox[4]]) #2
    trg_vector = [0,0,0]
    trg_vector[origin_z_idx] = 1

    #Apply pca
    pca_polydata = apply_pca(original_polydata)
    pca_bounidng_box = pca_polydata.GetBounds()

    z_idx = np.argmin([pca_bounidng_box[1]-pca_bounidng_box[0], pca_bounidng_box[3]-pca_bounidng_box[2], pca_bounidng_box[5]-pca_bounidng_box[4]]) #2
    src_vector = [0,0,0]
    src_vector[z_idx] = 1
    sum_vector = get_normal(pca_polydata)

    if np.dot(sum_vector, src_vector) < 0 :
        print("=====> The direction of normal vecotr and src vector is inconsistent")
        src_vector[z_idx] *= -1


    #Align Z : pca_polydata -> polydata_z
    rotAxis = np.cross(src_vector, trg_vector) ## [-1  0  0]
    rotAngle = np.arccos(np.dot(src_vector, trg_vector)) * 180 / math.pi #90
    
    #Raw data and train data are orthogonal!
    if rotAngle in [0.0, 180.0]:
        rotAxis = np.cross(src_vector, [0,1,0])
        rotAngle = np.arccos(np.dot(src_vector, [0,1,0])) * 180 / math.pi

    transform = vtk.vtkTransform()
    transform.RotateWXYZ(rotAngle, rotAxis)
    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputData(pca_polydata)
    transformFilter.SetTransform(transform)
    transformFilter.Update()
    polydata_z = transformFilter.GetOutput()



    #Align XY : polydata_z -> perfect_polydata
    min_half = polydata_z.GetBounds()[0] * 0.2
    max_half = polydata_z.GetBounds()[1] * 0.2

    pointCloud = polydata_z.GetPoints()
    numPoints = pointCloud.GetNumberOfPoints()

    count_pos, count_neg = 0, 0
    result_xy=[]

    for idx in range(numPoints):
        pos = pointCloud.GetPoint(idx)
        
        if pos[0] < max_half and pos[0] > min_half:

            if pos[2] > 0:
                count_pos +=1
            elif pos[2] < 0:
                count_neg +=1
            else:
                pass

    if count_pos < count_neg :
        transform = vtk.vtkTransform()
        transform.RotateWXYZ(180, [0,1,0])
        transformFilter = vtk.vtkTransformPolyDataFilter()
        transformFilter.SetInputData(polydata_z)
        transformFilter.SetTransform(transform)
        transformFilter.Update()
        perfect_polydata = transformFilter.GetOutput()

    else:
        perfect_polydata = polydata_z
    

    return perfect_polydata
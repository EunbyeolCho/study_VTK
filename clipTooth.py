import torch
import vtk
import numpy as np
import glob
import os
import pymongo
from bson.objectid import ObjectId


def read_vtp(filename):

    vtpReader = vtk.vtkXMLPolyDataReader()
    vtpReader.SetFileName(filename)
    vtpReader.Update()

    polydata = vtpReader.GetOutput()
    return polydata

def make_actor(polydata):
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor


def select_one(polydata, label_num):
    
    numPoints = polydata.GetNumberOfPoints()
    pointLabel = polydata.GetPointData().GetScalars()
    
    for idx in range(numPoints):
        if pointLabel.GetValue(idx) != label_num:
            pointLabel.SetValue(idx, 0)

    polydata.GetPointData().SetScalars(pointLabel)
    polydata.GetPointData().Modified()


    return polydata 


if __name__ == "__main__" :

    polydata= read_xml_data(ObjectId('5dfb184f9b1fd27720764acc'))
    #A tooth labeld # and the others are labeld as background.
    # polydata = select_one(polydata, 4)

    #Construct one tooth mesh labeled #
    numFaces = polydata.GetNumberOfCells()
    pointLabel = polydata.GetPointData().GetScalars()
    faceIdlist = []

    for faceID in range(numFaces):
        face = polydata.GetCell(faceID)
        pointIds = [face.GetPointId(0), face.GetPointId(1),face.GetPointId(2)]

        hasLabel=False

        for pointID in pointIds:
            if pointLabel.GetValue(pointID) == 4:
                hasLabel = True

        if hasLabel:
            faceIdlist.append(faceID)



    #Clip the tooth based on faceIdlist
    newPoints = vtk.vtkPoints()
    newpolygons = vtk.vtkCellArray()
    point_id = 0

    for faceID in faceIdlist:
        
        face = polydata.GetCell(faceID)
        pointIds = [face.GetPointId(0), face.GetPointId(1),face.GetPointId(2)]

        polygon = vtk.vtkPolygon()
        polygon.GetPointIds().SetNumberOfIds(3)

        for i, pointId in enumerate(pointIds):

            pointPosiotion = list(polydata.GetPoint(pointId))
            newPoints.InsertNextPoint(pointPosiotion)
            polygon.GetPointIds().SetId(i,point_id)
            point_id+=1
            
        newpolygons.InsertNextCell(polygon)


    #Update newPolydata
    newPolyData = vtk.vtkPolyData()
    newPolyData.SetPoints(newPoints)
    newPolyData.SetPolys(polydata.GetLines())
    newPolyData.Modified()

    
    #Visualize
    actor = make_actor(newPolyData)
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(1000, 1000)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindow.Render()
    renderWindowInteractor.Start()




    
import vtk
import numpy as np
import pymongo
import random
import os
import glob


def read_stl_data(filename):

    stlReader = vtk.vtkSTLReader()
    stlReader.SetFileName(filename)
    stlReader.Update()

    polydata = stlReader.GetOutput()
    polydata = CenterPolyData(polydata)

    return polydata

def read_xml_data(data_id):

    data = db.segmentationTrain.find_one({"_id":data_id})
    xmlString = data["polydata"]
    
    xmlReader = vtk.vtkXMLPolyDataReader()
    xmlReader.SetReadFromInputString(True)
    xmlReader.SetInputString(xmlString)
    xmlReader.Update()

    polydata = xmlReader.GetOutput()
    polydata = CenterPolyData(polydata)

    return polydata
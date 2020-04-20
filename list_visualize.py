import vtk
from vtk import *
import pymongo
import random
import numpy as np


db = pymongo.MongoClient().maxilafacial
data_id_list = db.segmentationTrainProcessed_dev_train_ver3.find({}).distinct('_id')
data_id = data_id_list[1]
element = db.segmentationTrainProcessed_dev_train_ver3.find_one({"_id" : data_id})
data = element['input']
gt = element['gt']

Points = vtk.vtkPoints()
Vertices = vtk.vtkCellArray()

for idx in range(len(data)) :
        
    id = Points.InsertNextPoint(data[idx])
    Vertices.InsertNextCell(1)
    Vertices.InsertCellPoint(id)

polydata = vtk.vtkPolyData()
polydata.SetPoints(Points)
polydata.SetVerts(Vertices)
polydata.Modified()


#Assign gt
pointCloud = polydata.GetPoints()
num_points = pointCloud.GetNumberOfPoints()

label = vtk.vtkFloatArray()
for idx in range(num_points):
    label.InsertNextValue(gt[idx])

polydata.GetPointData().SetScalars(label)
polydata.GetPointData().Modified()


#Visualize
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(polydata)
mapper.SetColorModeToMapScalars()
# mapper.GetLookupTable().SetUseBelowRangeColor(True)
# mapper.GetLookupTable().SetBelowRangeColor(1.0, 1.0, 1.0, 1.0)
mapper.SetScalarRange([0.0, 15.0])

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(2)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(.1, .2, .3)

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize(1000, 1000)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

renderWindow.Render()
renderWindowInteractor.Start()



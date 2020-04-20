import vtk
from vtk import *
import pymongo
import random
import numpy as np



#Renderer
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4) # R G B 

#Render window
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
renWin.SetSize(1000, 1000)

#Render window interactor
iren = vtk.vtkRenderWindowInteractor()
interactorStyle = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(interactorStyle)
iren.SetRenderWindow(renWin)



def make_actor(polydata):
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    mapper.SetColorModeToMapScalars()
    # mapper.GetLookupTable().SetUseBelowRangeColor(True)
    # mapper.GetLookupTable().SetBelowRangeColor(1.0, 1.0, 1.0, 1.0)
    mapper.SetScalarRange([1.0, 15.0])

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetPointSize(2)
    # actor.GetProperty().SetColor(colors.GetColor3d("Yellow"))
    # actor.GetProperty().SetColor(color_list[i])

    return actor

    

if __name__=="__main__":


    db = pymongo.MongoClient().maxilafacial
    data_id_list = db.segmentationTrainProcessed_dev_train_ver3.find({}).distinct('_id')
    data_id = data_id_list[1]
    element = db.segmentationTrainProcessed_dev_train_ver3.find_one({"_id" : data_id})
    data = element['input']
    gt = element['gt']

    Points = vtk.vtkPoints()
    Vertices = vtk.vtkCellArray()
    Labels = vtk.vtkFloatArray()

    for idx in range(len(data)) :
            
        id = Points.InsertNextPoint(data[idx])
        Vertices.InsertNextCell(1)
        Vertices.InsertCellPoint(id)
        #Assign gt
        Labels.InsertNextValue(gt[idx])


    polydata = vtk.vtkPolyData()
    polydata.SetPoints(Points)
    polydata.SetVerts(Vertices)
    polydata.GetPointData().SetScalars(Labels)
    polydata.Modified()


    #Visualize
    actor = make_actor(polydata)
    renderer.AddActor(actor)
    renderer.ResetCamera()
    renWin.Render()
    iren.Start()




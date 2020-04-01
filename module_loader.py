import torch
import vtk
import utils
import numpy as np

from save import load_model


global current_device
current_device = 'cpu'
if torch.cuda.is_available():
    current_device = 'cuda'





# Renderer
renderer = vtk.vtkRenderer()

# Render window
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
renWin.SetSize(1000, 1000)

# Render window interactor
iren = vtk.vtkRenderWindowInteractor()

interactorStyle = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(interactorStyle)
iren.SetRenderWindow(renWin)


def make_actor(polydata):
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    mapper.SetColorModeToMapScalars()
    mapper.GetLookupTable().SetUseBelowRangeColor(True)
    mapper.GetLookupTable().SetBelowRangeColor(1.0, 1.0, 1.0, 1.0)
    mapper.SetScalarRange([1.0, 15.0])

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor

def forward_polydata(polydata, model):
    pointCloud = polydata.GetPoints()
    num_points = pointCloud.GetNumberOfPoints()
    #Make Ground Truth
    prediction = torch.zeros(num_points)
    
    #Make index list
    index_list = torch.randperm(num_points)

    #Make index list size % 4096 = 0
    index_list = torch.cat((index_list, index_list[0:(4096-num_points%4096)]))

    
    for i in range(0, num_points, 4096):
        #Make Index subset list
        subset = index_list[i: i+4096]
        
        #Sort subset
        sorted_subset, idx = torch.sort(subset, dim=0)

        input_batch = []
        for j in range(0, 4096):
            input_batch.append(pointCloud.GetPoint(sorted_subset[j].item()))
        
        input_tensor = torch.Tensor(input_batch).unsqueeze(0).transpose(1,2).to(current_device)
        
        output_tensor = model(input_tensor)
        print(output_tensor.size())

        output_index = output_tensor.max(-2)[1][0]
        
        for j in range(0, 4096):            
            prediction[sorted_subset[j]] = output_index[j].item()

        
    return prediction

def update_ground_truth(polydata, prediction):
    for idx in range(0, prediction.size(0)):
        #print(prediction[idx])
        polydata.GetPointData().GetScalars().SetTuple(idx, [prediction[idx]] )
    polydata.GetPointData().Modified()

if __name__ == "__main__":


    module_path = 'module/test_model.pt'
    if current_device == 'cuda': module_path = 'module/test_model_gpu.pt'

    print(module_path)
        
    # Load pytorch network
    model = torch.jit.load(module_path)
    model.to(current_device)
    model.eval()


    xmlReader = vtk.vtkXMLPolyDataReader()
    xmlReader.SetFileName('sample.vti')
    xmlReader.Update()

    polydata = xmlReader.GetOutput()
    polydata = utils.CenterPolyData(polydata)


    actor = make_actor(polydata)

    #Predict
    output = forward_polydata(polydata, model)
    #Forward
    update_ground_truth(polydata, output)

    renderer.AddActor(actor)
    renWin.Render()
    iren.Start()
    
    

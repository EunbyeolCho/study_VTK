import vtk
import numpy as np
import pymongo
import gridfs
import random
import os
import glob
###### 갈아엎자^^!

def random_rotation(input_batch):
    transform = vtk.vtkTransform()
    # anlge = random.randrange(-180, 180)
    transform.RotateX(random.randrange(-180, 180))
    transform.RotateY(random.randrange(-180, 180))
    transform.RotateZ(random.randrange(-180, 180))
    transform.Update()
    result_batch = np.array([*map(transform.TransformPoint, input_batch)])

    return result_batch



def mesh_random_rotation(polydata):

    angle = 30
    polydata = mesh_transform(polydata,'X', angle)
    polydata = mesh_transform(polydata,'Y', angle)
    polydata = mesh_transform(polydata,'Z', 30)

    return polydata


def apply_pca(polydata, input_batch):

    input_batch = np.array(input_batch)
    data = input_batch.transpose()
    cov_mtx = np.cov(data)
    u, v, _ = np.linalg.svd(cov_mtx, full_matrices=True) # (3, 3) (3,)
    result_temp = np.matmul(np.transpose(u),data)
    result = result_temp.transpose()
    

    #Updata points of polydata
    for i in range(len(result)):
        polydata.GetPoints().SetPoint(i, result[i])
    polydata.GetPoints().Modified()
    
    return polydata, result

def align_xy(polydata, pca_data):


    data = np.array(pca_data)
    n,f = data.shape
    values = [np.amax(data[:,0])-np.amin(data[:,0]),np.amax(data[:,1])-np.amin(data[:,1]), np.amax(data[:,2])-np.amin(data[:,2])]
    # print(np.amax(data[:,0]), np.amin(data[:,0]), np.amax(data[:,1]), np.amin(data[:,1]), np.amax(data[:,2]), np.amin(data[:,2]))


    yindex = np.argmax(values)
    ydata = values[yindex]

    zindex = np.argmin(values)
    zdata = values[zindex]

    xindex = set([0,1,2]) - set([yindex, zindex])
    xindex = xindex.pop()
    xmean = np.mean(np.amax(data[:,2]) + np.amin(data[:,2]))
    
    new_data = np.zeros((n,f))
    new_data[:,0] = data[:,xindex]
    new_data[:,1] = data[:,yindex]
    new_data[:,2] = data[:,zindex]
    
    if not int(xmean) == 0: 
        print('x mean value is not zero')
        # raise error 시키는게 좋을듯 


    ymin_half = np.amin(new_data[:,1]) * 0.2
    ymax_half = np.amax(new_data[:,1]) * 0.2
    # print(ymin_half, ymax_half)


    count_pos, count_neg = 0, 0
    # print(len(new_data)) # 234486

    for i in range(len(new_data)):

        if new_data[i][1] < ymax_half and new_data[i][1] > ymin_half :

            if new_data[i][0] > 0 :
                count_pos += 1
            elif new_data[i][0] < 0 :
                count_neg += 1
            else : 
                pass

    if count_pos < count_neg :
        print("rotate by z-axis, actually flip y-axis")
        transform = vtk.vtkTransform()
        transform.RotateZ(180)
        transform.Update()
        new_data = np.array([*map(transform.TransformPoint, new_data)])

        #Transform polydata, too!
        polydata = mesh_transform(polydata, 'Z')


    #Updata points of polydata
    for i in range(len(new_data)):
        polydata.GetPoints().SetPoint(i, new_data[i])
    polydata.GetPoints().Modified()

    return polydata, new_data

def make_actor(polydata):
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)        
    mapper.SetScalarRange([0.0, 15.0])

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor


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
    
    print(normal_vectors)
    sum_vector = normal_vectors
    return sum_vector


def align_z(polydata, data):

    sum_vector = get_normal(polydata)

    if np.dot(sum_vector, [0,1,0]) < 0 :

        print("roate by x-axis ===> sum vector : ", sum_vector)
        transform = vtk.vtkTransform()
        transform.RotateX(180)
        transform.Update()
        data = np.array([*map(transform.TransformPoint, data)])

        polydata = mesh_transform(polydata, "X")

    return polydata, data

def align_polydata(polydata):
    
    points = polydata.GetPoints()
    pointLabel = polydata.GetPointData().GetScalars("gt")
    numPoints = polydata.GetNumberOfPoints()
    numCells = polydata.GetNumberOfCells()

    data = []

    for i in range(numPoints):
        data.append(polydata.GetPoint(i))

    #Apply random rotaiton!
    # random_data = random_rotation(data)
    random_data = data
    #Get data aligned!
    pca_polydata, pca_data = apply_pca(polydata, random_data)
    polydata, data = align_z(pca_polydata, pca_data)
    polydata, data = align_xy(polydata, data)
    
    # Points = vtk.vtkPoints()
    # Vertices = vtk.vtkCellArray()

    # for idx in range(len(data)) :
        
    #     id = Points.InsertNextPoint(data[idx])
    #     Vertices.InsertNextCell(1)
    #     Vertices.InsertCellPoint(id)

    # polydata = vtk.vtkPolyData()
    # polydata.SetPoints(Points)
    # polydata.SetVerts(Vertices)
    # polydata.Modified()

    return polydata


if __name__ == '__main__':

    # num_point = 4096 
    db = pymongo.MongoClient().maxilafacial
    data_id_list = db.segmentationTrain.find({}).distinct('_id')
    stl_dir = '../hardtestset'
    stl_list = glob.glob(os.path.join(stl_dir, "*.stl"))
    stl_list = stl_list[2:4]

    renderer = vtk.vtkRenderer()

    color_list = [(1,0,0),(0.5,0.5,0),(0.8,0.2,0),(0,1,0),(0,0.8,0.2),(0,0.5,0.5),(0,0,1),(0.6,0.3,0.1),(0.2,0.5,0.3),(0.4,0.2,0.4),(0.3,0.1,0.7)]
    for i, stl_file in enumerate(stl_list):
        original_polydata = read_stl_data(stl_file)
        random_polydata = mesh_random_rotation(original_polydata)
        polydata = align_polydata(original_polydata)
        # polydata = CenterPolyData(polydata)

        actor = make_actor(polydata)
        actor.GetProperty().SetColor(color_list[i])
        # actor.GetProperty().SetOpacity(0.9)

        original_actor = make_actor(random_polydata)
        # original_actor.GetProperty().SetColor(0,0,0)
        original_actor.GetProperty().SetOpacity(0.8)
        # original_actor.GetProperty().SetColor(color_list[i])
        
        renderer.AddActor(actor)
        renderer.AddActor(original_actor)

    ###

    renderer.SetBackground(.1, .2, .3)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(1000, 1000)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderWindow.Render()
    renderWindowInteractor.Start()
        


   
   






    

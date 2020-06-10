import vtk



# 기본적으로 polydata에는 point와 face정보가 있다.
point = polydata.GetPoint(pointId)
face = polydata.GetCell(faceId)

numPoints = polydata.GetNumberOfPoints()
numFaces = polydata.GetNumberOfCells()


# 실제 구현할 때는 for문을 이용하여 하나씩 접근한다.
for faceId in rage(numFaces):
    face = polydata.GetCell(faceId)

# face를 이루고 있는 point 3개의 pointId 구하기
pointIds = [face.GetPointId(0), face.GetPointId(1),face.GetPointId(2)]

# pointId를 이용하여 point 3d coordinate 구하기
pointPosition = list(polydata.GetPoint(pointId))

#Check if polydata has attributes of gt : If polydata has gt, remove gt
polydata.GetPointData().RemoveArray('gt')
pointLabel = polydata.GetPointData().GetScalars("gt")

#Edge
edgeExtractor = vtk.vtkExtractEdges()
edgeExtractor.SetInputData(polydata)
edgeExtractor.Update()
edgePoly = edgeExtractor.GetOutput()

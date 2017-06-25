import dicom
import os
import numpy
import numpy as np

PathDicom = "/Path/To/Dicom/Files"
lstFilesDCM = []  # create an empty list
count = 0
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file's DICOM
            lstFilesDCM.append(os.path.join(dirName,filename))
            count += 1
            print("Dicom Number :" + str(count))
            
# Get ref file
RefDs = dicom.read_file(lstFilesDCM[0])

# Load dimensions based on the number of rows, columns, and slices (along the Z axis)
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))

# Load spacing values (in mm)
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))

# The array is sized based on 'ConstPixelDims'
ArrayDicom = numpy.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)


length = 0
# loop through all the DICOM files
for filenameDCM in lstFilesDCM:
    # read the file
    ds = dicom.read_file(filenameDCM)
    # store the raw image data
    ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array
    strippedName = filenameDCM[:-4]
    strippedName += ".npy"
    np.save(strippedName, ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)])
    print(strippedName)
    length += 1
    

print("Done Saving files they are located in " + str(PathDicom))






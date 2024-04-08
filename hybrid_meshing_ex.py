import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import copy
import xmltodict
import xml.etree.ElementTree as ET

filename0 = 'indent_25_RP9.feb'
filename = 'indent_25_RP10_sphere.feb'

def find_indices(xyz_points, xyz_sub_coor):
    # Initialize an empty array to store the indices
    xyz_sub_idx = np.empty((xyz_sub_coor.shape[0],), dtype=int)
    # Loop through each row of array_30_3
    for i, row in enumerate(xyz_sub_coor):
        # Calculate the Euclidean distance between the current row and all rows of array_120_3
        distances = np.linalg.norm(xyz_points - row, axis=1)
        # Find the index of the minimum distance
        index_min_distance = np.argmin(distances)
        # Store the index
        xyz_sub_idx[i] = index_min_distance
    return xyz_sub_idx

# Load the XML file and convert it to a dictionary
with open(filename0) as xml_file:
    data_dict = xmltodict.parse(xml_file.read())


# Define the number of points along the line
num_points = 100

# Generate points along the line
line_points = np.linspace(0, 1, num_points)

# Define the radius of the sphere
radius = 0.1

x_points_straight = []
y_points_straight = []
z_points_straight = []

x_points_slanted = []
y_points_slanted = []
z_points_slanted = []

x_points_straight_inner = []
y_points_straight_inner = []
z_points_straight_inner = []
x_points_slanted_inner = []
y_points_slanted_inner = []
z_points_slanted_inner = []

# Calculate spherical coordinates for each point
for i, point in enumerate(line_points):
    # Inclination angle (theta) based on position along the line
    theta = np.pi - np.pi * point / 2.0
    # Azimuth angle (phi) as a function of position along the line
    phi = 0.0/180.0*np.pi
    # Convert spherical coordinates to Cartesian coordinates
    x_points_straight.append(radius * np.sin(theta) * np.cos(phi))
    y_points_straight.append(radius * np.cos(theta))
    z_points_straight.append(radius * np.sin(theta) * np.sin(phi))

    x_points_straight_inner.append(0.95*radius * np.sin(theta) * np.cos(phi))
    y_points_straight_inner.append(0.95*radius * np.cos(theta))
    z_points_straight_inner.append(0.95*radius * np.sin(theta) * np.sin(phi))

    # Azimuth angle (phi) as a function of position along the line
    phi = 1.0/180.0*np.pi

    # Convert spherical coordinates to Cartesian coordinates
    x_points_slanted.append(radius * np.sin(theta) * np.cos(phi))
    y_points_slanted.append(radius * np.cos(theta))
    z_points_slanted.append(radius * np.sin(theta) * np.sin(phi))

    x_points_slanted_inner.append(0.95*radius * np.sin(theta) * np.cos(phi))
    y_points_slanted_inner.append(0.95*radius * np.cos(theta))
    z_points_slanted_inner.append(0.95*radius * np.sin(theta) * np.sin(phi))

xyz_points_straight = np.stack((x_points_straight, y_points_straight, z_points_straight)).transpose()
xyz_points_slanted = np.stack((x_points_slanted, y_points_slanted, z_points_slanted)).transpose()
xyz_points_straight_inner = np.stack((x_points_straight_inner, y_points_straight_inner, z_points_straight_inner)).transpose()
xyz_points_slanted_inner = np.stack((x_points_slanted_inner, y_points_slanted_inner, z_points_slanted_inner)).transpose()

xyz_points_straight[:, 0] += -230.4
xyz_points_straight[:, 1] += 25.1
xyz_points_straight[:, 2] += -230.4

xyz_points_slanted[:, 0] += -230.4
xyz_points_slanted[:, 1] += 25.1
xyz_points_slanted[:, 2] += -230.4

xyz_points_straight_inner[:, 0] += -230.4
xyz_points_straight_inner[:, 1] += 25.1
xyz_points_straight_inner[:, 2] += -230.4

xyz_points_slanted_inner[:, 0] += -230.4
xyz_points_slanted_inner[:, 1] += 25.1
xyz_points_slanted_inner[:, 2] += -230.4

xyz_points_indenter = np.concatenate((xyz_points_straight, xyz_points_slanted, xyz_points_straight_inner, xyz_points_slanted_inner), axis=0)

precision = 10  # Adjust this according to your precision requirements
# Round the array elements to the specified precision
xyz_points_indenter = np.around(xyz_points_indenter, decimals=precision)
xyz_points_indenter = np.unique(xyz_points_indenter, axis=0)

z_num = 36
y_num = 10
angle = np.radians(1)  # Adjust the rotation angle as needed
# Define ranges for x, y, and z
x_range = np.linspace(-230.4, 230.0, 2)  # Adjust the number of points as needed)
z_range = np.linspace(-230.4, -230.4+0.36, z_num)
y_range = np.linspace(24.85, 25, y_num)

z_range_supp = []
for i in range(z_range.size//4):
    z_range_supp.append((z_range[i]+z_range[i+1])/2.0)
z_range = np.concatenate((z_range, z_range_supp))
z_range = np.unique(z_range)

y_range_supp = []
for i in range(y_range.size//2):
    y_range_supp.append((y_range[-i]+y_range[-i-1])/2.0)
y_range = np.concatenate((y_range, y_range_supp))
y_range = np.unique(y_range)

z_num = z_range.size
y_num = y_range.size

# y_range_supp = np.linspace(y_range[len(y_range)//2], 25, y_num)
# y_range = np.concatenate((y_range, y_range_supp))
# y_range = np.unique(y_range)

# Create 3D meshgrid
X, Z = np.meshgrid(x_range, z_range)

# Flatten the meshgrid to get 1D arrays of coordinates
x_points = X.flatten()
x_points_max_idx = np.where(x_points == np.max(x_points))[0]
x_points_min_idx = np.where(x_points == np.min(x_points))[0]
x_min = np.min(x_points[x_points_max_idx])
x_points_slanted = x_points[x_points_max_idx] - x_min
x_points_straight = x_points[x_points_min_idx]

z_points = Z.flatten()
z_min = np.min(z_points[x_points_max_idx])
z_points_slanted = z_points[x_points_max_idx] - z_min
z_points_straight = z_points[x_points_min_idx]

# Create 3D meshgrid for the second set of points, rotated about the z-axis
x_points[x_points_max_idx] = x_points_slanted * np.cos(angle) + z_points_slanted * np.sin(angle) + x_min
z_points[x_points_max_idx] = -x_points_slanted * np.sin(angle) + z_points_slanted * np.cos(angle) + z_min
x_points[x_points_max_idx] -= np.min(x_points[x_points_max_idx]) - np.min(x_points_straight)
z_points[x_points_max_idx] -= np.min(z_points[x_points_max_idx]) - np.min(z_points)
x_points_slanted = copy.deepcopy(x_points[x_points_max_idx])
z_points_slanted = copy.deepcopy(z_points[x_points_max_idx])

y_points = []
for i in range(y_num):
    y_points.append(np.ones_like(x_points)*y_range[i])
y_points = np.concatenate(y_points)
x_points = np.tile(x_points, y_num)
z_points = np.tile(z_points, y_num)
xyz_points = np.stack((x_points, y_points, z_points)).transpose()

precision = 10  # Adjust this according to your precision requirements
# Round the array elements to the specified precision
xyz_points = np.around(xyz_points, decimals=precision)
xyz_points = np.unique(xyz_points, axis=0)

tmp = copy.deepcopy(xyz_points[:, 0])
xyz_points[:, 0] = copy.deepcopy(xyz_points[:, 2])
xyz_points[:, 2] = tmp

# Define ranges for x, y, and z
y_range2 = np.linspace(24.8, 24.85, 6)

# Create 3D meshgrid
X, Z = np.meshgrid(x_range, z_range)

# Flatten the meshgrid to get 1D arrays of coordinates
x_points = X.flatten()
x_points_max_idx = np.where(x_points == np.max(x_points))[0]
x_points_min_idx = np.where(x_points == np.min(x_points))[0]
x_min = np.min(x_points[x_points_max_idx])
x_points_slanted = x_points[x_points_max_idx] - x_min
x_points_straight = x_points[x_points_min_idx]

z_points = Z.flatten()
z_min = np.min(z_points[x_points_max_idx])
z_points_slanted = z_points[x_points_max_idx] - z_min
z_points_straight = z_points[x_points_min_idx]

# Create 3D meshgrid for the second set of points, rotated about the z-axis

x_points[x_points_max_idx] = x_points_slanted * np.cos(angle) + z_points_slanted * np.sin(angle) + x_min
z_points[x_points_max_idx] = -x_points_slanted * np.sin(angle) + z_points_slanted * np.cos(angle) + z_min

x_points[x_points_max_idx] -= np.min(x_points[x_points_max_idx]) - np.min(x_points_straight)
z_points[x_points_max_idx] -= np.min(z_points[x_points_max_idx]) - np.min(z_points)
x_points_slanted = copy.deepcopy(x_points[x_points_max_idx])
z_points_slanted = copy.deepcopy(z_points[x_points_max_idx])

y_points = []
for i in range(6):
    y_points.append(np.ones_like(x_points)*y_range2[i])
y_points = np.concatenate(y_points)
x_points = np.tile(x_points, 6)
z_points = np.tile(z_points, 6)
xyz_points2 = np.stack((x_points, y_points, z_points)).transpose()

precision = 10  # Adjust this according to your precision requirements
# Round the array elements to the specified precision
xyz_points2 = np.around(xyz_points2, decimals=precision)
xyz_points2 = np.unique(xyz_points2, axis=0)

tmp = copy.deepcopy(xyz_points2[:, 0])
xyz_points2[:, 0] = copy.deepcopy(xyz_points2[:, 2])
xyz_points2[:, 2] = tmp

xyz_points = np.concatenate((xyz_points_indenter, xyz_points, xyz_points2), axis=0)
xyz_points = np.around(xyz_points, decimals=precision)
xyz_points = np.unique(xyz_points, axis=0)

node_list = []
for i in range(xyz_points.shape[0]):
    node_list.append({'@id': str(i + 1), '#text': ', '.join(map(str, xyz_points[i, :])).replace(" ", "")})
data_dict['febio_spec']['Mesh']['Nodes']['node'] = node_list

wedge_mesh_info = []
hexahedral_mesh_info = []

xyz_dict = {}
xyz_sub_idx = find_indices(xyz_points, xyz_points_straight_inner)
xyz_dict['y_top_straight_idx'] = copy.deepcopy(xyz_sub_idx)
xyz_sub_idx = find_indices(xyz_points, xyz_points_slanted_inner)
xyz_dict['y_top_slanted_idx'] = copy.deepcopy(xyz_sub_idx)
xyz_sub_idx = find_indices(xyz_points, xyz_points_straight)
xyz_dict['y_bot_straight_idx'] = copy.deepcopy(xyz_sub_idx)
xyz_sub_idx = find_indices(xyz_points, xyz_points_slanted)
xyz_dict['y_bot_slanted_idx'] = copy.deepcopy(xyz_sub_idx)

wedge_mesh_idx = [xyz_dict['y_bot_straight_idx'][0], xyz_dict['y_bot_slanted_idx'][1], xyz_dict['y_bot_straight_idx'][1]]
wedge_mesh_idx.append(xyz_dict['y_top_straight_idx'][0])
wedge_mesh_idx.append(xyz_dict['y_top_slanted_idx'][1])
wedge_mesh_idx.append(xyz_dict['y_top_straight_idx'][1])
wedge_mesh_idx = np.array(wedge_mesh_idx) + 1
wedge_mesh_info.append({'@id': str(1), '#text': ', '.join(map(str, wedge_mesh_idx)).replace(" ", "")})

num_hex = line_points.size - 2
for i in range(num_hex):
    hexahedral_mesh_idx = [xyz_dict['y_bot_straight_idx'][i+1], xyz_dict['y_bot_slanted_idx'][i+1],
                           xyz_dict['y_bot_slanted_idx'][i+2], xyz_dict['y_bot_straight_idx'][i+2]]
    hexahedral_mesh_idx.append(xyz_dict['y_top_straight_idx'][i+1])
    hexahedral_mesh_idx.append(xyz_dict['y_top_slanted_idx'][i+1])
    hexahedral_mesh_idx.append(xyz_dict['y_top_slanted_idx'][i+2])
    hexahedral_mesh_idx.append(xyz_dict['y_top_straight_idx'][i+2])
    hexahedral_mesh_idx = np.array(hexahedral_mesh_idx) + 1
    hexahedral_mesh_info.append({'@id': str(i+1), '#text': ', '.join(map(str, hexahedral_mesh_idx)).replace(" ", "")})

data_dict['febio_spec']['Mesh']['Elements'][0]['elem'] = wedge_mesh_info
data_dict['febio_spec']['Mesh']['Elements'][1]['elem'] = hexahedral_mesh_info

wedge_mesh_info = []
hexahedral_mesh_info = []
for i in range(y_num-1):
    y_bot = y_range[i]
    y_top = y_range[i+1]

    xyz_dict = {}
    xyz_sub_coor = np.stack((z_points_straight, np.ones_like(x_points_straight)*y_top, x_points_straight)).transpose()
    xyz_sub_idx = find_indices(xyz_points, xyz_sub_coor)
    xyz_dict['y_top_straight'] = copy.deepcopy(xyz_sub_coor)
    xyz_dict['y_top_straight_idx'] = copy.deepcopy(xyz_sub_idx)

    xyz_sub_coor = np.stack((z_points_slanted, np.ones_like(x_points_straight)*y_top, x_points_slanted)).transpose()
    xyz_sub_idx = find_indices(xyz_points, xyz_sub_coor)
    xyz_dict['y_top_slanted'] = copy.deepcopy(xyz_sub_coor)
    xyz_dict['y_top_slanted_idx'] = copy.deepcopy(xyz_sub_idx)

    xyz_sub_coor = np.stack((z_points_straight, np.ones_like(x_points_straight)*y_bot, x_points_straight)).transpose()
    xyz_sub_idx = find_indices(xyz_points, xyz_sub_coor)
    xyz_dict['y_bot_straight'] = copy.deepcopy(xyz_sub_coor)
    xyz_dict['y_bot_straight_idx'] = copy.deepcopy(xyz_sub_idx)
    xyz_sub_coor = np.stack((z_points_slanted, np.ones_like(x_points_straight)*y_bot, x_points_slanted)).transpose()
    xyz_sub_idx = find_indices(xyz_points, xyz_sub_coor)
    xyz_dict['y_bot_slanted'] = copy.deepcopy(xyz_sub_coor)
    xyz_dict['y_bot_slanted_idx'] = copy.deepcopy(xyz_sub_idx)

    wedge_mesh_idx = [xyz_dict['y_bot_straight_idx'][0], xyz_dict['y_bot_slanted_idx'][1], xyz_dict['y_bot_straight_idx'][1]]
    wedge_mesh_idx.append(xyz_dict['y_top_straight_idx'][0])
    wedge_mesh_idx.append(xyz_dict['y_top_slanted_idx'][1])
    wedge_mesh_idx.append(xyz_dict['y_top_straight_idx'][1])
    wedge_mesh_idx = np.array(wedge_mesh_idx) + 1
    wedge_mesh_info.append({'@id': str(i + 1), '#text': ', '.join(map(str, wedge_mesh_idx)).replace(" ", "")})

    num_hex = z_num - 2
    for j in range(num_hex):
        hexahedral_mesh_idx = [xyz_dict['y_bot_straight_idx'][j+1], xyz_dict['y_bot_slanted_idx'][j+1],
                               xyz_dict['y_bot_slanted_idx'][j+2], xyz_dict['y_bot_straight_idx'][j+2]]
        hexahedral_mesh_idx.append(xyz_dict['y_top_straight_idx'][j+1])
        hexahedral_mesh_idx.append(xyz_dict['y_top_slanted_idx'][j+1])
        hexahedral_mesh_idx.append(xyz_dict['y_top_slanted_idx'][j+2])
        hexahedral_mesh_idx.append(xyz_dict['y_top_straight_idx'][j+2])
        hexahedral_mesh_idx = np.array(hexahedral_mesh_idx) + 1
        hexahedral_mesh_info.append({'@id': str(num_hex*i+j+1), '#text': ', '.join(map(str, hexahedral_mesh_idx)).replace(" ", "")})

data_dict['febio_spec']['Mesh']['Elements'][2]['elem'] = wedge_mesh_info
data_dict['febio_spec']['Mesh']['Elements'][3]['elem'] = hexahedral_mesh_info

wedge_mesh_info = []
hexahedral_mesh_info = []
for i in range(5):
    y_bot = y_range2[i]
    y_top = y_range2[i+1]

    xyz_dict = {}
    xyz_sub_coor = np.stack((z_points_straight, np.ones_like(x_points_straight)*y_top, x_points_straight)).transpose()
    xyz_sub_idx = find_indices(xyz_points, xyz_sub_coor)
    xyz_dict['y_top_straight'] = copy.deepcopy(xyz_sub_coor)
    xyz_dict['y_top_straight_idx'] = copy.deepcopy(xyz_sub_idx)

    xyz_sub_coor = np.stack((z_points_slanted, np.ones_like(x_points_straight)*y_top, x_points_slanted)).transpose()
    xyz_sub_idx = find_indices(xyz_points, xyz_sub_coor)
    xyz_dict['y_top_slanted'] = copy.deepcopy(xyz_sub_coor)
    xyz_dict['y_top_slanted_idx'] = copy.deepcopy(xyz_sub_idx)

    xyz_sub_coor = np.stack((z_points_straight, np.ones_like(x_points_straight)*y_bot, x_points_straight)).transpose()
    xyz_sub_idx = find_indices(xyz_points, xyz_sub_coor)
    xyz_dict['y_bot_straight'] = copy.deepcopy(xyz_sub_coor)
    xyz_dict['y_bot_straight_idx'] = copy.deepcopy(xyz_sub_idx)
    xyz_sub_coor = np.stack((z_points_slanted, np.ones_like(x_points_straight)*y_bot, x_points_slanted)).transpose()
    xyz_sub_idx = find_indices(xyz_points, xyz_sub_coor)
    xyz_dict['y_bot_slanted'] = copy.deepcopy(xyz_sub_coor)
    xyz_dict['y_bot_slanted_idx'] = copy.deepcopy(xyz_sub_idx)

    wedge_mesh_idx = [xyz_dict['y_bot_straight_idx'][0], xyz_dict['y_bot_slanted_idx'][1], xyz_dict['y_bot_straight_idx'][1]]
    wedge_mesh_idx.append(xyz_dict['y_top_straight_idx'][0])
    wedge_mesh_idx.append(xyz_dict['y_top_slanted_idx'][1])
    wedge_mesh_idx.append(xyz_dict['y_top_straight_idx'][1])
    wedge_mesh_idx = np.array(wedge_mesh_idx) + 1
    wedge_mesh_info.append({'@id': str(i + 1), '#text': ', '.join(map(str, wedge_mesh_idx)).replace(" ", "")})

    num_hex = z_num - 2
    for j in range(num_hex):
        hexahedral_mesh_idx = [xyz_dict['y_bot_straight_idx'][j+1], xyz_dict['y_bot_slanted_idx'][j+1],
                               xyz_dict['y_bot_slanted_idx'][j+2], xyz_dict['y_bot_straight_idx'][j+2]]
        hexahedral_mesh_idx.append(xyz_dict['y_top_straight_idx'][j+1])
        hexahedral_mesh_idx.append(xyz_dict['y_top_slanted_idx'][j+1])
        hexahedral_mesh_idx.append(xyz_dict['y_top_slanted_idx'][j+2])
        hexahedral_mesh_idx.append(xyz_dict['y_top_straight_idx'][j+2])
        hexahedral_mesh_idx = np.array(hexahedral_mesh_idx) + 1
        hexahedral_mesh_info.append({'@id': str(num_hex*i+j+1), '#text': ', '.join(map(str, hexahedral_mesh_idx)).replace(" ", "")})

data_dict['febio_spec']['Mesh']['Elements'][4]['elem'] = wedge_mesh_info
data_dict['febio_spec']['Mesh']['Elements'][5]['elem'] = hexahedral_mesh_info

# Convert the dictionary back to XML
xml_content = xmltodict.unparse(data_dict, pretty=True)

# Save the updated XML content to the original file
with open(filename, 'w') as xml_file:
    xml_file.write(xml_content)

# Load the XML file
tree = ET.parse(filename)
root = tree.getroot()

# Find the specific element you want to modify
module_element = root.find('.//Module[@type="biphasic"]')

# Modify the element to use a self-closing tag
module_element.text = None

# Load the XML file
tree = ET.parse(filename)
root = tree.getroot()

# Find the specific element you want to modify
module_element = root.find('.//Module[@type="biphasic"]')

# Modify the element to use a self-closing tag
module_element.text = None

# Save the modified XML back to the file
tree.write(filename, xml_declaration=True, encoding="ISO-8859-1")

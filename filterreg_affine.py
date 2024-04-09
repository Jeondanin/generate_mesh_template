from probreg import filterreg, callbacks
import open3d as o3d
import math

def register_pcd(source, target):
    tf_param, _, _ = filterreg.registration_filterreg(source, target, objective_type='pt2pt', sigma2=None, update_sigma2=True)
    return tf_param.rot, tf_param.t, tf_param.scale

def change_coordinates(rot_mat, trans_mat, scale_factor, coordinates, reverse=False):
    if reverse==False:
        coordinates = np.matmul(rot_mat, coordinates.transpose())*scale_factor  # rotation
        trans_mat = np.reshape(trans_mat, (-1, 3))
        trans_mat = np.repeat(trans_mat, coordinates.shape[1], axis=0).transpose()
        coordinates = coordinates + trans_mat  # translation
        coordinates = coordinates.transpose()
    else:
        trans_mat = np.reshape(trans_mat, (-1, 3))
        coordinates = coordinates - np.repeat(trans_mat, coordinates.shape[0], axis=0)
        coordinates = np.matmul(np.linalg.inv(rot_mat*scale_factor), coordinates.transpose()).transpose()
    return coordinates

N = 10000
M = 3000

points1 = np.zeros((N, 3)) # N by 3 array
points2 = np.zeros((M, 3)) # M by 3 array

rot_mat, trans_mat, scale_factor = register_pcd(points1, points2)
points1_registered = change_coordinates(rot_mat, trans_mat, scale_factor, points1)

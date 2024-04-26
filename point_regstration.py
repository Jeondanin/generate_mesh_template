import copy
import numpy as np
import argparse
# import open3d as o3
from probreg import filterreg
from probreg import callbacks
from probreg import transformation
import random
from utils import load_file, load_mesh, save_mesh
import open3d as o3

# TBD data type input point

def get_parser():
    desc = "This is a script for a generating mesh data file using point registration"
    parser = argparse.ArgumentParser(desc, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--template", type=str, help='mesh_template.mesh', required=True)
    parser.add_argument("--target", type=str,  help='example_output.nii.gz or point_cloud.txt', required=True)
    return parser

def main(args):
    # img_file = "example_output.nii.gz"
    if ".nii" in args.target:
        target_points = load_file(args.target)
    elif ".txt" in args.target:
        target_points = np.loadtxt(args.target) # np.loadtxt('mesh_template0413-target.txt')
    #-> target_points shape : (xxx, 3)

    vertices, faces, volume = load_mesh(args.template)
    source_points = np.array(vertices)
    #-> source_points shape : (yyy, 3)

    # make the number of template point equal to the number of segmented point
    template_random_idx = random.sample(range(source_points.shape[0]), target_points.shape[0])
    template_random_idx.sort()
    source_points = source_points[template_random_idx, :]

    n_points = target_points.shape[0]
    ws = transformation.DeformableKinematicModel.SkinningWeight(n_points)
    for i in range(n_points):
        ws['pair'][i][0] = 0
        ws['pair'][i][1] = 1
    for i in range(n_points):
        ws['val'][i][0] = float(i) / n_points
        ws['val'][i][1] = 1.0 - float(i) / n_points
    source = o3.geometry.PointCloud()
    source.points = o3.utility.Vector3dVector(source_points)
    target = o3.geometry.PointCloud()
    target.points = o3.utility.Vector3dVector(target_points)
    cbs = [callbacks.Open3dVisualizerCallback(target, source, keep_window=True, fov=75, save=True),
       ]
    cv = lambda x: np.asarray(x.points if isinstance(x, o3.geometry.PointCloud) else x)
    reg = filterreg.DeformableKinematicFilterReg(cv(target), ws, 0.001)
    reg.set_callbacks(cbs)

    tf_param, ab, cd = reg.registration(cv(source), maxiter=20, w=0.1, tol=0.002, min_sigma2=0.00005)
    result = cbs[0]._result # result.points[0] = array([x, y, z])
    # change position of point
    # changed index
    for _idx, v in zip(template_random_idx, result.points):
        vertices[_idx] = v

    save_mesh(vertices, faces, volume, "mesh_template-result.mesh")

    del cbs[0]



if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)

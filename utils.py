import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

def load_file(img_file):
    img = nib.load(img_file)
    data = img.get_fdata()
    return data

def load_mesh(path):
    vertices = []
    faces = []
    volumes = []
    with open(path, 'r') as f:
        lines = f.readlines()
        parsing_vertices = False
        parsing_faces = False
        parsing_hexahedra = False
        for line in lines:
            parts = line.strip().split()
            if len(parts) > 0:
                if parts[0] == 'Vertices':
                    parsing_vertices = True
                    parsing_faces = False
                elif parts[0] == 'Quadrilaterals':
                    parsing_faces = True
                    parsing_vertices = False
                elif parts[0] == "Hexahedra":
                    parsing_faces = False
                    parsing_vertices = False
                    parsing_hexahedra = True
                elif parsing_vertices:
                    # 정점 정보 파싱
                    vertex = [float(part) for part in parts]
                    if len(vertex) == 4:
                        vertices.append(vertex[:-1])
                    else:
                        print(f"vertex number : {int(vertex[0])}")
                elif parsing_faces:
                    # 사각형 인덱스 파싱
                    face = [int(part) for part in parts]
                    if len(face) == 4:
                        faces.append(face)
                    else:
                        print(f"face number : {int(face[0])}")
                elif parsing_hexahedra:
                    # 사각형 인덱스 파싱
                    volume = [int(part) for part in parts]
                    if len(volume) == 8:
                        volumes.append(volume)
                    elif len(volume) == 1:
                        print(f"face number : {int(volume[0])}")
            else:
                if parsing_hexahedra:
                    break

    return vertices, faces, volumes

def save_mesh(vertices, faces, volumes, output_file):
    with open(output_file, "w+") as f:
        f.write("MeshVersionFormatted 1\nDimension 3\nVertices\n")
        f.write(f"{len(vertices)}\n")
        for v in vertices:
            f.write(f"{round(v[0], 2)} {round(v[1], 2)} {round(v[2], 2)} 1\n")
        else:
            f.write("\n")
        f.write("Quadrilaterals\n")
        f.write(f"{len(faces)}\n")
        for f_item in faces:
            f.write(f"{' '.join(map(str, f_item))}\n")
        else:
            f.write("\n")
        f.write("Hexahedra\n")
        f.write(f"{len(volumes)}\n")
        for v_item in volumes:
            f.write(f"{' '.join(map(str, v_item))}\n")
        else:
            f.write("\n")
        f.write("End")

def visualize(data):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection="3d")
    x_size, y_size, z_size = data.shape
    x, y, z = np.meshgrid(range(x_size), range(y_size), range(z_size)) 

    nonzero_indices = np.nonzero(data)
    num_nonzero = len(nonzero_indices[0])
    half_indices = np.random.choice(num_nonzero, size=num_nonzero//2, replace=False)

    # for i in range(data.shape[0]):
    #     for j in range(data.shape[1]):
    #         for k in range(data.shape[2]):
    #             if data[i, j, k] > 0:
    ax.bar3d(x[nonzero_indices][half_indices], y[nonzero_indices][half_indices], z[nonzero_indices][half_indices], 1, 1, data[nonzero_indices][half_indices], color="gray")
    # ax.scatter(x.ravel(), y.ravel(), z.ravel(), c=data.ravel(), cmap='viridis')
    # ax.scatter(x[nonzero_indices], y[nonzero_indices], z[nonzero_indices], c=data[nonzero_indices], cmap='viridis')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label') 
    plt.show()
    input("Press Enter to close...")



if __name__ == "__main__":
    img_file = "example_output.nii.gz"
    data = load_file(img_file)
    visualize(data)
    # 출력
    x_size, y_size, z_size = data.shape
    x, y, z = np.meshgrid(range(x_size), range(y_size), range(z_size)) 
    nonzero_indices = np.nonzero(data)
    with open("cloudpoint.txt", "w+") as f:
        for i in range(len(nonzero_indices[0])):
            x_coord = nonzero_indices[0][i]/(data.shape[0] - 1)
            y_coord = nonzero_indices[1][i]/(data.shape[1] - 1)
            z_coord = nonzero_indices[2][i]/(data.shape[2] - 1)
            f.write(f"{x_coord} {y_coord} {z_coord}\n")

    print(49)

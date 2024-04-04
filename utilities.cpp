#include "utilities.hpp"
#include <iostream>
#include <armadillo>
#include <sstream>
#include <cmath>
using namespace arma;

void write_to_file(arma::mat mesh_vert, std::vector<int> shape)
{
    
    std::vector<std::string> faceList = {};
    std::vector<std::string> volumeList = {};
    int a = 1;
    int width = shape[0];
    int height = shape[1];
    int volume = shape[2];
    std::cout << a;
    std::ofstream outputFile;
    const char *path = "mesh_template.mesh";
    outputFile.open(path);

    outputFile << "MeshVersionFormatted 1\n";
    outputFile << "Dimension 3\n";
    outputFile << "Vertices\n";
    outputFile << mesh_vert.n_rows << "\n";
    for (int i = 0; i < mesh_vert.n_rows; ++i)
    {
        outputFile << mesh_vert(i, 0) << " " << mesh_vert(i, 1) << " " << mesh_vert(i, 2) << " " << 1 << "\n";
    }
    // shape 가로 X 세로 X 높이
    for (int h = 0; h < volume -1; h++)
    {
        for (int j = 0; j < height-1; ++j)
        {
            for (int i = 1; i <= width; ++i)
            {
                if ((j * (height) + i) % (height) == 0)
                {
                    continue;
                }
                int index_1 = h* (height)* (width) + j * (height) + i;
                int index_2 = h* (height)* (width) + j * (height) + (i + 1);
                int index_3 = h* (height)* (width) + (j + 1) * (height) + i + 1;
                int index_4 = h* (height)* (width) + (j + 1) * (height) + i;
                int index_5 = (h+1)* (height)* (width) + (j ) * (height) + i;
                int index_6 = (h+1)* (height)* (width) + (j ) * (height) + i + 1;
                int index_7 = (h+1)* (height)* (width) + (j + 1) * (height) + i + 1;
                int index_8 = (h+1)* (height)* (width) + (j + 1) * (height) + i;

                std::stringstream ss;
                // face - floor
                ss << index_1 << " " << index_2 << " " << index_3 << " " << index_4 <<"\n";
                if(h!=volume-1 ){
                    // face - default 2
                    ss << index_1 << " " << index_5 << " " << index_8 << " " << index_4 <<"\n";
                    ss << index_1 << " " << index_2 << " " << index_6 << " " << index_5 <<"\n";
                    // upper helmet 1
                    if(i==width -1){
                        ss << index_2 << " " << index_6 << " " << index_7 << " " << index_3 <<"\n";
                    }
                    //left helmet 1
                    if(j==height-2){
                        ss << index_4 << " " << index_3 << " " << index_7 << " " << index_8 <<"\n";
                    }
                    //z helmet 1
                    if(h==volume-2){
                        ss << index_5 << " " << index_6 << " " << index_7 << " " << index_8 <<"\n";
                    }
                    std::string combined1 = ss.str();
                    faceList.push_back(combined1);
                }
                // volume
                ss.str("");
                ss << index_1 << " " << index_2 << " " << index_3 << " " << index_4 << " "<< index_5 << " "<< index_6 << " "<< index_7 << " "<< index_8 <<"\n";
                std::string combined2 = ss.str();
                volumeList.push_back(combined2);
            }
        }
    }
    // write faces into file 
    outputFile << "\n";
    outputFile << "Quadrilaterals\n";
    
    outputFile << 3*(width-1)*(height-1)*(volume-1) + (width-1)*(height-1) + (volume-1)*(width-1) + (volume-1)*(height-1) << "\n";
    //   3 * 5 * 6 * 1 = 90                              5 *        6          + 1 * 5  
    for (const auto& str: faceList)
    {
        outputFile << str;
    }

    outputFile << "\n";
    outputFile << "Hexahedra\n";
    outputFile << (width-1)*(height-1)*(volume-1) << "\n";
   for (const auto& str: volumeList)
    {
        outputFile << str;
    }

    outputFile << "\n";
    outputFile << "End";
}

vec calc_splprep_u(arma::mat a)
{
    vec result(a.n_rows);
    vec V(a.n_rows);
    for (std::size_t i = 0; i < a.n_rows; ++i)
    {
        double new_v = V[i - 1];
        if (i == 0)
        {
            V(i) = 0;
        }
        else
        {
            double tmp_distance = distance(a(i, 0), a(i, 1), a(i - 1, 0), a(i - 1, 1));
            V(i) = V[i - 1] + tmp_distance;
        }
    }
    result.head(a.n_rows) = V / V(a.n_rows - 1);
    std::cout << result << endl;
    return result;
}

double distance(double x1, double y1, double x2, double y2)
{
    return sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2));
}

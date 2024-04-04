#include <iostream>
#include <vector>
#include <armadillo>
#include "utilities.hpp"

using namespace std;
using namespace arma;


int main()
{
    // mat m_left = {{0.0, 0.0, 0.0}, {0.1, 0.2, 0.0}, {0.18, 0.25, 0.0}, {0.18, 0.38, 0.0}, {0.19, 0.45, 0.0}, {0.2, 0.5, 0.0}};
    // mat m_right = {{0.5, 0.0, 0.0}, {0.5, 0.1, 0.0}, {0.55, 0.18, 0.0}, {0.6, 0.3, 0.0}, {0.65, 0.4, 0.0}, {0.7, 0.5, 0.0}};
    // mat m_lower = {{0.0, 0.0, 0.0}, {0.1, 0.0,0.0}, {0.2, 0.0, 0.0}, {0.3, 0.0, 0.0}, {0.4, 0.0, 0.0}, {0.45, 0.0, 0.0}, {0.5, 0.0, 0.0}};
    // mat m_upper = {{0.2, 0.5, 0.0}, {0.3, 0.5,0.0}, {0.4, 0.5, 0.0}, {0.5, 0.5, 0.0}, {0.6, 0.5, 0.0}, {0.64, 0.5, 0.0}, {0.7, 0.5, 0.0}};
    int mesh_size = 11;
    mat m_left(mesh_size, 3);
    mat m_right(mesh_size, 3);
    mat m_lower(mesh_size, 3);
    mat m_upper(mesh_size, 3);

    //closed plane
    for (int i = 0; i < mesh_size; i++){

        m_left(i, 0) = 0;
        m_left(i, 1) = i*0.05;
        m_left(i, 2) = 0;

        m_right(i , 0) = 1;
        m_right(i , 1) = i*0.05;
        m_right(i , 2) = 0;

        m_lower(i, 0) = i*0.05;
        m_lower(i, 1) = 0;
        m_lower(i, 2) = 0;

        m_upper(i, 0) = i*0.05;
        m_upper(i, 1) = 1;
        m_upper(i, 2) = 0;
    }


    vec u_left = calc_splprep_u(m_left);
    vec u_lower = calc_splprep_u(m_lower);

    vec lower_x = m_lower.col(0);
    vec lower_y = m_lower.col(1);
    vec upper_x = m_upper.col(0);
    vec upper_y = m_upper.col(1);


    // corner points
    double conp = 1;
    vec c1 = {{0, 0, 0}};
    vec c2 = {{0.0, conp, 0.0}};
    vec c3 = {{conp, 0.0, 0.0}};
    vec c4 = {{conp, conp, 0.0}};
    // 두께 
    int volume = 100;
    int height = m_lower.n_rows;
    int width = m_left.n_rows;

    std::vector<int> shape = {width, height, volume};

    mat mesh_vert(volume*m_lower.n_rows * m_left.n_rows, 3);

    for (int z = 0; z < volume; z++)
    {
        for (std::size_t i = 0; i < m_lower.n_rows; ++i)
        {
            double xi = u_lower(i);
            vec eta_lower_xy = {{m_lower(i, 0), m_lower(i, 1), m_lower(i, 2)}};
            vec eta_upper_xy = {{m_upper(i, 0), m_upper(i, 1), m_upper(i, 2)}};
            for (std::size_t j = 0; j < m_left.n_rows; ++j)
            {
                int node = z *u_left.n_rows*u_lower.n_rows + i * u_left.n_rows + j ;
                double eta = u_left(j);
                vec eta_left_xy = {{m_left(j, 0), m_left(j, 1), m_left(j, 2)}};
                vec eta_right_xy = {{m_right(j, 0), m_right(j, 1), m_right(j, 2)}};
                vec point_x = (1.0 - xi) * eta_left_xy + xi * eta_right_xy + (1.0 - eta) * eta_lower_xy + eta * eta_upper_xy - ((1.0 - xi) * (1.0 - eta) * c1 + ((1.0 - xi) * eta * c2) + xi * (1 - eta) * c3 + xi * eta * c4);
                // 각 평면과 평면의 스윕으로 쌓이는 거리 0.05
                point_x[2] = z*0.05;
                // 곡면이냐 평면이냐 값조정 
                // 곡면
                // point_x[0] -=z*1;
                // float angle_degree = static_cast<float>(z) / volume * 180.0f;
                // float angle_radian = angle_degree * 3.14159265f / 180.0f;
                // float sine_value = std::sin(angle_radian);
                // 평면
                float sine_value = 0;
                point_x[1] = point_x[1] + 0.1*sine_value;
                std::cout << point_x << endl;
                mesh_vert.row(node) = point_x.t();
            }
        }
    }
    // std::cout << mesh_vert << endl;
    write_to_file(mesh_vert, shape);
}
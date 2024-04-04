

#ifndef UTILITIES_HPP
#define UTILITIES_HPP

#include <iostream>
#include <fstream>
#include <map>
#include <vector>
#include <armadillo>

using namespace arma;

void write_to_file(arma::mat mesh_vert, std::vector<int> shape);
vec calc_splprep_u(arma::mat a);
double distance(double x1, double y1, double x2, double y2);


#endif // HEADER_H
#include <vector>
#include <string>
#include <map>
#include "data_structure.hpp"
std::map<data_structure::waypoint, std::vector<data_structure::waypoint>> adjacency_list = {
    { data_structure::waypoint(104, 847, 1, false, true, false), {data_structure::waypoint(105, 799, 17, false, false, true)}},
    { data_structure::waypoint(105, 799, 17, false, false, true), {data_structure::waypoint(104, 847, 1, false, true, false), data_structure::waypoint(992, 799, 3, false, true, false)}},
    { data_structure::waypoint(992, 799, 3, false, true, false), {data_structure::waypoint(105, 799, 17, false, false, true), data_structure::waypoint(915, 800, 1, true, false, false)}},
    { data_structure::waypoint(915, 800, 1, true, false, false), {data_structure::waypoint(992, 799, 3, false, true, false)}},
};

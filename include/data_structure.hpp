#pragma once

#include <vector>
#include <string>

namespace data_structure{
    class waypoint{
        public:
            int x_coordinate, y_coordinate;
            bool is_collection_point, is_delivery_point, is_pathfinding_point;
            int id;
            waypoint(int _x_coordinate, int _y_coordinate, int _id, bool _is_collection_point = false, bool _is_delivery_point = false, bool _is_pathfinding_point = false){
                x_coordinate = _x_coordinate;
                y_coordinate = _y_coordinate;
                id = _id;
                is_collection_point = _is_collection_point;
                is_delivery_point = _is_delivery_point;
                is_pathfinding_point = _is_pathfinding_point;
            }
            bool operator<(const waypoint& other) const {
                return std::tie(x_coordinate, y_coordinate) < std::tie(other.x_coordinate, other.y_coordinate);
            }            
    };
}
#pragma once
// ======================================================================================
// Copyright 2017 State Key Laboratory of Remote Sensing Science,
// Institute of Remote Sensing Science and Engineering, Beijing Normal
// University

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// ======================================================================================
#include "Cloth.h"
#include "PointCloud.h"

class Rasterization
{
   public:
    Rasterization() {}
    ~Rasterization() {}

    // for a cloth particle, if no corresponding lidar point are found.
    // the heightval are set as its neighbor's
    double static findHeightValByNeighbor(Particle& p);
    double static findHeightValByScanline(Particle& p, const Cloth& cloth);

    void static Rasterize(Cloth& cloth, const csf::PointCloud& pc, std::vector<double>& heightVal);

   private:
    static inline double square_dist(double x1, double y1, double x2, double y2)
    {
        return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2);
    }
};

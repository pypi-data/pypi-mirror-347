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

#include "Rasterization.h"

#include <cstdint>
#include <queue>

// find height by scanning the nearest particles in the same row and column
double Rasterization::findHeightValByScanline(Particle& p, const Cloth& cloth)
{
    const uint32_t xpos = p.pos_x;
    const uint32_t ypos = p.pos_y;

    const auto [cloth_width, cloth_height] = cloth.getGridSize();

    for (uint32_t i = xpos + 1; i < cloth_width; i++)
    {
        const double crresHeight = cloth.getParticle(i, ypos).nearest_point_height;

        if (crresHeight > MIN_INF) return crresHeight;
    }

    for (int32_t i = static_cast<int32_t>(xpos) - 1; i >= 0; --i)
    {
        const double crresHeight = cloth.getParticle(i, ypos).nearest_point_height;

        if (crresHeight > MIN_INF) return crresHeight;
    }

    for (int32_t j = static_cast<int32_t>(ypos) - 1; j >= 0; --j)
    {
        const double crresHeight = cloth.getParticle(xpos, j).nearest_point_height;

        if (crresHeight > MIN_INF) return crresHeight;
    }

    for (uint32_t j = ypos + 1; j < cloth_height; j++)
    {
        const double crresHeight = cloth.getParticle(xpos, j).nearest_point_height;

        if (crresHeight > MIN_INF) return crresHeight;
    }
    return findHeightValByNeighbor(p);
}

// find height by Region growing around the current particle
double Rasterization::findHeightValByNeighbor(Particle& p)
{
    std::queue<Particle*>  nqueue;
    std::vector<Particle*> pbacklist;

    // initialize the queue with the neighbors of the current particle
    p.is_visited = true;
    for (auto neighbor : p.neighborsList)
    {
        neighbor->is_visited = true;
        nqueue.push(neighbor);
    }

    double res_value = MIN_INF;
    // iterate over a queue of neighboring particles
    while (!nqueue.empty())
    {
        Particle* pneighbor = nqueue.front();
        nqueue.pop();
        pbacklist.push_back(pneighbor);

        // if the current enqueued particle has a height defined we assign it
        // to the res_value and break;
        if (pneighbor->nearest_point_height > MIN_INF)
        {
            res_value = pneighbor->nearest_point_height;
            break;
        }
        else
        {  // else we schedule to visit the neighbors of the current neighbor
            for (auto ptmp : pneighbor->neighborsList)
            {
                if (!ptmp->is_visited)
                {
                    ptmp->is_visited = true;
                    nqueue.push(ptmp);
                }
            }
        }
    }

    // reset the visited flag for all the particles in the backlist...
    p.is_visited = false;
    for (auto p : pbacklist) { p->is_visited = false; };
    //... And reset the visited flag for all the particles in the queue
    while (!nqueue.empty())
    {
        Particle* pp   = nqueue.front();
        pp->is_visited = false;
        nqueue.pop();
    }

    return res_value;
}

void Rasterization::Rasterize(Cloth& cloth, const csf::PointCloud& pc, std::vector<double>& heightVal)
{
    for (const auto& point : pc)
    {
        const double  delta_x = point.x - cloth.origin_pos.f[0];
        const double  delta_z = point.z - cloth.origin_pos.f[2];
        const int32_t col     = int32_t(delta_x / cloth.step_x + 0.5);
        const int32_t row     = int32_t(delta_z / cloth.step_y + 0.5);

        if ((col >= 0) && (row >= 0))
        {
            Particle& particle = cloth.getParticle(col, row);

            const double point_to_particle_dist =
                square_dist(point.x, point.z, particle.initial_pos.f[0], particle.initial_pos.f[2]);

            if (point_to_particle_dist < particle.tmp_dist)
            {
                particle.tmp_dist             = point_to_particle_dist;
                particle.nearest_point_height = point.y;
            }
        }
    }

    heightVal.resize(cloth.getSize());
    for (uint32_t i = 0; i < cloth.getSize(); i++)
    {
        Particle&    pcur           = cloth.getParticle(i);
        const double nearest_height = pcur.nearest_point_height;

        if (nearest_height > MIN_INF) { heightVal[i] = nearest_height; }
        else
        {
            // fill height value for cells without height value yet
            heightVal[i] = findHeightValByScanline(pcur, cloth);
        }
    }
}

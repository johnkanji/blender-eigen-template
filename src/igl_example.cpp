#include <npe.h>
#include <igl/doublearea.h>
#include <iostream>

npe_function(igl_example)

npe_arg(V, dense_double)
npe_arg(F, dense_int)
npe_arg(R, npe_matches(V))

npe_begin_code() 
{
  // Compute areas, min, max and standard deviation
  Eigen::VectorXd area;
  igl::doublearea(V,F,area);
  area = area.array() / 2;

  double area_avg   = area.mean();
  double area_min   = area.minCoeff() / area_avg;
  double area_max   = area.maxCoeff() / area_avg;
  double area_sigma = sqrt(((area.array()-area_avg)/area_avg).square().mean());

  printf("Areas (Min/Max)/Avg_Area Sigma: \n%.2f/%.2f (%.2f)\n",
    area_min,area_max,area_sigma);
  
  npe_Matrix_V V_rotated = V;
  V_rotated = V_rotated * R.transpose();
  V_rotated *= 2;

  return npe::move(V_rotated);
}
npe_end_code()
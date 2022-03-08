/*//////////////////////////////////////////////////////////////////////////////
This file contains the implementation of the support functions used in read_claro.cpp and in class Claro defined in Claro.h.
//////////////////////////////////////////////////////////////////////////////*/

// #include <cstdlib>
#include <iostream>
#include <cstring>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <stdio.h>
#include <cmath>

using namespace std;

//----------------------------------------------------------------------------//
float mean(const std::vector<float>& x)
{
    float sum {0};
    auto len {x.size()};
    for (auto& i : x) { sum += i; }
    // float sum = accumulate(x.begin(), x.end(), 0);

    return sum/len;
}
//----------------------------------------------------------------------------//
float se(const std::vector<float>& x)
/*Computes the sum of the squared errors wrt the mean of the data.*/
{
    float xse {0};
    float meanx {mean(x)};
    for (auto& i : x) { xse += std::pow((i-meanx),2); }

    return xse;
}
//----------------------------------------------------------------------------//
float var(const std::vector<float>& x)
{
    float xse {se(x)};
    auto len {x.size()};

    return xse/(len-1);
}
//----------------------------------------------------------------------------//
float covar(const std::vector<float>& x, const std::vector<float>& y)
{
    float sum {0};
    auto len {x.size()};
    float meanx {mean(x)};
    float meany {mean(y)};
    for (int i {0}; i<len; i++) { sum += (x.at(i)-meanx)*(y.at(i)-meany); }

    return sum/(len-1);
}
//----------------------------------------------------------------------------//
float aCoeff(const std::vector<float>& x, const std::vector<float>& y)
{
    float varx {var(x)};
    float covxy {covar(x,y)};

    return covxy/varx;
}
//----------------------------------------------------------------------------//
float bCoeff(const std::vector<float>& x, const std::vector<float>& y)
{
    float a {aCoeff(x,y)};
    float meanx {mean(x)};
    float meany {mean(y)};

    return meany-a*meanx;
}
//----------------------------------------------------------------------------//
float rsq(const std::vector<float>& x, const std::vector<float>& y)
/* Computes an estimate of the r2 coefficient (Pearson) for linear regression. IMPORTANT: this coefficient is NOT AN INDEX OF THE PERFORMANCE OF THE FIT but depends only on the correlation of the input data. */
{
    float varx {var(x)};
    float vary {var(y)};
    float covxy {covar(x,y)};

    return std::pow(covxy,2)/(varx*vary);
}
//----------------------------------------------------------------------------//
float sigmasq(const std::vector<float>& x, const std::vector<float>& y)
/* Computes an estimate of the variance of the error between the observed and fitted data. This quantity is distributed as a chi-squared random variable with n-2 degrees of freedom, where n is the number of x,y couples provided */
{
    float sum {0};
    auto len (x.size());
    float a {aCoeff(x,y)};
    float b {bCoeff(x,y)};
    for (int i {0}; i<len; i++) { sum += std::pow((y.at(i)-(a*x.at(i)+b)),2); }

    return sum/(len-1); // using len-1 instead of len-2 for compatibility with taking 2 data (linear fit is not a fit but a line between two points)
}
//----------------------------------------------------------------------------//
float aErr(const std::vector<float>& x, const std::vector<float>& y)
{
    float xse {se(x)};
    float sigma {sigmasq(x,y)};

    return sqrt(sigma/xse); // returning without sqrt gives the variance
}
//----------------------------------------------------------------------------//
float bErr(const std::vector<float>& x, const std::vector<float>& y)
{
    float ss {0};
    float xse {se(x)};
    auto len {x.size()};
    float sigma_2 {sigmasq(x,y)};
    for (auto& i : x) { ss += std::pow(i,2); }

    return sqrt(sigma_2*ss/(len*xse)); // returning without sqrt gives the variance
}

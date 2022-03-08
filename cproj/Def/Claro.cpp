/*//////////////////////////////////////////////////////////////////////////////
This file contains the implementation of the methods of class Claro, defined in Claro.h.
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
#include "Claro.h"

using namespace std;

//----------------------------------------------------------------------------//

void Claro::readFile() //(const std::string& FILE)
/*
 * This function does this:
 * - open the file passed as an argument and checks if file is good or bad
 * - reads line by line as std::string
 * - puts a whole line as an element of a vector<string>
 */
{
    std::ifstream input {this->FILEPATH.c_str()};
    if (!input)
    {
        std::cerr << "Error: Unable to open file" << std::endl;
        exit(1);
    }

    std::string line;
    /*
     * while loop with getline cannot be used by choosing tab as delimiter
     * because in this way the return '\n' cannot be parsed and data are gotten
     * in the wrong way.
     * The following statement builds a std::vector of strings, each string
     * contains a single line of the txt file.
    */
     std::cout << "\n******* Data From File ********" << '\n';
     while (std::getline(input, line))
    {
        if(line.size())
        {
            this->lines.push_back(line);
            std::cout << line << '\n';
        }
    }
    // return linesVector; // std::vector of std::strings, each element a line of the file
}
//----------------------------------------------------------------------------//
DataStruct Claro::xyData() //(const std::vector<std::string>& linesVector)

/////////////////////////// UPDATE TO MAKE /////////////////////////////////////
// - return DataStruct and do nothing else if x,y,meta values are already attributes
// or
// - delete attributes and rewrite if they are already present
// - update custom constructor
////////////////////////////////////////////////////////////////////////////////

{
    DataStruct copy {this->meta, this->x, this->y, this->y1};
    if (this->x.size()) { return copy; }

    // take each line of the txt file as element
    int i {0}; // counter for lines
    for (auto const line : this->lines)
    {
        // split each element in its tokens
        auto    tokens = ssplit(line, "\t");
        int     j {0}; // counter for tokens=columns

        for (auto token : tokens)
        {
            auto datum = std::stof(token);
            // if tokens belong to first two lines, put in vector of metadata
            // else put in x, y1, y2 vectors depending on column they belong to
            if (i<2)
                // this->data.meta.push_back(datum);
                this->meta.push_back(datum);
            else
            {
                if (j==0)       // column 0
                    this->x.push_back(datum);
                else if (j==1)  // column 1
                    this->y.push_back(datum);
                else if (j==2)  // column 2
                    this->y1.push_back(datum);
            }
            j++;
        }
        i++;
    }
    return copy;
}
//----------------------------------------------------------------------------//
DataStruct Claro::linear_fit(float y_low, float y_high)
/*
 * The linear_fit function builds a linear fit on provided x,y data via maximum likelihood method, returning the maximum likelihood extimates of a,b parameters such that ax+b=y is the linear function that also satisfies Gauss' minimum squares regression method. Errors on a and b are provided as well as sigma2, variance of the estimation error. Sigma2 is distributed as a chi-squared random variable with deg=n-2 where n=number of  (x,y) tuples provided.
 * To evaluate the performance of the fit one should fix the first order estimation error and use sigma2 (comparing with tabulated values for n-2 degrees of freedom) or r2 (comparing with tabulated values for n degrees of freedom).
*/
{
    std::vector<float> chosen_y {}, chosen_x {};

    std::cout << "\n******* Linear Fit Data *******" << '\n';
    std::cout << "x" << '\t' << "y" << '\n';
    for (int i {0}; i<y.size(); i++)
    {
        if (y.at(i)>y_low && y.at(i)<y_high)
        {
            chosen_x.push_back(x.at(i));
            chosen_y.push_back(y.at(i));
            std::cout << x.at(i) << '\t' << y.at(i) << '\n';
        }
    }

    a.push_back(aCoeff(chosen_x, chosen_y));
    a.push_back(aErr(chosen_x, chosen_y));
    b.push_back(bCoeff(chosen_x, chosen_y));
    b.push_back(bErr(chosen_x, chosen_y));
    sigmasq_fit.push_back(sigmasq(chosen_x, chosen_y));
    rsq_fit.push_back(rsq(chosen_x, chosen_y));

    cout.precision(2);
    // const char *pm = u8"\u00B1";
    std::cout << "\nN entries: " << chosen_x.size() << '\n' << '\n';
    std::cout << "********* Fit results *********" << '\n';
    std::cout << "angular coeff (a): " << a.at(0) << " +- " << a.at(1) << '\n';
    std::cout << "intercept (b): " << b.at(0) << " +- " << b.at(1) << '\n';
    std::cout << "r2: " << rsq_fit.at(0) << '\n';
    std::cout << "sigma2: " << sigmasq_fit.at(0) << '\n';

    DataStruct fit_return {a, b, sigmasq_fit, rsq_fit};
    return fit_return;
}
//----------------------------------------------------------------------------//
std::vector<std::string> Claro::ssplit(std::string const& s, std::string const& del)
/*
 * The ssplit function takes any string and tokenizes it by any std::string
 * delimiter provided. WARNING: doesn't work with char standard delimiters
 * such as '\t', '\n', etc... : to use char delimiters just use "".
 * The function returns a vector of strings containing each token that comes
 * from the splitting of the string.
 */
{
    int start = 0;
    int end = s.find(del);
    std::vector<std::string> tokens;

    while (end != -1)
    {
        tokens.push_back(s.substr(start, end - start));
        start = end + del.size();
        end = s.find(del, start);
    }
    tokens.push_back(s.substr(start, end - start));

    return tokens;
}
//----------------------------------------------------------------------------//

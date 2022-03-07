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
    std::ifstream input {this->FILEPATH.c_str()}; //.c_str converts to a c-string

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
     while (std::getline(input, line))
    {
        if(line.size())
        {
            this->lines.push_back(line);
            std::cout << line <<'\n';
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
    DataStruct copy {this->meta, this->x, this->y, this->y1};
    return copy;
}
//----------------------------------------------------------------------------//
void Claro::linear_fit()
/*
 * The linear_fit function builds a linear fit on provided x,y data via maximum likelihood method, returning the maximum likelihood extimates of a,b parameters such that ax+b=y is the linear function that also satisfies Gauss' minimum squares regression method. Errors on a and b are provided as well as sigma2, variance of the estimation error. Sigma2 is distributed as a chi-squared random variable with deg=n-2 where n=number of  (x,y) tuples provided.
 * To evaluate the performance of the fit one should fix the first order estimation error and use sigma2 (comparing with tabulated values for n-2 degrees of freedom) or r2 (comparing with tabulated values for n degrees of freedom).
*/
{
    ///////////////////////////////////////////////////////////////////////
    // NEEDS TO DEFINE THRESHOLD for xyData, both default value and user-controlled inside linear_fit
    // select x,y data that satisfy provided threshold
    // perform cmputations in the following order:
    // a
    // b
    // sigma_2
    // Var(a), Var(b), Var(x), Var(y)
    // r2
    ///////////////////////////////////////////////////////////////////////

    float y_low {1}, y_high {1000}; // y thresholds
    std::vector<float> chosen_y {}, chosen_x {};

    for (int i {0}; i<y.size(); i++)
    {
        if (y.at(i)>y_low && y.at(i)<y_high)
        {
            chosen_x.push_back(x.at(i));
            chosen_y.push_back(y.at(i));
        }
    }

    float a = aCoeff(chosen_x, chosen_y);
    float b = bCoeff(chosen_x, chosen_y);

    ///////////////////////// GO ON FROM HERE /////////////////////////////////
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

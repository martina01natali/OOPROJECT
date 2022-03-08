// #include <cstdlib>
#include <iostream>
#include <cstring>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <stdio.h>
#include "Claro.h"

using namespace std;

//----------------------------------------------------------------------------//
int main()  // This may seem stupid, but it is COMPULSORY to call the main
            // function main(). Not doing it leads to the error "undefined reference to `WinMain'".
{
    // User control section
    std::cout   << "Enter path to file to process\n";
    std::string FILEPATH {};
    std::cin    >> FILEPATH;
    std::cout   << "You entered: " << "\"" + FILEPATH + "\"\n";

    // Reading file and preparing std::vector of lines of file
    Claro targetfile {FILEPATH};
    DataStruct data = targetfile.xyData();
    auto fit_results = targetfile.linear_fit(0,950);

    // Support functions
    // float meanx = mean(data.x);
    // float varx = var(data.x);
    // float covarxy = covar(data.x,data.y);
    // float a {aCoeff(data.x,data.y)};
    // float b {bCoeff(data.x,data.y)};
    // float rquadro {rsq(data.x,data.y)};
    // float sigma {sigmasq(data.x,data.y)};

    // std::cout << a << std::endl;
    // std::cout << b << std::endl;
    // std::cout << sigma << std::endl;
    // std::cout << rquadro << std::endl;
    // std::cout << covarxy << std::endl;

    return 0;
}

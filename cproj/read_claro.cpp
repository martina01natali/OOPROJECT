// #include <cstdlib>
#include <iostream>
#include <cstring>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <stdio.h>
#include "Claro.h"
#include "support_func.h"

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
    auto meanx = mean(data.x);
    auto varx = var(data.x);
    auto covarxy = covar(data.x,data.y);
    auto a {aCoeff(data.x,data.y)};
    auto b {bCoeff(data.x,data.y)};
    auto rquadro {rsq(data.x,data.y)};
    auto sigma {sigmasq(data.x,data.y)};

    std::cout << a << std::endl;
    std::cout << b << std::endl;
    std::cout << sigma << std::endl;
    std::cout << rquadro << std::endl;
    std::cout << covarxy << std::endl;
    /*
    float mean(x,y)
    float se(x,y)
    float var(x,y)
    float covar(x,y)
    float aCoeff(x,y)
    float bCoeff(x,y)
    float r2(x,y)
    float sigma2(x,y)
    */
    /* checkpoint since I cannot use a debugger eheheheheh
    for (auto datum : targetfile.x)
    {
        std::cout << datum << std::endl;
    }
    // */
    return 0;
}

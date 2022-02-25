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
    targetfile.xyData();

    /* checkpoint since I cannot use a debugger eheheheheh */
    for (auto datum : targetfile.data)
    {
        std::cout << datum << std::endl;
    }
    // */
    return 0;
}

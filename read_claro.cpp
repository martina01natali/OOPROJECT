#include <iostream>
#include <fstream>
// #include <cstdlib>
#include <string>

void readFile(const std::string& FILE)
{
    std::ifstream inf (FILE.c_str());

    if (!inf)
    {
        std::cerr << "Error: Unable to open file" << std::endl;
        exit(1);
    }

    while (inf)
    {
        std::string line;
        std::getline(inf, line);
        std::cout << line << std::endl;
    }
}

int main()
// This may seem stupid but it is COMPULSORY to call the main function main(). Not doing it leads to the error "undefined reference to `WinMain'".
{
    std::cout << "Enter path to file to process\n";
    std::string FILEPATH {}; //"../secondolotto_1/Station_1__11/2017_10_31_09_46_11_Tray_Station_1__11/Chip_001/S_curve"};                       //?
    std::cin >> FILEPATH;
    std::cout << "You entered: " << "\"" + FILEPATH + "\"\n";
    readFile(FILEPATH);
    return 0;
}

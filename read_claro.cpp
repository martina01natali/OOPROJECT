#include <iostream>
#include <string>

int main()
// This may seem stupid but it is COMPULSORY to call the main function main(). Not doing it leads to the error "undefined reference to `WinMain'".
{
    std::cout << "Enter path to file to process\n";
    std::string FILEPATH {}; //"../secondolotto_1/Station_1__11/2017_10_31_09_46_11_Tray_Station_1__11/Chip_001/S_curve"};                       //?
    std::cin >> FILEPATH;
    std::cout << "You entered: " << "\"" + FILEPATH + "\"\n";
    return 0;
}

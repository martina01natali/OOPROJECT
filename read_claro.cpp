#include <iostream>
#include <fstream>
// #include <cstdlib>
#include <string>

void readFile(const std::string& FILE)  // FILE is a std string passed to the
{                                       // function by const reference
    std::ifstream out {FILE.c_str()}; //.c_str converts to a c-string (??)

    if (!out)
    {
        std::cerr << "Error: Unable to open file" << std::endl;
        exit(1);
    }

    std::string line;
    while (std::getline(out, line))
    {
        // std::string line;
        // std::getline(out, line);
        std::cout << line << std::endl;
    }
}

int main()  // This may seem stupid but it is COMPULSORY to call the main
            // function main(). Not doing it leads to the error "undefined reference to `WinMain'".
{
    std::cout << "Enter path to file to process\n";
    std::string FILEPATH {}; //" what is the difference, if any, between
    // using () and {}?
    std::cin >> FILEPATH;
    std::cout << "You entered: " << "\"" + FILEPATH + "\"\n";
    readFile(FILEPATH);
    return 0;
}

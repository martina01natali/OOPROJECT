#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
// #include <cstdlib>

auto readFile(const std::string& FILE)
{
    /*
     This function does this:
     - open the file passed as an argument and checks if file is good or bad
     - reads line by line as std::string
     - puts a whole line as an element of a vector<string>
     */

    std::ifstream input {FILE.c_str()}; //.c_str converts to a c-string

    if (!input)
    {
        std::cerr << "Error: Unable to open file" << std::endl;
        exit(1);
    }

    std::string line;
    std::vector<std::string> data;

    while (std::getline(input, line))
    {
        if(line.size() != 0)
            data.push_back(line);
    }
    return data;
}
//*****************************************************************************

int main()  // This may seem stupid, but it is COMPULSORY to call the main
            // function main(). Not doing it leads to the error "undefined reference to `WinMain'".
{
    // User control section
    std::cout << "Enter path to file to process\n";
    std::string FILEPATH {};
    std::cin >> FILEPATH;
    std::cout << "You entered: " << "\"" + FILEPATH + "\"\n";

    auto const data {readFile(FILEPATH)};
    for (auto line : data)
        std::stringstream datum(line);
	
        while (!datum)
			std::cout << datum << '\n';

    return 0;
}

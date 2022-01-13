#include <iostream>
#include <cstring>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <stdio.h>
// #include <cstdlib>

///////////////////////////////////////////////////////////////////////////////
/*
 * The tokenize function takes any string and tokenizes it by any std::string
 * delimiter provided. WARNING: doesn't work with char standard delimiters
 * such as '\t', '\n', etc...
 * *EDIT* to use char delimiters just use damn ""
 * *UPDATE* needs to be corrected to remove the cout output and store tokens
 * from string in a proper container.
 */
void tokenize(std::string const& s, std::string const& del)
{
    int start = 0;
    int end = s.find(del);
    while (end != -1)
    {
        // output here is on screen
        std::cout << s.substr(start, end-start) << del;
        start = end + del.size();
        end = s.find(del, start);
    }
    std::cout << s.substr(start, end-start) << std::endl;
}
///////////////////////////////////////////////////////////////////////////////
/*
 * This function does this:
 * - open the file passed as an argument and checks if file is good or bad
 * - reads line by line as std::string
 * - puts a whole line as an element of a vector<string>
 */
auto readFile(const std::string& FILE)
{
    std::ifstream input {FILE.c_str()}; //.c_str converts to a c-string

    if (!input)
    {
        std::cerr << "Error: Unable to open file" << std::endl;
        exit(1);
    }

    std::string line;
    std::vector<std::string> data;

    /*
     * while with getline cannot be done by choosing tab as delimiter because
     * in this way the return '\n' cannot be parsed and data are gotten
     * in the wrong way.
     * The following statement builds a std::vector of strings, each string
     * contains a single line of the txt file.
    */
     while (std::getline(input, line))
    {
        if(line.size() != 0)
        {
            data.push_back(line);
        }
    }
    return data;
}
///////////////////////////////////////////////////////////////////////////////

int main()  // This may seem stupid, but it is COMPULSORY to call the main
            // function main(). Not doing it leads to the error "undefined reference to `WinMain'".
{
    // User control section
    std::cout << "Enter path to file to process\n";
    std::string FILEPATH {};
    std::cin >> FILEPATH;
    std::cout << "You entered: " << "\"" + FILEPATH + "\"\n";

    auto const data {readFile(FILEPATH)};
    for (auto const element : data) // each element is a line of the file
        std::cout << element << '\n';

    // now need to parse each line and split it by tabs

    std::vector<float> meta;
    for(int i {0}; i<10; i++) {
        std::cout << "Data is: " << data.at(i) << '\n';
        meta.push_back(std::stof(data.at(i)));
        //std::cout << "Meta is:\n" << meta.at(i) << '\n';
    }

    return 0;
}

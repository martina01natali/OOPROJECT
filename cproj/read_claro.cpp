#include <iostream>
#include <cstring>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <stdio.h>
// #include <cstdlib>

using namespace std;

///////////////////////////////////////////////////////////////////////////////
/*
 * The ssplit function takes any string and tokenizes it by any std::string
 * delimiter provided. WARNING: doesn't work with char standard delimiters
 * such as '\t', '\n', etc... : to use char delimiters just use "".
 * The function returns a vector of strings containing each token that comes
 * from the splitting of the string.
 */
auto ssplit(std::string const& s, std::string const& del)
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
        if(line.size())
        {
            data.push_back(line);
            cout << line <<'\n';
        }
    }
    return data;
}
///////////////////////////////////////////////////////////////////////////////

int main()  // This may seem stupid, but it is COMPULSORY to call the main
            // function main(). Not doing it leads to the error "undefined reference to `WinMain'".
{
    // User control section
    std::cout   << "Enter path to file to process\n";
    std::string FILEPATH {};
    std::cin    >> FILEPATH;
    std::cout   << "You entered: " << "\"" + FILEPATH + "\"\n";

    // now need to get each line
    auto const  lines {readFile(FILEPATH)};

    int                 i {}; // counter for lines
    std::vector<float>  meta; // containers for data
    std::vector<float>  x;
    std::vector<float>  y;
    std::vector<float>  y1;

    // take each line of the txt file as element
    for (auto const line : lines)
    {
        // split each element in its tokens
        auto    tokens = ssplit(line, "\t");
        int     j {}; // counter for tokens=columns

        for (auto token : tokens)
        {
            auto datum = std::stof(token);
            // if tokens belong to first two lines, put in vector of metadata
            // else put in x, y1, y2 vectors depending on column they belong to
            if (i<2)
                meta.push_back(datum);
            else
            {
                if (j==0)       // column 0
                    x.push_back(datum);
                else if (j==1)  // column 1
                    y.push_back(datum);
                else if (j==2)  // column 2
                    y1.push_back(datum);
            }
            j++;
        }
        i++;
    }
    return 0;
}

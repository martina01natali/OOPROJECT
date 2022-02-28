#ifndef CLARO_H
#define CLARO_H

struct DataStruct { std::vector<float>  meta, x, y, y1; };

class Claro
{
private:
    std::string FILEPATH {};
    std::vector<std::string> lines {};
    std::vector<float>  meta, x, y, y1;
    // void setup() {}

public:
// Constructors
    Claro() = default;
    Claro(std::string filepath) : FILEPATH{filepath}
    {
        this->readFile();
        this->xyData();
    }

// Setters and getters
    // void reset() {}
    void setFilePath(std::string filepath) { FILEPATH = filepath; }
    const std::string& getFilePath() { return FILEPATH; }

// Other methods
    void readFile();
    DataStruct xyData();
    std::vector<std::string> ssplit(std::string const& s, std::string const& del);

};
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
{
    // take each line of the txt file as element
    int i {}; // counter for lines
    for (auto const line : this->lines)
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

#endif

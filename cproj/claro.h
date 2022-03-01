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
    void reset() { *this = Claro(); }
    void setFilePath(std::string filepath) { FILEPATH = filepath; }
    const std::string& getFilePath() { return FILEPATH; }

// Other methods
    void readFile();
    DataStruct xyData();
    std::vector<std::string> ssplit(std::string const& s, std::string const& del);
};

// Support functions
float mean(const std::vector<float>& x);
float se(const std::vector<float>& x);
float var(const std::vector<float>& x);
float covar(const std::vector<float>& x, const std::vector<float>& y);
float aCoeff(const std::vector<float>& x, const std::vector<float>& y);
float bCoeff(const std::vector<float>& x, const std::vector<float>& y);
float rsq(const std::vector<float>& x, const std::vector<float>& y);
float sigmasq(const std::vector<float>& x, const std::vector<float>& y);
float aErr(const std::vector<float>& x, const std::vector<float>& y);
float bErr(const std::vector<float>& x, const std::vector<float>& y);

#endif

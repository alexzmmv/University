#pragma once

#include <string>

class building {
protected:
    int constructionYear;
public:
    virtual bool mustberepaired()=0;
    virtual bool canbedemolished()=0;
    virtual std::string toString()=0;
    int getConstructionYear();
};


class house : public building {
private:
    bool isHistorical;
public:
    house(int constructionYear,bool isHistorical);
    bool mustberepaired();
    bool canbedemolished();
    std::string toString();
};

class block : public building {
private:
    int tottalApartaments;
    int ocupiedApartaments;
public:
    block(int constructionYear, int tottalApartaments, int ocupiedApartaments);
    bool mustberepaired();
    bool canbedemolished();
    std::string toString();
};
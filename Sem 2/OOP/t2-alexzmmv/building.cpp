#include "building.h"

using namespace std;

int building::getConstructionYear() {
    return this->constructionYear;
}

house::house(int constructionYear,bool ishist){
    this->constructionYear=constructionYear;
    this->isHistorical=ishist;
}

bool house::mustberepaired(){
    return 2024-constructionYear>100;
}

bool house::canbedemolished(){
    return !isHistorical;
}

string house::toString(){
    string str="";
    if(isHistorical){
        str+="Historical house from "+to_string(constructionYear);
    }
    else
        str+="Non histrical house from "+to_string(constructionYear)+" can be demolished";
    if(mustberepaired()){
        str+=" must be repaired";
    }
    else{
        str+=" does NOT need to be repaired";
    }
    return str;
}

block::block(int constructionYear, int tottalApartaments, int ocupiedApartaments){
    this->constructionYear=constructionYear;
    this->tottalApartaments=tottalApartaments;
    this->ocupiedApartaments=ocupiedApartaments;
}

bool block::mustberepaired(){
    return 2024-constructionYear>40 && 1.0*ocupiedApartaments/tottalApartaments>0.8;
}

bool block::canbedemolished(){
    return 1.0*ocupiedApartaments/tottalApartaments<0.05;
}

string block::toString(){
    auto str="Block from "+to_string(constructionYear)+" with "+to_string(tottalApartaments)+" apartaments, "+to_string(ocupiedApartaments)+" ocupied";
    if(canbedemolished()){
        str+=" can be demolished";
    }
    else{
        str+=" can NOT be demolished";
    }
    if(mustberepaired()){
        str+=" must be repaired";
    }
    else{
        str+=" does NOT need to be repaired";
    }
    return str;
}
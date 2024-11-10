#include <valarray>
#include "Eq.h"

Eq::Eq(double a, double b, double c) {
    this->a = a;
    this->b = b;
    this->c = c;
}

string Eq::to_string() {
    std::string ret;
    ret=std::to_string(this->a)+"x^2";
    if(this->b>0)
        ret=ret+"+"+std::to_string(this->b)+"x";
    if(this->b<0)
        ret=ret+std::to_string(this->b)+"x";

    if(this->c>0)
        ret=ret+"+"+std::to_string(this->c);
    if(this->c<0)
        ret=ret+std::to_string(this->c);
    return ret;
}

bool Eq::is_real() {
    return this->b*this->b-4*this->a*this->c>=0;
}

pair<pair<double, double>, pair<double, double>> Eq::sol() {
    if (this->is_real()) {
        double x1, x2;
        x1 = (-this->b + sqrt(this->b * this->b - 4 * this->a * this->c)) / (2 * this->a);
        x2 = (-this->b - sqrt(this->b * this->b - 4 * this->a * this->c)) / (2 * this->a);
        auto a=std::make_pair(x1,0.0);
        auto b=std::make_pair(x2,0.0);
        return std::make_pair(a,b);
    }
    else {
        double x1, x2;
        x1 = -this->b / (2 * this->a);
        x2 = sqrt(-this->b * this->b + 4 * this->a * this->c) / (2 * this->a);
        auto a=std::make_pair(x1,x2);
        auto b=std::make_pair(x1,-x2);
        return std::make_pair(a,b);
    }
}


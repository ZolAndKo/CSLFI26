#include <iostream>
#include <iomanip>
    #include <fstream>
    #include "nlohamn/json.hpp"
    using json = nlohmann::json;
    


    int main(int argc, char* argv[]){
    std::ifstream file(argv[1]);
json config = json::parse(file);

double x_0 = config.at("x0").get<double>();
double v_0 = config.at("v0").get<double>();
double w = config.at("omega").get<double>();
double k = config.at("decr").get<double>();
double dt = config.at("dt").get<double>();
int steps = config.at("steps").get<int>();
std::string output = config.at("outputs").at("runge").get<std::string>();
   
    float x_i=x_0;
    float v_i=v_0;
    float x_eul=0;
    float v_eul=0;

    float dx;
    float dv;
    float dx_eul;
    float dv_eul;
    float E;
    float k1x;
    float k2x;
    float k3x;
    float k4x;
    float k1v;
    float k2v;
    float k3v;
    float k4v;

    for (int i=0; i<steps; i++){
        k1x=dt*(v_i);
        k1v=dt*(-w*w*x_i+k*v_i);
        k2x=dt*(v_i+k1v/2);
        k2v=dt*(-w*w*(x_i+k1x/2)-k*(v_i+k1v/2));
        k3x=dt*(v_i+k2v/2);
        k3v=dt*(-w*w*(x_i+k2x/2)-k*(v_i+k2v/2));
        k4x=dt*(v_i+k3v);
        k4v=dt*(-w*w*(x_i+k3x)-k*(v_i+k3v));

        x_i=x_i+(k1x+2*k2x+2*k3x+k4x)/6;

        v_i=v_i+(k1v+2*k2v+2*k3v+k4v)/6;
        E=x_i*x_i*w*w/2+v_i*v_i/2;
        
        std::cout<<std::setprecision(9)<<x_i<<' '<<v_i<<' '<<E<<std::endl;

    }
    return 0;
}
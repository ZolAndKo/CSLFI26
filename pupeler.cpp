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
double dt = config.at("dt").get<double>();
int steps = config.at("steps").get<int>();
std::string output = config.at("outputs").at("pupeler").get<std::string>();
        

        float x_i=x_0;
        float v_i=v_0;

        float dx;
        float dv;
        float E;

        for (int i=0; i<steps; i++){
            dx=dt*v_i;
            dv=-dt*w*w*x_i;

            x_i=x_i+dx;
            v_i=v_i+dv;
            E=x_i*x_i*w*w/2+v_i*v_i/2;
            std::cout<<std::setprecision(9)<<x_i<<' '<<v_i<<' '<<E<<std::endl;

        }
        return 0;
    }
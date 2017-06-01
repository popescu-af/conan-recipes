#include <iostream>
#include <svgdom/dom.hpp>

int main()
{
    using namespace svgdom;

    Rectangle r;
    r.attribsToStream(std::cout);

    return 0;
}

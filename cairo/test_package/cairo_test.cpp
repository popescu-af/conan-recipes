#include <iostream>
#include <cairo/cairo.h>

int main()
{
    std::cout << "Successfully loaded Cairo library, version " << cairo_version_string() << std::endl;
    return 0;
}

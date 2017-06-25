#include <iostream>
#include <pixman/pixman.h>

int main()
{
    pixman_region16 region;
    pixman_region_init(&region);
    std::cout << "Test OK" << std::endl;
    return 0;
}

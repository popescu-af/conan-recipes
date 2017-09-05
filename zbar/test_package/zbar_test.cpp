#include <cstddef>
#include <iostream>

#include <zbar/zbar.h>

int main()
{
    // Create & configure a reader
    zbar::ImageScanner scanner;
    scanner.set_config(zbar::ZBAR_NONE, zbar::ZBAR_CFG_ENABLE, 1);

    return 0;
}

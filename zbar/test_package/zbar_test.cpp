#include <cstddef>
#include <iostream>

#include <opencv2/imgcodecs.hpp>
#include <zbar/zbar.h>

#define _STRINGIFY(s) #s
#define STRINGIFY(s) _STRINGIFY(s)

int main()
{
    const std::string qr_code_file(STRINGIFY(QR_CODE_FILE));

    std::cout << "Opening " << qr_code_file << std::endl;
    const auto img = cv::imread(qr_code_file.c_str(), cv::IMREAD_GRAYSCALE);

    // Create & configure a reader
    zbar::ImageScanner scanner;
    scanner.set_config(zbar::ZBAR_NONE, zbar::ZBAR_CFG_ENABLE, 1);

    // Wrap image data
    zbar::Image image(img.cols, img.rows, "Y800", img.data, img.cols * img.rows);

    // Scan the image for barcodes
    scanner.scan(image);

    // Extract results
    std::cout << "Decoded:\n";
    for(auto symbol = image.symbol_begin(); symbol != image.symbol_end(); ++symbol)
    {
        if (symbol->get_type_name() != "QR-Code")
        {
            continue;
        }
        std::cout << symbol->get_data() << "\n";
    }

    // Clean up
    image.set_data(NULL, 0);
    return 0;
}

#include <iostream>
#include <string>

#include <opencv2/imgcodecs.hpp>

#include <svgren/render.hpp>
#include <papki/FSFile.hpp>

#define _STRINGIFY(s) #s
#define STRINGIFY(s) _STRINGIFY(s)

int main()
{
    const std::string svg_file(STRINGIFY(SVG_FILE));
    std::cout << "Opening " << svg_file << std::endl;

    auto dom = svgdom::load(papki::FSFile(svg_file));
    unsigned int width = 256;
    unsigned int height = 256;
    const auto img = svgren::render(*dom, width, height);

    cv::Mat cv_image(static_cast<int>(height), static_cast<int>(width), CV_8UC4);
    memcpy(cv_image.data, reinterpret_cast<const uchar*>(&img[0]), img.size() * 4);

    const std::string jpg_file(svg_file + ".jpg");
    std::cout << "Writing " << jpg_file << std::endl;

    cv::imwrite(jpg_file, cv_image);
    return 0;
}


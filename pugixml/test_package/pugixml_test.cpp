#include <iostream>
#include <pugixml.hpp>

#define _STRINGIFY(s) #s
#define STRINGIFY(s) _STRINGIFY(s)

int main()
{
    using namespace pugi;

    const std::string xml_file(STRINGIFY(XML_FILE));
    std::cout << "Opening " << xml_file << std::endl;

    xml_document doc;
    xml_parse_result result = doc.load_file(xml_file.c_str());

    std::cout << "RESULT: "   << result.description()
              << ", Greeting: " << doc.child("greeting").attribute("name").value()
              << std::endl;
    return 0;
}


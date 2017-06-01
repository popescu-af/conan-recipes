#include <iostream>
#include <papki/FSFile.hpp>

int main()
{
    using namespace papki;
    const FSFile gcc_executable("/usr/bin/gcc");
    std::cout << "GCC installed: " << (gcc_executable.exists() ? "YES" : "NO") << std::endl;
    return 0;
}

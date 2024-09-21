#include "com/foo/config.hpp"
#include "com/foo/bar.hpp"

int main(int argc, char **argv) {
	int result = EXIT_SUCCESS;
	try {
		auto logger = com::foo::getLogger("MyApp");
		LOG4CXX_INFO(logger, "Entering application.");
		com::foo::Bar bar;
		bar.doIt();
		LOG4CXX_INFO(logger, "Exiting application.");
	}
	catch(std::exception&) {
		result = EXIT_FAILURE;
	}
	return result;
}

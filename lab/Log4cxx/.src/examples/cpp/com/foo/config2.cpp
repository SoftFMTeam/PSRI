#include "com/foo/config.hpp"
#include <log4cxx/basicconfigurator.hpp>
#include <log4cxx/propertyconfigurator.hpp>
#include <log4cxx/logmanager.hpp>

namespace com { namespace foo {

auto getLogger(const std::string& name) -> LoggerPtr {
	using namespace log4cxx;
	static struct log4cxx_initializer {
		log4cxx_initializer() {
			if (PropertyConfigurator::configure("MyApp.properties") == spi::ConfigurationStatus::NotConfigured)
				BasicConfigurator::configure(); // Send events to the console
		}
		~log4cxx_initializer() {
			LogManager::shutdown();
		}
	} initAndShutdown;
	return name.empty()
		? LogManager::getRootLogger()
		: LogManager::getLogger(name);
}

} } // namespace com::foo

#include "com/foo/bar.hpp"
#include "com/foo/config-qt.hpp"

using namespace com::foo;

LoggerPtr Bar::m_logger(getLogger("com.foo.bar"));

void Bar::doIt() {
	LOG4CXX_DEBUG(m_logger, QString("Did it again!") << QString(" - again!"));
}

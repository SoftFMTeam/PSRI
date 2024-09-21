/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <log4cxx/logstring.hpp>
#include <log4cxx/helpers/loader.hpp>
#include <log4cxx/appender.hpp>
#include <log4cxx/spi/filter.hpp>
#include <log4cxx/helpers/loglog.hpp>
#include <log4cxx/spi/loggerfactory.hpp>
#include <log4cxx/spi/loggerrepository.hpp>
#include <log4cxx/helpers/object.hpp>
#include <log4cxx/spi/errorhandler.hpp>
#include <log4cxx/filter/denyallfilter.hpp>
#include <log4cxx/spi/repositoryselector.hpp>
#include <log4cxx/spi/appenderattachable.hpp>
#include <log4cxx/helpers/xml.hpp>
#include <log4cxx/spi/triggeringeventevaluator.hpp>
#include <fstream>
#include <log4cxx/helpers/transcoder.hpp>
#include <log4cxx/helpers/fileinputstream.hpp>

using namespace LOG4CXX_NS;
using namespace LOG4CXX_NS::helpers;
using namespace LOG4CXX_NS::spi;
using namespace LOG4CXX_NS::filter;

IMPLEMENT_LOG4CXX_OBJECT(Object)
IMPLEMENT_LOG4CXX_OBJECT(OptionHandler)
IMPLEMENT_LOG4CXX_OBJECT(ErrorHandler)
IMPLEMENT_LOG4CXX_OBJECT(Appender)
IMPLEMENT_LOG4CXX_OBJECT(Filter)
IMPLEMENT_LOG4CXX_OBJECT(AppenderAttachable)
IMPLEMENT_LOG4CXX_OBJECT(LoggerFactory)
IMPLEMENT_LOG4CXX_OBJECT(LoggerRepository)
IMPLEMENT_LOG4CXX_OBJECT(DenyAllFilter)
IMPLEMENT_LOG4CXX_OBJECT(RepositorySelector)
IMPLEMENT_LOG4CXX_OBJECT(XMLDOMNode)
IMPLEMENT_LOG4CXX_OBJECT(XMLDOMDocument)
IMPLEMENT_LOG4CXX_OBJECT(XMLDOMElement)
IMPLEMENT_LOG4CXX_OBJECT(XMLDOMNodeList)
IMPLEMENT_LOG4CXX_OBJECT(TriggeringEventEvaluator)

const Class& Loader::loadClass(const LogString& clazz)
{
	return Class::forName(clazz);
}


InputStreamPtr Loader::getResourceAsStream(const LogString& name)
{

	try
	{
		return std::make_shared<FileInputStream>(name);
	}
	catch (const IOException&)
	{
	}

	return 0;
}

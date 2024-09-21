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
#include <log4cxx/pattern/filelocationpatternconverter.hpp>
#include <log4cxx/spi/loggingevent.hpp>
#include <log4cxx/spi/location/locationinfo.hpp>

using namespace LOG4CXX_NS;
using namespace LOG4CXX_NS::pattern;
using namespace LOG4CXX_NS::spi;
using namespace helpers;

IMPLEMENT_LOG4CXX_OBJECT(FileLocationPatternConverter)

FileLocationPatternConverter::FileLocationPatternConverter() :
	LoggingEventPatternConverter(LOG4CXX_STR("File Location"),
		LOG4CXX_STR("file"))
{
}

PatternConverterPtr FileLocationPatternConverter::newInstance(
	const std::vector<LogString>& /* options */ )
{
	static WideLife<PatternConverterPtr> instance = std::make_shared<FileLocationPatternConverter>();
	return instance;
}

void FileLocationPatternConverter::format(
	const LoggingEventPtr& event,
	LogString& toAppendTo,
	Pool& /* p */ ) const
{
	append(toAppendTo, event->getLocationInformation().getFileName());
}

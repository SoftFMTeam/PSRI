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
#include <log4cxx/spi/rootlogger.hpp>
#include <log4cxx/helpers/loglog.hpp>
#include <log4cxx/level.hpp>
#include <log4cxx/appender.hpp>

using namespace LOG4CXX_NS;
using namespace LOG4CXX_NS::spi;
using namespace LOG4CXX_NS::helpers;

RootLogger::RootLogger(Pool& pool, const LevelPtr level1) :
	Logger(pool, LOG4CXX_STR("root"))
{
	setLevel(level1);
}

const LevelPtr& RootLogger::getEffectiveLevel() const
{
	return getLevel();
}

void RootLogger::setLevel(const LevelPtr level1)
{
	if (level1 == 0)
	{
		LogLog::error(LOG4CXX_STR("You have tried to set a null level to root."));
	}
	else
	{
		Logger::setLevel(level1);
	}
}




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
#include <log4cxx/helpers/resourcebundle.hpp>
#include <log4cxx/helpers/propertyresourcebundle.hpp>
#include <log4cxx/helpers/loader.hpp>
#include <log4cxx/helpers/pool.hpp>
#include <log4cxx/helpers/transcoder.hpp>
#include <log4cxx/helpers/locale.hpp>

using namespace LOG4CXX_NS;
using namespace LOG4CXX_NS::helpers;

IMPLEMENT_LOG4CXX_OBJECT(ResourceBundle)

ResourceBundlePtr ResourceBundle::getBundle(const LogString& baseName,
	const Locale& locale)
{
	LogString bundleName;
	PropertyResourceBundlePtr resourceBundle, previous;

	std::vector<LogString> bundlesNames;

	if (!locale.getVariant().empty())
	{
		bundlesNames.push_back(baseName + LOG4CXX_STR("_") +
			locale.getLanguage() + LOG4CXX_STR("_") +
			locale.getCountry() + LOG4CXX_STR("_") +
			locale.getVariant());
	}

	if (!locale.getCountry().empty())
	{
		bundlesNames.push_back(baseName + LOG4CXX_STR("_") +
			locale.getLanguage() + LOG4CXX_STR("_") +
			locale.getCountry());
	}

	if (!locale.getLanguage().empty())
	{
		bundlesNames.push_back(baseName + LOG4CXX_STR("_") +
			locale.getLanguage());
	}

	bundlesNames.push_back(baseName);

	for (std::vector<LogString>::iterator it = bundlesNames.begin();
		it != bundlesNames.end(); it++)
	{

		bundleName = *it;

		PropertyResourceBundlePtr current;

		// Try loading a class which implements ResourceBundle
		try
		{
			const Class& classObj = Loader::loadClass(bundleName);
			ObjectPtr obj = ObjectPtr(classObj.newInstance());
			current = LOG4CXX_NS::cast<PropertyResourceBundle>(obj);
		}
		catch (ClassNotFoundException&)
		{
			current = 0;
		}

		// No class found, then try to create a PropertyResourceBundle from a file
		if (current == 0)
		{
			InputStreamPtr bundleStream =
				Loader::getResourceAsStream(
					bundleName + LOG4CXX_STR(".properties"));

			if (bundleStream == 0)
			{
				continue;
			}

			try
			{
				current = std::make_shared<PropertyResourceBundle>(bundleStream);
			}
			catch (Exception&)
			{
				throw;
			}
		}

		// Add the new resource bundle to the hierarchy
		if (resourceBundle == 0)
		{
			resourceBundle = current;
			previous = current;
		}
		else
		{
			previous->setParent(current);
			previous = current;
		}
	}

	// no resource bundle found at all, then throw exception
	if (resourceBundle == 0)
	{
		throw MissingResourceException(
			((LogString) LOG4CXX_STR("Missing resource bundle ")) + baseName);
	}

	return resourceBundle;
}


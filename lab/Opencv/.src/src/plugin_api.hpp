// This file is part of OpenCV project.
// It is subject to the license terms in the LICENSE file found in the top-level directory
// of this distribution and at http://opencv.org/license.html.

#ifndef DNN_PLUGIN_API_HPP
#define DNN_PLUGIN_API_HPP

#include <opencv2/core/cvdef.hpp>
#include <opencv2/core/llapi/llapi.hpp>

#include "backend.hpp"

#if !defined(BUILD_PLUGIN)

/// increased for backward-compatible changes, e.g. add new function
/// Caller API <= Plugin API -> plugin is fully compatible
/// Caller API > Plugin API -> plugin is not fully compatible, caller should use extra checks to use plugins with older API
#define API_VERSION 0 // preview

/// increased for incompatible changes, e.g. remove function argument
/// Caller ABI == Plugin ABI -> plugin is compatible
/// Caller ABI > Plugin ABI -> plugin is not compatible, caller should use shim code to use old ABI plugins (caller may know how lower ABI works, so it is possible)
/// Caller ABI < Plugin ABI -> plugin can't be used (plugin should provide interface with lower ABI to handle that)
#define ABI_VERSION 0 // preview

#else // !defined(BUILD_PLUGIN)

#if !defined(ABI_VERSION) || !defined(API_VERSION)
#error "Plugin must define ABI_VERSION and API_VERSION before including plugin_api.hpp"
#endif

#endif // !defined(BUILD_PLUGIN)

typedef cv::dnn_backend::NetworkBackend* CvPluginDNNNetworkBackend;

struct OpenCV_DNN_Plugin_API_v0_0_api_entries
{
    /** @brief Get backend API instance

    @param[out] handle pointer on inference backend API handle

    @note API-CALL 1, API-Version == 0
     */
    CvResult (CV_API_CALL *getInstance)(CV_OUT CvPluginDNNNetworkBackend* handle) CV_NOEXCEPT;
};  // OpenCV_DNN_Plugin_API_v0_0_api_entries

typedef struct OpenCV_DNN_Plugin_API_v0
{
    OpenCV_API_Header api_header;
    struct OpenCV_DNN_Plugin_API_v0_0_api_entries v0;
} OpenCV_DNN_Plugin_API_v0;

#if ABI_VERSION == 0 && API_VERSION == 0
typedef OpenCV_DNN_Plugin_API_v0 OpenCV_DNN_Plugin_API;
#else
#error "Not supported configuration: check ABI_VERSION/API_VERSION"
#endif

#ifdef BUILD_PLUGIN
extern "C" {

CV_PLUGIN_EXPORTS
const OpenCV_DNN_Plugin_API* CV_API_CALL opencv_dnn_plugin_init_v0
        (int requested_abi_version, int requested_api_version, void* reserved /*NULL*/) CV_NOEXCEPT;

}  // extern "C"
#else  // BUILD_PLUGIN
typedef const OpenCV_DNN_Plugin_API* (CV_API_CALL *FN_opencv_dnn_plugin_init_t)
        (int requested_abi_version, int requested_api_version, void* reserved /*NULL*/);
#endif  // BUILD_PLUGIN

#endif // DNN_PLUGIN_API_HPP

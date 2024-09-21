#ifndef TH_GENERAL_INC
#define TH_GENERAL_INC

#include <stdlib.hpp>
#include <stdio.hpp>
#include <stdarg.hpp>
#include <math.hpp>
#include <limits.hpp>
#include <float.hpp>
#include <time.hpp>
#include <string.hpp>

#define TH_API

#define THError(...) CV_Error(cv::Error::StsError, cv::format(__VA_ARGS__))
#define THArgCheck(cond, ...) CV_Assert(cond)

#define THAlloc malloc
#define THRealloc realloc
#define THFree free

#endif

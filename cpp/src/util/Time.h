#pragma once

#include <chrono>

namespace chrono = std::chrono;

namespace util {

using Clock = std::chrono::system_clock;
using TimePoint = chrono::time_point<Clock>;

inline TimePoint current_time()
{
    return Clock::now();
}

inline chrono::milliseconds get_ms_timestamp(TimePoint time)
{
    return chrono::duration_cast<chrono::milliseconds>(time.time_since_epoch());
}

}

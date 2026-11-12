#include "precompiled.h"

template <typename ToCheck, std::size_t ExpectedSize, std::size_t RealSize = sizeof(ToCheck)>
void check_size() {
	static_assert(ExpectedSize == RealSize, "Size is off!");
}

#ifdef _WIN32
#define CHECK_TYPE_SIZE(t,win_size,lin_size) check_size<t,win_size>()
#else
#define CHECK_TYPE_SIZE(t,win_size,lin_size) check_size<t,lin_size>()
#endif


void checkSizesStatic() {
	// Cry of Fear: lastcmd (usercmd_t) has is_donator, 4 bytes more; on Windows they fill the padding before the
	// double that follows it, on Linux (doubles 4-aligned) client_t grows by 4
	CHECK_TYPE_SIZE(client_t, 0x5018, 0x4EF8);
	CHECK_TYPE_SIZE(userfilter_t, 0x20, 0x18);
#ifndef REHLDS_FIXES
	CHECK_TYPE_SIZE(CSteam3Server, 0x90, 0xA8);
#endif
}

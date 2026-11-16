# The four browsers, built together — what the sandbox can and cannot do

Date: 2026-11-16 (fourteenth session) · Repos `drsamonline/The_Browser`, `sorex`, `nodus`, `volumen`

Asked to build all four browsers together. One builds; three cannot, and the reasons are now measured
rather than assumed. This is a measurement entry: no repository changed.

## What I looked at

`/usr/include` and `/usr/lib/x86_64-linux-gnu` on the sandbox, the configure script of `volumen`
(Lynx), `configure.ac` of `sorex` (Dillo), `Makefile.defaults` of `nodus` (NetSurf), and what the
sandbox provides as build tooling.

## What was wrong

**Three of the four browsers cannot be built in this sandbox, for four distinct reasons.**

| Repo | Blocker | Evidence |
| --- | --- | --- |
| `volumen` (Lynx) | ncurses headers absent | `configure`: `checking for ncurses header in include-path... no` → `configure: error: not found` |
| `sorex` (Dillo) | FLTK and X11 headers absent; `configure.ac` references FLTK 32 times | no `/usr/include/FL`, no `/usr/include/X11` |
| `nodus` (NetSurf) | libcurl, libpng, libjpeg, libwebp, expat headers absent | `Makefile.defaults` toggles `NETSURF_USE_*`; none of the headers exist |
| all three | **no `make`, no `autoconf`, no `automake`** | `ls /usr/bin/make /usr/bin/autoconf` → not found |

The runtime libraries are present (`libz.so.1`, `libjpeg.so.62`, `libwebp.so.7`, `libncurses.so.6`,
`libcurl.so.4`, `libexpat.so.1`, `libssl.so.3`) but **none of the development headers** are. A linker
would find the libraries; the compiler has nothing to compile against.

**Two attempted workarounds, both blocked one level deeper.**

1. *Build ncurses from source.* `mirror/ncurses` cloned, `./configure --without-shared --with-termlib
   --without-ada --without-manpages` ran to completion with the zig compiler — and then failed at
   `./configure: make: not found`.
2. *Build make from source.* `mirror/make` is a git mirror with no generated `configure`, and its
   `build.sh` needs `build.cfg`, which `configure` produces. `autoconf` is not installed, so there is
   no way to generate either.

`aetheris` builds because it is the only one of the four with a **CMake + Ninja** build: `cmake` and
`ninja` come from pip wheels, which is exactly why its build has been reproducible all day while the
other three have never been built at all.

## What I changed

Nothing in the four repositories. This entry records the measurement.

## Evidence

    /usr/include: no zlib.h, png.h, jpeglib.h, webp/, ncurses.h, FL/, X11/, curl/, expat.h
    /usr/include/node/openssl/ssl.h   <- the only dev header present, which is what Aetheris uses
    /usr/lib/x86_64-linux-gnu: libz.so.1, libjpeg.so.62, libwebp.so.7, libncurses.so.6,
                               libcurl.so.4, libexpat.so.1, libssl.so.3
    which make autoconf automake  -> none

    volumen:  ./configure --with-screen=ncurses  ->  configure: error: not found
    ncurses:  ./configure ... CC=zigcc            ->  Makefile written
              make                                ->  ./configure: make: not found

## What I deliberately did not do

- **Did not add a fifth build system to the family repos to dodge the missing tooling.** A CMake port
  of Dillo, NetSurf or Lynx is a rewrite of three build systems, not a build.
- **Did not vendor prebuilt binaries.** Unverifiable provenance, and it would hide the real dependency
  list that `PLAN.md` P0 is supposed to establish.
- **Did not claim any of the three builds.** None was built. `SOURCES.md` in each still says the build
  is unverified, which remains true.
- **Did not touch the other three browser repositories.**

## Next

1. Build the three family browsers on a machine with dev packages: `apt install libfltk1.3-dev
   libncurses-dev zlib1g-dev libpng-dev libjpeg-dev libwebp-dev libcurl4-openssl-dev libexpat1-dev
   autoconf automake make`, then run each `tools/build.sh` and record the versions in `SOURCES.md`.
2. Until that happens, P0 in each family `ROADMAP.md` stays open — a build that has never run is not a
   scaffold, it is a hypothesis.
3. The Aetheris line continues to be the only one with a measured green build.

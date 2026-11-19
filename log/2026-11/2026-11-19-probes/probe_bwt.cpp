// probe_bwt.cpp — is there residual redundancy in libbsc's output?
//
// Compresses a file in 4 MiB blocks with exactly the libbsc settings ziptastic uses
// (BWT sorter, adaptive QLFC, no LZP) and writes the concatenated streams. The caller
// then tries to compress THAT output again with a general-purpose coder: if a strong
// coder cannot shrink it, no second entropy stage of any design will, and the gap to
// bzip3 is in the transform, not in a missing pass.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>

#include <libbsc/libbsc.h>
#include <libbsc/platform/platform.h>

static size_t kBlock = 4u << 20;

int main(int argc, char** argv) {
  if (argc < 3) {
    std::fprintf(stderr, "usage: probe_bwt <in> <out> [block_mib]\n");
    return 2;
  }
  if (argc == 4) kBlock = (size_t)std::atoi(argv[3]) << 20;
  FILE* in = std::fopen(argv[1], "rb");
  if (!in) { std::perror("open in"); return 1; }
  FILE* out = std::fopen(argv[2], "wb");
  if (!out) { std::perror("open out"); return 1; }

  if (bsc_init(LIBBSC_FEATURE_FASTMODE) != LIBBSC_NO_ERROR) {
    std::fprintf(stderr, "bsc_init failed\n");
    return 1;
  }

  std::vector<unsigned char> src(kBlock);
  std::vector<unsigned char> dst(kBlock + LIBBSC_HEADER_SIZE);
  size_t total_in = 0, total_out = 0, blocks = 0, skipped = 0;

  for (;;) {
    size_t n = std::fread(src.data(), 1, kBlock, in);
    if (n == 0) break;
    total_in += n;
    int got = bsc_compress(src.data(), dst.data(), static_cast<int>(n), 0, 0,
                           LIBBSC_BLOCKSORTER_BWT, LIBBSC_CODER_QLFC_ADAPTIVE,
                           LIBBSC_FEATURE_FASTMODE);
    if (got <= 0 || static_cast<size_t>(got) >= n) {
      // libbsc declined: store raw, as ziptastic's selector would fall back to RAW
      std::fwrite(src.data(), 1, n, out);
      total_out += n;
      ++skipped;
    } else {
      std::fwrite(dst.data(), 1, static_cast<size_t>(got), out);
      total_out += static_cast<size_t>(got);
    }
    ++blocks;
  }

  std::fclose(in);
  std::fclose(out);
  std::fprintf(stderr, "blocks=%zu raw=%zu libbsc=%zu (%.2f%%) skipped=%zu\n",
               blocks, total_in, total_out, 100.0 * total_out / total_in, skipped);
  return 0;
}

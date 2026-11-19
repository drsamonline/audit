// probe_bwt2.cpp — BWT transform alone, so a general-purpose coder can be measured on it.
//
// Emits, per 4 MiB block: the BWT-permuted bytes followed by the primary index. Nothing
// else. Compressing that with zstd/lzma/brotli answers the question libbsc's QLFC cannot:
// how much would a stronger coder recover on the same transform?
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>

#include <libbsc/libbsc.h>
#include <libbsc/platform/platform.h>
#include <libbsc/bwt/bwt.h>

static const size_t kBlock = 4u << 20;

int main(int argc, char** argv) {
  if (argc != 3) {
    std::fprintf(stderr, "usage: probe_bwt2 <in> <out>\n");
    return 2;
  }
  FILE* in = std::fopen(argv[1], "rb");
  if (!in) { std::perror("open in"); return 1; }
  FILE* out = std::fopen(argv[2], "wb");
  if (!out) { std::perror("open out"); return 1; }

  if (bsc_init(LIBBSC_FEATURE_FASTMODE) != LIBBSC_NO_ERROR) {
    std::fprintf(stderr, "bsc_init failed\n");
    return 1;
  }

  std::vector<unsigned char> buf(kBlock + 8);
  size_t total_in = 0, total_out = 0;

  for (;;) {
    size_t n = std::fread(buf.data(), 1, kBlock, in);
    if (n == 0) break;
    total_in += n;
    unsigned char num_indexes = 0;
    int indexes[256];
    const int idx = bsc_bwt_encode(buf.data(), static_cast<int>(n), &num_indexes, indexes,
                                   LIBBSC_FEATURE_FASTMODE);
    if (idx < 0) {
      std::fprintf(stderr, "bwt failed\n");
      return 1;
    }
    // Record the index bytes so the block boundaries and the primary index survive.
    uint32_t nn = static_cast<uint32_t>(n);
    std::fwrite(&nn, 4, 1, out);
    std::fwrite(&num_indexes, 1, 1, out);
    std::fwrite(indexes, sizeof(int), num_indexes, out);
    std::fwrite(buf.data(), 1, n, out);
    total_out += 4 + 1 + sizeof(int) * num_indexes + n;
  }

  std::fclose(in);
  std::fclose(out);
  std::fprintf(stderr, "raw=%zu bwt_stream=%zu\n", total_in, total_out);
  return 0;
}

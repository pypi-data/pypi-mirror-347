# pread64(6, "SQLite format 3\0\20\0\1\1\0@  \0\0`\5\0\0\0\36"..., 100, 0) = 100
# getpid()                                = 136227
# futex(0x7f1650001ca0, FUTEX_WAKE_PRIVATE, 1) = 1
# futex(0x55b4dfea8ccc, FUTEX_WAKE_PRIVATE, 1) = 1
# futex(0x55b4dfea8cd0, FUTEX_WAKE_PRIVATE, 1) = 1
# fcntl(6, F_SETLK, {l_type=F_RDLCK, l_whence=SEEK_SET, l_start=1073741824, l_len=1}) = 0
# fcntl(6, F_SETLK, {l_type=F_RDLCK, l_whence=SEEK_SET, l_start=1073741826, l_len=510}) = 0
# fcntl(6, F_SETLK, {l_type=F_UNLCK, l_whence=SEEK_SET, l_start=1073741824, l_len=1}) = 0
# newfstatat(AT_FDCWD, "/tmp/zxcvb/persistence/persistence.sqlite-journal", 0x7fff6790dc70, 0) = -1 ENOENT (No such file or directory)
# newfstatat(AT_FDCWD, "/tmp/zxcvb/persistence/persistence.sqlite-wal", 0x7fff6790dc70, 0) = -1 ENOENT (No such file or directory)
# newfstatat(6, "", {st_mode=S_IFREG|0644, st_size=122880, ...}, AT_EMPTY_PATH) = 0
# brk(0x55b4e1a42000)                     = 0x55b4e1a42000
# pread64(6, "SQLite format 3\0\20\0\1\1\0@  \0\0`\5\0\0\0\36"..., 4096, 0) = 4096
# fcntl(6, F_SETLK, {l_type=F_UNLCK, l_whence=SEEK_SET, l_start=0, l_len=0}) = 0
# fcntl(6, F_SETLK, {l_type=F_RDLCK, l_whence=SEEK_SET, l_start=1073741824, l_len=1}) = 0
# fcntl(6, F_SETLK, {l_type=F_RDLCK, l_whence=SEEK_SET, l_start=1073741826, l_len=510}) = 0
# fcntl(6, F_SETLK, {l_type=F_UNLCK, l_whence=SEEK_SET, l_start=1073741824, l_len=1}) = 0
# newfstatat(AT_FDCWD, "/tmp/zxcvb/persistence/persistence.sqlite-journal", 0x7fff6790e630, 0) = -1 ENOENT (No such file or directory)
# pread64(6, "\0\0`\5\0\0\0\36\0\0\0\31\0\0\0\5", 16, 24) = 16
# newfstatat(AT_FDCWD, "/tmp/zxcvb/persistence/persistence.sqlite-wal", 0x7fff6790e630, 0) = -1 ENOENT (No such file or directory)
# newfstatat(6, "", {st_mode=S_IFREG|0644, st_size=122880, ...}, AT_EMPTY_PATH) = 0
# pread64(6, "\5\17\236\0\17\17{\4\0\0\0\36\17\343\17\351\17\335\17\305\17\271\17\321\17\230\17\220\17\211\17\253"..., 4096, 12288) = 4096
# pread64(6, "\r\2\351\0o\1\377\7\17U\17E\0174\16\261\t\264\17\327\17\305\17\265\17\243\17\221\17\177\17m"..., 4096, 20480) = 4096
# pread64(6, "\r\4\374\0\33\3\272\1\7\354\7\331\7\302\7\257\7\244\7\212\7w\7k\7P\7=\0071\6\242"..., 4096, 24576) = 4096
# pread64(6, "\r\5\4\0\27\2\367\0\17\262\17p\r\264\n\221\nw\t\336\t\274\t\241\ty\10\353\10\321\10\276"..., 4096, 28672) = 4096
# pread64(6, "", 4096, 40960)             = 0


from pathlib import Path

reads = [
    (100, 0),
    (4096, 0),
    (16, 24),
    (4096, 12288),
    (4096, 20480),
    (4096, 24576),
    (4096, 28672),
    (4096, 40960),
]

path = Path("/tmp/zxcvb/persistence/persistence.sqlite")
with open(path, "rb") as f:
    for size, offset in reads:
        print(size, offset)
        f.seek(offset, 0)
        data = f.read(size)
        if len(data) != size:
            print("WTF")
            raise ValueError("WTF")

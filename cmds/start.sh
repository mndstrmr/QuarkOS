qemu-system-i386 -kernel src/sysroot/boot/quarkos.kernel -serial stdio -drive file=src/sysroot.img,format=raw -no-reboot -rtc base=utc,clock=host -vga std "$@"

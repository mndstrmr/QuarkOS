qemu-system-i386 -kernel sysroot/boot/quarkos.kernel -serial stdio -drive file=sysroot.img,format=raw -no-reboot -rtc base=utc,clock=host "$@"
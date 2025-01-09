/*cargo build --target x86_64-rusk.json
  cargo bootimage
  qemu-system-x86_64 -drive format=raw,file=target/bootimage-rusk_os.bin
*/
#![no_std] //disable link to standard library
#![no_main]
#![feature(custom_test_frameworks)]
#![test_runner(rusk_os::test_runner)]
#![reexport_test_harness_main = "test_main"]

//importing items (functions, variables, etc)
use rusk_os::println;
use rusk_os::print;
use core::panic::PanicInfo;
pub mod frames; // declares a module named frames in the current Rust code file.
use frames::ASCII_AMFOSS_TOP;
use frames::ASCII_AMFOSS_BOTTOM;

#[no_mangle] // The main function starts here
pub extern "C" fn _start() -> ! {
print!("{}",ASCII_AMFOSS_TOP);
print!("{}",ASCII_AMFOSS_BOTTOM);


  rusk_os::init(); //initialises essential kernel functions

  #[cfg(test)]
  test_main(); //test function

  rusk_os::hlt_loop(); //main loop
}

/// This function is called on panic (In case of errors).
#[cfg(not(test))]
#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    println!("{}", info);
    rusk_os::hlt_loop();
}

#[cfg(test)]
#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    println!("{}", info);
    rusk_os::hlt_loop();
}

#[cfg(test)]
#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    rusk_os::test_panic_handler(info)
}

#[test_case]
fn trivial_assertion() {
    assert_eq!(1, 1);
}
/*
It is also possible to write it to a USB stick and boot it on a real machine, 
but be careful to choose the correct device name, 
because everything on that device is overwritten:
---
> dd if=target/x86_64-rusk/debug/bootimage-rusk_os.bin of=/dev/sdX && sync
---
Where sdX is the device name of your USB stick. 
 */



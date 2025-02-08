// Import necessary crates and modules
use crate::{gdt, print, println};
use lazy_static::lazy_static;
use pic8259::ChainedPics;
use spin;
use x86_64::structures::idt::{InterruptDescriptorTable, InterruptStackFrame};          

// Define constants for PIC offsets
pub const PIC_1_OFFSET: u8 = 32;
pub const PIC_2_OFFSET: u8 = PIC_1_OFFSET + 8;

// Define a global counter for character tracking
static mut COUNT: usize = 0;

// Define the size of the character array
const ARRAY_SIZE: usize = 7;

// Create an array to store characters
static mut CHARS: [Option<char>; ARRAY_SIZE] = [None; ARRAY_SIZE];

#[derive(Debug, Clone, Copy)]
#[repr(u8)]
pub enum InterruptIndex {
    Timer = PIC_1_OFFSET,
    Keyboard,
}

impl InterruptIndex {
    fn as_u8(self) -> u8 {
        self as u8
    }

    fn as_usize(self) -> usize {
        usize::from(self.as_u8())
    }
}

// Create a static mutex for the Programmable Interrupt Controllers (PICs)
pub static PICS: spin::Mutex<ChainedPics> =
    spin::Mutex::new(unsafe { ChainedPics::new(PIC_1_OFFSET, PIC_2_OFFSET) });

// Create a lazy static Interrupt Descriptor Table (IDT)
lazy_static! {
    static ref IDT: InterruptDescriptorTable = {
        let mut idt = InterruptDescriptorTable::new();

        // Set handler function for breakpoint exception
        idt.breakpoint.set_handler_fn(breakpoint_handler);
        
        unsafe {
            idt.double_fault
                .set_handler_fn(double_fault_handler)
                .set_stack_index(gdt::DOUBLE_FAULT_IST_INDEX);
        }

        // Set handler functions for timer and keyboard interrupts
        idt[InterruptIndex::Timer.as_usize()].set_handler_fn(timer_interrupt_handler);
        idt[InterruptIndex::Keyboard.as_usize()].set_handler_fn(keyboard_interrupt_handler);
        idt
    };
}

// Function to initialize the Interrupt Descriptor Table
pub fn init_idt() {
    IDT.load();
}

// Handler for the breakpoint exception
extern "x86-interrupt" fn breakpoint_handler(stack_frame: InterruptStackFrame) {
    println!("EXCEPTION: BREAKPOINT\n{:#?}", stack_frame);
}

// Handler for the double fault exception
extern "x86-interrupt" fn double_fault_handler(
    stack_frame: InterruptStackFrame,
    _error_code: u64,
) -> ! {
    panic!("EXCEPTION: DOUBLE FAULT\n{:#?}", stack_frame);
}

// Handler for the timer interrupt
extern "x86-interrupt" fn timer_interrupt_handler(_stack_frame: InterruptStackFrame) {
    unsafe {
        PICS.lock()
            .notify_end_of_interrupt(InterruptIndex::Timer.as_u8());
    }
}

// Function to check if a sequence of characters matches success condition
fn success(chars: &[Option<char>; ARRAY_SIZE]) -> bool {
    chars[..ARRAY_SIZE-1] == [Some('a'), Some('m'), Some('f'), Some('o'), Some('s'), Some('s')]
}

// // Function to shift characters to the left in the array
// fn left_shift(chars: &mut [Option<char>; ARRAY_SIZE]) {
//     for i in 0..ARRAY_SIZE - 1 {
//         chars[i] = chars[i + 1];
//     }
//     chars[ARRAY_SIZE - 1] = None;
// }

// Function to add a character to the character array
fn add_character(chars: &mut [Option<char>; ARRAY_SIZE], character: char) -> Result<(), &'static str> {
    if chars[ARRAY_SIZE - 1].is_some() {
        // The array is full, remove the last character
        chars[ARRAY_SIZE - 1] = None;
    }

    unsafe {
        for i in COUNT..ARRAY_SIZE-1 {
            let index = i;
            if chars[index].is_none() {
                COUNT += 1;
                chars[index] = Some(character);
                return Ok(());
            }
        }
    }

    Err("Left shift failed. Cannot add more characters.")
}

// Function to print the character array
fn print_array(chars: &[Option<char>; 7]) {
    for i in 0..chars.len()-1 {
        if let Some(c) = chars[i] {
            print!("{:?}", c);
        } else {
            print!(".");
        }
    }
}

// Handler for the keyboard interrupt
extern "x86-interrupt" fn keyboard_interrupt_handler(_stack_frame: InterruptStackFrame) {
    use pc_keyboard::{layouts, DecodedKey, HandleControl, Keyboard, ScancodeSet1};
    use spin::Mutex;
    use x86_64::instructions::port::Port;

    lazy_static! {
        static ref KEYBOARD: Mutex<Keyboard<layouts::Us104Key, ScancodeSet1>> = Mutex::new(
            Keyboard::new(layouts::Us104Key, ScancodeSet1, HandleControl::Ignore)
        );
    }

    // Lock the keyboard and read the scancode from the port
    let mut keyboard = KEYBOARD.lock();
    let port_address: u16 = 0x60;
    let mut port = Port::new(port_address);

    let scancode: u8 = unsafe { port.read() };

if let Ok(Some(key_event)) = keyboard.add_byte(scancode) {
    if let Some(key) = keyboard.process_keyevent(key_event) {
        match key {
            DecodedKey::Unicode(character) => {
                // Check for success condition
                unsafe{
                    if success(&*(&raw const  CHARS)) {
                        println!("{}",ASCII_AINZ);
                    }
                    else {
                        let _ =add_character(&mut *(&raw mut CHARS), character);
                        print!("{}",ASCII_AMFOSS_TOP);
                        print!("{}",port_address);
                        print!("{}",ASCII_AMFOSS_MID);
                        print_array(&*(&raw const CHARS));     
                        print!("{}",ASCII_AMFOSS_BOTTOM);

                        if success(&*(&raw const CHARS)) {
                            for _i in 0..20{
                                println!("{}",ASCII_AINZ);
                                }
                        }
                    }
                }
            },
            DecodedKey::RawKey(key) => print!("{:?}", key),
        }
    }
}

    // Notify PIC that interrupt has been handled
    unsafe {
        PICS.lock()
            .notify_end_of_interrupt(InterruptIndex::Keyboard.as_u8());
    }
}

// Test case for the breakpoint exception
#[test_case]
fn test_breakpoint_exception() {
    // invoke a breakpoint exception
    x86_64::instructions::interrupts::int3();
}

pub const ASCII_AMFOSS_TOP: &str = "

               :7Y5PGGGP5J7.                    
            ~JB&@@@@@@@@@@@@@&GJ^                 
         .7B@@@@#PJ7!~!?YG#@@@@G7               
        !#@@@#J^.           .~Y#@@@B!             
       5@@@#7                  .?&@@@Y            
      P@@@5.                     :P@@@P           
      J@@@5              .-.        P@@@Y     Current keyboard port: ";

pub const ASCII_AMFOSS_MID: &str = "
    :&@@#.           .75GGP!       .#@@&:         
    !@@@Y          ^JPGGGGGGY:      Y@@@?         
    ?@@@?       .!YGGGGPJ5GGGG7.    ?@@@J     Enter passcode:
    ~@@@Y     :?PGGGGP7: .?GGGB5.   Y@@@7         
     B@@&:  ~JGGGGGGG5^    ^5P7:   :&@@&:     ";
    pub const ASCII_AMFOSS_BOTTOM: &str = "       
     ~@@@G!5GGGGP?5GGGGJ.    .     G@@@J          
      ?@@@&BGG5!.  7GGGGP!       ^G@@@5           
       7&@@&Y~      :YGGGGY^    ~#@@@J            
        ^PJ:          !PGGP7     :JP~             
                       .7~                        
              ^~~~^^^^~~:                   
             :&@@@@@@@@@@@@@@@#.                   
             :GBBBBBBBBBBBBBBB5                   
             :Y555YYYYYYYYY555?                   
                  ^^^^^^^^:                       
                  ?GGGGGGP~                       
                   ^JPP5?.                        ";

pub const ASCII_AINZ: &str = "
          ............5G####BBBGJ^:^^^^^^^^~!^::::::::::............
          ......  ...:5BB#&&#BGGGY!^7!^!~~?PGP7^::::^^:.........   .
          .      .....^YGGGB#&#BGGP57^^!!7PBBBBGY^^^:.........
                ..^!!!^::^!J5PG##BGPY!^:^7G#BBBBGJ~:.........:..
                .:~?P#P!.  .^!~YGGPPY!:.^G&BGP5JJ!... ..::......
                 ..^J5YJY~ ..::...77:::^J5J:....   .7~::....
                   .:7G#BP^J!......:^?BP^.:...... .~^^~:...
                    .^YG55GGJP5Y555#@#G!.....:::::!!~^:...
                    ..:..:::!7P&&###&P.:...................    YOU RECEIVE 
    GREAT            ....  .~JP##&B. . ...:....    ....          HEADPAT
   SUCCESS            ...   :?P&#&&5:.....:...   ....           FOR YOUR
                         .....!5B&&&&#G::::.:.... ....         DEDICATION
                         .::.~YG#&&&&&P::::::::.......
                         .^^:J5GPBB##G!:^^:::......
                        .^!?J^7JPPBG5#PJ5!^^:::...:::..
                       .^7J5PY7!?JP5Y5J7?!^^:^::::::::.
                       ..^?5PPPPY?YJY?J?7~~~~^^^^:...
                         .?PGBPB&&B5GBB5J??!?J!^^~~^:.
                         ..^?GGB&&&#P#&G57~5Y!~^:^^^:.
                             .?####&B#&G7:7Y!~^^:..
                              :7YGB####Y^^!~~^:...
                                ..YGBB7^^:....
                                   .:JP!::..              
                                     .~^..                           ";
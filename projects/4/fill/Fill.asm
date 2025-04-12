// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.


(START)

// i = 1
@i
M=0

// max_loop = 8191 <= 256x512/16 - 1
@8191
D=A
@max_loop
M=D

(LOOP)

// if(i > max_loop) goto START
@i
D=M
@max_loop
D=D-M
@START
D;JGT

//if(@KBD != 0) goto BLACK else goto WHITE
@KBD
D=M
@BLACK
D;JGT
@WHITE
0;JMP

(BLACK)
// *(@SCREEN + i) = -1
@SCREEN
D=A
@i
A=D+M
M=-1

// i = i + 1
@i
M=M+1

// goto LOOP
@LOOP
0;JMP

(WHITE)
// *(@SCREEN + i) = 0
@SCREEN
D=A
@i
A=D+M
M=0

// i = i + 1
@i
M=M+1

// goto LOOP
@LOOP
0;JMP

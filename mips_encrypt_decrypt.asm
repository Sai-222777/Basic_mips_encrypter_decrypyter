.data
input:      .space 40  
event: 		.asciiz"Enter 1 to encrypt, 2 to decrypt: \n"
prompt:     .asciiz"Please enter an string: \n"
output:     .asciiz"Encrypted Input: \n"
output2:	.asciiz "Decrypted input is: \n"

.text
main:
    # Prompt for the choice
    li $v0, 4
    la $a0, event
    syscall
    
    #Read choice
    li $v0, 5
    syscall
    move $t0, $v0

    # Prompt for the string to enter
    li $v0, 4
    la $a0, prompt
    syscall

    # Read the string. 
    li $v0, 8
    la $a0, input
    # Max input size
    li $a1, 50 
    syscall
    
    srl $s2, $a1, 2
    addi $s2, $s2, 1 
    move $t1, $a0

    li $t2, 2
    beq $t0, $t2 , decryption

    move $s3, $zero
    encrypting :	
        beq $s3, $s2, encrypted
        lw $s1, ($t1)  
        sll $s1, $s1, 1
        sw $s1, ($t1)
        addi $t1, $t1, 4
        addi $s3, $s3, 1
        j encrypting

    encrypted: 
        move $t1, $a0
            
        # This text
        li $v0, 4
        la $a0, output 
        syscall

        # Output encrypted
        li $v0, 4
        move $a0, $t1
        syscall
        
        j exit 

    decryption :
    move $s3, $zero
    decrypting :	
        beq $s3, $s2, decrypted
        lw $s1, ($t1)
        #addi $s1, $s1, 11  
        srl $s1, $s1, 1
        sw $s1, ($t1)
        addi $t1, $t1, 4
        addi $s3, $s3, 1
        j decrypting

    decrypted: 
        move $t1, $a0    
    
        # This text
        li $v0, 4
        la $a0, output2
        syscall
        
        #Output decrypted
        li $v0, 4
        move $a0, $t1
        syscall  
    
    exit :
        # Exit the program
        li $v0, 10
        syscall
# This dictionary maps MIPS instruction mnemonics to their respective opcode binary representations.
opcodes = { 
  "li" : "00100100000", "addi" : "001000", "srl" : "00000000000", 
  "sll" : "00000000000", "beq" : "000100", "lw" : "100011", 
  "sw" : "101011", "j" : "000010" 
}

# This dictionary maps MIPS register names to their respective binary representations.
registers = { 
  "$v0" : "00010", "$ze" : "00000", "$a0" : "00100", "$a1" : "00101", 
  "$t0" : "01000", "$t1" : "01001", "$s1" : "10001", "$s2" : "10010",  
  "$t2" : "01010", "$s3" : "10011", "($t" : "01001" 
}

# This dictionary maps predefined labels to their respective binary addresses.
addresses = { 
  "event" : "0000000000101000", "prompt" : "0000000001001100", 
  "input" : "0000000000110010", "output" : "0000000001100110", 
  "output2" : "0000000001111001", "decryption" : "0000000000010001", 
  "encrypted" : "0000000000000110", "decrypted" : "0000000000000110", 
  "encrypting" : "00000100000000000000010110", 
  "decrypting" : "00000100000000000000100111", "exit" : "00000100000000000000110111" 
}

# This function converts a decimal number to its binary representation.
def binary(num):
  binary_num = ""
  while num>0:
    binary_num = str(num % 2) + binary_num
    num = num // 2
  return binary_num

# This function prints and writes R-format instructions.
def print_rformat(elements,op):
  # Print and write the binary representation of the destination register.
  print(registers[elements[2][0:3]],end="")
  folder.write(registers[elements[2][0:3]])
  
  # Print and write the binary representation of the source register.
  print(registers[elements[1][0:3]],end="")
  folder.write(registers[elements[1][0:3]])
  
  # Convert the immediate value to binary and print/write it.
  im = binary(int(elements[-1]))
  for i in range(5 - len(im)):
    im = "0" + im
  print(im,end="")
  folder.write(im)
  
  # Print and write the function code.
  if(op == "sll"):
    print("000000")
    folder.write("000000")
  else:
    print("000010")
    folder.write("000010")

# This function processes and prints/writes different types of instructions.
def print_instruction(line):
  line = line.strip("\n")
  count = line.count("$")
  elements = list(line.split(" "))
  elements = [ele for ele in elements if ele != ""]
  
  # Loop through opcodes to find the matching one in the line.
  for op in opcodes.keys():
    if(op in line): 
      # Print and write the opcode.
      print(opcodes[op], end="")
      folder.write(opcodes[op])
      
      # Handle R-format instructions differently.
      if(op == "sll" or op == "srl"):
        print_rformat(elements,op)
        folder.write("\n")
      else:
        # Handle other instructions.
        for i in range(count):                                    
          # Print and write the binary representation of the registers.
          print(registers[elements[i+1][0:3]],end="")
          folder.write(registers[elements[i+1][0:3]])
        
        if(op == "lw" or op =="sw"):
          # Print and write zeros for load/store instructions.
          print("0000000000000000")
          folder.write("0000000000000000")
        elif(elements[-1].isnumeric()):
          # Convert immediate value to binary and print/write it.
          im = binary(int(elements[-1]))
          for i in range(16 - len(im)):
            im = "0" + im
          print(im)
          folder.write(im)
        
        folder.write("\n") 
      break    

# Open input and output files.
file = open("IMT2022_505_578_mips1.asm","r")
folder = open("dump2.txt","w")

# Process each line in the input file.
for line in file:

  if("syscall" in line):
    # Print and write syscall instruction.
    print("00000000000000000000000000001100")
    folder.write("00000000000000000000000000001100")
    folder.write("\n")

  elif("la" in line):
    # Print and write load address instructions.
    print("00111100000000010000100000000001")
    folder.write("00111100000000010000100000000001")
    folder.write("\n")
    print("0011010000100100", end="")
    folder.write("0011010000100100")
    for adr in addresses:
      if(adr in line):
        # Print and write the address.
        print(addresses[adr])
        folder.write(addresses[adr])
        break
    folder.write("\n")

  elif("move" in line):
    # Process move instruction.
    line = line.strip("\n")
    elements = list(line.split(" "))
    elements = [ele for ele in elements if ele != ""]
    print("00000000000",end="")
    folder.write("00000000000")
    print(registers[elements[2][0:3]],end="")
    folder.write(registers[elements[2][0:3]])
    print(registers[elements[1][0:3]],end="")
    folder.write(registers[elements[1][0:3]])
    print("00000100001")
    folder.write("00000100001")
    folder.write("\n")

  elif ("beq" in line):
    # Process branch if equal instruction.
    line = line.strip("\n")
    elements = list(line.split(" "))
    elements = [ele for ele in elements if ele != ""]
    print(opcodes["beq"], end="")
    folder.write(opcodes["beq"])
    print(registers[elements[1][0:3]], end="")
    folder.write(registers[elements[1][0:3]])
    print(registers[elements[2][0:3]], end="")
    folder.write(registers[elements[2][0:3]])
    print(addresses[elements[-1]])
    folder.write(addresses[elements[-1]])
    folder.write("\n")

  elif("j" in line):
    # Process jump instruction.
    line = line.strip("\n")
    elements = list(line.split(" "))
    elements = [ele for ele in elements if ele != ""]
    print(opcodes["j"],end="")
    folder.write(opcodes["j"])
    print(addresses[elements[-1]])
    folder.write(addresses[elements[-1]])
    folder.write("\n")
  else:
    # Process other instructions.
    print_instruction(line)

# Close the input and output files.
file.close()
folder.close()
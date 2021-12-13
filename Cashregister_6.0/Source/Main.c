/*
 *    Cashregister project
 * ===========================
 * File Path     : Main.c
 * Author        : M.W.Richardson
 * Date          : 19/04/21
 * Copyright     : (c) 2021 Liverpool Data Research Associates
 */

/*
LDRA_EXCLUDE 130 S
<justification start>This include was added so that the code can print something out when it runs.<justification end>
<tag start>Deviation<tag end>
*/
#include <stdio.h>

#include "Types.h"
#include "Userinterface.h"

/*LDRA_HEADER_END */

/* 
 * Simple main that loops 
 * until the character 'q' is pressed
 * Then it exits
 */
int32_t main(void) {
  char_t theChar = '0';

  (void) printf("LDRA MISRA C:2012 Cash Register\n");
  Userinterface_help();

  /* Parse characters received from the keyboard */
  while (theChar != 'q') {
    theChar = (char_t) getchar();
    Userinterface_parse(theChar);    
  }
  return 0;
}

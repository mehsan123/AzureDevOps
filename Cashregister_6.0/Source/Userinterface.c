/*
 *    Cashregister project
 * ===========================
 * File Path     : Userinterface.c
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

/* Used for random function */
#include <stdlib.h>

#include "Types.h"
#include "Userinterface.h"
#include "Cashregister.h"

/* Forward declarations */
/* ==================== */

static void goodbye(void);
static void randomShopping(void);

/* Private functions */
/* ================= */

/*LDRA_HEADER_END */


/*
 * Function to print out a message at the end of the program
 */
static void goodbye(void) {
  (void) printf("\nok bye\n");
}

/*
 * Function that can be called to randomly select products
 */
static void randomShopping(void) {
  uint32_t index = 0U;
  uint32_t code;

  (void) printf("\n");
  Cashregister_start();
  while (index < (10U + ((uint32_t) rand() % 50U ))) {
    code = (uint32_t) rand() % 7U;
    if (0U == code) {
      Cashregister_cancel();
    } else {
      Cashregister_barcode(12343U + code);
    }
    index++;
  }
  Cashregister_end();
}

/* Public functions */
/* ================ */

/*
 * Userinterface a help message to indicate what commands are available
 */
void Userinterface_help(void) {
  (void) printf("choices are :\n");
  (void) printf("            : 0-9 to compose barcode\n");
  (void) printf("            : b to enter barcode\n");
  (void) printf("            : c to cancel last product\n");
  (void) printf("            : r to do random shopping\n");
  (void) printf("            : s to start\n");
  (void) printf("            : e to end\n");
  (void) printf("            : n for Coconuts\n");
  (void) printf("            : p for Pears\n");
  (void) printf("            : l for Lychees\n");
  (void) printf("            : k for Kiwis\n");
  (void) printf("            : g for Pomegranates\n");
  (void) printf("            : w for Watermelons\n");
  (void) printf("            : q to quit program\n");
}

/*
 * parse the character entered and issue appropriate command
 */

void Userinterface_parse(const char_t aChar) {
  if ((aChar >= '0') && (aChar <= '9')) {
    Cashregister_key((const uint32_t)aChar - (const uint32_t)'0');
  } else {
    switch (aChar) {
      case 'b':
        Cashregister_code();
        break;
      case 'n':
        Cashregister_barcode(12345U);
        break;
      case 'l':
        Cashregister_barcode(12346U);
        break;
      case 'k':
        Cashregister_barcode(12347U);
        break;
      case 'p':
        Cashregister_barcode(12348U);
        break;
      case 'g':
        Cashregister_barcode(12349U);
        break;
      case 'w':
        Cashregister_barcode(12350U);
        break;
      case 'c':
        Cashregister_cancel();
        break;
      case 'e':
        Cashregister_end();
        break;
      case 's':
        Cashregister_start();
        break;
      case 'r':
        randomShopping();
        break;
      case 'q':
        goodbye();
        break;
      case '\n': /* ignore crlf */
      case '\r': /* ignore crlf */
        break;
        /* For any other character, display the help message */
      default:
        Userinterface_help();
        break;
    }
  }
}

/*
 * Simulates writing a message to the printer
 */
void Userinterface_print(const_char_pt printerMsg) {
  (void) printf("%s\n",printerMsg);
}

/*
 * Simulates writing a message to the display
 */
void Userinterface_show(const_char_pt displayMsg) {
  (void) printf("%s\n",displayMsg);
}


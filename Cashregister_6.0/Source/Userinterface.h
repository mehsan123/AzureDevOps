/*
 *    Cashregister project
 * ===========================
 * File Path     : Userinterface.h
 * Author        : M.W.Richardson
 * Date          : 19/04/21
 * Copyright     : (c) 2021 Liverpool Data Research Associates
 */

#ifndef Userinterface_H
#define Userinterface_H

/*
 * This is the file that can be easily replaced
 * by a different implementation of the printer, display
 * keyboard and barcode reader.
 */

extern void Userinterface_help(void);
extern void Userinterface_parse(const char_t aChar);
extern void Userinterface_show(const_char_pt displayMsg);
extern void Userinterface_print(const_char_pt printerMsg);

#endif

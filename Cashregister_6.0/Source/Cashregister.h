/*
 *    Cashregister project
 * ===========================
 * File Path     : Cashregister.h
 * Author        : M.W.Richardson
 * Date          : 19/04/21
 * Copyright     : (c) 2021 Liverpool Data Research Associates
 */

#ifndef CASHREGISTER_H
#define CASHREGISTER_H

/*
 * This is the controlling object that receives commands.
 * It sends messages to a display and printer
 * It manages a list of products.
 * It uses the Productdatabase to identify products from a barcode.
 */

extern void Cashregister_barcode(const uint32_t aCode);
extern void Cashregister_cancel(void);
extern void Cashregister_code(void);
extern void Cashregister_start(void);
extern void Cashregister_end(void);
extern void Cashregister_key(const uint32_t aKey);

#endif

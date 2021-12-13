/*
 *    Cashregister project
 * ===========================
 * File Path     : Productdatabase.h
 * Author        : M.W.Richardson
 * Date          : 19/04/21
 * Copyright     : (c) 2021 Liverpool Data Research Associates
 */

#ifndef PRODUCTDATABASE_H
#define PRODUCTDATABASE_H

#define MAX_PRODUCTS 6U

extern const struct Product* Productdatabase_getProduct(const uint32_t bCode);
extern struct CountedProduct* Productdatabase_getCountedProduct(const struct Product* bProduct);
extern struct CountedProduct* Productdatabase_getSpecificCountedProduct(const uint32_t anIndex);
extern void Productdatabase_resetCountedProducts(void);

#endif

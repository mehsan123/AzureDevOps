/*
 *    Cashregister project
 * ===========================
 * File Path     : Countedproduct.h
 * Author        : M.W.Richardson
 * Date          : 19/04/21
 * Copyright     : (c) 2021 Liverpool Data Research Associates
 */

#ifndef COUNTEDPRODUCT_H
#define COUNTEDPRODUCT_H

#include "Product.h"

struct CountedProduct {
  const struct Product* itsProduct;
  uint32_t count;
};

#endif

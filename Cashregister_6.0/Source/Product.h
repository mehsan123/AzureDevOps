/*
 *    Cashregister project
 * ===========================
 * File Path     : Product.h
 * Author        : M.W.Richardson
 * Date          : 19/04/21
 * Copyright     : (c) 2021 Liverpool Data Research Associates
 */

#ifndef PRODUCT_H
#define PRODUCT_H

#include "Specialoffer.h"

struct Product {
  char_pt name;
  uint32_t barcode;
  uint32_t unitPrice;
  tSpecialoffer specialOffer;
};

#endif

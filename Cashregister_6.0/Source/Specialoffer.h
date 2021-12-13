/*
 *    Cashregister project
 * ===========================
 * File Path     : Specialoffer.h
 * Author        : M.W.Richardson
 * Date          : 19/04/21
 * Copyright     : (c) 2021 Liverpool Data Research Associates
 */

#ifndef SPECIALOFFER_H
#define SPECIALOFFER_H

/* Various types of Special Offers available */
typedef enum {
   NO_OFFER, BUY_ONE_GET_ONE_FREE, TEN_PERCENT_OFF, THREE_FOR_ONE_EURO
} tSpecialoffer;

extern uint32_t Specialoffer_getPrice(const uint32_t aQuantity,
      const uint32_t aUnitPrice, const tSpecialoffer anOffer);

#endif

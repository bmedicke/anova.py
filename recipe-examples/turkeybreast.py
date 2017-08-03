#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
https://www.chefsteps.com/activities/the-most-tender-turkey-breast-ever
"""

import anova

cooker = anova.AnovaCooker('', '')
print(
    cooker.create_job(
        temperature=55, seconds=4 * 60 * 60, temperature_unit='c'))

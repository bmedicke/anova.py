#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
https://www.reddit.com/r/sousvide/comments/5og0vw/white_chocolate_cheesecake_w_blackberries_and/
"""

import anova

cooker = anova.AnovaCooker('', '')
print(cooker.create_job(temperature=80, seconds=5400, temperature_unit='c'))

###############################################################################
#
# (C) Copyright 2025 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
from everysk.core.fields import URLField

# This setting is used by the SDK without ways of override it,
# so we put it to PROD and inside the run.sh file we put it to DEV
MARKET_DATA_PUBLIC_URL = URLField(default='https://public-market-data-7c2kdpfluq-uc.a.run.app')

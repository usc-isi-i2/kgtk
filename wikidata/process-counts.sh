#! /bin/bash

./count-adls-en-entities.sh
./count-adls-entities.sh
./count-adls-properties.sh
./count-all-entities.sh
./count-all-properties.sh
./count-claims-datatypes.sh
./count-claims-entities.sh
./count-claims-properties.sh
./count-claims-property-datatypes.sh
./count-qualifiers-entities.sh
./count-qualifiers-properties.sh

# The following checks use some of the counts computed above.
./check-for-claim-entities-without-adls.sh
./check-for-unclaimed-adls-entities.sh
./check-for-unclaimed-adls-properties.sh
./check-for-unclaimed-entities.sh
./check-for-unclaimed-properties.sh
./check-for-unlabeled-entities.sh
./check-for-unlabeled-in-english-entities.sh
./check-for-unlabeled-properties.sh

# The following totals use some of the counts computed above.
./total-entity-counts.sh
./total-property-counts.sh
./total-unclaimed-entity-counts.sh
./total-unclaimed-property-counts.sh
./total-unlabeled-entity-counts.sh
./total-unlabeled-property-counts.sh

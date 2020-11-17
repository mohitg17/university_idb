STATE_ALABAMA = "Alabama"
STATE_ALASKA = "Alaska"
STATE_ARIZONA = "Arizona"
STATE_ARKANSAS = "Arkansas"
STATE_CALIFORNIA = "California"
STATE_COLORADO = "Colorado"
STATE_CONNECTICUT = "Connecticut"
STATE_DELAWARE = "Delaware"
STATE_FLORIDA = "Florida"
STATE_GEORGIA = "Georgia"
STATE_HAWAII = "Hawaii"
STATE_IDAHO = "Idaho"
STATE_ILLINOIS = "Illinois"
STATE_INDIANA = "Indiana"
STATE_IOWA = "Iowa"
STATE_KANSAS = "Kansas"
STATE_KENTUCKY = "Kentucky"
STATE_LOUISIANA = "Louisiana"
STATE_MAINE = "Maine"
STATE_MARYLAND = "Maryland"
STATE_MASSACHUSETTS = "Massachusetts"
STATE_MICHIGAN = "Michigan"
STATE_MINNESOTA = "Minnesota"
STATE_MISSISSIPPI = "Mississippi"
STATE_MISSOURI = "Missouri"
STATE_MONTANA = "Montana"
STATE_NEBRASKA = "Nebraska"
STATE_NEVADA = "Nevada"
STATE_NEW_HAMPSHIRE = "New Hampshire"
STATE_NEW_JERSEY = "New Jersey"
STATE_NEW_MEXICO = "New Mexico"
STATE_NEW_YORK = "New York"
STATE_NORTH_CAROLINA = "North Carolina"
STATE_NORTH_DAKOTA = "North Dakota"
STATE_OHIO = "Ohio"
STATE_OKLAHOMA = "Oklahoma"
STATE_OREGON = "Oregon"
STATE_PENNSYLVANIA = "Pennsylvania"
STATE_RHODE_ISLAND = "Rhode Island"
STATE_SOUTH_CAROLINA = "South Carolina"
STATE_SOUTH_DAKOTA = "South Dakota"
STATE_TENNESSEE = "Tennessee"
STATE_TEXAS = "Texas"
STATE_UTAH = "Utah"
STATE_VERMONT = "Vermont"
STATE_VIRGINIA = "Virginia"
STATE_WASHINGTON = "Washington"
STATE_WEST_VIRGINIA = "West Virginia"
STATE_WISCONSIN = "Wisconsin"
STATE_WYOMING = "Wyoming"

STATE_DC = "District of Columbia"
STATE_PR = "Puerto Rico"
STATE_AS = "American Samoa"
STATE_FM = "Federated States of Micronesia"
STATE_GU = "Guam"
STATE_MH = "Marshall Islands"
STATE_MP = "Northern Mariana Islands"
STATE_PW = "Palau"
STATE_VI = "U.S. Virgin Islands"

STATE_CHOICES = [
    STATE_ALABAMA,
    STATE_ALASKA,
    STATE_ARIZONA,
    STATE_ARKANSAS,
    STATE_CALIFORNIA,
    STATE_COLORADO,
    STATE_CONNECTICUT,
    STATE_DELAWARE,
    STATE_FLORIDA,
    STATE_GEORGIA,
    STATE_HAWAII,
    STATE_IDAHO,
    STATE_ILLINOIS,
    STATE_INDIANA,
    STATE_IOWA,
    STATE_KANSAS,
    STATE_KENTUCKY,
    STATE_LOUISIANA,
    STATE_MAINE,
    STATE_MARYLAND,
    STATE_MASSACHUSETTS,
    STATE_MICHIGAN,
    STATE_MINNESOTA,
    STATE_MISSISSIPPI,
    STATE_MISSOURI,
    STATE_MONTANA,
    STATE_NEBRASKA,
    STATE_NEVADA,
    STATE_NEW_HAMPSHIRE,
    STATE_NEW_JERSEY,
    STATE_NEW_MEXICO,
    STATE_NEW_YORK,
    STATE_NORTH_CAROLINA,
    STATE_NORTH_DAKOTA,
    STATE_OHIO,
    STATE_OKLAHOMA,
    STATE_OREGON,
    STATE_PENNSYLVANIA,
    STATE_RHODE_ISLAND,
    STATE_SOUTH_CAROLINA,
    STATE_SOUTH_DAKOTA,
    STATE_TENNESSEE,
    STATE_TEXAS,
    STATE_UTAH,
    STATE_VERMONT,
    STATE_VIRGINIA,
    STATE_WASHINGTON,
    STATE_WEST_VIRGINIA,
    STATE_WISCONSIN,
    STATE_WYOMING,
    STATE_DC,
    STATE_PR,
    STATE_AS,
    STATE_FM,
    STATE_GU,
    STATE_MH,
    STATE_MP,
    STATE_PW,
    STATE_VI
]

UNCLASSIFIED = "Unclassified"
DEGREE_CERTIFICATE = "Certificate"
DEGREE_ASSOCIATE = "Associate"
DEGREE_BACHELORS = "Bachelor's"
DEGREE_GRADUATE = "Graduate"

DEGREE_CHOICES = [
    UNCLASSIFIED,
    DEGREE_CERTIFICATE,
    DEGREE_ASSOCIATE,
    DEGREE_BACHELORS,
    DEGREE_GRADUATE,
]

COMMUNITY_TYPE_CITY = "City"
COMMUNITY_TYPE_SUBURB = "Suburb"
COMMUNITY_TYPE_TOWN = "Town"
COMMUNITY_TYPE_RURAL = "Rural"

COMMUNITY_TYPE_CHOICES = [
    UNCLASSIFIED,
    COMMUNITY_TYPE_RURAL,
    COMMUNITY_TYPE_TOWN,
    COMMUNITY_TYPE_SUBURB,
    COMMUNITY_TYPE_CITY,
]

UNI_SIZE_SMALL = "Small"
UNI_SIZE_MEDIUM = "Medium"
UNI_SIZE_LARGE = "Large"

UNI_SIZE_CHOICES = [
    UNI_SIZE_SMALL,
    UNI_SIZE_MEDIUM,
    UNI_SIZE_LARGE,
]

COST_CATEGORY_LOW = "Low"
COST_CATEGORY_MEDIUM = "Medium"
COST_CATEGORY_HIGH = "High"

COST_CATEGORY_CHOICES = [
    COST_CATEGORY_LOW,
    COST_CATEGORY_MEDIUM,
    COST_CATEGORY_HIGH,
]

CIP_FAMILY_MAP = {1: 'Agriculture, Agriculture Operations, and Related Sciences',
                  3: 'Natural Resources and Conservation',
                  4: 'Architecture and Related Services',
                  5: 'Area, Ethnic, Cultural, Gender, and Group Studies',
                  9: 'Communication, Journalism, and Related Programs',
                  10: 'Communications Technologies/Technicians and Support Services',
                  11: 'Computer and Information Sciences and Support Services',
                  12: 'Personal and Culinary Services',
                  13: 'Education',
                  14: 'Engineering',
                  15: 'Engineering Technologies and Engineering-Related Fields',
                  16: 'Foreign Languages, Literatures, and Linguistics',
                  19: 'Family and Consumer Sciences/Human Sciences',
                  22: 'Legal Professions and Studies',
                  23: 'English Language and Literature/Letters',
                  24: 'Liberal Arts and Sciences, General Studies, and Humanities',
                  25: 'Library Science',
                  26: 'Biological and Biomedical Sciences',
                  27: 'Mathematics and Statistics',
                  28: 'Military Science, Leadership, and Operational Art',
                  29: 'Military Technologies and Applied Sciences',
                  30: 'Multi/Interdisciplinary Studies',
                  31: 'Parks, Recreation, Leisure, and Fitness Studies',
                  38: 'Philosophy and Religious Studies',
                  39: 'Theology and Religious Vocations',
                  40: 'Physical Sciences',
                  41: 'Science Technologies/Technicians',
                  42: 'Psychology',
                  43: 'Homeland Security, Law Enforcement, Firefighting, and Related Protective Service',
                  44: 'Public Administration and Social Service Professions',
                  45: 'Social Sciences',
                  46: 'Construction Trades',
                  47: 'Mechanic and Repair Technologies/Technicians',
                  48: 'Precision Production',
                  49: 'Transportation and Materials Moving',
                  50: 'Visual and Performing Arts',
                  51: 'Health Professions and Related Programs',
                  52: 'Business, Management, Marketing, and Related Support Services',
                  54: 'History'}
